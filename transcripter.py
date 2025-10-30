import subprocess
import sys
from pathlib import Path

# --- Automatic dependency installer ---
def install_requirements():
    """Install dependencies if missing, with CUDA warning."""
    try:
        import whisper, torch  # noqa
    except ImportError:
        print("\n" + "="*70)
        print("MISSING DEPENDENCIES DETECTED")
        print("="*70)
        print("\nFor BEST PERFORMANCE, install PyTorch with CUDA support:")
        print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        print("\nThen install Whisper:")
        print("  pip install openai-whisper tqdm")
        print("\n" + "="*70)
        
        choice = input("\nDo you want to install CPU-only version now? (y/n): ").strip().lower()
        if choice == 'y':
            print("\nInstalling CPU-only version (will be 10-20x slower than GPU)...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper", "torch", "tqdm"])
            print("\nDependencies installed. Re-run the script to start transcription.")
            sys.exit(0)
        else:
            print("\nInstallation cancelled. Please install dependencies manually.")
            sys.exit(1)

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
        print("Usage: python transcripter.py <video_file> [--json-only]")
        sys.exit(1)

    video_path = Path(sys.argv[1])
    if not video_path.exists():
        print(f"File not found: {video_path}")
        sys.exit(1)

    json_only = "--json-only" in sys.argv
    language = ask_language()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nUsing device: {device.upper()}")
    
    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        print(f"GPU: {gpu_name}")
    else:
        print("WARNING: CUDA not available. Using CPU (will be slower).")
        print("To use GPU, install PyTorch with CUDA:")
        print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")

    print(f"\n🎧 Loading Whisper model '{MODEL_NAME}' ...")
    model = whisper.load_model(MODEL_NAME, device=device)

    print(f"\n🕓 Transcribing {video_path.name} ...")
    print("⏳ Processing... (this may take several minutes)\n")
    
    import time
    start_time = time.time()
    
    # Transcribe without verbose output
    result = model.transcribe(
        str(video_path), 
        language=language,
        verbose=False,  # Disable text output during transcription
        fp16=(device == "cuda")  # Use FP16 only on CUDA
    )
    
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"\n✅ Transcription completed in {minutes}m {seconds}s!\n")

    full_text = result["text"]
    segments = result["segments"]
    base_name = video_path.stem

    json_path = video_path.parent / f"{base_name}_segments.json"
    print("💾 Saving results...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "language": language,
            "segments": segments,
            "text": full_text
        }, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON segments saved to: {json_path}")

    if json_only:
        print("\n💡 JSON-only mode enabled. Skipping text file generation.")
        print(f"📊 Total segments: {len(segments)}")
        print(f"📊 Total characters: {len(full_text):,}")
        return

    # Split and save text files
    print("\n📝 Creating text files...")
    chunks = split_text(full_text, CHUNK_SIZE)
    output_files = []
    
    for i, chunk in enumerate(tqdm(chunks, desc="💾 Saving chunks", unit="file"), start=1):
        output_path = video_path.parent / f"{base_name}_part{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        output_files.append(output_path)

    print("\n" + "="*60)
    print("✅ TRANSCRIPTION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"📊 Total characters: {len(full_text):,}")
    print(f"📊 Total segments: {len(segments)}")
    print(f"📄 Text files created: {len(chunks)} (parts of ~{CHUNK_SIZE:,} chars)")
    for file in output_files:
        print(f"   • {file.name}")
    print(f"📋 JSON file: {json_path.name}")
    print("="*60)
    print(f"JSON file: {json_path.name}")

if __name__ == "__main__":
    main()
