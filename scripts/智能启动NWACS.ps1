# NWACS FINAL 智能启动脚本
# 自动查找Python并启动程序

Write-Host "="*80 -ForegroundColor Cyan
Write-Host "  NWACS FINAL - 终极小说写作助手" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

# 尝试查找Python
$pythonPath = $null

Write-Host "🔍 正在查找Python..." -ForegroundColor Yellow

# 方法1：使用Get-Command查找
try {
    $cmd = Get-Command python -ErrorAction Stop
    $pythonPath = $cmd.Source
    Write-Host "✅ 通过Get-Command找到: $pythonPath" -ForegroundColor Green
} catch {
    Write-Host "❌ Get-Command未找到" -ForegroundColor Red
}

# 方法2：查找常见安装位置
if (-not $pythonPath) {
    $possiblePaths = @(
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "C:\Python39\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python313\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe"
    )

    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $pythonPath = $path
            Write-Host "✅ 在常见位置找到: $pythonPath" -ForegroundColor Green
            break
        }
    }
}

# 方法3：尝试使用py命令
if (-not $pythonPath) {
    try {
        $test = & py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonPath = "py"
            Write-Host "✅ 使用py启动器" -ForegroundColor Green
        }
    } catch {
    }
}

# 方法4：最后尝试：直接使用python命令
if (-not $pythonPath) {
    $pythonPath = "python"
    Write-Host "⚠️ 将尝试直接使用python命令" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 正在启动 NWACS FINAL..." -ForegroundColor Green
Write-Host ""

# 切换到脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "当前目录: $scriptDir" -ForegroundColor Cyan
Write-Host "Python路径: $pythonPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

# 启动程序
try {
    if ($pythonPath -eq "py") {
        py NWACS_FINAL.py
    } else {
        & $pythonPath NWACS_FINAL.py
    }
} catch {
    Write-Host ""
    Write-Host "❌ 启动失败！错误信息:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 请尝试手动运行:" -ForegroundColor Yellow
    Write-Host "   cd $scriptDir" -ForegroundColor Gray
    Write-Host "   python NWACS_FINAL.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 或者直接在VS Code中打开 NWACS_FINAL.py 运行" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按回车键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
