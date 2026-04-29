# NWACS 学习系统启动脚本
# 使用PowerShell运行，更稳定

$ErrorActionPreference = "Stop"
$workingDir = "e:\Program Files (x86)\Trae CN\github\NWACS"

Write-Host "====================================="
Write-Host "    NWACS 小说创作系统 - 自动学习"
Write-Host "====================================="
Write-Host ""

# 检查Python
Write-Host "[1/3] 检查Python环境..."
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion"
} catch {
    Write-Host "[错误] Python未安装或未添加到PATH"
    Write-Host "请先安装Python并添加到系统PATH"
    Read-Host "按Enter键退出"
    exit 1
}

Write-Host ""

# 检查脚本
Write-Host "[2/3] 检查学习脚本..."
$scriptPath = Join-Path $workingDir "run_learning.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "[错误] 学习脚本 run_learning.py 不存在"
    Read-Host "按Enter键退出"
    exit 1
}
Write-Host "[OK] 学习脚本已找到"

Write-Host ""

# 启动
Write-Host "[3/3] 启动学习系统..."
Write-Host ""
Write-Host "====================================="
Write-Host "    学习系统已启动"
Write-Host "    关闭此窗口即可停止"
Write-Host "====================================="
Write-Host ""

# 切换到工作目录
Set-Location $workingDir

# 运行学习系统
python run_learning.py

# 如果出错，显示错误
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[错误] 学习系统异常退出，错误代码: $LASTEXITCODE"
}

Read-Host "按Enter键退出"