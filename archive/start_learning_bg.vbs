' NWACS 自动学习系统 - 后台运行脚本
' 此脚本会在后台启动学习系统，不显示命令行窗口

Set WshShell = CreateObject("WScript.Shell")
Dim scriptPath, pythonPath, workingDir

scriptPath = "e:\Program Files (x86)\Trae CN\github\NWACS\run_learning.py"
pythonPath = "C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe"
workingDir = "e:\Program Files (x86)\Trae CN\github\NWACS"

' 在后台运行，不显示窗口
WshShell.Run pythonPath & " """ & scriptPath & """", 0, False

' 记录启动时间
Dim fso, ts, logFile
logFile = workingDir & "\learning_startup.log"
Set fso = CreateObject("Scripting.FileSystemObject")
Set ts = fso.OpenTextFile(logFile, 8, True, 0)
ts.WriteLine "[" & Now() & "] NWACS学习系统已启动"
ts.Close

Set WshShell = Nothing
Set fso = Nothing