# ChatPPT 服务启动脚本（PowerShell）

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT 服务启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查环境变量
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[警告] OPENAI_API_KEY 环境变量未设置" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "请先设置环境变量：" -ForegroundColor Cyan
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    Write-Host "或者在此脚本中临时设置：" -ForegroundColor Cyan
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host "[信息] 正在启动 ChatPPT 服务..." -ForegroundColor Green
Write-Host "[信息] 服务将在 http://0.0.0.0:7860 启动" -ForegroundColor Green
Write-Host "[信息] 本地访问: http://localhost:7860" -ForegroundColor Green
Write-Host "[信息] 按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动服务
python src/gradio_server.py

