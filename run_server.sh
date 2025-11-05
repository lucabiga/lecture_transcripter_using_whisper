#!/bin/bash

echo "============================================"
echo "  Whisper Transcription API Server"
echo "============================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run install_cuda.sh first."
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if API dependencies are installed
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "API dependencies not installed!"
    echo "Installing FastAPI and dependencies..."
    echo ""
    pip install fastapi uvicorn[standard] python-multipart aiofiles
    echo ""
fi

# Start the server
echo ""
echo "Starting API server..."
echo ""
echo "Web Interface: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

python api_server.py
