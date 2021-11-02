Why AR.PY
    AR.PY - Admin and React simplifies the account managing in order to make managing, disabling and password resetting automated.

How to install AR.PY
    To use AR.PY you need to follow the following steps:

    Install python and pip
    Install python modules (shell: pip install flask ldap3)
    Set execution policy for CurrentUser (ps as admin: Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser )
    Install powershell modules (ps as admin: Install-Module MsOnline)

How to use AR.PY

                                                 == Monitoring Tools ==
                                                 [1] Search AD Account
                                                [2] Search O365 Account

                                                   == React Tools ==
                                             [3] Enable/Disable AD Account
                                            [4] Enable/Disable O365 Account


   You can manage both an AD and a O365 user by selecting options.



   == Monitoring Tools ==
   
   [1] Search AD Account

   A read only user will be required in order to query your Active Directory. The target username must be insered as "userPrincipalName".


    ***************************************

    Insert your complete username: [username@domain.local]
    Password:

    Which user would you like to check? [username] [!A for Abort]
    Username:
    
    == ============== ==
    Display Name: 
    User: 
    Last Logon: 
    pwdLastSet: 
    badPwdCount:
    userAccountControl: [ will display "User Enabled", "User Disabled" or the userAccountControl decimal value ]
    == ============== ==
    
    ***************************************


   [2] Search O365 Account

   A privileged user will be required in order to access AzureAD and read users details. MsOnline module will show the authentication form.

    ***************************************

    Which user would you like to check? [email address] [!A for Abort] 
    Email address: 
    
    
    DisplayName                 : 
    UserPrincipalName           : 
    ProxyAddresses              : 
    BlockCredential             : 
    LastPasswordChangeTimestamp : 
    MFA Status                  : 
    UsageLocation               : 
    IsLicensed                  : 
    Licenses                    : 
    
    ***************************************



   == React Tools ==

   [3] Enable/Disable AD Account

   A privileged user will be required in order to access your Active Directory and manage users. The target username must be insered as "userPrincipalName".

    ***************************************
    
    Insert your administrative user: [youradmin@domain.local] [!A for Abort]
    Username:
    Password:
    
    Which user would you like to manage? [username] [!A for Abort]
    
    == ============== ==
    User status: [ will display "User Enabled", "User Disabled" or the userAccountControl decimal value ]
    == ============== ==
    
    READ CAREFULLY
    Press [1] to ENABLE selected user, [2] to DISABLE it or any key to abort:
    
    == ============== ==
    User status: [ will display "User Enabled", "User Disabled" or the userAccountControl decimal value ]
    == ============== ==
    
    ***************************************

   In the last step you can choose to enable or disable the target user. Ar.py will overwrite the userAccountControl decimal value with 512 to enable the user or 514 to disable it.
   For further information: http://www.selfadsi.org/ads-attributes/user-userAccountControl.htm



   [4] Enable/Disable O365 Account

   A privileged user will be required in order to access AzureAD and manage users details. MsOnline module will show the authentication form.

    ***************************************
    
    Which user would you like to manage? [email address] [!A for Abort]
    User:
    
    READ CAREFULLY
    Press [1] to CHANGE PASSWORD AND UNLOCK selected user, [2] to CHANGE PASSWORD AND LOCK it or any key to abort:

    ***************************************