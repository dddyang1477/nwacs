@echo off
chcp 65001 >nul
title NWACS ngrok Auto Installer
echo.
echo ========================================
echo    NWACS ngrok 自动安装器
echo ========================================
echo.

echo [1/4] 检查ngrok是否已安装...
where ngrok >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ ngrok已安装!
    goto :config
)

echo [2/4] 准备下载ngrok...
echo.

echo 下载地址: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-archive-win64.zip
echo.

echo [3/4] 正在下载ngrok...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-archive-win64.zip' -OutFile 'ngrok.zip'"

echo.
echo [4/4] 解压ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
del ngrok.zip

echo.
echo ✅ ngrok安装完成!
echo.

:config
echo ========================================
echo 配置ngrok
echo ========================================
echo.
echo 请到 https://ngrok.com 注册并获取 authtoken
echo 注册后，在 https://dashboard.ngrok.com/get-started/your-authtoken 找到你的token
echo.
set /p TOKEN=请输入你的ngrok authtoken: 

echo.
echo 配置authtoken...
ngrok config add-authtoken %TOKEN%

echo.
echo ✅ 配置完成!
echo.
echo ========================================
echo 启动ngrok
echo ========================================
echo.
echo 下一步:
echo 1. 打开飞书群
echo 2. 配置机器人消息订阅
echo 3. 运行: ngrok http 8088
echo.

pause
