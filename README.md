![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![CUDA](https://img.shields.io/badge/CUDA-Supported-green.svg)

# Whisper Transcription Tool (CUDA-compatible)

This repository provides a Python script for **automatic speech transcription** from video or audio files using OpenAI's [Whisper](https://github.com/openai/whisper) model.  
It supports GPU acceleration (CUDA), multi-language selection, JSON export with timestamps, and text splitting for use with LLMs or documentation tools.

---

## Features

- Supports **English** and **Italian** (other languages can be autodetected).
- Automatically uses **GPU (CUDA)** if available, otherwise defaults to CPU.
- Saves transcription both as:
  - Multiple `.txt` files (split into chunks of ~30,000 characters each, suitable for LLM input limits).
  - A `.json` file with full metadata (timestamps, segments, language, and confidence data).
- Optional `--json-only` mode to skip text generation and only export structured JSON data.
- Progress bar (`tqdm`) for real-time transcription feedback.
- Compatible with long audio or video recordings.

---

## Installation

### 1. Clone this repository
```bash
git clone https://github.com/lucabiga/lecture_transcripter_using_whisper.git
cd whisper-transcriber
```

### 2. Create and activate a Python virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

#### Windows Execution Policy Issue

If you encounter an execution policy error like:

```
+ CategoryInfo          : SecurityError: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
```

Run the following command **before executing scripts**:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
This temporarily allows PowerShell to run local scripts (like activate.ps1) during your session without permanently changing the system policy.


### 3. Install dependencies

#### QUICK INSTALL (Windows - RECOMMENDED)

Simply run the automated installation script:

```bash
install_cuda.bat
```

This will:
- Create a virtual environment (if not exists)
- Install PyTorch with CUDA 12.1 support
- Install Whisper and dependencies
- Verify CUDA is working

#### 🚀 QUICK INSTALL (Linux/macOS)

```bash
chmod +x install_cuda.sh
./install_cuda.sh
```

#### Manual Installation

**IMPORTANT: Install PyTorch with CUDA support FIRST!**

##### For GPU (CUDA) - RECOMMENDED for speed:

```bash
# For CUDA 12.x (RTX 30xx, 40xx, A100, etc.)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Then install other dependencies
pip install openai-whisper tqdm
```

##### For CPU-only (NOT recommended - 10-20x slower):

```bash
pip install torch torchvision torchaudio
pip install openai-whisper tqdm
```

#### Verify CUDA installation:

After installation, verify that PyTorch can see your GPU:

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

You should see:
```
CUDA available: True
GPU: NVIDIA GeForce RTX XXXX
```

---


## Usage

### Basic transcription
```bash
python transcripter.py path/to/video.mp4
```

### JSON-only output
If you only need structured data (timestamps, language, and text):
```bash
python transcripter.py path/to/video.mp4 --json-only
```

During execution, you will be asked to select the spoken language:
```
Select language for transcription:
1) English
2) Italian
```

The script will automatically detect and use your GPU if available.

---

## Output structure

After transcription, you will find the following files in the same directory as your input video:

```
lecture_part1.txt
lecture_part2.txt
lecture_segments.json
```

### `.txt` files
Contain the raw transcription split into ~30,000-character parts.  
This makes it easier to feed the text into an LLM (such as ChatGPT, Claude, or Gemini) without hitting token limits.

### `.json` file
Contains all transcribed segments with metadata:

```json
{
  "language": "en",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 8.3,
      "text": "Hello everyone, welcome to today's lecture."
    },
    ...
  ],
  "text": "Full concatenated transcription here."
}
```

This file is extremely useful if you plan to:
- Synchronize notes or subtitles with timestamps.
- Generate summaries, structured notes, or question-answer sets.
- Integrate the output into your own data processing or LLM pipelines.

---

## Using the Output with an LLM

To make the best use of this transcription data, you can combine the generated files with an LLM to produce summaries, structured notes, or formatted Markdown documents.

### Recommended approach

1. **Provide both**:
   - The `*_segments.json` file (so the LLM can reference timestamps).
   - The original slides or lecture materials (for semantic context).
2. Ask the LLM to:
   - Summarize the transcription section by section.
   - Create a structured Markdown file (headings, bullet points, timestamps).
   - Extract definitions, examples, or code references.

Example prompt:
```
Using this lecture transcription (JSON format) and the accompanying slides, 
generate a Markdown study guide with timestamps, section titles, and short summaries.
Highlight key concepts and transitions between topics.
```

---

## Troubleshooting

### Script says "Using device: CPU" instead of CUDA

This means PyTorch was installed **without CUDA support**. To fix:

1. **Uninstall the CPU-only version**:
   ```bash
   pip uninstall torch torchvision torchaudio -y
   ```

2. **Reinstall with CUDA support**:
   ```bash
   # For CUDA 12.x (most modern GPUs)
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

3. **Verify CUDA is now available**:
   ```bash
   python -c "import torch; print('CUDA:', torch.cuda.is_available())"
   ```

### "FP16 is not supported on CPU" warning

This warning appears when using CPU mode. It's harmless but indicates slower performance.  
**Solution**: Install PyTorch with CUDA support (see above).

### Transcription stops after one sentence

This was a bug in earlier versions caused by `whisper.pad_or_trim()` cutting audio to 30 seconds.  
**Solution**: Make sure you're using the latest version of `transcripter.py` which uses `model.transcribe()` correctly.

### Out of memory error on GPU

If you get CUDA out of memory errors:
- Try a smaller model: change `MODEL_NAME = "medium"` to `"small"` or `"tiny"` in the script
- Close other GPU-intensive applications
- Check GPU memory usage: `nvidia-smi`

---

## Performance Notes

**GPU (CUDA) vs CPU speed comparison** for a 1-hour lecture:

| Device | Model Size | Approximate Time |
|--------|-----------|------------------|
| CPU | medium | ~60-90 minutes |
| GPU (RTX 4060) | medium | ~5-8 minutes |
| GPU (RTX 4090) | large | ~4-6 minutes |

**⚠️ Using CUDA is 10-20x faster than CPU!**

---

## License

This project uses [OpenAI Whisper](https://github.com/openai/whisper), which is licensed under the MIT License as well.

---

