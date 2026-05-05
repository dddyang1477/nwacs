# NWACS 自动学习系统 - 计划任务设置脚本
# 将NWACS学习系统注册为Windows计划任务，在系统空闲时自动启动

$taskName = "NWACS_AutoLearning"
$taskDescription = "NWACS小说创作系统自动学习任务"
$scriptPath = "e:\Program Files (x86)\Trae CN\github\NWACS\run_learning.py"
$pythonPath = "C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"
$workingDir = "e:\Program Files (x86)\Trae CN\github\NWACS"

Write-Host "====================================="
Write-Host "    NWACS 自动学习计划任务设置"
Write-Host "====================================="
Write-Host ""

if (-not (Test-Path $scriptPath)) {
    Write-Host "错误：启动脚本不存在: $scriptPath"
    exit 1
}

Write-Host "找到启动脚本: $scriptPath"

$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$scriptPath`"" -WorkingDirectory $workingDir

$trigger = New-ScheduledTaskTrigger -Daily -At "09:00"

$trigger2 = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

try {
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger,$trigger2 -Settings $settings -Principal $principal -Description $taskDescription -Force
    
    Write-Host ""
    Write-Host "计划任务注册成功！"
    Write-Host ""
    Write-Host "任务名称: $taskName"
    Write-Host "描述: $taskDescription"
    Write-Host "执行程序: $pythonPath"
    Write-Host "参数: $scriptPath"
    Write-Host "工作目录: $workingDir"
    
} catch {
    Write-Host "注册任务失败: $_"
    exit 1
}

Write-Host ""
Write-Host "设置完成"