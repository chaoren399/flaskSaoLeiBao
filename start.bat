@echo off
title 股票扫雷宝系统

echo ========================================
echo 股票扫雷宝系统启动脚本
echo ========================================

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖包
echo 正在检查依赖包...
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖包...
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    if %errorlevel% neq 0 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

REM 检查stockcode.txt文件
if not exist "stockcode.txt" (
    echo 警告: 未找到stockcode.txt文件，正在生成...
    python getStockList.py
    if %errorlevel% neq 0 (
        echo 警告: 股票代码文件生成失败，系统将使用示例数据
    )
)

REM 启动Flask应用
echo.
echo ========================================
echo 股票扫雷宝系统正在启动...
echo 访问地址: http://localhost:5010
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python app.py

pause
