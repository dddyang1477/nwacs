[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
Set-Location "E:\Program Files (x86)\Trae CN\github\NWACS\core\v8"
$host.UI.RawUI.WindowTitle = "NWACS FINAL - AI Writing Assistant"
Clear-Host
Write-Host "*******************************************************************************" -ForegroundColor Cyan
Write-Host "*                                                                               *" -ForegroundColor Cyan
Write-Host "*     NWACS FINAL - Ultimate Novel Writing Assistant                           *" -ForegroundColor Cyan
Write-Host "*     Version: 2026.05  |  One Version, All Features                           *" -ForegroundColor Cyan
Write-Host "*                                                                               *" -ForegroundColor Cyan
Write-Host "*******************************************************************************" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting..." -ForegroundColor Green
Write-Host ""
& "C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" "NWACS_FINAL.py"
