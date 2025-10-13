@echo off
title 停止股票扫雷宝系统

echo ========================================
echo 停止股票扫雷宝系统
echo ========================================

echo 正在查找并停止股票扫雷宝系统进程...

REM 查找并终止Python进程（根据窗口标题）
taskkill /F /FI "WINDOWTITLE eq 股票扫雷宝系统*" 2>nul
if %errorlevel% equ 0 (
    echo 成功停止股票扫雷宝系统
) else (
    echo 未找到正在运行的股票扫雷宝系统进程
)

echo.
echo 正在查找并停止所有Python Flask进程...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
if %errorlevel% equ 0 (
    echo 成功停止Python Flask进程
) else (
    echo 未找到正在运行的Python Flask进程
)

echo.
echo 如果上述方法无效，请使用任务管理器手动结束进程
echo.

pause
