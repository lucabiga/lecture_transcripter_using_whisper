# QUICK START - Installazione CUDA

## ⚡ METODO VELOCE (Windows)

1. **Apri PowerShell nella cartella del progetto**

2. **Se necessario, bypassa la policy di esecuzione**:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. **Esegui lo script di installazione automatica**:
   ```bash
   .\install_cuda.bat
   ```

4. **Verifica che CUDA sia attivo** - dovresti vedere:
   ```
   CUDA available: True
   GPU: NVIDIA GeForce RTX 4060 Laptop GPU
   ```

5. **Attiva il virtual environment e usa lo script**:
   ```bash
   .\venv\Scripts\activate
   python transcripter.py tuo_video.mp4
   ```

---

## 🔧 METODO MANUALE

Se hai già un venv attivo e vuoi solo reinstallare PyTorch con CUDA:

```bash
# 1. Disinstalla PyTorch CPU-only
pip uninstall torch torchvision torchaudio -y

# 2. Installa PyTorch con CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. Installa Whisper (se non già installato)
pip install openai-whisper tqdm

# 4. Verifica CUDA
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

---

## ✅ COME VERIFICARE CHE FUNZIONI

Quando runni lo script, dovresti vedere:

```
Select language for transcription:
1) English
2) Italian
Choose (1 or 2): 2

🚀 Using device: CUDA
🎮 GPU: NVIDIA GeForce RTX 4060 Laptop GPU

🎧 Loading Whisper model 'medium' ...
🕓 Transcribing video.mp4 ... please wait.

[Progress bar qui...]
```

**Se vedi "Using device: CPU"** → PyTorch non ha CUDA, segui i passi sopra!

---

## 📊 VELOCITÀ ATTESA

| Dispositivo | Tempo per 1 ora di video |
|------------|--------------------------|
| CPU | 60-90 minuti ⏱️ |
| RTX 4060 + CUDA | 5-8 minuti 🚀 |

**Differenza: 10-20x più veloce con CUDA!**
