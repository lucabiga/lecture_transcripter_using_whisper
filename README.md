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
cd lecture_transcripter_using_whisper
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
Contains all transcribed segments with metadata and timestamps:

```json
{
  "language": "it",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 9.0,
      "text": "Transcribed text for this segment.",
      "tokens": [50364, 28473, ...],
      "temperature": 0.0,
      "avg_logprob": -0.44,
      "compression_ratio": 1.25,
      "no_speech_prob": 0.0024
    }
  ],
  "text": "Full concatenated transcription here."
}
```

**JSON Structure Explanation:**

**Top-level fields:**
- `language`: Detected or selected language code (e.g., "en", "it")
- `segments`: Array of time-stamped transcription segments
- `text`: Complete transcription as a single string

**Segment fields:**
- `id`: Sequential segment number (0, 1, 2, ...)
- `start`: Start time in seconds (e.g., 0.0)
- `end`: End time in seconds (e.g., 9.0)
- `text`: Transcribed text for this time segment
- `seek`: Internal audio position (used by Whisper for processing)
- `tokens`: Numerical token IDs used by the AI model
- `temperature`: Sampling temperature (0.0 = deterministic, higher = more random)
- `avg_logprob`: Average log probability (closer to 0 = higher confidence)
- `compression_ratio`: Text compression ratio (helps detect repetitions)
- `no_speech_prob`: Probability of silence/no speech (0.0-1.0, lower = speech detected)

**Practical uses:**

**1. Creating subtitles with precise timing:**
```python
for segment in data['segments']:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

**2. Quality assessment:**
- Check `avg_logprob`: values below -1.0 may indicate uncertain transcriptions
- Check `no_speech_prob`: values above 0.5 may indicate silence or background noise
- Review segments with low confidence for manual correction

**3. Timestamped notes and documentation:**
```markdown
## Lecture Notes

[00:00 - 00:09] Introduction and overview
[00:09 - 00:25] First main concept explained
...
```

**4. Integration with LLMs:**
- Feed the JSON to ChatGPT, Claude, or other LLMs
- Request summaries with preserved timestamps
- Generate structured notes, Q&A sets, or study guides

**5. Data processing and analysis:**
- Extract specific time ranges
- Search for keywords with timestamps
- Analyze speech patterns and pacing
- Create searchable transcription databases

This file is extremely useful if you plan to:
- Synchronize notes or subtitles with timestamps
- Generate summaries, structured notes, or question-answer sets
- Verify transcription quality and identify uncertain segments
- Integrate the output into your own data processing or LLM pipelines
- Create time-coded references for study materials

---

## 📚 Using the Output with an LLM to Generate Lecture Notes

This repository includes a **comprehensive prompt template** (`PROMPT_TEMPLATE.md`) specifically designed to convert your transcription files and lecture slides into high-quality, academic-style Markdown notes.

### Why use the prompt template?

- **Structured workflow**: Clear instructions for processing multiple transcript files with slides
- **Language flexibility**: Support for both English and Italian output (easily expandable)
- **Subject-agnostic**: Works for any university course (Computer Science, Physics, Math, etc.)
- **Professional output**: Generates discursive, well-organized notes suitable for study or publication
- **LaTeX support**: Properly formats mathematical formulas and code snippets
- **Handles long transcripts**: Workflow for processing multiple `.txt` files in sequence

---

### 🚀 Quick Start: Generating Lecture Notes

#### Step 1: Transcribe your lecture
```bash
python transcripter.py path/to/lecture_video.mp4
```

This will generate:
- `lecture_part1.txt`, `lecture_part2.txt`, etc. (transcript chunks)
- `lecture_segments.json` (timestamped data)

#### Step 2: Prepare your materials

Gather:
- ✅ The generated `.txt` transcription files
- ✅ Your lecture slides (PDF)
- ✅ The `PROMPT_TEMPLATE.md` file from this repository

#### Step 3: Customize the prompt

Open `PROMPT_TEMPLATE.md` and configure:

1. **Subject/Topic**: Replace `[SUBJECT]` with your course name
   - Example: "Computer Graphics", "Machine Learning", "Quantum Physics"

2. **Language**: Replace `[LANGUAGE: Italian / English]` with your choice
   - Use "Italian" or "English" throughout the template

3. **Number of files**: Note how many transcript files were generated

#### Step 4: Use with your preferred LLM

**Recommended LLMs** (choose one):
- ChatGPT (GPT-4 or GPT-4 Turbo for best results)
- Claude (Anthropic - excellent for long documents)
- Gemini (Google - large context window)

**Workflow:**

1. Copy the **customized prompt** from `PROMPT_TEMPLATE.md`
2. Paste it into your LLM conversation
3. Upload your **PDF slides**
4. Paste the **first transcript file** (`lecture_part1.txt`)
5. Wait for acknowledgment, then paste the next file
6. Continue until all files are provided
7. Type **"Done"** when finished
8. The LLM will generate a complete Markdown document

#### Step 5: Download and use your notes

The LLM will produce a comprehensive `.md` file that you can:
- Use in Obsidian, Notion, or any Markdown editor
- Convert to PDF, HTML, or other formats
- Study directly or share with classmates
- Further edit and annotate

---

### 📋 Example Usage Session

**You:**
```
I will now provide you with materials for a Computer Graphics lecture.

Target language: English

I will upload:
- Slide deck (PDF)
- 3 transcript files (.txt)

Please create detailed, discursive lecture notes in Markdown 
following the structure outlined above.

Starting with the slides and first transcript...

[Upload slides.pdf]
[Paste lecture_part1.txt content]
```

**LLM:** *Acknowledges and processes first part*

**You:** 
```
[Paste lecture_part2.txt content]
```

**LLM:** *Acknowledges and processes second part*

**You:**
```
[Paste lecture_part3.txt content]
```

**LLM:** *Acknowledges and processes third part*

**You:**
```
Done
```

**LLM:** *Generates complete Markdown lecture notes*

---

### 💡 Tips for Best Results

**For better transcription quality:**
- Use the `medium` or `large` Whisper model for academic content
- Select the correct language during transcription
- Ensure good audio quality in your source video

**For better LLM-generated notes:**
- Always provide both slides (PDF) and transcripts
- Use GPT-4 or Claude for complex technical subjects
- If output is cut off, ask the LLM to "continue" or "complete the section"
- Review and manually adjust formulas or code if needed

**Time management:**
- Transcription: 5-10 minutes per hour of lecture (with GPU)
- LLM processing: 2-5 minutes per transcript chunk
- Manual review: 10-15 minutes

**Total time: ~30-45 minutes for a full 2-hour lecture** ⚡

---

### 🎯 What You Get

The final Markdown notes will include:

✅ **Structured headings** organized by topic  
✅ **Continuous prose** (not bullet points) - reads like a textbook  
✅ **LaTeX formulas** properly formatted (`$$` for blocks, `$` for inline)  
✅ **Code snippets** with syntax highlighting  
✅ **Integrated explanations** from both slides and spoken content  
✅ **Academic tone** suitable for study or publication  
✅ **Logical flow** that follows the lecture progression  

**Example output structure:**
```markdown
# Lecture 4: Ray Tracing Fundamentals

## Introduction to Ray Tracing

Ray tracing is a rendering technique that simulates the physical 
behavior of light to generate photorealistic images...

### The Ray-Scene Intersection Problem

Given a ray $\mathbf{r}(t) = \mathbf{o} + t\mathbf{d}$ where 
$\mathbf{o}$ is the origin and $\mathbf{d}$ is the direction...

## Implementation in OpenGL

```cpp
vec3 rayDirection = normalize(pixelPos - cameraPos);
float t = intersectSphere(rayOrigin, rayDirection, sphere);
```

...
```

---

### 📁 Alternative: Quick LLM Prompt (Simple Version)

If you don't need the full template workflow, here's a quick prompt:

```
Using this lecture transcription (JSON format) and the accompanying slides, 
generate a Markdown study guide with timestamps, section titles, and short summaries.
Highlight key concepts and transitions between topics.

Write in [English/Italian], include LaTeX formulas ($$...$$), and code blocks (```).
Make it suitable for academic study.
```

Then provide:
- The `*_segments.json` file (for timestamps)
- The original slides
- Any specific formatting requirements

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

