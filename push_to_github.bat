@echo off
REM GitHub Push Script for Credit Classification Project
REM This script pushes code to GitHub after Git is installed

setlocal enabledelayedexpansion

echo ============================================================
echo      Pushing Code to GitHub
echo ============================================================
echo.

set REPO_PATH=C:\Users\jfern\credit
set GITHUB_URL=https://github.com/jferns13-cmyk/Credit-DataScience-Project.git
set USERNAME=jferns13-cmyk
set EMAIL=jferns13@gmail.com

cd /d %REPO_PATH%

REM Check if Git is installed
set GIT="C:\Program Files\Git\cmd\git.exe"
if not exist %GIT% (
    REM Try alternative path
    set GIT="C:\Program Files (x86)\Git\cmd\git.exe"
    if not exist %GIT% (
        echo ERROR: Git is not installed!
        echo Please install Git from: https://git-scm.com/download/win
        pause
        exit /b 1
    )
)

echo 1. Initializing Git repository...
%GIT% init
echo.

echo 2. Configuring Git user...
%GIT% config user.name "%USERNAME%"
%GIT% config user.email "%EMAIL%"
echo    Username: %USERNAME%
echo    Email: %EMAIL%
echo.

echo 3. Adding remote repository...
%GIT% remote remove origin 2>nul
%GIT% remote add origin %GITHUB_URL%
echo    Remote: %GITHUB_URL%
echo.

echo 4. Creating .gitignore...
(
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo *.so
    echo .Python
    echo build/
    echo dist/
    echo eggs/
    echo .eggs/
    echo *.egg-info/
    echo # Virtual environments
    echo venv/
    echo ENV/
    echo # IDE
    echo .vscode/
    echo .idea/
    echo # Cache
    echo .streamlit/cache/
) > .gitignore
echo    .gitignore created
echo.

echo 5. Adding files to Git...
%GIT% add .gitignore
%GIT% add *.py
%GIT% add models/
echo    Files added
echo.

echo 6. Creating commit...
%GIT% commit -m "Initial commit: Credit classification ML project with Streamlit"
echo    Commit created
echo.

echo 7. Setting default branch...
%GIT% branch -M main
echo    Branch: main
echo.

echo 8. Pushing to GitHub...
echo.
%GIT% push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo      SUCCESS! Code pushed to GitHub
    echo ============================================================
    echo Repository: %GITHUB_URL%
    echo.
) else (
    echo.
    echo ============================================================
    echo      PUSH FAILED
    echo ============================================================
    echo Make sure you have set up GitHub authentication:
    echo - SSH Key: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
    echo - Personal Access Token: https://github.com/settings/tokens
    echo.
)

pause
