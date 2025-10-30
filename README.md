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

## Windows Execution Policy Issue

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
```bash
pip install -r requirements.txt
```

You can also install them manually:
```bash
pip install openai-whisper torch tqdm
```

---

## requirements.txt

For convenience, this file should contain:
```
openai-whisper
torch
tqdm
```

---

## Usage

### Basic transcription
```bash
python transcribe_video_cuda.py path/to/video.mp4
```

### JSON-only output
If you only need structured data (timestamps, language, and text):
```bash
python transcribe_video_cuda.py path/to/video.mp4 --json-only
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

## GPU notes

If CUDA is available, the script will automatically use it.  
To verify that PyTorch detects your GPU:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

If it returns `True`, Whisper will run significantly faster on your GPU.

---

## License

This project uses [OpenAI Whisper](https://github.com/openai/whisper), which is licensed under the MIT License as well.

---

