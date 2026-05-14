# NWACS FINAL 简单启动脚本
# 使用py命令启动

Write-Host "="*80 -ForegroundColor Cyan
Write-Host "  NWACS FINAL - 终极小说写作助手" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 正在启动..." -ForegroundColor Green
Write-Host ""

# 切换到脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 启动程序
py NWACS_FINAL.py

Write-Host ""
Write-Host "按回车键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
