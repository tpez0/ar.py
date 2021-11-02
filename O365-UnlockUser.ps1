Import-Module MsOnline
Connect-MsolService -Credential $cred
Set-MsolUserPassword -UserPrincipalName $userUPN -ForceChangePassword $True
Set-MsolUser -UserPrincipalName $userUPN -BlockCredential $False