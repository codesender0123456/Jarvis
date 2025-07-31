@echo off
echo Setting up Jarvis AI Assistant...
echo.

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo Installing Node.js dependencies...
cd frontend
npm install
cd ..

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Copy backend/env_example.txt to backend/.env
echo 2. Add your OpenAI API key to backend/.env
echo 3. Run start.bat to launch the application
echo.
pause 