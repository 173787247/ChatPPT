# 配置 Docker Desktop 使用国内镜像源
# 适用于 Windows Docker Desktop

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker 镜像源配置工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$daemonPath = "$env:USERPROFILE\.docker\daemon.json"
$backupPath = "$env:USERPROFILE\.docker\daemon.json.backup"

# 检查并备份现有配置
if (Test-Path $daemonPath) {
    Write-Host "[INFO] 发现现有配置文件，正在备份..." -ForegroundColor Yellow
    Copy-Item $daemonPath $backupPath -Force
    Write-Host "[SUCCESS] 已备份到: $backupPath" -ForegroundColor Green
}

# 创建配置内容
$config = @{
    "registry-mirrors" = @(
        "https://docker.mirrors.ustc.edu.cn",
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com"
    )
    "insecure-registries" = @()
    "debug" = $false
    "experimental" = $false
}

# 写入配置文件
Write-Host "[INFO] 正在写入配置文件..." -ForegroundColor Yellow
$configJson = $config | ConvertTo-Json -Depth 10
$configJson | Out-File -FilePath $daemonPath -Encoding UTF8 -Force

Write-Host "[SUCCESS] 配置文件已更新: $daemonPath" -ForegroundColor Green
Write-Host ""
Write-Host "配置内容：" -ForegroundColor Cyan
Write-Host $configJson -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "重要提示：" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 请重启 Docker Desktop 使配置生效" -ForegroundColor White
Write-Host "2. 或者通过 Docker Desktop 设置界面配置：" -ForegroundColor White
Write-Host "   Settings -> Docker Engine -> 添加 registry-mirrors" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 配置完成后，重新运行部署脚本：" -ForegroundColor White
Write-Host "   .\docker_deploy_simple.ps1" -ForegroundColor Green
Write-Host ""

