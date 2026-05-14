@echo off
chcp 65001 >nul
title NWACS v7.0 核心创作引擎

echo.
echo ========================================
echo   📚 NWACS v7.0 小说创作引擎
echo   支持8种小说类型，32个知识库
echo ========================================
echo.
echo 请选择操作:
echo.
echo 1. 交互式小说创作（推荐）
echo 2. 快速测试功能
echo 3. 查看支持的小说类型
echo 4. 启动诊断工具
echo.
set /p choice=请输入选项 (1-4): 

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto test
if "%choice%"=="3" goto types
if "%choice%"=="4" goto diagnostic

:invalid
echo.
echo 无效选项
pause
goto end

:interactive
echo.
echo ========================================
echo   🎨 启动交互式创作模式
echo ========================================
echo.
cd /d "%~dp0"
python core/nwacs_novel_engine.py --interactive --api-key sk-f3246fbd1eef446e9a11d78efefd9bba
pause
goto end

:test
echo.
echo ========================================
echo   🧪 快速功能测试
echo ========================================
echo.
cd /d "%~dp0"
python quick_check.py
pause
goto end

:types
echo.
echo ========================================
echo   📖 NWACS支持的小说类型
echo ========================================
echo.
echo 1. 🐉 玄幻仙侠 - 修仙、玄幻、仙侠
echo 2. 🏙️ 都市言情 - 都市、言情、职场
echo 3. 🔍 悬疑推理 - 悬疑、推理、侦探
echo 4. 🚀 科幻未来 - 科幻、未来、末世
echo 5. 📜 历史穿越 - 历史、穿越、架空
echo 6. 👻 恐怖惊悚 - 恐怖、惊悚、灵异
echo 7. 🎮 游戏竞技 - 游戏、竞技、电竞
echo 8. 💖 女频系列 - 总裁、年代、马甲、萌宝
echo.
echo NWACS v7.0 拥有28个三级Skill，32个知识库！
echo.
pause
goto end

:diagnostic
echo.
echo ========================================
echo   🔍 启动诊断工具
echo ========================================
echo.
cd /d "%~dp0"
python quick_check.py
pause
goto end

:end
echo.
echo 感谢使用NWACS v7.0！
timeout /t 3
