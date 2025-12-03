# ChatPPT 故障排查脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Troubleshooting Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Docker
Write-Host "[1] Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  [OK] Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Docker not found" -ForegroundColor Red
    exit 1
}

# 2. Check container status
Write-Host ""
Write-Host "[2] Checking container status..." -ForegroundColor Yellow
$container = docker ps -a --filter "name=chatppt" --format "{{.Names}}|{{.Status}}|{{.Ports}}"
if ($container) {
    $parts = $container -split '\|'
    Write-Host "  Container: $($parts[0])" -ForegroundColor Cyan
    Write-Host "  Status: $($parts[1])" -ForegroundColor Cyan
    Write-Host "  Ports: $($parts[2])" -ForegroundColor Cyan
    
    if ($parts[1] -like "*Up*") {
        Write-Host "  [OK] Container is running" -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] Container is not running" -ForegroundColor Yellow
        Write-Host "  Try: docker start chatppt" -ForegroundColor White
    }
} else {
    Write-Host "  [WARNING] Container 'chatppt' not found" -ForegroundColor Yellow
    Write-Host "  Try: .\docker_deploy_simple.ps1" -ForegroundColor White
}

# 3. Check port 7860
Write-Host ""
Write-Host "[3] Checking port 7860..." -ForegroundColor Yellow
$portCheck = netstat -ano | findstr ":7860"
if ($portCheck) {
    Write-Host "  [OK] Port 7860 is in use:" -ForegroundColor Green
    Write-Host "  $portCheck" -ForegroundColor Gray
} else {
    Write-Host "  [WARNING] Port 7860 is not in use" -ForegroundColor Yellow
    Write-Host "  Service may not be running" -ForegroundColor Yellow
}

# 4. Check IP addresses
Write-Host ""
Write-Host "[4] Checking IP addresses..." -ForegroundColor Yellow
$ipAddresses = ipconfig | Select-String "IPv4"
foreach ($ip in $ipAddresses) {
    $ipValue = ($ip -split ":")[1].Trim()
    if ($ipValue -like "192.168.*" -or $ipValue -like "10.*" -or $ipValue -like "172.*") {
        Write-Host "  Found: $ipValue" -ForegroundColor Cyan
        Write-Host "  Access URL: http://$ipValue:7860" -ForegroundColor Green
    }
}

# 5. Check container logs
Write-Host ""
Write-Host "[5] Checking container logs (last 20 lines)..." -ForegroundColor Yellow
if ($container) {
    Write-Host "  Recent logs:" -ForegroundColor Cyan
    docker logs chatppt --tail 20 2>&1 | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
} else {
    Write-Host "  [SKIP] Container not found" -ForegroundColor Yellow
}

# 6. Test local connection
Write-Host ""
Write-Host "[6] Testing local connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:7860" -TimeoutSec 3 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Service is accessible at http://localhost:7860" -ForegroundColor Green
    }
} catch {
    Write-Host "  [ERROR] Cannot connect to http://localhost:7860" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Gray
}

# 7. Recommendations
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Recommendations:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

if (-not $container) {
    Write-Host "1. Start Docker container:" -ForegroundColor White
    Write-Host "   .\docker_deploy_simple.ps1" -ForegroundColor Green
} elseif ($container -and $parts[1] -notlike "*Up*") {
    Write-Host "1. Start existing container:" -ForegroundColor White
    Write-Host "   docker start chatppt" -ForegroundColor Green
    Write-Host "2. Check logs:" -ForegroundColor White
    Write-Host "   docker logs -f chatppt" -ForegroundColor Green
} else {
    Write-Host "1. Check if service is starting:" -ForegroundColor White
    Write-Host "   docker logs -f chatppt" -ForegroundColor Green
    Write-Host "2. Wait a few seconds for service to start" -ForegroundColor White
    Write-Host "3. Try accessing: http://localhost:7860" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

