# 🌐 API Server Quick Start Guide

## Starting the Server

### Windows
```bash
run_server.bat
```

### Linux/macOS
```bash
chmod +x run_server.sh
./run_server.sh
```

---

## Access Points

Once running, access:

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

---

## Using the Web Interface

1. Open http://localhost:8000 in your browser
2. Drag and drop your audio/video file (or click to browse)
3. Select language (or use auto-detect)
4. Click upload and wait for processing
5. Download the results when complete

**That's it!** ✨

---

## Using the API Programmatically

### Python Example

```python
import requests
import time

# 1. Upload file
with open('lecture.mp4', 'rb') as f:
    files = {'file': f}
    data = {'language': 'english', 'json_only': 'false'}
    response = requests.post('http://localhost:8000/api/upload', files=files, data=data)

job_id = response.json()['job_id']
print(f"Job ID: {job_id}")

# 2. Poll for completion
while True:
    status = requests.get(f'http://localhost:8000/api/status/{job_id}').json()
    print(f"{status['progress']}% - {status['message']}")
    
    if status['status'] == 'completed':
        # 3. Download results
        for filepath in status['files']:
            filename = filepath.split('/')[-1]
            file_data = requests.get(f'http://localhost:8000/api/download/{job_id}/{filename}')
            with open(f'downloaded_{filename}', 'wb') as f:
                f.write(file_data.content)
        print("Done!")
        break
    elif status['status'] == 'failed':
        print(f"Error: {status.get('error')}")
        break
    
    time.sleep(2)
```

### cURL Example

```bash
# Upload
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@lecture.mp4" \
  -F "language=auto" \
  -F "json_only=false"

# Check status (replace JOB_ID)
curl http://localhost:8000/api/status/JOB_ID

# Download result (replace JOB_ID and FILENAME)
curl -O http://localhost:8000/api/download/JOB_ID/FILENAME
```

### JavaScript Example

```javascript
// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('language', 'english');
formData.append('json_only', false);

const response = await fetch('http://localhost:8000/api/upload', {
    method: 'POST',
    body: formData
});

const { job_id } = await response.json();

// Poll for status
const checkStatus = async () => {
    const status = await fetch(`http://localhost:8000/api/status/${job_id}`).then(r => r.json());
    console.log(`${status.progress}% - ${status.message}`);
    
    if (status.status === 'completed') {
        // Download files
        status.files.forEach(filepath => {
            const filename = filepath.split('/').pop();
            window.open(`http://localhost:8000/api/download/${job_id}/${filename}`);
        });
    } else if (status.status !== 'failed') {
        setTimeout(checkStatus, 2000);
    }
};

checkStatus();
```

---

## Configuration

Edit `config.py` to customize:

```python
SERVER_PORT = 8000              # Change port
MAX_FILE_SIZE = 2 * 1024**3     # Max 2GB
WHISPER_MODEL = "medium"        # Model size
```

---

## Remote Access

To access from other devices on your network:

1. Find your local IP:
   ```bash
   # Windows
   ipconfig
   
   # Linux/macOS
   hostname -I
   ```

2. Access from other devices:
   ```
   http://YOUR_IP:8000
   ```

   Example: `http://192.168.1.100:8000`

---

## Troubleshooting

### Port already in use
Change the port in `config.py`:
```python
SERVER_PORT = 8080  # Use different port
```

### Can't access from other devices
Make sure:
- Server is running with `SERVER_HOST = "0.0.0.0"` in config.py
- Firewall allows incoming connections on port 8000
- You're using your local IP (not localhost) from other devices

### GPU not detected
Run health check:
```bash
curl http://localhost:8000/api/health
```

If `cuda_available: false`, check your PyTorch installation:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/api/health` | Server health check |
| POST | `/api/upload` | Upload file for transcription |
| GET | `/api/status/{job_id}` | Get job status |
| GET | `/api/download/{job_id}/{filename}` | Download result file |
| GET | `/api/jobs` | List all jobs |
| DELETE | `/api/jobs/{job_id}` | Delete job and files |

Full interactive documentation: http://localhost:8000/docs

---

## Next Steps

- Check the main [README.md](README.md) for detailed API documentation
- Explore the Swagger UI at http://localhost:8000/docs
- Customize settings in `config.py`
- See `PROMPT_TEMPLATE.md` for generating lecture notes from transcriptions

---

**Enjoy your transcription service! 🎙️**
