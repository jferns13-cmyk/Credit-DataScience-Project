$ErrorActionPreference = "Stop"

$GIT = "C:\Program Files\Git\cmd\git.exe"
$REPO_PATH = "C:\Users\jfern\credit"
$GITHUB_URL = "https://github.com/jferns13-cmyk/Credit-DataScience-Project.git"
$USERNAME = "jferns13-cmyk"
$EMAIL = "jferns13@gmail.com"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Pushing Code to GitHub" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

try {
    Set-Location $REPO_PATH
    Write-Host "1. Configuring Git user..." -ForegroundColor Green
    & $GIT config --global user.name $USERNAME
    & $GIT config --global user.email $EMAIL
    Write-Host "   ✓ Username: $USERNAME" -ForegroundColor Green
    Write-Host "   ✓ Email: $EMAIL" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "2. Initializing repository..." -ForegroundColor Green
    & $GIT init
    Write-Host "   ✓ Repository initialized" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "3. Adding remote..." -ForegroundColor Green
    & $GIT remote remove origin 2>$null
    & $GIT remote add origin $GITHUB_URL
    Write-Host "   ✓ Remote: $GITHUB_URL" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "4. Staging files..." -ForegroundColor Green
    & $GIT add .
    Write-Host "   ✓ Files staged" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "5. Creating commit..." -ForegroundColor Green
    & $GIT commit -m "Initial commit: Credit classification ML project with Streamlit"
    Write-Host "   ✓ Commit created" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "6. Setting main branch..." -ForegroundColor Green
    & $GIT branch -M main
    Write-Host "   ✓ Branch: main" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "7. Pushing to GitHub..." -ForegroundColor Green
    Write-Host "   (This may require GitHub authentication)" -ForegroundColor Yellow
    & $GIT push -u origin main --force
    Write-Host "   ✓ Pushed successfully!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Code pushed to GitHub" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository: https://github.com/jferns13-cmyk/Credit-DataScience-Project" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host "==========================================================" -ForegroundColor Red
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host "==========================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "GitHub Authentication Required:" -ForegroundColor Yellow
    Write-Host "You need to set up one of the following:" -ForegroundColor Yellow
    Write-Host "  1. SSH Key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh" -ForegroundColor Yellow
    Write-Host "  2. Personal Access Token: https://github.com/settings/tokens" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
