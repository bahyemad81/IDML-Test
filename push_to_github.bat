@echo off
echo ========================================
echo IDML Translation Tool - GitHub Push
echo ========================================
echo.

REM Try to find Git from GitHub Desktop
set "GIT_PATH="
for /d %%i in ("%LOCALAPPDATA%\GitHubDesktop\app-*") do (
    if exist "%%i\resources\app\git\cmd\git.exe" (
        set "GIT_PATH=%%i\resources\app\git\cmd\git.exe"
    )
)

REM If not found, try system Git
if "%GIT_PATH%"=="" (
    where git >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "GIT_PATH=git"
    )
)

if "%GIT_PATH%"=="" (
    echo ERROR: Git not found!
    echo.
    echo Please either:
    echo 1. Use GitHub Desktop GUI (easier)
    echo 2. Install Git from https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Found Git: %GIT_PATH%
echo.

REM Configure Git (if not already configured)
"%GIT_PATH%" config --global user.name >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Configuring Git...
    set /p USERNAME="Enter your GitHub username: "
    set /p EMAIL="Enter your GitHub email: "
    "%GIT_PATH%" config --global user.name "%USERNAME%"
    "%GIT_PATH%" config --global user.email "%EMAIL%"
)

echo Step 1: Initializing Git repository...
"%GIT_PATH%" init
if %ERRORLEVEL% NEQ 0 (
    echo Git repository already initialized or error occurred
)

echo.
echo Step 2: Adding all files...
"%GIT_PATH%" add .

echo.
echo Step 3: Creating initial commit...
"%GIT_PATH%" commit -m "Initial commit - IDML Arabic Translation Tool"

echo.
echo Step 4: Setting up remote repository...
"%GIT_PATH%" remote remove origin >nul 2>&1
"%GIT_PATH%" remote add origin https://github.com/bahyemad81/IDML-Test.git

echo.
echo Step 5: Renaming branch to main...
"%GIT_PATH%" branch -M main

echo.
echo Step 6: Pushing to GitHub...
echo.
echo NOTE: You may be prompted for GitHub credentials.
echo Use your GitHub username and Personal Access Token (not password).
echo.
echo To create a token: https://github.com/settings/tokens
echo.
"%GIT_PATH%" push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Your code is now on GitHub!
    echo ========================================
    echo.
    echo View your repository at:
    echo https://github.com/bahyemad81/IDML-Test
    echo.
    echo Next steps:
    echo 1. Deploy to Streamlit Cloud: https://share.streamlit.io
    echo 2. Share your app with the world!
    echo.
) else (
    echo.
    echo ========================================
    echo Push failed. Common issues:
    echo ========================================
    echo.
    echo 1. Authentication failed
    echo    - Use Personal Access Token, not password
    echo    - Create token: https://github.com/settings/tokens
    echo.
    echo 2. Repository already exists
    echo    - Delete it on GitHub first
    echo    - Or use: git pull origin main --allow-unrelated-histories
    echo.
    echo 3. Permission denied
    echo    - Check you're logged into the correct GitHub account
    echo.
)

pause
