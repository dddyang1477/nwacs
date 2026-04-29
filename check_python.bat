@echo off
echo =====================================
echo     Python 诊断工具
echo =====================================
echo.

echo 检查 python 命令...
where python
echo 返回值: %errorlevel%
echo.

echo 检查 python3 命令...
where python3
echo 返回值: %errorlevel%
echo.

echo 检查完整路径...
if exist "C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe" (
    echo 找到: C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe
    C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\python.exe -V
) else (
    echo Python 不在默认位置
)
echo.

echo 检查 PATH 环境变量...
echo %PATH%
echo.

pause