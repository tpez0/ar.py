Import-Module MsOnline
Connect-MsolService -Credential $cred
$users = Get-MsolUser -SearchString $usersearchfilter
$users | Select-Object DisplayName,UserPrincipalName,ProxyAddresses,BlockCredential,LastPasswordChangeTimestamp,@{N="MFA Status"; E={
    if( $_.StrongAuthenticationRequirements.State -ne $null) {$_.StrongAuthenticationRequirements.State} else { "Disabled"}}},UsageLocation,IsLicensed,Licenses

#Get-MsolUser -UserPrincipalName $usersearchfilter | Select-Object *|Format-List