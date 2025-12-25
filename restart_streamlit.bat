@echo off
echo ========================================
echo Restarting Streamlit with Latest Code
echo ========================================
echo.

echo Step 1: Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 >nul

echo.
echo Step 2: Killing Python processes running Streamlit...
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python.exe"') do (
    taskkill /F /PID %%a 2>nul
)
timeout /t 2 >nul

echo.
echo Step 3: Starting Streamlit with updated code...
echo.
echo IMPORTANT: Watch the terminal output for DEBUG messages
echo You should see: "DEBUG: Target language is: en"
echo.

start cmd /k "streamlit run streamlit_app.py"

echo.
echo ========================================
echo Streamlit is starting in a new window!
echo ========================================
echo.
echo Go to: http://localhost:8501
echo.
echo When you translate:
echo 1. Upload Arabic IDML file
echo 2. Select "English" from dropdown
echo 3. Click "Translate Now"
echo 4. Watch the terminal for DEBUG messages
echo.
pause
