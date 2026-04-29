@echo off
echo =====================================
echo     NWACS 学习系统诊断
echo =====================================
echo.

echo [1] 检查Python...
python --version
if errorlevel 1 (
    echo [错误] Python未找到!
    echo 请先安装Python: https://www.python.org/downloads/
    pause
    exit
)
echo [OK] Python已安装
echo.

echo [2] 检查脚本目录...
cd /d "e:\Program Files (x86)\Trae CN\github\NWACS\src\core"
if errorlevel 1 (
    echo [错误] 目录不存在!
    pause
    exit
)
echo [OK] 目录存在
echo.

echo [3] 检查skill_learning_manager.py...
if not exist "skill_learning_manager.py" (
    echo [错误] 文件不存在!
    pause
    exit
)
echo [OK] 文件存在
echo.

echo [4] 检查logger.py...
if not exist "logger.py" (
    echo [错误] logger.py 不存在!
    pause
    exit
)
echo [OK] logger.py存在
echo.

echo =====================================
echo     所有检查通过!
echo =====================================
echo.
echo 正在启动学习系统...
echo.

python skill_learning_manager.py

pause