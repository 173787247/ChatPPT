# 直接拉取基础镜像（使用国内镜像源）
# 如果配置镜像源后仍然失败，可以手动拉取

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "拉取 Docker 基础镜像" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[INFO] 正在拉取 python:3.10-slim 镜像..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟，请耐心等待..." -ForegroundColor Yellow
Write-Host ""

# 尝试拉取镜像
docker pull python:3.10-slim

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] 镜像拉取成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "现在可以运行部署脚本：" -ForegroundColor Cyan
    Write-Host "  .\docker_deploy_simple.ps1" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] 镜像拉取失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "建议：" -ForegroundColor Yellow
    Write-Host "1. 先运行 .\setup_docker_mirror.ps1 配置镜像源" -ForegroundColor White
    Write-Host "2. 重启 Docker Desktop" -ForegroundColor White
    Write-Host "3. 重新运行此脚本" -ForegroundColor White
    Write-Host ""
    Write-Host "或者使用替代方案（直接运行 Python）：" -ForegroundColor Yellow
    Write-Host "  python src/gradio_server.py" -ForegroundColor Green
}

Write-Host ""

