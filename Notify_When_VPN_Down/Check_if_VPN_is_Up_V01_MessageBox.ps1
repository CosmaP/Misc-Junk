#######################################################################
#
#  Checks to see if a specific VPN is up and notifies if it is not
#
#  Cosma Papouis : 31/05/23
#
#######################################################################

# Name of VPN to monitor
$VPNName = "POA VPN"
# How often to check in seconds
$CheckFrequency = 10

write-host "Starting"

Add-Type -AssemblyName PresentationFramework

# Used to test if messages are working
#[System.Windows.MessageBox]::Show("Test box")

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
        
        [System.Windows.MessageBox]::Show("Your POA VPN has been disconnected!", "VPN Disconnected", [System.Windows.MessageBoxButton]::OK, [System.Windows.MessageBoxImage]::Warning)
    }

    Start-Sleep -Seconds $CheckFrequency
}
