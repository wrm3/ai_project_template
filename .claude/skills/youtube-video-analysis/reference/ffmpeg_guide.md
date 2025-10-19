# FFmpeg Guide for YouTube Video Analysis

## FFmpeg Installation

**⚠️ IMPORTANT**: FFmpeg binaries (141MB each) are too large for GitHub's 100MB limit and are NOT included in this repository.

### Installation Options

**Option 1: Use imageio-ffmpeg (Recommended - Easiest)**
```bash
pip install imageio-ffmpeg
```
This automatically downloads and bundles ffmpeg binaries (~50MB). No manual setup needed!

**Option 2: Download FFmpeg Manually**
1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `.claude/skills/youtube-video-analysis/bin/`
3. Or add to system PATH

**Option 3: System Installation**
- **Windows**: Download from ffmpeg.org, add to PATH
- **Mac**: `brew install ffmpeg`
- **Linux**: `apt-get install ffmpeg` or `yum install ffmpeg`

**Version Used**: 2025-03-27 build (git-114fccc4a5) - but any recent version works

## Common FFmpeg Commands

### Extract Audio from Video

```bash
# Extract audio as MP3 (good quality)
ffmpeg -i input.mp4 -q:a 0 -map a output.mp3

# Extract audio as WAV (lossless)
ffmpeg -i input.mp4 -vn -acodec pcm_s16le output.wav

# Extract audio with specific bitrate
ffmpeg -i input.mp4 -b:a 192k output.mp3
```

### Get Video Information

```bash
# Get detailed metadata
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Get duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4
```

### Convert Video Formats

```bash
# Convert to MP4
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4

# Compress video
ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4
```

## Python Integration

### Using subprocess

```python
import subprocess
import os

# Skill's ffmpeg path (relative to project root)
FFMPEG_PATH = r".claude\skills\youtube-video-analysis\bin\ffmpeg.exe"

def extract_audio_ffmpeg(video_path, audio_path):
    """Extract audio using ffmpeg directly."""
    if not os.path.exists(FFMPEG_PATH):
        raise FileNotFoundError(f"FFmpeg not found at: {FFMPEG_PATH}")
    
    cmd = [
        FFMPEG_PATH,
        '-i', video_path,      # Input file
        '-q:a', '0',           # Best audio quality
        '-map', 'a',           # Map audio stream
        audio_path,            # Output file
        '-y'                   # Overwrite without asking
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return audio_path
```

### Using moviepy (with ffmpeg backend)

```python
from moviepy.editor import VideoFileClip

def extract_audio_moviepy(video_path, audio_path):
    """Extract audio using moviepy (uses ffmpeg internally)."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    video.close()
    return audio_path
```

## Troubleshooting

### FFmpeg Not Found

```python
def find_ffmpeg():
    """Find ffmpeg with multiple fallback options."""
    import shutil
    from pathlib import Path
    
    # 1. Skill's bundled ffmpeg
    skill_ffmpeg = Path(".claude/skills/youtube-video-analysis/bin/ffmpeg.exe")
    if skill_ffmpeg.exists():
        return str(skill_ffmpeg)
    
    # 2. imageio-ffmpeg (bundled)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    
    # 3. System PATH
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg
    
    raise FileNotFoundError("FFmpeg not found")
```

### Common Errors

**Error**: "ffmpeg: command not found"
- **Solution**: Use full path to ffmpeg.exe

**Error**: "Permission denied"
- **Solution**: Check file permissions, run as administrator if needed

**Error**: "Invalid argument"
- **Solution**: Check file paths, escape special characters

---

**Last Updated**: 2025-10-19  
**FFmpeg Location**: .claude/skills/youtube-video-analysis/bin/ffmpeg.exe

