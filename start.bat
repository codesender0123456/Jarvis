@echo off
echo Starting Jarvis AI Assistant...
echo.

echo Starting Backend Server...
start "Jarvis Backend" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Frontend...
start "Jarvis Frontend" cmd /k "cd frontend && npm start"

echo.
echo Jarvis AI Assistant is starting up!
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press any key to exit this launcher...
pause > nul 