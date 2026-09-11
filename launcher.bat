@echo off
REM ============================================================
REM  BD2MAA 启动器（官方推荐入口，纯 PowerShell 实现，无需 Python）
REM  先检测 GitHub 新版本 -> 弹窗选择 -> 选“更新”则下载并自动覆盖 -> 启动 mxu.exe
REM  参数：-Force 强制检测 / -Demo 演示弹窗 / -Test 仅自检
REM ============================================================
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "BD2MAA-Updater.ps1" %*
