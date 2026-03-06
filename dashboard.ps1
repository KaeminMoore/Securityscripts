param(
    [int]$IntervalMinutes = 4,
    [int]$NudgePx = 3
)

Add-Type -AssemblyName System.Windows.Forms

function Nudge-Mouse {
    param([int]$px)
    $pos = [System.Windows.Forms.Cursor]::Position
    [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($pos.X + $px, $pos.Y)
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.Cursor]::Position = $pos
}

Write-Host ""
Write-Host "  KEEP AWAKE" -ForegroundColor Cyan
Write-Host "  Nudging mouse ${NudgePx}px every ${IntervalMinutes} min  |  Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

$count = 0
while ($true) {
    $count++
    $ts = (Get-Date).ToString("HH:mm:ss")
    Nudge-Mouse -px $NudgePx
    Write-Host "  [$ts]  nudge #$count — PC awake, Teams Available " -NoNewline
    Write-Host "OK" -ForegroundColor Green
    Start-Sleep -Seconds ($IntervalMinutes * 60)
}
