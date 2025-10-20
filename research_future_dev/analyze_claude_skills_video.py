#!/usr/bin/env python3
"""
YouTube Video Analysis - Claude Skills Video
Based on .claude/skills/youtube-video-analysis/

Analyzes: https://www.youtube.com/watch?v=FOqbS_llAms
Topic: Claude Skills
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("YouTube Video Analysis - Claude Skills")
print("=" * 80)
print()

# Video URL
VIDEO_URL = "https://www.youtube.com/watch?v=FOqbS_llAms"
VIDEO_ID = "FOqbS_llAms"
OUTPUT_DIR = Path(__file__).parent

print(f"Video URL: {VIDEO_URL}")
print(f"Output Directory: {OUTPUT_DIR}")
print()

# Check dependencies
print("Checking dependencies...")
dependencies_ok = True

try:
    from pytubefix import YouTube
    print("[OK] pytubefix - installed")
except ImportError:
    print("[FAIL] pytubefix - NOT INSTALLED")
    print("   Install: pip install pytubefix>=6.0.0")
    dependencies_ok = False

try:
    import whisper
    print("[OK] whisper - installed")
except ImportError:
    print("[FAIL] whisper - NOT INSTALLED")
    print("   Install: pip install openai-whisper>=20231117")
    dependencies_ok = False

try:
    import moviepy
    print("[OK] moviepy - installed")
except ImportError:
    print("[FAIL] moviepy - NOT INSTALLED")
    print("   Install: pip install moviepy>=1.0.3")
    dependencies_ok = False

try:
    import imageio_ffmpeg
    print("[OK] imageio-ffmpeg - installed")
except ImportError:
    print("[WARN] imageio-ffmpeg - NOT INSTALLED (optional)")
    print("   Install: pip install imageio-ffmpeg>=0.4.9")

print()

if not dependencies_ok:
    print("=" * 80)
    print("MISSING DEPENDENCIES")
    print("=" * 80)
    print()
    print("Please install missing dependencies:")
    print("pip install pytubefix openai-whisper moviepy imageio-ffmpeg")
    print()
    sys.exit(1)

# Import after dependency check
from pytubefix import YouTube
import whisper

print("=" * 80)
print("STEP 1: Download Video")
print("=" * 80)
print()

try:
    yt = YouTube(VIDEO_URL)
    
    print(f"Title: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Length: {yt.length} seconds ({yt.length // 60} minutes)")
    print(f"Views: {yt.views:,}")
    print()
    
    # Get highest quality video stream
    video_stream = yt.streams.get_highest_resolution()
    
    print(f"Downloading: {video_stream.resolution} - {video_stream.filesize / 1024 / 1024:.2f} MB")
    video_path = video_stream.download(
        output_path=str(OUTPUT_DIR),
        filename=f"{VIDEO_ID}_video.mp4"
    )
    print(f"[OK] Downloaded: {video_path}")
    print()
    
except Exception as e:
    print(f"❌ Error downloading video: {e}")
    sys.exit(1)

print("=" * 80)
print("STEP 2: Extract Audio")
print("=" * 80)
print()

audio_path = OUTPUT_DIR / f"{VIDEO_ID}_audio.mp3"

try:
    # Try moviepy first
    try:
        from moviepy import VideoFileClip
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(str(audio_path), logger=None)
        video.close()
        print(f"[OK] Audio extracted (moviepy): {audio_path}")
    except Exception as e:
        print(f"[WARN] moviepy failed: {e}")
        print("Trying ffmpeg fallback...")
        
        # Fallback to direct ffmpeg
        import subprocess
        ffmpeg_path = project_root / ".claude/skills/youtube-video-analysis/bin/ffmpeg.exe"
        
        if ffmpeg_path.exists():
            print(f"Using local ffmpeg: {ffmpeg_path}")
            subprocess.run([
                str(ffmpeg_path), '-i', video_path,
                '-q:a', '0', '-map', 'a',
                str(audio_path), '-y'
            ], check=True, capture_output=True)
            print(f"[OK] Audio extracted (ffmpeg): {audio_path}")
        else:
            raise Exception("No ffmpeg available")
    
    print()
    
except Exception as e:
    print(f"[FAIL] Error extracting audio: {e}")
    sys.exit(1)

print("=" * 80)
print("STEP 3: Transcribe Audio")
print("=" * 80)
print()

transcript_path = OUTPUT_DIR / f"{VIDEO_ID}_transcript.txt"

try:
    # Set ffmpeg path for Whisper
    import os
    ffmpeg_path = project_root / ".claude/skills/youtube-video-analysis/bin"
    if ffmpeg_path.exists():
        os.environ["PATH"] = str(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")
        print(f"Added ffmpeg to PATH: {ffmpeg_path}")
    
    print("Loading Whisper model (base)...")
    model = whisper.load_model("base")
    
    print("Transcribing audio (this may take a few minutes)...")
    result = model.transcribe(str(audio_path))
    
    transcript = result["text"]
    
    # Save transcript
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    print(f"[OK] Transcript saved: {transcript_path}")
    print(f"   Length: {len(transcript)} characters")
    print()
    print("First 500 characters:")
    print("-" * 80)
    print(transcript[:500])
    print("-" * 80)
    print()
    
except Exception as e:
    print(f"[FAIL] Error transcribing: {e}")
    sys.exit(1)

print("=" * 80)
print("STEP 4: Analyze with LLM (Manual)")
print("=" * 80)
print()

# Create analysis prompt
analysis_prompt = f"""Analyze this YouTube video transcript about Claude Skills.

VIDEO INFORMATION:
- Title: {yt.title}
- Author: {yt.author}
- Length: {yt.length // 60} minutes
- URL: {VIDEO_URL}

TRANSCRIPT:
{transcript}

Please extract:
1. **Summary**: 2-3 paragraph overview of the video content
2. **Key Points**: Main concepts and takeaways (bullet list)
3. **Claude Skills Features**: Specific features or capabilities mentioned
4. **Technical Details**: Implementation details, file formats, syntax
5. **Best Practices**: Recommendations or tips mentioned
6. **Examples**: Any example Skills or use cases shown
7. **Actionable Items**: Things we should implement or try
8. **Questions**: Any unclear points that need clarification

Format as JSON.
"""

prompt_path = OUTPUT_DIR / f"{VIDEO_ID}_analysis_prompt.txt"
with open(prompt_path, 'w', encoding='utf-8') as f:
    f.write(analysis_prompt)

print(f"[OK] Analysis prompt saved: {prompt_path}")
print()
print("To analyze with Claude API, you can:")
print("1. Copy the prompt from the file above")
print("2. Use Claude API or Claude.ai web interface")
print("3. Save the response as JSON")
print()

# Create metadata file
metadata = {
    "video_url": VIDEO_URL,
    "video_id": VIDEO_ID,
    "title": yt.title,
    "author": yt.author,
    "length_seconds": yt.length,
    "views": yt.views,
    "downloaded_at": datetime.now().isoformat(),
    "files": {
        "video": str(Path(video_path).name),
        "audio": str(audio_path.name),
        "transcript": str(transcript_path.name),
        "analysis_prompt": str(prompt_path.name)
    }
}

metadata_path = OUTPUT_DIR / f"{VIDEO_ID}_metadata.json"
with open(metadata_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print(f"[OK] Metadata saved: {metadata_path}")
print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print()
print("Files created:")
print(f"  1. {Path(video_path).name} - Downloaded video")
print(f"  2. {audio_path.name} - Extracted audio")
print(f"  3. {transcript_path.name} - Whisper transcription")
print(f"  4. {prompt_path.name} - LLM analysis prompt")
print(f"  5. {metadata_path.name} - Video metadata")
print()
print("Next steps:")
print("  - Review the transcript")
print("  - Use the analysis prompt with Claude API")
print("  - Save LLM response as JSON")
print()

