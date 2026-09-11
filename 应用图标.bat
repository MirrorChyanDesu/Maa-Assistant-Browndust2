@echo off
REM ============================================================
REM  Apply the BD2MAA program icon:
REM    - embed mxu.ico into mxu.exe  (close MXU first!)
REM    - (re)create launcher shortcut with the same icon
REM  Re-run this after MXU updates itself, to restore the icon.
REM ============================================================
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools\apply_icon.ps1"
echo.
pause
