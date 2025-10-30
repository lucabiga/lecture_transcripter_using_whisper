import subprocess
import sys
from pathlib import Path

# --- Automatic dependency installer ---
def install_requirements():
    """Install dependencies from requirements.txt if missing."""
    req_path = Path(__file__).parent / "requirements.txt"
    if not req_path.exists():
        print("requirements.txt not found. Creating default one...")
        req_path.write_text("openai-whisper\ntorch\ntqdm\n", encoding="utf-8")

    try:
        import whisper, torch, tqdm  # noqa
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_path)])
        print("Dependencies installed successfully.\n")

install_requirements()

# --- Now import the libraries safely ---
import whisper
import torch
import json
from tqdm import tqdm

# --- Configuration ---
MODEL_NAME = "medium"   # "tiny", "small", "medium", "large"
CHUNK_SIZE = 30000      # characters per text file
# ----------------------

def ask_language():
    print("\nSelect language for transcription:")
    print("1) English")
    print("2) Italian")
    choice = input("Choose (1 or 2): ").strip()
    if choice == "2":
        return "it"
    elif choice == "1":
        return "en"
    else:
        print("Invalid choice. Defaulting to English.")
        return "en"

def split_text(text, chunk_size):
    """Split text into chunks of approximately `chunk_size` characters."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe_video_cuda.py <video_file> [--json-only]")
        sys.exit(1)

    video_path = Path(sys.argv[1])
    if not video_path.exists():
        print(f"File not found: {video_path}")
        sys.exit(1)

    json_only = "--json-only" in sys.argv
    language = ask_language()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nUsing device: {device.upper()}")

    print(f"Loading Whisper model '{MODEL_NAME}' ...")
    model = whisper.load_model(MODEL_NAME, device=device)

    print(f"Loading audio from {video_path.name} ...")
    audio = whisper.load_audio(str(video_path))
    audio = whisper.pad_or_trim(audio)

    print("Preprocessing audio ...")
    mel = whisper.log_mel_spectrogram(audio).to(device)

    if language not in ["en", "it"]:
        print("Detecting language ...")
        _, probs = model.detect_language(mel)
        language = max(probs, key=probs.get)
        print(f"Detected language: {language}")

    print(f"Transcribing {video_path.name} ... please wait.")
    options = whisper.DecodingOptions(language=language, fp16=(device == "cuda"))

    import math
    duration_s = len(audio) / whisper.audio.SAMPLE_RATE
    segment_dur = 30
    num_segments = math.ceil(duration_s / segment_dur)

    segments = []
    for i in tqdm(range(num_segments), desc="Transcribing", unit="segment"):
        start = i * segment_dur
        end = min((i + 1) * segment_dur, duration_s)
        seg_audio = audio[int(start * whisper.audio.SAMPLE_RATE):int(end * whisper.audio.SAMPLE_RATE)]
        seg_mel = whisper.log_mel_spectrogram(seg_audio).to(device)
        result = whisper.decode(model, seg_mel, options)
        segments.append({
            "id": i,
            "start": start,
            "end": end,
            "text": result.text.strip()
        })

    full_text = "\n".join([s["text"] for s in segments]).strip()
    base_name = video_path.stem

    json_path = video_path.parent / f"{base_name}_segments.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "language": language,
            "segments": segments,
            "text": full_text
        }, f, indent=2, ensure_ascii=False)
    print(f"\nJSON segments saved to: {json_path}")

    if json_only:
        print("JSON-only mode enabled. Skipping text file generation.")
        return

    chunks = split_text(full_text, CHUNK_SIZE)
    output_files = []
    for i, chunk in enumerate(chunks, start=1):
        output_path = video_path.parent / f"{base_name}_part{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        output_files.append(output_path)

    print("\nTranscription completed successfully!")
    print(f"Total characters: {len(full_text):,}")
    print(f"Files created ({len(chunks)} parts of ~{CHUNK_SIZE} chars):")
    for file in output_files:
        print(f"  - {file.name}")
    print(f"JSON file: {json_path.name}")

if __name__ == "__main__":
    main()
