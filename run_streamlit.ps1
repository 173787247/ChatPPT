# 启动 Streamlit 应用

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Streamlit Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Streamlit 是否安装
try {
    $streamlitVersion = streamlit --version 2>&1
    Write-Host "[SUCCESS] Streamlit is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Streamlit is not installed" -ForegroundColor Red
    Write-Host "Please install: pip install streamlit" -ForegroundColor Yellow
    exit 1
}

# 检查环境变量
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[WARNING] OPENAI_API_KEY not set" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please set the environment variable:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY="your_api_key_here"' -ForegroundColor Green
    Write-Host ""
    $setKey = Read-Host "Set it now? (y/n)"
    if ($setKey -eq "y" -or $setKey -eq "Y") {
        $apiKey = Read-Host "Enter OpenAI API Key"
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "[SUCCESS] API Key set for this session" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "[INFO] Starting Streamlit application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "The application will open in your browser automatically" -ForegroundColor Cyan
Write-Host "Default URL: http://localhost:8501" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# 启动 Streamlit
streamlit run src/streamlit_app.py

