# ChatPPT Screenshot Upload Script
# Help user upload screenshot to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ChatPPT Screenshot Upload Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$screenshotDir = Join-Path $PSScriptRoot "screenshots"
$screenshotFile = Join-Path $screenshotDir "ip_port_access.png"

# Check if screenshot file exists
if (-not (Test-Path $screenshotFile)) {
    Write-Host "[ERROR] Screenshot file not found: $screenshotFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please take screenshot first and save to: $screenshotFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Screenshot steps:" -ForegroundColor Cyan
    Write-Host "  1. Run capture_screenshot.ps1 to start service" -ForegroundColor White
    Write-Host "  2. Open browser and take screenshot" -ForegroundColor White
    Write-Host "  3. Save screenshot as: ip_port_access.png" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[SUCCESS] Found screenshot file: $screenshotFile" -ForegroundColor Green

# Check file size
$fileSize = (Get-Item $screenshotFile).Length / 1MB
Write-Host "[INFO] File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Yellow

if ($fileSize -gt 10) {
    Write-Host "[WARNING] File is large, consider compressing before upload" -ForegroundColor Yellow
}

# Update SUBMISSION.md
$submissionFile = Join-Path $PSScriptRoot "SUBMISSION.md"
if (Test-Path $submissionFile) {
    Write-Host "[INFO] Updating submission document..." -ForegroundColor Yellow
    
    $content = Get-Content $submissionFile -Raw -Encoding UTF8
    
    # Check if screenshot path needs to be updated
    if ($content -notmatch "ip_port_access\.png") {
        Write-Host "[TIP] Please add screenshot reference in SUBMISSION.md" -ForegroundColor Yellow
    }
}

# Git operations
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Preparing to commit to Git..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Git status
$gitStatus = git status --porcelain 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[INFO] Git repository status OK" -ForegroundColor Green
    
    # Add files
    Write-Host "[INFO] Adding screenshot file to Git..." -ForegroundColor Yellow
    git add $screenshotFile
    if (Test-Path $submissionFile) {
        git add $submissionFile
    }
    
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Check files: git status" -ForegroundColor White
    Write-Host "  2. Commit changes: git commit -m 'docs: add deployment screenshot'" -ForegroundColor White
    Write-Host "  3. Push to remote: git push myfork gradio-chatbot-integration" -ForegroundColor White
    Write-Host ""
    
    $confirm = Read-Host "Commit and push now? (y/n)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host ""
        Write-Host "[INFO] Committing changes..." -ForegroundColor Yellow
        git commit -m "docs: add deployment screenshot"
        
        Write-Host "[INFO] Pushing to remote..." -ForegroundColor Yellow
        git push myfork gradio-chatbot-integration
        
        Write-Host ""
        Write-Host "[SUCCESS] Screenshot uploaded to GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "GitHub link:" -ForegroundColor Cyan
        Write-Host "  https://github.com/173787247/ChatPPT/tree/gradio-chatbot-integration/screenshots" -ForegroundColor Green
    }
} else {
    Write-Host "[WARNING] Current directory is not a Git repository or Git not initialized" -ForegroundColor Yellow
    Write-Host "[TIP] Please manually add screenshot file to Git" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
