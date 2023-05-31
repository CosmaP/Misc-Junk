#######################################################################
#
#  Checks to see if a specific VPN is up and notifies if it is not
#
#  Cosma Papouis : 31/05/23
#
#  Note:  This requires the BurntToast Module
#         install as follows
#         Run PowerShell as Admin
#         Run this:  Install-Module -Name BurntToast
#
#######################################################################

# Name of VPN to monitor
$VPNName = "POA VPN"
# How often to check in seconds
$CheckFrequency = 10

function Show-ToastNotification {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Title,
        
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    $Notification = New-BurntToastNotification -Text $Title, $Message -AppLogo '.\Pinnacle-logo-reduced.png' -Silent
}

function checkifvpnisup {
    $VPNConnection = Get-VpnConnection -Name $VPNName
    if ($VPNConnection.ConnectionStatus -eq "Connected") {
        $t = Get-Date
        Write-Host "POA VPN is connected at $t"
        $Result = $true 
    } else {
        $t = Get-Date
        Write-Warning "POA VPN is not connected at $t"
        $Result = $false
    }
    return $Result
}

while ($true) {
    $vpnActive = checkifvpnisup

    if (-not $vpnActive) {
        Show-ToastNotification -Title "POA VPN Disconnected" -Message "Your POA VPN has been disconnected!"
    }

    Start-Sleep -Seconds $CheckFrequency
}
