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
#         To Check VPN Number
#         Run PowerShell
#         Run Get-NetIPInterface
#
#######################################################################

# Name of VPN to monitor
$VPNName = "POA VPN"
# Number of VPN to monitor
$VPNNumber = 79
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

    $VPNConnection = Get-NetIPInterface -InterfaceIndex $VPNNumber -ErrorAction SilentlyContinue
    if ($VPNConnection.ConnectionState -eq "Connected") {
        $t = Get-Date
        Write-Host "POA VPN is connected at $t"
        $Result = $true 
    }
    else {
        $t = Get-Date
        Write-Warning "POA VPN is not connected at $t"
        rasdial $VPNName
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
