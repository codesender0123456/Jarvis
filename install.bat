@echo off
echo ========================================
echo    Jarvis AI Assistant - Installation
echo ========================================
echo.

echo Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo ✓ Python found
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✓ Node.js found
)

echo.
echo All prerequisites met!
echo.

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Installing Node.js dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo Setting up environment file...
if not exist "backend\.env" (
    copy "backend\env_example.txt" "backend\.env"
    echo ✓ Environment file created
) else (
    echo ✓ Environment file already exists
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your API keys:
echo    - OPENAI_API_KEY (required)
echo    - GOOGLE_API_KEY (optional - for Gemini)
echo    - GOOGLE_SEARCH_API_KEY (optional - for web search)
echo    - SEARCH_ENGINE_ID (optional - for web search)
echo    - OPENWEATHER_API_KEY (optional - for weather)
echo.
echo 2. Run start.bat to launch Jarvis
echo.
echo 3. Open http://localhost:3000 in your browser
echo.
pause 