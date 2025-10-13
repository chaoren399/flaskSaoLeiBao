@echo off
title 股票扫雷宝系统后台启动

echo ========================================
echo 股票扫雷宝系统后台启动脚本
echo ========================================

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境，请先安装Python 3.7+
    timeout /t 5 >nul
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
        timeout /t 5 >nul
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

REM 后台启动Flask应用
echo.
echo ========================================
echo 股票扫雷宝系统正在后台启动...
echo ========================================
echo.

REM 使用START命令后台运行Python程序
REM /MIN 参数使窗口最小化
REM "" 第一个参数是窗口标题
start "股票扫雷宝系统" /MIN python app.py

REM 等待几秒钟确保程序启动
timeout /t 3 /nobreak >nul

echo 系统已在后台启动完成！
echo.
echo 访问地址: http://localhost:5010
echo.
echo 要停止服务，请运行 stop_service.bat
echo 或使用任务管理器结束 python.exe 进程
echo.

REM 等待10秒后自动关闭此窗口
echo 此窗口将在10秒后自动关闭...
timeout /t 10 /nobreak >nul

exit
