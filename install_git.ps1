#!/usr/bin/env powershell
# Download and install Git for Windows silently

$gitVersion = "2.43.0"
$gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v$gitVersion.windows.1/Git-$gitVersion-64-bit.exe"
$installerPath = "$env:TEMP\git-installer.exe"

Write-Host "=" * 60
Write-Host "Installing Git for Windows"
Write-Host "=" * 60
Write-Host ""

# Download Git
Write-Host "1. Downloading Git installer..."
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $installerPath -TimeoutSec 300
    Write-Host "   ✓ Download complete"
} catch {
    Write-Host "   ✗ Download failed: $_"
    Write-Host ""
    Write-Host "Please download Git manually from: https://git-scm.com/download/win"
    exit 1
}

Write-Host ""
Write-Host "2. Installing Git..."
try {
    # Run installer silently
    & $installerPath /SILENT /NORESTART
    Start-Sleep -Seconds 5
    Write-Host "   ✓ Installation complete"
} catch {
    Write-Host "   ✗ Installation failed: $_"
    exit 1
}

Write-Host ""
Write-Host "3. Verifying Git installation..."
try {
    $gitVersion = & git --version
    Write-Host "   ✓ Git installed: $gitVersion"
} catch {
    Write-Host "   ✗ Git verification failed"
    Write-Host "   Please restart PowerShell and try again"
    exit 1
}

Write-Host ""
Write-Host "=" * 60
Write-Host "Git installation successful!"
Write-Host "=" * 60
Write-Host ""
Write-Host "Next step: Run the push_to_github.bat file"
Write-Host ""

# Clean up
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

exit 0
