#!/usr/bin/env python3
"""
YouTube Video Analysis with Caching
Wrapper around analyze_video.py that adds intelligent caching support.

Features:
- Multi-layer caching (transcripts, embeddings, frames, analysis)
- Batch processing (playlists, channels)
- Progress tracking
- Cache statistics

Usage:
    # Single video with cache
    python analyze_with_cache.py VIDEO_URL

    # Process playlist
    python analyze_with_cache.py --playlist PLAYLIST_URL

    # Process channel
    python analyze_with_cache.py --channel CHANNEL_ID --max-videos 20

    # Show cache stats
    python analyze_with_cache.py --cache-stats

    # Clear cache
    python analyze_with_cache.py --clear-cache VIDEO_ID
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Import cache and batch modules
try:
    from cache.cache_manager import CacheManager
    from batch_processor import BatchProcessor
except ImportError as e:
    print(f"[ERROR] Could not import modules: {e}")
    print("Make sure you're in the scripts directory")
    sys.exit(1)

# Import existing video processing
try:
    from analyze_video import (
        download_video,
        extract_audio,
        transcribe_audio,
        prepare_analysis_prompts,
        save_results
    )
except ImportError as e:
    print(f"[ERROR] Could not import analyze_video: {e}")
    sys.exit(1)


def process_video_with_cache(
    video_url: str,
    output_dir: Path,
    cache_manager: CacheManager,
    model_size: str = 'base',
    extract_visual: bool = False,
    smart_frames: bool = False,
    no_ocr: bool = False
) -> dict:
    """
    Process video with intelligent caching

    Args:
        video_url: YouTube video URL
        output_dir: Output directory
        cache_manager: Cache manager instance
        model_size: Whisper model size
        extract_visual: Extract frames
        smart_frames: Use smart frame selection
        no_ocr: Disable OCR

    Returns:
        Processing result dict
    """
    video_id = cache_manager.extract_video_id(video_url)

    print("\n" + "=" * 80)
    print(f"PROCESSING VIDEO: {video_id}")
    print("=" * 80)
    print()

    # Check cache
    cached_transcript = cache_manager.has_transcript(video_id)
    cached_frames = cache_manager.has_frames(video_id) if extract_visual or smart_frames else False

    # Download video (if not in output dir)
    video_path = output_dir / "video.mp4"
    metadata_path = output_dir / "metadata.json"

    if not video_path.exists():
        print("[DOWNLOAD] Downloading video...")
        video_path, metadata = download_video(video_url, str(output_dir))
        metadata['url'] = video_url
    else:
        print("[SKIP] Video already exists")
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"url": video_url}

    # Get or generate transcript
    if cached_transcript:
        print("[CACHE HIT] Loading transcript from cache")
        transcript = cache_manager.get_transcript(video_id)
    else:
        print("[CACHE MISS] Generating transcript...")

        # Extract audio
        audio_path = output_dir / "audio.mp3"
        if not audio_path.exists():
            audio_path = extract_audio(str(video_path), str(output_dir))

        # Transcribe
        transcript = transcribe_audio(str(audio_path), model_size)

        # Save to cache
        cache_manager.save_transcript(video_id, transcript)
        print("[CACHE SAVE] Transcript cached")

    # Prepare prompts
    prompts_data = prepare_analysis_prompts(transcript, metadata)

    # Save results
    save_results(str(output_dir), metadata, transcript, prompts_data)

    # Handle frame extraction
    if extract_visual or smart_frames:
        frames_dir = output_dir / ("smart_frames" if smart_frames else "frames")

        if cached_frames:
            print(f"[CACHE HIT] Loading frames from cache")
            # Copy from cache to output
            cached_frame_dir = cache_manager.get_frame_dir(video_id)
            if not frames_dir.exists():
                import shutil
                shutil.copytree(cached_frame_dir, frames_dir)
            frames = list(frames_dir.glob("*.jpg"))
        else:
            print(f"[CACHE MISS] Extracting frames...")

            # Import frame extraction modules
            if smart_frames:
                from smart_frame_selector import SmartFrameSelector
                selector = SmartFrameSelector(output_dir=str(frames_dir))
                frames = selector.select_frames(str(video_path), metadata, enable_ocr=not no_ocr)
            else:
                from frame_extractor import FrameExtractor
                extractor = FrameExtractor(output_dir=str(frames_dir), interval_seconds=30)
                frames = extractor.extract_frames(str(video_path), metadata)

            # Save to cache
            cache_manager.save_frame_dir(video_id, frames_dir)
            print("[CACHE SAVE] Frames cached")

        # Prepare vision analysis
        from vision_analyzer import VisionAnalyzer
        vision_dir = output_dir / "vision_results"
        analyzer = VisionAnalyzer(output_dir=str(vision_dir))

        transcript_data = {'text': transcript}
        analyzer.prepare_frame_analysis_prompts(frames, transcript_data)
        analyzer.create_claude_code_workflow(frames)

        print(f"[OK] Vision analysis prepared ({len(frames)} frames)")

    return {
        'success': True,
        'video_id': video_id,
        'metadata': metadata,
        'cached_transcript': cached_transcript,
        'cached_frames': cached_frames
    }


def create_batch_processor(cache_manager: CacheManager, args) -> BatchProcessor:
    """Create batch processor with caching"""

    def process_function(video_url: str, video_output_dir: Path) -> dict:
        """Custom processing function for batch processor"""
        return process_video_with_cache(
            video_url,
            video_output_dir,
            cache_manager,
            model_size=args.model,
            extract_visual=args.extract_visual,
            smart_frames=args.smart_frames,
            no_ocr=args.no_ocr
        )

    return BatchProcessor(
        output_dir=args.output,
        process_function=process_function,
        use_cache=True,
        continue_on_error=True
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='YouTube Video Analysis with Caching',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Single video with cache
  python analyze_with_cache.py https://youtube.com/watch?v=VIDEO_ID

  # Process playlist (first 10 videos)
  python analyze_with_cache.py --playlist PLAYLIST_URL --max-videos 10

  # Process channel (recent 20 videos)
  python analyze_with_cache.py --channel CHANNEL_ID --max-videos 20

  # With frame extraction
  python analyze_with_cache.py VIDEO_URL --extract-visual

  # With smart frames
  python analyze_with_cache.py VIDEO_URL --smart-frames

  # Show cache stats
  python analyze_with_cache.py --cache-stats

  # Clear specific video cache
  python analyze_with_cache.py --clear-cache VIDEO_ID

  # Clear all cache
  python cache_cli.py clear
        '''
    )

    # Video source
    parser.add_argument('url', nargs='?', help='YouTube video URL')
    parser.add_argument('--playlist', help='YouTube playlist URL')
    parser.add_argument('--channel', help='YouTube channel ID or URL')
    parser.add_argument('--max-videos', type=int, help='Max videos to process')

    # Processing options
    parser.add_argument('--output', '-o', default='./output',
                       help='Output directory (default: ./output)')
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size')
    parser.add_argument('--extract-visual', action='store_true',
                       help='Extract frames for vision analysis')
    parser.add_argument('--smart-frames', action='store_true',
                       help='Use smart frame selection')
    parser.add_argument('--no-ocr', action='store_true',
                       help='Disable OCR in smart frames')

    # Cache management
    parser.add_argument('--cache-dir', default='.cache',
                       help='Cache directory')
    parser.add_argument('--cache-stats', action='store_true',
                       help='Show cache statistics')
    parser.add_argument('--clear-cache', metavar='VIDEO_ID',
                       help='Clear cache for video')

    args = parser.parse_args()

    # Initialize cache manager
    cache_manager = CacheManager(cache_dir=args.cache_dir)

    # Handle cache-only commands
    if args.cache_stats:
        cache_manager.print_stats()
        return

    if args.clear_cache:
        video_id = cache_manager.extract_video_id(args.clear_cache)
        deleted = cache_manager.clear_video(video_id)
        if deleted > 0:
            print(f"[OK] Cleared cache for {video_id} ({deleted} entries)")
        else:
            print(f"[INFO] No cache found for {video_id}")
        return

    # Require video source
    if not args.url and not args.playlist and not args.channel:
        parser.error("Provide URL, --playlist, or --channel")

    # Batch processing
    if args.playlist or args.channel:
        print("\n" + "=" * 80)
        print("BATCH PROCESSING WITH CACHE")
        print("=" * 80)
        print()

        processor = create_batch_processor(cache_manager, args)

        if args.playlist:
            results = processor.process_playlist(args.playlist, args.max_videos)
        else:
            results = processor.process_channel(
                args.channel,
                args.max_videos or 50
            )

        # Show final cache stats
        print("\n" + "=" * 80)
        print("FINAL CACHE STATISTICS")
        print("=" * 80)
        cache_manager.print_stats()

        return

    # Single video processing
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = process_video_with_cache(
        args.url,
        output_dir,
        cache_manager,
        model_size=args.model,
        extract_visual=args.extract_visual,
        smart_frames=args.smart_frames,
        no_ocr=args.no_ocr
    )

    # Show cache stats
    print("\n" + "=" * 80)
    print("CACHE STATISTICS")
    print("=" * 80)
    cache_manager.print_stats()

    if result['success']:
        print("\n✓ Video processing complete!")
        if result['cached_transcript']:
            print("  - Transcript loaded from cache (saved ~2-5 minutes)")
        if result.get('cached_frames'):
            print("  - Frames loaded from cache (saved ~1-3 minutes)")
    else:
        print("\n✗ Video processing failed")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CANCELLED] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
