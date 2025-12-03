# Run ChatPPT directly (without Docker)
# For network issues or quick testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Direct Run (No Docker)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[SUCCESS] Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check environment variable
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[WARNING] OPENAI_API_KEY not set" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set API Key:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    $setKey = Read-Host "Set it now? (y/n)"
    if ($setKey -eq "y" -or $setKey -eq "Y") {
        $apiKey = Read-Host "Enter OpenAI API Key"
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "[SUCCESS] API Key set (session only)" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] API Key required" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] OPENAI_API_KEY is set" -ForegroundColor Green
}

# Check dependencies
Write-Host ""
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERROR] requirements.txt not found" -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
Write-Host "[INFO] Checking Python packages..." -ForegroundColor Yellow
$missingPackages = @()
$requiredPackages = @("gradio", "pptx", "openai", "langchain")
foreach ($package in $requiredPackages) {
    $importName = $package
    if ($package -eq "pptx") {
        $importName = "pptx"
    } elseif ($package -eq "python-pptx") {
        $importName = "pptx"
    }
    $result = python -c "import $importName" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "[WARNING] Missing packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "[SUCCESS] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[OK] All dependencies installed" -ForegroundColor Green
}

# Get local IP
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
    }
} catch {
    $ipAddress = "localhost"
}

$accessUrl = "http://$ipAddress:7860"
$localUrl = "http://localhost:7860"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting service..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor Yellow
Write-Host "  Local:  $localUrl" -ForegroundColor Green
Write-Host "  Network: $accessUrl" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop service" -ForegroundColor Yellow
Write-Host ""

# Set environment variables
$env:SERVER_NAME = "0.0.0.0"
$env:SERVER_PORT = "7860"

# Start service
try {
    python src/gradio_server.py
} catch {
    Write-Host "[ERROR] Failed to start service" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
