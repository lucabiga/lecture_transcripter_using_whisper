@echo off
echo ============================================
echo   Whisper Transcription API Server
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run install_cuda.bat first.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if API dependencies are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo.
    echo API dependencies not installed!
    echo Installing FastAPI and dependencies...
    echo.
    pip install fastapi uvicorn[standard] python-multipart aiofiles
    echo.
)

REM Start the server
echo.
echo Starting API server...
echo.
echo Web Interface: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

python api_server.py

pause
