#!/usr/bin/env python3
"""
Batch Processing Example: Process multiple YouTube videos from playlists or channels

This example demonstrates:
1. Processing entire playlists
2. Processing channel videos
3. Custom processing with progress tracking
4. Error recovery and retry logic
5. Results aggregation and reporting

Requirements:
    pip install pytubefix tqdm

Usage:
    # Process playlist (first 10 videos)
    python batch_processing_example.py --playlist "https://youtube.com/playlist?list=..." --max-videos 10

    # Process channel videos
    python batch_processing_example.py --channel "UCsomechannelid" --max-videos 20

    # Custom processing with transcript + frames
    python batch_processing_example.py --playlist "..." --mode full --output ./my_batch
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Callable
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from batch_processor import BatchProcessor, VideoResult
from analyze_video import download_video, extract_audio, transcribe_audio
from frame_extractor import FrameExtractor
from smart_frame_selector import SmartFrameSelector
from tqdm import tqdm


class CustomBatchProcessor:
    """
    Custom batch processor with additional features:
    - Multiple processing modes (metadata, transcript, full)
    - Custom progress callbacks
    - Results filtering and aggregation
    - Export in multiple formats
    """

    def __init__(
        self,
        mode: str = "metadata",
        output_dir: str = "./batch_output",
        enable_cache: bool = True
    ):
        """
        Initialize custom batch processor

        Args:
            mode: Processing mode ('metadata', 'transcript', 'full')
            output_dir: Output directory
            enable_cache: Enable caching for reuse
        """
        self.mode = mode
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.enable_cache = enable_cache

    def process_video_metadata(self, video_url: str, video_output_dir: Path) -> Dict[str, Any]:
        """
        Mode 1: Metadata only (fast - no download)

        Returns basic video information without downloading
        """
        from pytubefix import YouTube

        yt = YouTube(video_url)
        metadata = {
            'title': yt.title,
            'author': yt.author,
            'duration': yt.length,
            'views': yt.views,
            'description': yt.description[:500],  # First 500 chars
            'publish_date': str(yt.publish_date),
            'thumbnail_url': yt.thumbnail_url,
            'rating': yt.rating,
            'url': video_url
        }

        # Save metadata
        with open(video_output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        return {
            'success': True,
            'metadata': metadata,
            'mode': 'metadata'
        }

    def process_video_transcript(self, video_url: str, video_output_dir: Path) -> Dict[str, Any]:
        """
        Mode 2: Transcript only (download + transcribe, no frames)

        Returns video metadata and full transcript
        """
        # Check cache
        transcript_path = video_output_dir / 'transcript.txt'
        if self.enable_cache and transcript_path.exists():
            print(f"  [CACHE] Using cached transcript")
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()

            metadata_path = video_output_dir / 'metadata.json'
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            return {
                'success': True,
                'metadata': metadata,
                'transcript': transcript,
                'cached_transcript': True,
                'mode': 'transcript'
            }

        # Download and transcribe
        video_path, metadata = download_video(video_url, str(video_output_dir))
        audio_path = extract_audio(video_path, str(video_output_dir))
        transcript = transcribe_audio(audio_path, model_size="base")

        # Save transcript
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)

        # Save metadata
        with open(video_output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)

        return {
            'success': True,
            'metadata': metadata,
            'transcript': transcript,
            'cached_transcript': False,
            'mode': 'transcript'
        }

    def process_video_full(self, video_url: str, video_output_dir: Path) -> Dict[str, Any]:
        """
        Mode 3: Full processing (download + transcribe + frames)

        Returns complete analysis with frames
        """
        # Check cache
        transcript_path = video_output_dir / 'transcript.txt'
        frames_dir = video_output_dir / 'smart_frames'
        frame_index = frames_dir / 'frame_index.json'

        cached_transcript = False
        cached_frames = False

        # Get or download transcript
        if self.enable_cache and transcript_path.exists():
            print(f"  [CACHE] Using cached transcript")
            with open(transcript_path, 'r', encoding='utf-8') as f:
                transcript = f.read()
            metadata_path = video_output_dir / 'metadata.json'
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            video_path = video_output_dir / 'video.mp4'
            cached_transcript = True
        else:
            video_path, metadata = download_video(video_url, str(video_output_dir))
            audio_path = extract_audio(str(video_path), str(video_output_dir))
            transcript = transcribe_audio(audio_path, model_size="base")

            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            with open(video_output_dir / 'metadata.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

        # Get or extract frames
        if self.enable_cache and frame_index.exists():
            print(f"  [CACHE] Using cached frames")
            with open(frame_index, 'r', encoding='utf-8') as f:
                frames_data = json.load(f)
            frames = frames_data['frames']
            cached_frames = True
        else:
            selector = SmartFrameSelector(output_dir=str(frames_dir))
            frames = selector.select_frames(str(video_path), metadata, enable_ocr=False)

        return {
            'success': True,
            'metadata': metadata,
            'transcript': transcript,
            'frames_count': len(frames),
            'cached_transcript': cached_transcript,
            'cached_frames': cached_frames,
            'mode': 'full'
        }

    def create_processing_function(self) -> Callable:
        """
        Create appropriate processing function based on mode

        Returns:
            Processing function compatible with BatchProcessor
        """
        if self.mode == "metadata":
            return self.process_video_metadata
        elif self.mode == "transcript":
            return self.process_video_transcript
        elif self.mode == "full":
            return self.process_video_full
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def process_batch(
        self,
        video_urls: list = None,
        playlist_url: str = None,
        channel_id: str = None,
        max_videos: int = None
    ) -> Dict[str, Any]:
        """
        Process batch of videos

        Args:
            video_urls: List of video URLs (if providing directly)
            playlist_url: YouTube playlist URL
            channel_id: YouTube channel ID or URL
            max_videos: Maximum videos to process

        Returns:
            Batch processing results
        """
        # Get video URLs
        if video_urls:
            urls = video_urls
        elif playlist_url:
            urls = BatchProcessor.get_playlist_videos(playlist_url, max_videos)
        elif channel_id:
            urls = BatchProcessor.get_channel_videos(channel_id, max_videos or 50)
        else:
            raise ValueError("Must provide video_urls, playlist_url, or channel_id")

        if not urls:
            return {'error': 'No videos found'}

        # Create batch processor
        processor = BatchProcessor(
            output_dir=str(self.output_dir),
            process_function=self.create_processing_function(),
            use_cache=self.enable_cache,
            continue_on_error=True
        )

        # Process batch
        results = processor.process_batch(urls, batch_name=f"{self.mode}_batch")

        # Generate additional reports
        self._generate_summary_report(results)
        self._generate_csv_export(results)

        return results

    def _generate_summary_report(self, results: Dict[str, Any]):
        """Generate markdown summary report"""
        report_path = self.output_dir / 'SUMMARY_REPORT.md'

        stats = results['statistics']
        video_results = results['results']

        # Group by status
        successful = [r for r in video_results if r.success]
        failed = [r for r in video_results if not r.success]

        # Calculate statistics
        total_duration = sum(r.metadata.get('duration', 0) for r in successful if r.metadata)
        avg_duration = total_duration / len(successful) if successful else 0

        if self.mode in ['transcript', 'full']:
            cached_count = sum(1 for r in video_results if r.cached_transcript)
            cache_rate = (cached_count / len(video_results) * 100) if video_results else 0
        else:
            cached_count = 0
            cache_rate = 0

        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Batch Processing Summary Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Mode**: {self.mode}\n\n")
            f.write(f"**Output Directory**: {self.output_dir}\n\n")
            f.write(f"---\n\n")

            # Statistics
            f.write(f"## Statistics\n\n")
            f.write(f"- **Total Videos**: {stats.total_videos}\n")
            f.write(f"- **Successful**: {stats.successful} ({stats.success_rate:.1f}%)\n")
            f.write(f"- **Failed**: {stats.failed}\n")
            if cached_count > 0:
                f.write(f"- **Cached**: {cached_count} ({cache_rate:.1f}%)\n")
            f.write(f"- **Total Duration**: {total_duration / 3600:.1f} hours\n")
            f.write(f"- **Average Duration**: {avg_duration / 60:.1f} minutes\n")
            f.write(f"- **Processing Time**: {stats.total_duration_seconds / 60:.1f} minutes\n")
            f.write(f"- **Average per Video**: {stats.total_duration_seconds / stats.total_videos:.1f} seconds\n\n")

            # Successful videos
            if successful:
                f.write(f"## Successful Videos ({len(successful)})\n\n")
                f.write(f"| # | Title | Duration | Mode |\n")
                f.write(f"|---|-------|----------|------|\n")
                for i, r in enumerate(successful, 1):
                    title = r.title[:50] + '...' if len(r.title) > 50 else r.title
                    duration_min = r.metadata.get('duration', 0) / 60 if r.metadata else 0
                    cached = " (cached)" if r.cached_transcript else ""
                    f.write(f"| {i} | {title} | {duration_min:.1f}m | {self.mode}{cached} |\n")
                f.write(f"\n")

            # Failed videos
            if failed:
                f.write(f"## Failed Videos ({len(failed)})\n\n")
                for r in failed:
                    f.write(f"- **{r.title}**\n")
                    f.write(f"  - Video ID: {r.video_id}\n")
                    f.write(f"  - Error: {r.error}\n\n")

            # Recommendations
            f.write(f"## Recommendations\n\n")
            if stats.success_rate < 80:
                f.write(f"- Success rate is below 80%. Review failed videos and error messages.\n")
            if cache_rate > 50:
                f.write(f"- High cache hit rate ({cache_rate:.1f}%) - consider clearing cache if reprocessing is needed.\n")
            if stats.total_duration_seconds / stats.total_videos > 120:
                f.write(f"- Average processing time is high. Consider using cached mode or smaller Whisper model.\n")
            if not failed:
                f.write(f"- All videos processed successfully! ✓\n")

        print(f"\n[OK] Summary report saved: {report_path}")

    def _generate_csv_export(self, results: Dict[str, Any]):
        """Generate CSV export of results"""
        import csv

        csv_path = self.output_dir / 'results.csv'
        video_results = results['results']

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            headers = ['Video ID', 'Title', 'URL', 'Success', 'Duration (s)', 'Processing Time (s)', 'Error']
            if self.mode in ['transcript', 'full']:
                headers.append('Cached')
            if self.mode == 'full':
                headers.append('Frames')

            writer.writerow(headers)

            # Data
            for r in video_results:
                row = [
                    r.video_id,
                    r.title,
                    r.url,
                    'Yes' if r.success else 'No',
                    r.metadata.get('duration', 0) if r.metadata else 0,
                    r.duration_seconds,
                    r.error or ''
                ]

                if self.mode in ['transcript', 'full']:
                    row.append('Yes' if r.cached_transcript else 'No')
                if self.mode == 'full':
                    row.append(r.metadata.get('frames_count', 0) if r.metadata else 0)

                writer.writerow(row)

        print(f"[OK] CSV export saved: {csv_path}")


def main():
    """CLI interface for batch processing"""
    parser = argparse.ArgumentParser(
        description='Batch process YouTube videos from playlists or channels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    # Process playlist (metadata only - fast)
    python batch_processing_example.py --playlist "https://youtube.com/playlist?list=..." --mode metadata

    # Process playlist (with transcripts)
    python batch_processing_example.py --playlist "..." --mode transcript --max-videos 10

    # Process channel (full - with frames)
    python batch_processing_example.py --channel "UCchannelid" --mode full --max-videos 5

    # Process specific videos
    python batch_processing_example.py --videos video1.txt --mode transcript

Modes:
    metadata  - Fast, no download (just video info)
    transcript - Download + transcribe (no frames)
    full      - Complete analysis (download + transcribe + frames)
        '''
    )

    # Input source
    parser.add_argument('--playlist', help='YouTube playlist URL')
    parser.add_argument('--channel', help='YouTube channel ID or URL')
    parser.add_argument('--videos', help='Text file with video URLs (one per line)')
    parser.add_argument('--max-videos', type=int, help='Maximum videos to process')

    # Processing options
    parser.add_argument('--mode', default='transcript',
                       choices=['metadata', 'transcript', 'full'],
                       help='Processing mode (default: transcript)')
    parser.add_argument('--output', default='./batch_output',
                       help='Output directory (default: ./batch_output)')
    parser.add_argument('--no-cache', action='store_true',
                       help='Disable caching')

    args = parser.parse_args()

    # Validate input
    if not any([args.playlist, args.channel, args.videos]):
        print("Error: Must specify --playlist, --channel, or --videos")
        parser.print_help()
        sys.exit(1)

    # Get video URLs
    video_urls = None
    if args.videos:
        with open(args.videos, 'r') as f:
            video_urls = [line.strip() for line in f if line.strip()]

    # Create processor
    processor = CustomBatchProcessor(
        mode=args.mode,
        output_dir=args.output,
        enable_cache=not args.no_cache
    )

    # Process batch
    results = processor.process_batch(
        video_urls=video_urls,
        playlist_url=args.playlist,
        channel_id=args.channel,
        max_videos=args.max_videos
    )

    # Print summary
    if 'error' in results:
        print(f"\nError: {results['error']}")
        sys.exit(1)

    stats = results['statistics']
    print("\n" + "=" * 80)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 80)
    print()
    print(f"Total Videos: {stats.total_videos}")
    print(f"Successful: {stats.successful} ({stats.success_rate:.1f}%)")
    print(f"Failed: {stats.failed}")
    print(f"Processing Time: {stats.total_duration_seconds / 60:.1f} minutes")
    print()
    print(f"Results saved to: {args.output}/")
    print(f"  - batch_results.json")
    print(f"  - SUMMARY_REPORT.md")
    print(f"  - results.csv")
    print()

    sys.exit(0 if stats.failed == 0 else 1)


if __name__ == "__main__":
    main()
