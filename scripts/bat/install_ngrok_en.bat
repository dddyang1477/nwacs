@echo off
title NWACS ngrok Auto Installer
echo.
echo ========================================
echo    NWACS ngrok Auto Installer
echo ========================================
echo.

echo [1/4] Checking ngrok installation...
where ngrok >nul 2>&1
if %errorlevel%==0 (
    echo    [OK] ngrok is installed!
    goto :config
)

echo [2/4] Downloading ngrok...
echo Download: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-archive-win64.zip
echo.

powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-archive-win64.zip' -OutFile 'ngrok.zip'"

echo.
echo [3/4] Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"
del ngrok.zip

echo.
echo [OK] ngrok installed!

:config
echo.
echo ========================================
echo Configure ngrok
echo ========================================
echo.
echo 1. Go to https://ngrok.com and register
echo 2. Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
echo.
set /p TOKEN=Enter your ngrok authtoken:

echo.
echo Configuring authtoken...
ngrok config add-authtoken %TOKEN%

echo.
echo [OK] Configuration complete!
echo.
echo ========================================
echo Next Steps
echo ========================================
echo.
echo 1. Open Feishu group
echo 2. Configure bot message subscription
echo 3. Run: ngrok http 8088
echo.

pause
