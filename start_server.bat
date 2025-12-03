@echo off
REM ChatPPT 服务启动脚本（Windows）

echo ========================================
echo ChatPPT 服务启动脚本
echo ========================================
echo.

REM 检查环境变量
if "%OPENAI_API_KEY%"=="" (
    echo [警告] OPENAI_API_KEY 环境变量未设置
    echo.
    echo 请先设置环境变量：
    echo set OPENAI_API_KEY=your_api_key_here
    echo.
    echo 或者在此脚本中临时设置：
    echo set OPENAI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

echo [信息] 正在启动 ChatPPT 服务...
echo [信息] 服务将在 http://0.0.0.0:7860 启动
echo [信息] 按 Ctrl+C 停止服务
echo.
echo ========================================
echo.

python src/gradio_server.py

pause

