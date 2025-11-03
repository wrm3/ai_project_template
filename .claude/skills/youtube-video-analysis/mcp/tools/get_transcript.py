"""
get_transcript MCP tool handler
Downloads and transcribes YouTube videos
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import asyncio
import logging
import re

# Add scripts directory to path
SKILL_ROOT = Path(__file__).parent.parent.parent.resolve()
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


async def get_transcript_handler(
    video_url: str,
    output_dir: Optional[str] = None,
    force_redownload: bool = False,
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Get transcript for a YouTube video

    Args:
        video_url: YouTube URL or video ID
        output_dir: Output directory (defaults to ./output/<video_id>/)
        force_redownload: Re-download even if cached
        logger: Logger instance

    Returns:
        dict with transcript and metadata
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = datetime.now()

    try:
        # Import analyze_video functions
        from analyze_video import download_video, extract_audio, transcribe_audio

        # Extract video ID from URL
        video_id = extract_video_id(video_url)

        # Set output directory
        if output_dir is None:
            output_dir = f"./output/{video_id}"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Getting transcript for video: {video_id}")
        logger.info(f"Output directory: {output_path}")

        # Check for cached transcript
        transcript_path = output_path / "transcript.txt"
        metadata_path = output_path / "metadata.json"

        if not force_redownload and transcript_path.exists() and metadata_path.exists():
            logger.info("Found cached transcript, loading from disk...")

            # Load cached transcript
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()

            # Load metadata
            import json
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            processing_time = (datetime.now() - start_time).total_seconds()

            return {
                "success": True,
                "video_id": video_id,
                "title": metadata.get("title", "Unknown"),
                "author": metadata.get("author", "Unknown"),
                "duration_seconds": metadata.get("duration", 0),
                "transcript": transcript,
                "transcript_length": len(transcript),
                "word_count": len(transcript.split()),
                "cached": True,
                "output_dir": str(output_path),
                "processing_time_seconds": round(processing_time, 2)
            }

        # Download video
        logger.info("Downloading video...")
        video_path, metadata = await asyncio.to_thread(
            download_video,
            video_url,
            str(output_path)
        )

        # Extract audio
        logger.info("Extracting audio...")
        audio_path = await asyncio.to_thread(
            extract_audio,
            video_path,
            str(output_path)
        )

        # Transcribe
        logger.info("Transcribing audio (this may take a few minutes)...")
        transcript = await asyncio.to_thread(
            transcribe_audio,
            audio_path,
            model_size="base"
        )

        # Save transcript
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        # Save metadata
        import json
        metadata['url'] = video_url
        metadata['video_id'] = video_id
        metadata['transcribed_at'] = datetime.now().isoformat()

        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        processing_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"Transcript complete! Length: {len(transcript)} characters")

        return {
            "success": True,
            "video_id": video_id,
            "title": metadata.get("title", "Unknown"),
            "author": metadata.get("author", "Unknown"),
            "duration_seconds": metadata.get("duration", 0),
            "transcript": transcript,
            "transcript_length": len(transcript),
            "word_count": len(transcript.split()),
            "cached": False,
            "output_dir": str(output_path),
            "processing_time_seconds": round(processing_time, 2)
        }

    except Exception as e:
        logger.exception(f"Error getting transcript: {e}")
        return {
            "success": False,
            "error": str(e),
            "video_url": video_url
        }


def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL or return as-is if already an ID"""
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If no pattern matches, assume it's already a video ID
    # (11 characters, alphanumeric + _ and -)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url

    # Return as-is and let pytubefix handle it
    return url
