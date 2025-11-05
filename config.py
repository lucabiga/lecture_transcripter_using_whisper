"""
Configuration file for Whisper Transcription API Server
Modify these settings according to your needs
"""

import os
from pathlib import Path

# Server Settings
SERVER_HOST = "0.0.0.0"  # Listen on all interfaces (use "127.0.0.1" for localhost only)
SERVER_PORT = 8000

# File Upload Settings
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB in bytes

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    '.mp4', '.mp3', '.wav', '.m4a', 
    '.avi', '.mov', '.flac', '.ogg', 
    '.webm', '.mkv', '.wma'
}

# Whisper Model Settings
# Options: "tiny", "base", "small", "medium", "large"
# Larger models = better accuracy but slower and more VRAM
WHISPER_MODEL = "medium"

# Text splitting (for LLM compatibility)
MAX_CHARS_PER_FILE = 30000

# Automatic cleanup
AUTO_DELETE_UPLOADS = True  # Delete uploaded files after transcription
AUTO_DELETE_OUTPUTS_AFTER_DAYS = 7  # Delete old outputs (0 = never)

# CORS Settings (for web interface)
CORS_ORIGINS = ["*"]  # Allow all origins (restrict in production!)

# GPU Settings
FORCE_CPU = False  # Set to True to force CPU even if GPU is available

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Create directories if they don't exist
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
