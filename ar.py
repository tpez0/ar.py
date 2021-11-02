import subprocess, sys
from os import system, name
import ssl
from time import sleep
from getpass import getpass
from flask import json
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE, Tls, SASL, KERBEROS, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPCursorError
import string
import random # define the random module 
import datetime
import time
import shutil

server_name = '' # DOMAIN CONTROLLER
LDAP_BASE_DN = 'DC=domain,DC=local' # DOMAIN LDAP BASE DN
search_filter = "(displayName={0}*)"
tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)

def Intro():
    clear()
    txtSep1 = "==========================="
    txtScript = "ar.py"
    txtTitle = "Admin and React"
    txtDescription1 = "for Automated Account Managing,"
    txtDescription2 = "Disabling and Resetting"
    print(txtSep1.center(120))
    print(txtScript.center(120))
    print(txtTitle.center(120))
    print(txtDescription1.center(120))
    print(txtDescription2.center(120))
    print(txtSep1.center(120))

def startMenu():
    txtMonitor = "== Monitoring Tools =="
    txtReact = "== React Tools =="
    txtTool1 = "[1] Search AD Account"
    txtTool2 = "[2] Search O365 Account"
    txtTool3 = "[3] Enable/Disable AD Account"
    txtTool4 = "[4] Lock/Unlock O365 Account"    
    print(" ")
    print(txtMonitor.center(120))
    print(txtTool1.center(120))
    print(txtTool2.center(120))
    print(" ")
    print(txtReact.center(120))
    print(txtTool3.center(120))
    print(txtTool4.center(120))
    print(" ")
    print(" ")
    startInput = str(input("Select a tool [0-9]: "))
    if startInput == "1":
        clear()
        ADMonitor()
    elif startInput == "2":
        clear()
        O365Monitor() 
    elif startInput == "3":
        clear()
        ADChangeState() 
    elif startInput == "4":
        clear()
        O365ChangeState() 
    else:
        print(" ")
        print ("Bye!")
        print(" ")
        print(" ")
        sleep(2)
    exit


def ADMonitor():
    txtMonitor = "== Monitoring Tools =="
    txtSep2 = "== ============== =="
    txtTool1 = "[1] Search AD Account | Selected"    
    print(" ")
    print(txtMonitor.center(120))
    print(txtSep2.center(120))
    print(txtTool1.center(120))
    print(" ")
    print(" ")

    print("Insert your complete username: [username@domain.local] [!A for Abort] ")
    base_user = str(input("Username: "))
    password = getpass()
    server = Server(server_name, use_ssl=True, tls=tls, get_info=ALL)
    conn = Connection(server, user=base_user, password=password, auto_bind=True)
    conn.bind()
    #print(conn.extend.standard.who_am_i())
    print(' ')
    print("LDAP Connection: OK")
    print(' ')
    print('Which user would you like to check? [username] [!A for Abort]')
    searchuname = str(input("Username: "))

    if searchuname == "!A":
        conn.unbind()
        newRound()
        exit
    else:

        searchfilter = '(&(objectclass=person)(sAMAccountName='+searchuname+'))'
        format_string = '{:25} {:>6} {:19} {:19} {}'
        conn.search(LDAP_BASE_DN.format(LDAP_BASE_DN), searchfilter, attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        data = json.loads(conn.response_to_json())
        print(' ')
        print("== ============== ==")
        print('Display Name: '+data['entries'][0]['attributes']['cn'])
        print('User: '+data['entries'][0]['attributes']['distinguishedName'])
        print('Last Logon: '+data['entries'][0]['attributes']['lastLogon'])
        print('pwdLastSet: '+data['entries'][0]['attributes']['pwdLastSet'])
        print('badPwdCount: '+str(data['entries'][0]['attributes']['badPwdCount']))
        if data['entries'][0]['attributes']['userAccountControl'] == 512:
            print('User status: User Enabled')
        elif data['entries'][0]['attributes']['userAccountControl'] == 514:
            print('User status: User Disabled')
        else:
            print('userAccountControl decimal value: '+str(data['entries'][0]['attributes']['userAccountControl']))
        print("== ============== ==")
        print(' ')
        conn.unbind()
        newRound()
    
    exit

def O365Monitor():
    txtMonitor = "== Monitoring Tools =="
    txtSep2 = "== ============== =="
    txtTool2 = "[2] Search O365 Account | Selected"    
    print(" ")
    print(txtMonitor.center(120))
    print(txtSep2.center(120))
    print(txtTool2.center(120))
    print(" ")
    print(" ")
    print("Which user would you like to check? [email address] [!A for Abort]")
    usersearchfilter = str(input("Email address: "))

    if usersearchfilter == "!A":
        newRound()
        exit
    else:
        f_old = ".\O365-MonitorUser.ps1"
        f_new = ".\O365-MonitorUser"+str(datetime.date.today())+".ps1"
        shutil.copyfile(f_old, f_new)
        text_to_prepend = str('$usersearchfilter="'+usersearchfilter+'"\n')

        f = open(f_new, 'r')
        temp = f.read()
        f.close()
        f = open(f_new, 'w')
        f.write(text_to_prepend)
        f.write(temp)
        f.close()

        p = subprocess.Popen(["powershell.exe", f_new], stdout=sys.stdout)
        p.communicate()
        
        newRound()

def ADChangeState():
    txtMonitor = "== React Tools =="
    txtSep2 = "== ============== =="
    txtTool3 = "[3] Lock/Unlock AD Account | Selected"    
    print(" ")
    print(txtMonitor.center(120))
    print(txtSep2.center(120))
    print(txtTool3.center(120))
    print(" ")
    print(" ")

    print("Insert your administrative user: [youradmin@domain.local] [!A for Abort]")
    admin_user = str(input("Username: "))
    password = getpass()
    print(" ")

    #Create Connection with admin user
    server = Server(server_name, use_ssl=True)
    conn = Connection(server, admin_user, password=password, auto_bind=True)
    conn.bind()

    print("Which user would you like to manage? [username] [!A for Abort]")
    searchuname = str(input("Username: "))
    searchfilter = '(&(objectclass=person)(sAMAccountName='+searchuname+'))'
    format_string = '{:25} {:>6} {:19} {:19} {}'
    conn.search(LDAP_BASE_DN.format(LDAP_BASE_DN), searchfilter, attributes=['distinguishedName','userAccountControl'])
    data = json.loads(conn.response_to_json())
    userdn = data['entries'][0]['attributes']['distinguishedName']
    
    print(" ")
    print("== ============== ==")
    if data['entries'][0]['attributes']['userAccountControl'] == 512:
        print('User status: User Enabled')
    elif data['entries'][0]['attributes']['userAccountControl'] == 514:
        print('User status: User Disabled')
    else:
        print('userAccountControl decimal value: '+str(data['entries'][0]['attributes']['userAccountControl']))
    print("== ============== ==")
    print(" ")

    print("READ CAREFULLY")
    startInput = input("Press [1] to ENABLE selected user, [2] to DISABLE it or any key to abort: ")
    if startInput == "1":
        conn.modify(userdn, {'userAccountControl': (MODIFY_REPLACE, [512])})
    elif startInput == "2":
        S = 24  # number of characters in the string. 
        newPassword = str(''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = S)))
        conn.extend.microsoft.modify_password(userdn, old_password='', new_password=newPassword)
        conn.modify(userdn, {'userAccountControl': (MODIFY_REPLACE, [514])})
    else:
        print(" ")
        print ("Bye!")
        print(" ")
        print(" ")
        sleep(2)

    conn.search(LDAP_BASE_DN.format(LDAP_BASE_DN), searchfilter, attributes=['distinguishedName','userAccountControl'])
    data = json.loads(conn.response_to_json())
    print(' ')
    print("== ============== ==")
    if data['entries'][0]['attributes']['userAccountControl'] == 512:
        print('User status: User Enabled')
    elif data['entries'][0]['attributes']['userAccountControl'] == 514:
        print('User status: User Disabled')
    else:
        print('userAccountControl decimal value: '+str(data['entries'][0]['attributes']['userAccountControl']))
    print("== ============== ==")
    print(' ')
    conn.unbind()
    
    newRound()

    exit

def O365ChangeState():
    txtMonitor = "== React Tools =="
    txtSep2 = "== ============== =="
    txtTool4 = "[4] Enable/Disable Office 365 Account | Selected" 
    print(" ")
    print(txtMonitor.center(120))
    print(txtSep2.center(120))
    print(txtTool4.center(120))
    print(" ")
    print(" ")
    print("Which user would you like to manage? [email address] [!A for Abort]")
    user_upn = str(input("Email address: "))
    if user_upn == "!A":
        newRound()
        exit
    else:
        print(' ')
        print("READ CAREFULLY")
        startInput = input("Press [1] to CHANGE PASSWORD AND UNLOCK selected user, [2] to CHANGE PASSWORD AND LOCK it or any key to abort: ")
        print(' ')
        if startInput == "1":
            f_old = ".\O365-UnlockUser.ps1"
            f_new = ".\O365-UnlockUser"+str(datetime.date.today())+".ps1"
            shutil.copyfile(f_old, f_new)
            text_to_prepend = str('$userUPN="'+user_upn+'"\n')

            f = open(f_new, 'r')
            temp = f.read()
            f.close()
            f = open(f_new, 'w')
            f.write(text_to_prepend)
            f.write(temp)
            f.close()

            p = subprocess.Popen(["powershell.exe", f_new], stdout=sys.stdout)
            p.communicate()
        elif startInput == "2":
            f_old = ".\O365-LockUser.ps1"
            f_new = ".\O365-LockUser"+str(datetime.date.today())+".ps1"
            shutil.copyfile(f_old, f_new)
            text_to_prepend = str('$userUPN="'+user_upn+'"\n')

            f = open(f_new, 'r')
            temp = f.read()
            f.close()
            f = open(f_new, 'w')
            f.write(text_to_prepend)
            f.write(temp)
            f.close()

            p = subprocess.Popen(["powershell.exe", f_new], stdout=sys.stdout)
            p.communicate()
            print(' ')
        else:
            print(' ')
            print ("Bye!")
            print(' ')
            print(' ')
            sleep(2)

    newRound()


def newRound():
    startInput = str(input("Run ar.py again? [y-N]: "))
    if startInput == "y":
        clear()
        startMenu()
    else:
        print(" ")
        print ("Bye!")
        print(" ")
        print(" ")
        clear()
        sleep(2)

def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

try:
    Intro()
    startMenu()
except IndexError:
    print("Error")
    raise os._exit(0)
except Exception as e:
    print(e)