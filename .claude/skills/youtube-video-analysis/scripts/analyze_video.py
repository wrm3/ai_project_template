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
from tqdm import tqdm


def check_dependencies(check_vision=False):
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

    # Check vision dependencies if frame extraction is enabled
    if check_vision:
        try:
            import cv2
            print("[OK] opencv-python - installed")
        except ImportError:
            print("[FAIL] opencv-python - NOT INSTALLED (required for --extract-visual)")
            print("   Install: pip install opencv-python>=4.8.0")
            missing.append("opencv-python>=4.8.0")

        try:
            from PIL import Image
            print("[OK] Pillow - installed")
        except ImportError:
            print("[FAIL] Pillow - NOT INSTALLED (required for --extract-visual)")
            print("   Install: pip install Pillow>=10.0.0")
            missing.append("Pillow>=10.0.0")

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

    # Progress tracking with tqdm
    progress_bar = None

    def progress_callback(stream, chunk, bytes_remaining):
        nonlocal progress_bar
        if progress_bar is None:
            total = stream.filesize
            progress_bar = tqdm(
                total=total,
                desc="Downloading video",
                unit='B',
                unit_scale=True,
                unit_divisor=1024
            )

        progress_bar.update(len(chunk))

    yt = YouTube(url, on_progress_callback=progress_callback)
    print(f"\nTitle: {yt.title}")
    print(f"Author: {yt.author}")
    print(f"Duration: {yt.length} seconds ({yt.length // 60} minutes)")
    print(f"Views: {yt.views:,}")
    print()

    # Get highest resolution stream
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {stream.resolution} - {stream.filesize / 1024 / 1024:.2f} MB\n")

    # Download to output directory
    video_path = stream.download(output_path=output_dir, filename="video.mp4")

    if progress_bar:
        progress_bar.close()

    print(f"[OK] Downloaded: {video_path}")
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


def prepare_analysis_prompts(transcript, video_metadata):
    """
    Prepare analysis prompt templates for Claude Code to use natively.
    This function returns the prompts that Claude Code will execute directly.

    Args:
        transcript: Video transcript text
        video_metadata: Video metadata dict

    Returns:
        dict with 'comprehensive' and 'actionable' prompt templates
    """
    print("=" * 80)
    print("STEP 4: Prepare for Claude Code Analysis")
    print("=" * 80)
    print()

    print("[INFO] Transcript prepared for Claude Code native analysis")
    print("[INFO] Claude Code will analyze this transcript directly - no external API needed")
    print()

    # Comprehensive Analysis Prompt (Claude Code style - reference quality)
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

    # Actionable Analysis Prompt (Cursor style - project-specific)
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

    return {
        'comprehensive_prompt': comprehensive_prompt,
        'actionable_prompt': actionable_prompt,
        'metadata': video_metadata,
        'transcript': transcript
    }


def save_results(output_dir, video_metadata, transcript, prompts_data=None):
    """Save all results to files - transcript and prompts for Claude Code analysis"""
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

    # Save analysis prompts for Claude Code
    if prompts_data:
        # Save comprehensive prompt
        comprehensive_prompt_path = os.path.join(output_dir, "PROMPT_COMPREHENSIVE.txt")
        with open(comprehensive_prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompts_data['comprehensive_prompt'])
        print(f"[OK] Saved comprehensive analysis prompt: {comprehensive_prompt_path}")

        # Save actionable prompt
        actionable_prompt_path = os.path.join(output_dir, "PROMPT_ACTIONABLE.txt")
        with open(actionable_prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompts_data['actionable_prompt'])
        print(f"[OK] Saved actionable analysis prompt: {actionable_prompt_path}")

        # Create README for navigation
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# Video Analysis Results\n\n")
            f.write(f"**Video:** {video_metadata.get('title', 'Unknown')}\n")
            f.write(f"**Author:** {video_metadata.get('author', 'Unknown')}\n")
            f.write(f"**Duration:** {video_metadata.get('duration', 0) // 60} minutes\n")
            f.write(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write("## Files\n\n")
            f.write("### Source Files\n")
            f.write("- **[transcript.txt](transcript.txt)** - Full video transcript\n")
            f.write("- **[metadata.json](metadata.json)** - Video metadata\n")
            f.write("- **video.mp4** - Downloaded video\n")
            f.write("- **audio.mp3** - Extracted audio\n\n")
            f.write("### Analysis Prompts (for Claude Code)\n")
            f.write("- **[PROMPT_COMPREHENSIVE.txt](PROMPT_COMPREHENSIVE.txt)** - Comprehensive analysis prompt\n")
            f.write("- **[PROMPT_ACTIONABLE.txt](PROMPT_ACTIONABLE.txt)** - Actionable analysis prompt\n\n")
            f.write("## Next Steps\n\n")
            f.write("Claude Code will automatically analyze the transcript using these prompts.\n")
            f.write("No external API key needed - Claude Code uses native capabilities!\n")
        print(f"[OK] Saved README: {readme_path}")

    print()
    print("=" * 80)
    print("TRANSCRIPTION COMPLETE")
    print("=" * 80)
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("Files created:")
    print(f"  1. metadata.json - Video metadata")
    print(f"  2. transcript.txt - Full transcript")
    if prompts_data:
        print(f"  3. PROMPT_COMPREHENSIVE.txt - Comprehensive analysis prompt")
        print(f"  4. PROMPT_ACTIONABLE.txt - Actionable analysis prompt")
        print(f"  5. README.md - Navigation guide")
    print()
    print("=" * 80)
    print("READY FOR CLAUDE CODE ANALYSIS")
    print("=" * 80)
    print()
    print("The transcript is ready! Claude Code will now analyze it using native capabilities.")
    print("No external API needed - Claude Code handles the analysis directly.")
    print()


def main():
    """Main entry point - Claude Code native integration"""
    import argparse

    parser = argparse.ArgumentParser(
        description='YouTube Video Analysis - Download, transcribe, and optionally extract frames for vision analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic transcription only
  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms

  # With frame extraction for vision analysis
  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms --extract-visual

  # Custom interval for frame extraction (every 60 seconds)
  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms --extract-visual --frame-interval 60

  # Specify output directory and Whisper model
  python analyze_video.py https://www.youtube.com/watch?v=FOqbS_llAms --output ./my_output --model small

Note: This script prepares content for Claude Code to analyze natively.
      No external API key needed - Claude Code handles analysis directly!
        '''
    )

    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--output', '-o', default='./output',
                       help='Output directory (default: ./output)')
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--extract-visual', action='store_true',
                       help='Extract video frames for vision analysis (Task 044-1)')
    parser.add_argument('--frame-interval', type=int, default=30,
                       help='Interval between frame extractions in seconds (default: 30)')
    parser.add_argument('--smart-frames', action='store_true',
                       help='Use smart frame selection (scene detection + content analysis) - reduces frames by 70-80%')
    parser.add_argument('--no-ocr', action='store_true',
                       help='Disable OCR-based code detection in smart frames (faster but less accurate)')
    parser.add_argument('--multimodal', action='store_true',
                       help='Enable multi-modal integration (combines visual frames + transcript analysis)')
    parser.add_argument('--skip-download', action='store_true',
                       help='Skip download if video already exists')
    parser.add_argument('--skip-transcription', action='store_true',
                       help='Skip transcription if transcript already exists')

    args = parser.parse_args()

    url = args.url
    output_dir = args.output
    model_size = args.model

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("YouTube Video Analysis - Claude Code Native Integration")
    print("=" * 80)
    print()
    print("Features:")
    print("  - Download and transcribe YouTube videos")
    print("  - Prepare transcript for Claude Code native analysis")
    if args.multimodal:
        print("  - MULTI-MODAL INTEGRATION (combines visual + audio analysis)")
        if args.smart_frames:
            print("    - Smart frame selection (scene detection + content analysis)")
        elif args.extract_visual:
            print("    - Frame extraction for vision analysis")
    elif args.extract_visual or args.smart_frames:
        if args.smart_frames:
            print("  - SMART frame extraction (scene detection + content analysis)")
        else:
            print("  - Extract video frames for multi-modal vision analysis")
    print("  - No external API key required")
    print("  - Claude Code analyzes directly using built-in capabilities")
    print()
    print(f"Configuration:")
    print(f"  Video URL: {url}")
    print(f"  Output Directory: {output_dir}")
    print(f"  Whisper Model: {model_size}")
    if args.multimodal:
        print(f"  Multi-Modal Integration: ENABLED")
        if args.smart_frames:
            print(f"    Frame Selection: SMART (scene detection + content analysis)")
            print(f"    OCR Detection: {'Disabled' if args.no_ocr else 'Enabled'}")
        elif args.extract_visual:
            print(f"    Frame Extraction: Fixed interval (every {args.frame_interval}s)")
    elif args.smart_frames:
        print(f"  Frame Selection: SMART (scene detection + content analysis)")
        print(f"  OCR Detection: {'Disabled' if args.no_ocr else 'Enabled'}")
    elif args.extract_visual:
        print(f"  Frame Extraction: Fixed interval (every {args.frame_interval}s)")
    print()

    # Check dependencies first
    check_vision = args.extract_visual or args.smart_frames or args.multimodal
    check_dependencies(check_vision=check_vision)

    # Import frame extraction modules if needed
    if args.extract_visual or args.smart_frames or args.multimodal:
        try:
            from frame_extractor import FrameExtractor
            from vision_analyzer import VisionAnalyzer
            if args.smart_frames or args.multimodal:
                from smart_frame_selector import SmartFrameSelector
            if args.multimodal:
                from multimodal_integration import MultiModalIntegrator
            print("[OK] Frame extraction modules loaded")
            print()
        except ImportError as e:
            print(f"[FAIL] Could not import frame extraction modules: {e}")
            print("Make sure frame_extractor.py, vision_analyzer.py, smart_frame_selector.py, and multimodal_integration.py are in the same directory")
            sys.exit(1)

    try:
        # Step 1: Download video
        video_path = None
        if args.skip_download and os.path.exists(os.path.join(output_dir, "video.mp4")):
            print("[SKIP] Video already exists, skipping download")
            video_path = os.path.join(output_dir, "video.mp4")
            # Load metadata if exists
            metadata_path = os.path.join(output_dir, "metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {"url": url}
        else:
            video_path, metadata = download_video(url, output_dir)
            metadata['url'] = url  # Add URL to metadata

        # Step 2: Extract audio
        audio_path = os.path.join(output_dir, "audio.mp3")
        if args.skip_transcription and os.path.exists(audio_path):
            print("[SKIP] Audio already exists, skipping extraction")
        else:
            audio_path = extract_audio(video_path, output_dir)

        # Step 3: Transcribe
        transcript_path = os.path.join(output_dir, "transcript.txt")
        if args.skip_transcription and os.path.exists(transcript_path):
            print("[SKIP] Transcript already exists, loading from file")
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()
        else:
            transcript = transcribe_audio(audio_path, model_size)

        # Step 4: Prepare prompts for Claude Code native analysis
        prompts_data = prepare_analysis_prompts(transcript, metadata)

        # Step 5: Save results (transcript + prompts)
        save_results(output_dir, metadata, transcript, prompts_data)

        # Step 6: Extract frames and perform multi-modal integration (if requested)
        if args.multimodal:
            # Multi-modal integration: Combine visual + audio analysis
            print("=" * 80)
            print("STEP 6: Multi-Modal Integration (Visual + Audio)")
            print("=" * 80)
            print()

            frames_dir = os.path.join(output_dir, "smart_frames" if args.smart_frames else "frames")
            multimodal_dir = os.path.join(output_dir, "multimodal_output")

            # Extract frames using smart selection (recommended) or fixed interval
            print("Extracting frames...")
            if args.smart_frames or not args.extract_visual:
                # Default to smart selection for multimodal
                selector = SmartFrameSelector(output_dir=frames_dir)
                frames = selector.select_frames(video_path, metadata, enable_ocr=not args.no_ocr)
            else:
                # Fixed interval extraction
                extractor = FrameExtractor(output_dir=frames_dir, interval_seconds=args.frame_interval)
                frames = extractor.extract_frames(video_path, metadata)

            # Perform multi-modal integration
            integrator = MultiModalIntegrator(output_dir=multimodal_dir)

            # Align frames with transcript
            aligned_data = integrator.align_frames_with_transcript(
                frames=frames,
                transcript=transcript,
                window_seconds=30
            )

            # Merge multi-modal insights
            comprehensive_analysis = integrator.merge_multimodal_insights(
                aligned_data=aligned_data,
                video_metadata=metadata
            )

            # Generate all output formats
            output_files = integrator.generate_multimodal_output(comprehensive_analysis)

            print()
            print("=" * 80)
            print("MULTI-MODAL INTEGRATION COMPLETE")
            print("=" * 80)
            print()
            print(f"Analyzed {len(frames)} segments combining visual + audio")
            print(f"Frames saved to: {frames_dir}/")
            print(f"Multi-modal analysis: {multimodal_dir}/")
            print()
            print("Generated files:")
            for format_name, file_path in output_files.items():
                print(f"  - {format_name.upper()}: {file_path}")
            print()
            print("Next: Review MULTIMODAL_ANALYSIS.md or use PROMPT_MULTIMODAL.txt with Claude Code")
            print()

        elif args.extract_visual or args.smart_frames:
            # Vision-only analysis (no multi-modal integration)
            print("=" * 80)
            print("STEP 6: Extract Frames for Vision Analysis")
            print("=" * 80)
            print()

            frames_dir = os.path.join(output_dir, "smart_frames" if args.smart_frames else "frames")
            vision_dir = os.path.join(output_dir, "vision_results")

            # Extract frames using smart selection or fixed interval
            if args.smart_frames:
                # Smart frame selection (scene detection + content analysis)
                selector = SmartFrameSelector(output_dir=frames_dir)
                frames = selector.select_frames(video_path, metadata, enable_ocr=not args.no_ocr)
            else:
                # Fixed interval extraction
                extractor = FrameExtractor(output_dir=frames_dir, interval_seconds=args.frame_interval)
                frames = extractor.extract_frames(video_path, metadata)

            # Prepare vision analysis prompts
            analyzer = VisionAnalyzer(output_dir=vision_dir)

            # Load transcript segments if available (for context)
            transcript_data = None
            if hasattr(prompts_data, 'get') and 'transcript' in prompts_data:
                transcript_data = {'text': prompts_data['transcript']}

            prompts = analyzer.prepare_frame_analysis_prompts(frames, transcript_data)

            # Create workflow for Claude Code
            analyzer.create_claude_code_workflow(frames)

            print()
            print("=" * 80)
            print("VISION ANALYSIS PREPARED")
            print("=" * 80)
            print()
            print(f"Extracted {len(frames)} frames")
            print(f"Frames saved to: {frames_dir}/")
            print(f"Vision prompts saved to: {vision_dir}/")
            print(f"Claude Code workflow: {vision_dir}/vision_workflow_workflow.md")
            print()
            print("Next: Use Claude Code to analyze frames using the prepared workflow")
            print()

        # Return the data for Claude Code to use
        return prompts_data

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
