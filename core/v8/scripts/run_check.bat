@echo off
cd /d "d:\Trae CN\github\nwacs\nwacs\core\v8"
python static_check.py > static_check_output.txt 2>&1
echo Exit code: %ERRORLEVEL% >> static_check_output.txt
type static_check_output.txt