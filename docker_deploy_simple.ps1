# ChatPPT Docker 简单部署脚本
# 使用 Docker 部署并通过浏览器访问截图

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Docker Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "[SUCCESS] Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check environment variable
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[WARNING] OPENAI_API_KEY not set" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set the environment variable:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    $setKey = Read-Host "Do you want to set it now? (y/n)"
    if ($setKey -eq "y" -or $setKey -eq "Y") {
        $apiKey = Read-Host "Enter your OpenAI API Key"
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "[SUCCESS] API Key set for this session" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Cannot proceed without API Key" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Get local IP address
Write-Host ""
Write-Host "[INFO] Getting local IP address..." -ForegroundColor Yellow
try {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
        $_.IPAddress -like "192.168.*" -or 
        $_.IPAddress -like "10.*" -or 
        $_.IPAddress -like "172.*"
    } | Select-Object -First 1).IPAddress

    if (-not $ipAddress) {
        $ipAddress = "localhost"
        Write-Host "[WARNING] Cannot get LAN IP, will use localhost" -ForegroundColor Yellow
    } else {
        Write-Host "[SUCCESS] Local IP address: $ipAddress" -ForegroundColor Green
    }
} catch {
    $ipAddress = "localhost"
    Write-Host "[WARNING] Error getting IP, will use localhost" -ForegroundColor Yellow
}

$accessUrl = "http://$ipAddress:7860"
$localUrl = "http://localhost:7860"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment URLs:" -ForegroundColor Cyan
Write-Host "  Local:  $localUrl" -ForegroundColor Green
Write-Host "  IP:     $accessUrl" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if container is already running
$existingContainer = docker ps -a --filter "name=chatppt" --format "{{.Names}}"
if ($existingContainer -eq "chatppt") {
    Write-Host "[INFO] Existing container found" -ForegroundColor Yellow
    $restart = Read-Host "Do you want to remove and recreate? (y/n)"
    if ($restart -eq "y" -or $restart -eq "Y") {
        Write-Host "[INFO] Stopping and removing existing container..." -ForegroundColor Yellow
        docker stop chatppt 2>$null
        docker rm chatppt 2>$null
    } else {
        Write-Host "[INFO] Starting existing container..." -ForegroundColor Yellow
        docker start chatppt
        Write-Host "[SUCCESS] Container started!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Access the service at: $accessUrl" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "To take screenshot:" -ForegroundColor Yellow
        Write-Host "  1. Open browser: $accessUrl" -ForegroundColor White
        Write-Host "  2. Use Win + Shift + S to screenshot" -ForegroundColor White
        Write-Host "  3. Save to: screenshots\ip_port_access.png" -ForegroundColor White
        Read-Host "Press Enter to view logs (Ctrl+C to exit)"
        docker logs -f chatppt
        exit 0
    }
}

# Build Docker image
Write-Host "[INFO] Building Docker image..." -ForegroundColor Yellow
docker build -t chatppt:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Docker build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[SUCCESS] Docker image built successfully" -ForegroundColor Green

# Create outputs directory if not exists
if (-not (Test-Path "outputs")) {
    New-Item -ItemType Directory -Path "outputs" | Out-Null
}

# Run Docker container
Write-Host ""
Write-Host "[INFO] Starting Docker container..." -ForegroundColor Yellow
docker run -d `
    --name chatppt `
    -p 7860:7860 `
    -e OPENAI_API_KEY=$env:OPENAI_API_KEY `
    -v "${PWD}\outputs:/app/outputs" `
    -v "${PWD}\templates:/app/templates" `
    -v "${PWD}\prompts:/app/prompts" `
    --restart unless-stopped `
    chatppt:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to start container" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[SUCCESS] Container started successfully!" -ForegroundColor Green
Write-Host ""

# Wait a moment for service to start
Write-Host "[INFO] Waiting for service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check container status
$containerStatus = docker ps --filter "name=chatppt" --format "{{.Status}}"
Write-Host "[INFO] Container status: $containerStatus" -ForegroundColor Cyan
Write-Host ""

# Get container IP (optional)
$containerIP = docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chatppt 2>$null
if ($containerIP) {
    Write-Host "[INFO] Container IP: $containerIP" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Service is running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor Cyan
Write-Host "  Local:  $localUrl" -ForegroundColor Green
Write-Host "  IP:     $accessUrl" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Screenshot Instructions:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open browser and visit: $accessUrl" -ForegroundColor White
Write-Host "2. Use Win + Shift + S to take screenshot" -ForegroundColor White
Write-Host "3. Ensure screenshot shows:" -ForegroundColor White
Write-Host "   - Browser address bar with IP:PORT" -ForegroundColor Gray
Write-Host "   - Complete ChatPPT interface" -ForegroundColor Gray
Write-Host "4. Save screenshot to: screenshots\ip_port_access.png" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Try to open browser automatically
try {
    Start-Process $accessUrl
    Write-Host "[INFO] Browser opened automatically" -ForegroundColor Green
} catch {
    Write-Host "[TIP] Please manually open browser: $accessUrl" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  View logs:    docker logs -f chatppt" -ForegroundColor White
Write-Host "  Stop:         docker stop chatppt" -ForegroundColor White
Write-Host "  Start:        docker start chatppt" -ForegroundColor White
Write-Host "  Remove:       docker rm -f chatppt" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop viewing logs" -ForegroundColor Yellow
Write-Host ""

# Show logs
docker logs -f chatppt

