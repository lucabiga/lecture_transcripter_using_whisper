"""
FastAPI server for remote transcription service
Provides REST API endpoints and web interface for video/audio transcription
"""

import os
import uuid
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import whisper
import torch
from tqdm import tqdm

# Configuration
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
ALLOWED_EXTENSIONS = {'.mp4', '.mp3', '.wav', '.m4a', '.avi', '.mov', '.flac', '.ogg', '.webm'}

# Create necessary folders
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

# Initialize FastAPI
app = FastAPI(
    title="Whisper Transcription API",
    description="Remote video/audio transcription service using OpenAI Whisper",
    version="1.0.0"
)

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Job storage (in production, use Redis or database)
jobs: Dict[str, dict] = {}

# Global model (lazy loading)
model = None
device = None


def get_model():
    """Load Whisper model (lazy initialization)"""
    global model, device
    if model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading Whisper model on {device}...")
        model = whisper.load_model("medium", device=device)
        print("Model loaded successfully!")
    return model, device


def split_text(text: str, max_chars: int = 30000) -> list:
    """Split text into chunks"""
    chunks = []
    current_chunk = ""
    
    for sentence in text.split('. '):
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + '. '
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


async def transcribe_file(job_id: str, filepath: str, language: str, json_only: bool):
    """Background task for transcription"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        
        # Load model
        model, device = get_model()
        jobs[job_id]["progress"] = 20
        
        # Transcribe
        jobs[job_id]["message"] = "Transcribing audio..."
        
        # Language mapping
        lang_map = {"english": "en", "italian": "it", "auto": None}
        lang_code = lang_map.get(language.lower())
        
        result = model.transcribe(
            filepath,
            language=lang_code,
            verbose=False
        )
        
        jobs[job_id]["progress"] = 80
        
        # Prepare output paths
        base_name = Path(filepath).stem
        output_dir = Path(OUTPUT_FOLDER) / job_id
        output_dir.mkdir(exist_ok=True)
        
        # Save JSON
        json_path = output_dir / f"{base_name}_segments.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        jobs[job_id]["files"] = [str(json_path)]
        
        # Save text files (if not json_only)
        if not json_only:
            jobs[job_id]["message"] = "Generating text files..."
            text_chunks = split_text(result['text'])
            
            for i, chunk in enumerate(text_chunks, 1):
                txt_path = output_dir / f"{base_name}_part{i}.txt"
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(chunk)
                jobs[job_id]["files"].append(str(txt_path))
        
        jobs[job_id]["progress"] = 100
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["message"] = "Transcription completed successfully!"
        jobs[job_id]["language_detected"] = result.get('language', 'unknown')
        
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["message"] = f"Error: {str(e)}"
    
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)


@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve web interface"""
    html_file = Path(__file__).parent / "templates" / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    return HTMLResponse("""
        <html>
            <head><title>Whisper Transcription Service</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1>🎙️ Whisper Transcription API</h1>
                <p>Web interface not found. Please create templates/index.html</p>
                <p>API Documentation: <a href="/docs">/docs</a></p>
            </body>
        </html>
    """)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    }


@app.post("/api/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Form("auto"),
    json_only: bool = Form(False)
):
    """
    Upload and transcribe audio/video file
    
    - **file**: Audio or video file to transcribe
    - **language**: Language (english, italian, or auto)
    - **json_only**: If true, only generate JSON output
    """
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    upload_path = Path(UPLOAD_FOLDER) / f"{job_id}{file_ext}"
    
    try:
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            
            # Check file size
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024**3):.1f}GB"
                )
            
            buffer.write(content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Create job entry
    jobs[job_id] = {
        "id": job_id,
        "filename": file.filename,
        "status": "queued",
        "progress": 0,
        "message": "File uploaded, waiting to start...",
        "created_at": datetime.now().isoformat(),
        "files": [],
        "language": language,
        "json_only": json_only
    }
    
    # Start transcription in background
    background_tasks.add_task(transcribe_file, job_id, str(upload_path), language, json_only)
    
    return {
        "job_id": job_id,
        "message": "File uploaded successfully. Transcription started.",
        "status_url": f"/api/status/{job_id}"
    }


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get transcription job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/download/{job_id}/{filename}")
async def download_file(job_id: str, filename: str):
    """Download transcription result file"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    file_path = Path(OUTPUT_FOLDER) / job_id / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type='application/octet-stream',
        filename=filename
    )


@app.get("/api/jobs")
async def list_jobs():
    """List all transcription jobs"""
    return {
        "total": len(jobs),
        "jobs": list(jobs.values())
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a transcription job and its files"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete output files
    output_dir = Path(OUTPUT_FOLDER) / job_id
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # Remove from jobs
    del jobs[job_id]
    
    return {"message": "Job deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🎙️  Whisper Transcription API Server")
    print("="*60)
    print(f"Device: {'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}")
    print(f"Web Interface: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
