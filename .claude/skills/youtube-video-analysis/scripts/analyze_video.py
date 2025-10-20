#!/usr/bin/env python3
"""
YouTube Video Analysis Script
Downloads, transcribes, and analyzes YouTube videos using Whisper AI and Claude

Enhanced version combining best features from Cursor and Claude Code implementations:
- Comprehensive dependency checking (from Cursor)
- Moviepy fallback logic (from Cursor)
- Detailed step separators (from Cursor)
- Modular, reusable functions (from Claude Code)
- Full LLM integration (from Claude Code)
- Command-line interface (from Claude Code)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import subprocess


def check_dependencies():
    """Check if all required dependencies are installed (Cursor enhancement)"""
    print("=" * 80)
    print("DEPENDENCY CHECK")
    print("=" * 80)
    print()
    
    missing = []
    
    try:
        from pytubefix import YouTube
        print("[OK] pytubefix - installed")
    except ImportError:
        print("[FAIL] pytubefix - NOT INSTALLED")
        print("   Install: pip install pytubefix>=6.0.0")
        missing.append("pytubefix>=6.0.0")
    
    try:
        import whisper
        print("[OK] whisper - installed")
    except ImportError:
        print("[FAIL] whisper - NOT INSTALLED")
        print("   Install: pip install openai-whisper>=20231117")
        missing.append("openai-whisper>=20231117")
    
    try:
        import moviepy
        print("[OK] moviepy - installed")
    except ImportError:
        print("[FAIL] moviepy - NOT INSTALLED")
        print("   Install: pip install moviepy>=1.0.3")
        missing.append("moviepy>=1.0.3")
    
    try:
        import imageio_ffmpeg
        print("[OK] imageio-ffmpeg - installed")
    except ImportError:
        print("[WARN] imageio-ffmpeg - NOT INSTALLED (optional)")
        print("   Install: pip install imageio-ffmpeg>=0.4.9")
    
    print()
    
    if missing:
        print("=" * 80)
        print("MISSING DEPENDENCIES")
        print("=" * 80)
        print()
        print("Please install missing dependencies:")
        print(f"pip install {' '.join(missing)}")
        print()
        sys.exit(1)
    
    print("All required dependencies installed!")
    print()


# Import after dependency check
try:
    from pytubefix import YouTube
    import whisper
except ImportError:
    pass  # Will be caught by check_dependencies()


def download_video(url, output_dir):
    """Download YouTube video (Enhanced with Cursor's step separators)"""
    print("=" * 80)
    print("STEP 1: Download Video")
    print("=" * 80)
    print()
    print(f"Video URL: {url}")
    print()

    # Custom progress callback to avoid Unicode issues
    def progress_callback(stream, chunk, bytes_remaining):
        total = stream.filesize
        downloaded = total - bytes_remaining
        percent = (downloaded / total) * 100
        print(f"\rDownloading... {percent:.1f}%", end='', flush=True)

    yt = YouTube(url, on_progress_callback=progress_callback)
    print(f"\n\nTitle: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Duration: {yt.length} seconds ({yt.length // 60} minutes)")
    print(f"Views: {yt.views:,}")
    print()

    # Get highest resolution stream
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {stream.resolution} - {stream.filesize / 1024 / 1024:.2f} MB")

    # Download to output directory
    video_path = stream.download(output_path=output_dir, filename="video.mp4")
    print(f"\n[OK] Downloaded: {video_path}")
    print()

    return video_path, {
        "title": yt.title,
        "duration": yt.length,
        "author": yt.author,
        "views": yt.views,
        "description": yt.description
    }


def extract_audio(video_path, output_dir):
    """Extract audio from video using moviepy or ffmpeg (Enhanced with Cursor's fallback logic)"""
    print("=" * 80)
    print("STEP 2: Extract Audio")
    print("=" * 80)
    print()

    audio_path = os.path.join(output_dir, "audio.mp3")

    # Try moviepy first (easier, more compatible)
    try:
        from moviepy import VideoFileClip
        print("Trying moviepy for audio extraction...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()
        print(f"[OK] Audio extracted (moviepy): {audio_path}")
        print()
        return audio_path
    except Exception as e:
        print(f"[WARN] moviepy failed: {e}")
        print("Trying direct ffmpeg fallback...")
        print()

    # Fallback to direct ffmpeg
    skill_dir = Path(__file__).parent.parent
    ffmpeg_path = skill_dir / "bin" / "ffmpeg.exe"

    # Use bundled ffmpeg if available, otherwise try system ffmpeg
    ffmpeg_cmd = str(ffmpeg_path) if ffmpeg_path.exists() else "ffmpeg"
    
    if ffmpeg_path.exists():
        print(f"Using local ffmpeg: {ffmpeg_path}")
    else:
        print("Using system ffmpeg from PATH")

    # Extract audio using ffmpeg
    cmd = [
        ffmpeg_cmd,
        "-i", video_path,
        "-vn",  # No video
        "-acodec", "libmp3lame",
        "-q:a", "2",  # High quality
        "-y",  # Overwrite output file
        audio_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[OK] Audio extracted (ffmpeg): {audio_path}")
        print()
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] FFmpeg error: {e.stderr}")
        raise

    return audio_path


def transcribe_audio(audio_path, model_size="base"):
    """Transcribe audio using Whisper (Enhanced with Cursor's detailed logging)"""
    print("=" * 80)
    print("STEP 3: Transcribe Audio")
    print("=" * 80)
    print()

    # Set ffmpeg path for Whisper
    skill_dir = Path(__file__).parent.parent
    ffmpeg_path = skill_dir / "bin" / "ffmpeg.exe"

    if ffmpeg_path.exists():
        # Set environment variable so Whisper can find ffmpeg
        os.environ['PATH'] = str(ffmpeg_path.parent) + os.pathsep + os.environ.get('PATH', '')
        print(f"Added ffmpeg to PATH for Whisper: {ffmpeg_path.parent}")
    
    print(f"Loading Whisper model ({model_size})...")
    model = whisper.load_model(model_size)

    print("Transcribing audio (this may take a few minutes)...")
    result = model.transcribe(audio_path)
    
    transcript = result["text"]
    
    print(f"[OK] Transcription complete!")
    print(f"   Length: {len(transcript)} characters")
    print()
    print("First 500 characters:")
    print("-" * 80)
    print(transcript[:500])
    print("-" * 80)
    print()

    return transcript


def analyze_with_claude(transcript, video_metadata, api_key=None, analysis_style="both"):
    """
    Analyze transcript using Claude API with dual analysis styles
    
    Args:
        transcript: Video transcript text
        video_metadata: Video metadata dict
        api_key: Anthropic API key
        analysis_style: "comprehensive", "actionable", or "both" (default)
    
    Returns:
        dict with 'comprehensive' and/or 'actionable' analysis results
    """
    print("=" * 80)
    print("STEP 4: Analyze with Claude")
    print("=" * 80)
    print()
    
    if not api_key:
        print("[WARN] No Anthropic API key provided. Skipping LLM analysis.")
        print("   Set ANTHROPIC_API_KEY environment variable to enable analysis.")
        print()
        return None

    try:
        from anthropic import Anthropic
    except ImportError:
        print("[FAIL] anthropic package not installed.")
        print("   Install: pip install anthropic")
        print()
        return None

    client = Anthropic(api_key=api_key)
    results = {}
    
    # Comprehensive Analysis (Claude Code style - reference quality)
    if analysis_style in ["comprehensive", "both"]:
        print("Running comprehensive analysis (reference-quality)...")
        comprehensive_prompt = f"""Analyze this YouTube video transcript and provide a comprehensive, reference-quality analysis.

Video Title: {video_metadata.get('title', 'Unknown')}
Duration: {video_metadata.get('duration', 0)} seconds ({video_metadata.get('duration', 0) // 60} minutes)
Author: {video_metadata.get('author', 'Unknown')}
Views: {video_metadata.get('views', 'Unknown')}

Transcript:
{transcript}

Please provide a COMPREHENSIVE analysis suitable for documentation and sharing:

1. **Executive Summary** (2-3 paragraphs)
2. **Core Concepts Explained** (detailed explanations)
3. **Key Technical Details** (with specific numbers/metrics if mentioned)
4. **Direct Quotes** (5+ notable quotes from the video)
5. **Comparisons** (if video compares technologies/approaches)
6. **Industry Context** (broader implications)
7. **Limitations and Considerations**
8. **External Resources** (any links or resources mentioned)
9. **Conclusion** (overall assessment)

Format as detailed markdown suitable for a reference document.
"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,  # Larger for comprehensive analysis
            messages=[{"role": "user", "content": comprehensive_prompt}]
        )
        
        results['comprehensive'] = message.content[0].text
        print("[OK] Comprehensive analysis complete")
        print()
    
    # Actionable Analysis (Cursor style - project-specific)
    if analysis_style in ["actionable", "both"]:
        print("Running actionable analysis (implementation-focused)...")
        actionable_prompt = f"""Analyze this YouTube video transcript and provide ACTIONABLE insights for implementation.

Video Title: {video_metadata.get('title', 'Unknown')}
Duration: {video_metadata.get('duration', 0)} seconds
Author: {video_metadata.get('author', 'Unknown')}

Transcript:
{transcript}

Please provide an ACTIONABLE analysis focused on implementation:

1. **Quick Summary** (2-3 sentences - what's the video about?)
2. **Key Insights** (bullet list of main takeaways with comparison tables if relevant)
3. **Technical Implementation Notes** (specific technical details)
4. **Actionable Items** (what should we DO with this information?)
   - Things to implement
   - Code examples or patterns to try
   - Skills or tools to create
5. **Questions & Clarifications Needed** (things that need more research)
6. **Best Practices Mentioned** (specific recommendations from video)
7. **Potential Improvements** (how to apply these concepts)

Focus on PRACTICAL APPLICATION rather than comprehensive documentation.
Use comparison tables where helpful.
Include code examples if relevant.

Format as markdown optimized for quick reference during development.
"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=6144,  # Medium for actionable analysis
            messages=[{"role": "user", "content": actionable_prompt}]
        )
        
        results['actionable'] = message.content[0].text
        print("[OK] Actionable analysis complete")
        print()
    
    return results


def save_results(output_dir, video_metadata, transcript, analysis):
    """Save all results to files (Enhanced with dual analysis support)"""
    print("=" * 80)
    print("STEP 5: Save Results")
    print("=" * 80)
    print()

    # Save metadata
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(video_metadata, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved metadata: {metadata_path}")

    # Save transcript
    transcript_path = os.path.join(output_dir, "transcript.txt")
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    print(f"[OK] Saved transcript: {transcript_path}")

    # Save analysis files if available
    if analysis:
        # Save comprehensive analysis (Claude Code style)
        if 'comprehensive' in analysis:
            comprehensive_path = os.path.join(output_dir, "ANALYSIS_COMPREHENSIVE.md")
            with open(comprehensive_path, 'w', encoding='utf-8') as f:
                f.write(f"# Comprehensive Analysis: {video_metadata.get('title', 'Unknown')}\n\n")
                f.write(f"**Video URL:** {video_metadata.get('url', 'Unknown')}\n")
                f.write(f"**Author:** {video_metadata.get('author', 'Unknown')}\n")
                f.write(f"**Duration:** {video_metadata.get('duration', 0) // 60} minutes\n")
                f.write(f"**Views:** {video_metadata.get('views', 'Unknown'):,}\n")
                f.write(f"**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(analysis['comprehensive'])
            print(f"[OK] Saved comprehensive analysis: {comprehensive_path}")
        
        # Save actionable analysis (Cursor style)
        if 'actionable' in analysis:
            actionable_path = os.path.join(output_dir, "ANALYSIS_ACTIONABLE.md")
            with open(actionable_path, 'w', encoding='utf-8') as f:
                f.write(f"# Actionable Analysis: {video_metadata.get('title', 'Unknown')}\n\n")
                f.write(f"**Video URL:** {video_metadata.get('url', 'Unknown')}\n")
                f.write(f"**Author:** {video_metadata.get('author', 'Unknown')}\n")
                f.write(f"**Duration:** {video_metadata.get('duration', 0) // 60} minutes\n")
                f.write(f"**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(analysis['actionable'])
            print(f"[OK] Saved actionable analysis: {actionable_path}")
        
        # Create README for navigation
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Video Analysis Results\n\n")
            f.write(f"**Video:** {video_metadata.get('title', 'Unknown')}\n")
            f.write(f"**Author:** {video_metadata.get('author', 'Unknown')}\n")
            f.write(f"**Duration:** {video_metadata.get('duration', 0) // 60} minutes\n")
            f.write(f"**Analyzed:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("## Files\n\n")
            f.write("### Analysis Files\n")
            if 'comprehensive' in analysis:
                f.write("- **[ANALYSIS_COMPREHENSIVE.md](ANALYSIS_COMPREHENSIVE.md)** - Reference-quality analysis (Claude Code style)\n")
                f.write("  - Best for: Documentation, sharing, deep understanding\n")
                f.write("  - Includes: Executive summary, detailed explanations, quotes, industry context\n\n")
            if 'actionable' in analysis:
                f.write("- **[ANALYSIS_ACTIONABLE.md](ANALYSIS_ACTIONABLE.md)** - Implementation-focused analysis (Cursor style)\n")
                f.write("  - Best for: Quick reference, immediate action items, code examples\n")
                f.write("  - Includes: Quick summary, actionable items, questions, best practices\n\n")
            f.write("### Source Files\n")
            f.write("- **[transcript.txt](transcript.txt)** - Full video transcript\n")
            f.write("- **[metadata.json](metadata.json)** - Video metadata\n")
            f.write("- **video.mp4** - Downloaded video\n")
            f.write("- **audio.mp3** - Extracted audio\n")
        print(f"[OK] Saved README: {readme_path}")

    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("Files created:")
    print(f"  1. metadata.json - Video metadata")
    print(f"  2. transcript.txt - Full transcript")
    if analysis:
        if 'comprehensive' in analysis:
            print(f"  3. ANALYSIS_COMPREHENSIVE.md - Reference-quality analysis")
        if 'actionable' in analysis:
            print(f"  4. ANALYSIS_ACTIONABLE.md - Implementation-focused analysis")
        print(f"  5. README.md - Navigation guide")
    print()
    print("Next steps:")
    if analysis and 'comprehensive' in analysis:
        print("  - Read ANALYSIS_COMPREHENSIVE.md for deep understanding")
    if analysis and 'actionable' in analysis:
        print("  - Read ANALYSIS_ACTIONABLE.md for immediate action items")
    print()


def main():
    """Main entry point (Enhanced with dependency checking and dual analysis)"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_video.py <youtube_url> [output_dir] [model_size] [analysis_style]")
        print()
        print("Arguments:")
        print("  youtube_url     - YouTube video URL (required)")
        print("  output_dir      - Output directory (default: ./output)")
        print("  model_size      - Whisper model: tiny, base, small, medium, large (default: base)")
        print("  analysis_style  - Analysis type: comprehensive, actionable, both (default: both)")
        print()
        print("Examples:")
        print("  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms")
        print("  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms ./output base both")
        print("  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms ./output small actionable")
        print()
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    model_size = sys.argv[3] if len(sys.argv) > 3 else "base"
    analysis_style = sys.argv[4] if len(sys.argv) > 4 else "both"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("YouTube Video Analysis - Enhanced Edition")
    print("=" * 80)
    print()
    print("Combining best features from Cursor and Claude Code implementations:")
    print("  - Comprehensive dependency checking (Cursor)")
    print("  - Moviepy fallback logic (Cursor)")
    print("  - Detailed step separators (Cursor)")
    print("  - Modular, reusable functions (Claude Code)")
    print("  - Full LLM integration (Claude Code)")
    print("  - Dual analysis styles (Both!)")
    print()
    print(f"Configuration:")
    print(f"  Video URL: {url}")
    print(f"  Output Directory: {output_dir}")
    print(f"  Whisper Model: {model_size}")
    print(f"  Analysis Style: {analysis_style}")
    print()

    # Check dependencies first (Cursor enhancement)
    check_dependencies()

    try:
        # Step 1: Download video
        video_path, metadata = download_video(url, output_dir)
        metadata['url'] = url  # Add URL to metadata

        # Step 2: Extract audio
        audio_path = extract_audio(video_path, output_dir)

        # Step 3: Transcribe
        transcript = transcribe_audio(audio_path, model_size)

        # Step 4: Analyze with Claude (if API key available)
        api_key = os.getenv('ANTHROPIC_API_KEY')
        analysis = analyze_with_claude(transcript, metadata, api_key, analysis_style)

        # Step 5: Save results
        save_results(output_dir, metadata, transcript, analysis)

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
