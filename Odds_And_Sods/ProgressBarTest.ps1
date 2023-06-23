#  Progress bar at top of screen as seen in installers

$TotalItems = 100
for ($i = 1; $i -le $TotalItems; $i++) {
    $progress = @{
        Activity = 'Processing Items'
        Status = "$i/$TotalItems"
        PercentComplete = ($i / $TotalItems) * 100
    }

    Write-Progress @progress
    Start-Sleep -Milliseconds 100
}


#  Simple Progress bar 

function Show-ProgressBar {
    param (
        [int]$Total,
        [int]$Current,
        [int]$Width = 50
    )

    $completedCount = [int]($Width * ($Current / $Total))
    $remainingCount = $Width - $completedCount

    $completed = [string]::Empty.PadLeft($completedCount, '=')
    $remaining = [string]::Empty.PadLeft($remainingCount, ' ')

    Write-Host -NoNewline "`r[$completed$remaining] $Current/$Total"
}

# Example usage
$TotalItems = 100
for ($i = 1; $i -le $TotalItems; $i++) {
    Show-ProgressBar -Total $TotalItems -Current $i
    Start-Sleep -Milliseconds 100
}

#  Progress bar at top of screen

function Show-ProgressBar {
    param (
        [int]$Total,
        [int]$Current,
        [int]$Width = 50
    )

    $completedCount = [int]($Width * ($Current / $Total))
    $remainingCount = $Width - $completedCount

    $completed = [string]::Empty.PadLeft($completedCount, '=')
    $remaining = [string]::Empty.PadLeft($remainingCount, ' ')

    [console]::SetCursorPosition(0, 0)
    Write-Host "[$completed$remaining] $Current/$Total"
}


