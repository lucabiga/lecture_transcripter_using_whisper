#!/bin/bash

echo "========================================"
echo "Installing Whisper with CUDA support"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Uninstalling any existing PyTorch installation..."
pip uninstall torch torchvision torchaudio -y

echo ""
echo "Installing PyTorch with CUDA 12.1 support..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo ""
echo "Installing Whisper and other dependencies..."
pip install openai-whisper tqdm

echo ""
echo "========================================"
echo "Verifying CUDA installation..."
echo "========================================"
python -c "import torch; print('\nCUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('\nIf CUDA is True, you are ready to go!')"

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "To use the transcriber:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: python transcripter.py your_video.mp4"
echo ""
