# Technology Stack for YouTube Video Analysis

## Current Stack (October 2025)

Based on user's proven Hanx tools (4 months production use) with October 2025 context.

### Core Dependencies

```python
pytubefix>=6.0.0          # YouTube video downloading
openai-whisper>=20231117  # Audio transcription (Whisper AI)
moviepy>=1.0.3            # Video/audio processing
imageio-ffmpeg>=0.4.9     # FFmpeg binaries (bundled)
anthropic>=0.7.0          # Claude API for LLM analysis
```

### Optional Dependencies

```python
pydub>=0.25.1             # Audio manipulation (alternative to moviepy)
yt-dlp>=2023.10.13        # Alternative YouTube downloader
faster-whisper>=0.10.0    # Faster Whisper implementation (4x speedup)
```

## Component Analysis

### 1. YouTube Downloading: pytubefix

**Why pytubefix**:
- ✅ User's current choice, proven in production
- ✅ Active maintenance (fork of pytube)
- ✅ Handles YouTube's frequent API changes
- ✅ Simple API, good documentation
- ✅ Supports quality selection

**Alternatives**:
- **yt-dlp**: More features, more complex, slower for simple use cases
- **pytube**: Original library, less maintained
- **youtube-dl**: Python 2, deprecated

**Recommendation**: **Keep pytubefix** - it's working well for user

### 2. Audio Transcription: Whisper

**Why Whisper**:
- ✅ State-of-the-art accuracy (OpenAI)
- ✅ Multilingual support (99 languages)
- ✅ Multiple model sizes for speed/accuracy trade-off
- ✅ Open source, no API costs
- ✅ Works offline

**Model Sizes**:
| Model  | Size | RAM  | Speed (relative) | Accuracy |
|--------|------|------|------------------|----------|
| tiny   | 39M  | 1GB  | 32x realtime     | ~70%     |
| base   | 74M  | 2GB  | 16x realtime     | ~80%     |
| small  | 244M | 5GB  | 6x realtime      | ~85%     |
| medium | 769M | 10GB | 2x realtime      | ~90%     |
| large  | 1550M| 20GB | 1x realtime      | ~95%     |

**Alternatives**:
- **faster-whisper**: 4x faster, same accuracy, uses CTranslate2
- **distil-whisper**: Smaller, faster, slightly lower accuracy
- **Assembly AI**: Cloud API, costs money
- **Google Speech-to-Text**: Cloud API, costs money

**Recommendation**: 
- **Default**: Keep openai-whisper with **base** model
- **Upgrade**: Consider faster-whisper for 4x speedup if needed
- **Model**: Use **base** for general use, **small** for important content

### 3. Audio/Video Processing: moviepy + ffmpeg

**Why moviepy**:
- ✅ User's current choice, proven in production
- ✅ Simple Python API
- ✅ Handles most common formats
- ✅ Good documentation

**Why ffmpeg**:
- ✅ Industry standard for media processing
- ✅ Supports all formats
- ✅ Fast, efficient
- ✅ User has local copy: `research/ffmpeg-2025-03-27-git-114fccc4a5-full_build/bin/`

**User's Smart Pattern**:
```python
# Try moviepy first
try:
    import moviepy.editor as mp
    HAS_MOVIEPY = True
except ImportError:
    # Fall back to direct ffmpeg
    class VideoFileClip:
        def audio_write_audiofile(self, filename, **kwargs):
            subprocess.call(['ffmpeg', '-i', self.filename, '-q:a', '0', '-map', 'a', filename, '-y'])
```

**Alternatives**:
- **pydub**: Audio-focused, simpler for audio-only
- **ffmpeg-python**: Better Python bindings for ffmpeg
- **imageio**: Simpler, less features

**Recommendation**: **Keep moviepy + ffmpeg fallback** - user's pattern is excellent

### 4. LLM Analysis: Claude (Anthropic)

**Why Claude**:
- ✅ Excellent at structured extraction
- ✅ Large context window (200K tokens)
- ✅ Good at following JSON format instructions
- ✅ Fast response times
- ✅ Reasonable pricing

**Model Recommendation**:
- **claude-3-5-sonnet-20241022**: Best balance of speed/quality/cost
- **claude-3-opus**: Higher quality, slower, more expensive (if needed)

**Alternatives**:
- **GPT-4**: Similar quality, different strengths
- **GPT-3.5**: Faster, cheaper, lower quality
- **Local models**: Llama, Mistral (free, but lower quality)

**Recommendation**: **Keep Claude 3.5 Sonnet** - excellent for this use case

## FFmpeg Integration

### User's FFmpeg Location

```
research/ffmpeg-2025-03-27-git-114fccc4a5-full_build/bin/
├── ffmpeg.exe   # Main tool
├── ffplay.exe   # Player
└── ffprobe.exe  # Metadata extraction
```

### FFmpeg Path Resolution Strategy

```python
def get_ffmpeg_path():
    """Get ffmpeg path with fallback strategy."""
    # 1. Try user's project-specific ffmpeg
    project_ffmpeg = "research/ffmpeg-2025-03-27-git-114fccc4a5-full_build/bin/ffmpeg.exe"
    if os.path.exists(project_ffmpeg):
        return project_ffmpeg
    
    # 2. Try imageio-ffmpeg (bundled)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    
    # 3. Try system PATH
    import shutil
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    
    # 4. Give up
    raise FileNotFoundError("FFmpeg not found. Please install ffmpeg or imageio-ffmpeg")
```

## Installation Guide

### Recommended Installation (User's Stack)

```bash
# Core dependencies
pip install pytubefix>=6.0.0
pip install openai-whisper>=20231117
pip install moviepy>=1.0.3
pip install imageio-ffmpeg>=0.4.9
pip install anthropic>=0.7.0

# Optional: faster transcription
pip install faster-whisper>=0.10.0
```

### System Requirements

**Minimum**:
- Python 3.8+
- 4GB RAM (for base Whisper model)
- 2GB disk space (for Whisper model + videos)
- Internet connection (for downloading)

**Recommended**:
- Python 3.10+
- 8GB RAM (for small Whisper model)
- 10GB disk space
- CUDA-capable GPU (for faster Whisper)

**Optimal**:
- Python 3.11+
- 16GB RAM (for medium Whisper model)
- 50GB disk space
- NVIDIA GPU with 8GB+ VRAM

### GPU Acceleration

**Whisper with GPU** (5-10x faster):
```bash
# Install CUDA-enabled PyTorch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then install Whisper
pip install openai-whisper
```

**Check GPU availability**:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

## Performance Benchmarks

### Processing Times (10-minute video)

**With base model (recommended)**:
- Download: 30-60 seconds (depends on internet)
- Audio extraction: 5-10 seconds
- Transcription (CPU): 40 seconds
- Transcription (GPU): 8 seconds
- LLM analysis: 10-20 seconds
- **Total (CPU)**: ~2 minutes
- **Total (GPU)**: ~1 minute

**With small model (better accuracy)**:
- Transcription (CPU): 100 seconds
- Transcription (GPU): 15 seconds
- **Total (CPU)**: ~3 minutes
- **Total (GPU)**: ~1.5 minutes

**With tiny model (quick preview)**:
- Transcription (CPU): 20 seconds
- Transcription (GPU): 4 seconds
- **Total (CPU)**: ~1 minute
- **Total (GPU)**: ~45 seconds

### Cost Analysis

**Per 10-minute video**:
- Download: Free (YouTube)
- Transcription: Free (local Whisper)
- LLM analysis: ~$0.01-0.05 (Claude API, ~2K-10K tokens)
- **Total cost**: ~$0.01-0.05 per video

**Comparison to cloud services**:
- Assembly AI: ~$0.25 per 10 minutes
- Google Speech-to-Text: ~$0.24 per 10 minutes
- **Savings with local Whisper**: ~95%

## Upgrade Path

### Current → Faster (Optional)

If processing speed becomes an issue:

```bash
# Install faster-whisper (4x faster than openai-whisper)
pip install faster-whisper>=0.10.0
```

**Code changes**:
```python
# Old (openai-whisper)
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path)

# New (faster-whisper)
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cuda", compute_type="float16")
segments, info = model.transcribe(audio_path)
result = {"text": " ".join([segment.text for segment in segments])}
```

### Current → More Reliable (Optional)

If YouTube downloads become unreliable:

```bash
# Install yt-dlp (more robust than pytubefix)
pip install yt-dlp>=2023.10.13
```

**Code changes**:
```python
# Old (pytubefix)
from pytubefix import YouTube
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()
video_path = stream.download(output_path)

# New (yt-dlp)
import yt_dlp
ydl_opts = {'outtmpl': f'{output_path}/%(title)s.%(ext)s'}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    video_path = ydl.prepare_filename(info)
```

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'pytubefix'"
- **Solution**: `pip install pytubefix`

**Issue**: "ModuleNotFoundError: No module named 'whisper'"
- **Solution**: `pip install openai-whisper`

**Issue**: "FFmpeg not found"
- **Solution**: `pip install imageio-ffmpeg` or use user's local ffmpeg

**Issue**: "Out of memory during transcription"
- **Solution**: Use smaller Whisper model (tiny or base)

**Issue**: "Transcription is very slow"
- **Solution**: Use GPU, or install faster-whisper, or use smaller model

**Issue**: "YouTube download fails"
- **Solution**: Check internet, try yt-dlp, check if video is private/restricted

## Future Considerations

### Potential Upgrades

1. **Whisper v3** (when available):
   - Expected improvements in accuracy
   - Better multilingual support
   - Faster processing

2. **Video frame analysis**:
   - Extract diagrams, code screenshots
   - Requires: CLIP, GPT-4 Vision, or similar

3. **Real-time processing**:
   - Stream processing instead of download-then-process
   - Requires: streaming-capable libraries

4. **Distributed processing**:
   - Process multiple videos in parallel across machines
   - Requires: Celery, Redis, or similar

---

**Last Updated**: 2025-10-19  
**Status**: Production-ready based on user's 4-month experience  
**Maintainer**: Richard (Pied Piper)

