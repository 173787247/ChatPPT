# ChatPPT Screenshot Helper Script
# This script will start the service and provide screenshot guidance

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Screenshot Helper Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check environment variable
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[ERROR] OPENAI_API_KEY environment variable is not set" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set the environment variable first:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get local IP address
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

$localUrl = "http://localhost:7860"
$ipUrl = "http://$ipAddress:7860"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Service Access URLs:" -ForegroundColor Cyan
Write-Host "  Local: $localUrl" -ForegroundColor Green
Write-Host "  IP:    $ipUrl" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create screenshot directory
$screenshotDir = Join-Path $PSScriptRoot "screenshots"
if (-not (Test-Path $screenshotDir)) {
    New-Item -ItemType Directory -Path $screenshotDir | Out-Null
}

# Generate screenshot guide
$screenshotGuide = @"
# Screenshot Steps

## 1. Open browser and visit one of these URLs:
- Local: $localUrl
- IP:    $ipUrl

## 2. Take screenshot using:
- Windows shortcut: Win + Shift + S
- Or use Snipping Tool

## 3. Screenshot requirements:
- Show browser address bar (with IP:PORT or localhost:7860)
- Show complete ChatPPT interface
- Interface displays normally with input box and buttons

## 4. Save screenshot:
- Filename: ip_port_access.png
- Save location: $screenshotDir\ip_port_access.png

## 5. After screenshot, press Ctrl+C to stop the service
"@

$guidePath = Join-Path $screenshotDir "SCREENSHOT_INSTRUCTIONS.txt"
$screenshotGuide | Out-File -FilePath $guidePath -Encoding UTF8

Write-Host "[INFO] Screenshot guide saved to: $guidePath" -ForegroundColor Green
Write-Host ""
Write-Host "[TIP] Please follow these steps:" -ForegroundColor Yellow
Write-Host "  1. After service starts, open browser: $ipUrl" -ForegroundColor White
Write-Host "  2. Use Win + Shift + S to take screenshot" -ForegroundColor White
Write-Host "  3. Save screenshot to: $screenshotDir\ip_port_access.png" -ForegroundColor White
Write-Host "  4. After screenshot, press Ctrl+C to stop service" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting service..." -ForegroundColor Yellow
Write-Host "After service starts, open browser in a new window" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Try to open browser automatically (optional)
Start-Sleep -Seconds 2
try {
    Start-Process $ipUrl
    Write-Host "[INFO] Browser opened automatically" -ForegroundColor Green
} catch {
    Write-Host "[TIP] Please manually open browser: $ipUrl" -ForegroundColor Yellow
}

# Start service
python src/gradio_server.py
