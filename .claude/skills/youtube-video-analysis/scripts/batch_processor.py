"""
Batch Video Processor for YouTube Analysis
Process multiple videos from playlists or channels with progress tracking and error recovery.

Features:
- Playlist processing
- Channel video processing (with max limit)
- Progress tracking with tqdm
- Error recovery (continue on failure)
- Batch statistics reporting
- Cache integration

Usage:
    from batch_processor import BatchProcessor

    processor = BatchProcessor(output_dir="./batch_output")
    results = processor.process_playlist("https://youtube.com/playlist?list=...")
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
import traceback

try:
    from pytubefix import YouTube, Playlist, Channel
    from tqdm import tqdm
except ImportError:
    print("[ERROR] Missing dependencies. Install with:")
    print("pip install pytubefix tqdm")
    sys.exit(1)


@dataclass
class VideoResult:
    """Result of processing a single video"""
    video_id: str
    url: str
    title: str
    success: bool
    error: Optional[str] = None
    cached_transcript: bool = False
    cached_embeddings: bool = False
    cached_frames: bool = False
    duration_seconds: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class BatchStats:
    """Statistics for batch processing"""
    total_videos: int
    successful: int
    failed: int
    cached: int
    total_duration_seconds: float
    start_time: str
    end_time: str

    @property
    def success_rate(self) -> float:
        return (self.successful / self.total_videos * 100) if self.total_videos > 0 else 0.0

    @property
    def cache_rate(self) -> float:
        return (self.cached / self.total_videos * 100) if self.total_videos > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BatchProcessor:
    """
    Batch processor for YouTube videos

    Features:
    - Process playlists
    - Process channel videos
    - Cache integration
    - Progress tracking
    - Error recovery
    - Statistics reporting
    """

    def __init__(
        self,
        output_dir: str = "./batch_output",
        process_function: Optional[Callable] = None,
        use_cache: bool = True,
        continue_on_error: bool = True
    ):
        """
        Initialize batch processor

        Args:
            output_dir: Directory for output files
            process_function: Custom video processing function
            use_cache: Whether to use caching
            continue_on_error: Continue processing on video failure
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.process_function = process_function
        self.use_cache = use_cache
        self.continue_on_error = continue_on_error

        self.results: List[VideoResult] = []

    @staticmethod
    def get_playlist_videos(playlist_url: str, max_videos: Optional[int] = None) -> List[str]:
        """
        Get video URLs from playlist

        Args:
            playlist_url: YouTube playlist URL
            max_videos: Maximum number of videos to retrieve

        Returns:
            List of video URLs
        """
        print(f"\n[INFO] Fetching playlist videos from: {playlist_url}")

        try:
            playlist = Playlist(playlist_url)
            video_urls = list(playlist.video_urls)

            if max_videos and max_videos < len(video_urls):
                video_urls = video_urls[:max_videos]

            print(f"[OK] Found {len(video_urls)} videos in playlist")
            return video_urls

        except Exception as e:
            print(f"[ERROR] Could not fetch playlist: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def get_channel_videos(channel_id: str, max_videos: int = 50) -> List[str]:
        """
        Get video URLs from channel

        Args:
            channel_id: YouTube channel ID or URL
            max_videos: Maximum number of videos to retrieve

        Returns:
            List of video URLs
        """
        print(f"\n[INFO] Fetching channel videos from: {channel_id}")

        try:
            # Handle different channel URL formats
            if 'youtube.com' in channel_id:
                channel = Channel(channel_id)
            else:
                channel = Channel(f"https://www.youtube.com/channel/{channel_id}")

            video_urls = list(channel.video_urls)[:max_videos]

            print(f"[OK] Found {len(video_urls)} videos in channel")
            return video_urls

        except Exception as e:
            print(f"[ERROR] Could not fetch channel: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def extract_video_id(url: str) -> str:
        """Extract video ID from YouTube URL"""
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'watch?v=' in url:
            return url.split('watch?v=')[-1].split('&')[0]
        elif 'youtube.com/embed/' in url:
            return url.split('embed/')[-1].split('?')[0]
        else:
            return url

    def _default_process_video(self, video_url: str, video_output_dir: Path) -> Dict[str, Any]:
        """
        Default video processing (just metadata)

        Args:
            video_url: YouTube video URL
            video_output_dir: Output directory for this video

        Returns:
            Processing result dictionary
        """
        yt = YouTube(video_url)

        metadata = {
            'title': yt.title,
            'author': yt.author,
            'duration': yt.length,
            'views': yt.views,
            'description': yt.description,
            'url': video_url
        }

        # Save metadata
        metadata_path = video_output_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return {'success': True, 'metadata': metadata}

    def process_video(
        self,
        video_url: str,
        video_index: int,
        total_videos: int,
        pbar: Optional[tqdm] = None
    ) -> VideoResult:
        """
        Process a single video

        Args:
            video_url: YouTube video URL
            video_index: Index in batch (0-based)
            total_videos: Total number of videos
            pbar: Progress bar instance

        Returns:
            VideoResult object
        """
        start_time = datetime.now()
        video_id = self.extract_video_id(video_url)

        # Create output directory for this video
        video_output_dir = self.output_dir / f"video_{video_index + 1:03d}_{video_id}"
        video_output_dir.mkdir(parents=True, exist_ok=True)

        # Update progress bar
        if pbar:
            pbar.set_description(f"Processing {video_index + 1}/{total_videos}: {video_id}")

        try:
            # Use custom processing function if provided
            if self.process_function:
                result = self.process_function(video_url, video_output_dir)
            else:
                result = self._default_process_video(video_url, video_output_dir)

            duration = (datetime.now() - start_time).total_seconds()

            # Create success result
            video_result = VideoResult(
                video_id=video_id,
                url=video_url,
                title=result.get('metadata', {}).get('title', 'Unknown'),
                success=True,
                duration_seconds=duration,
                metadata=result.get('metadata'),
                cached_transcript=result.get('cached_transcript', False),
                cached_embeddings=result.get('cached_embeddings', False),
                cached_frames=result.get('cached_frames', False)
            )

            if pbar:
                pbar.set_postfix(status="✓", refresh=True)

            return video_result

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()

            error_msg = str(e)
            print(f"\n[ERROR] Failed to process {video_id}: {error_msg}")

            # Save error details
            error_file = video_output_dir / "error.txt"
            with open(error_file, 'w') as f:
                f.write(f"Error: {error_msg}\n\n")
                f.write(traceback.format_exc())

            if pbar:
                pbar.set_postfix(status="✗", refresh=True)

            # Get title if possible
            title = "Unknown"
            try:
                yt = YouTube(video_url)
                title = yt.title
            except:
                pass

            return VideoResult(
                video_id=video_id,
                url=video_url,
                title=title,
                success=False,
                error=error_msg,
                duration_seconds=duration
            )

    def process_batch(
        self,
        video_urls: List[str],
        batch_name: str = "batch"
    ) -> Dict[str, Any]:
        """
        Process a batch of videos

        Args:
            video_urls: List of YouTube video URLs
            batch_name: Name for this batch

        Returns:
            Dictionary with results and statistics
        """
        print("\n" + "=" * 80)
        print(f"BATCH PROCESSING: {batch_name}")
        print("=" * 80)
        print()
        print(f"Videos to process: {len(video_urls)}")
        print(f"Output directory: {self.output_dir}")
        print(f"Cache enabled: {self.use_cache}")
        print(f"Continue on error: {self.continue_on_error}")
        print()

        start_time = datetime.now()
        self.results = []

        # Process with progress bar
        with tqdm(total=len(video_urls), desc="Processing videos", unit="video") as pbar:
            for i, video_url in enumerate(video_urls):
                result = self.process_video(video_url, i, len(video_urls), pbar)
                self.results.append(result)

                # Update progress bar
                pbar.update(1)

                # Stop on error if configured
                if not result.success and not self.continue_on_error:
                    print("\n[STOP] Stopping batch due to error (continue_on_error=False)")
                    break

        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()

        # Calculate statistics
        successful = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        cached = sum(1 for r in self.results if r.cached_transcript)

        stats = BatchStats(
            total_videos=len(self.results),
            successful=successful,
            failed=failed,
            cached=cached,
            total_duration_seconds=total_duration,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat()
        )

        # Save results
        results_file = self.output_dir / "batch_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'batch_name': batch_name,
                'statistics': stats.to_dict(),
                'results': [asdict(r) for r in self.results]
            }, f, indent=2)

        # Print summary
        self._print_summary(stats)

        return {
            'statistics': stats,
            'results': self.results,
            'results_file': str(results_file)
        }

    def _print_summary(self, stats: BatchStats):
        """Print batch processing summary"""
        print("\n" + "=" * 80)
        print("BATCH PROCESSING COMPLETE")
        print("=" * 80)
        print()
        print(f"Total Videos: {stats.total_videos}")
        print(f"Successful: {stats.successful} ({stats.success_rate:.1f}%)")
        print(f"Failed: {stats.failed}")
        if self.use_cache:
            print(f"Cached: {stats.cached} ({stats.cache_rate:.1f}%)")
        print()
        print(f"Duration: {stats.total_duration_seconds:.1f}s ({stats.total_duration_seconds / 60:.1f} min)")
        print(f"Average per video: {stats.total_duration_seconds / stats.total_videos:.1f}s")
        print()

        if stats.failed > 0:
            print("Failed Videos:")
            for result in self.results:
                if not result.success:
                    print(f"  - {result.video_id}: {result.title}")
                    print(f"    Error: {result.error}")
            print()

        print(f"Results saved to: {self.output_dir / 'batch_results.json'}")
        print()

    def process_playlist(
        self,
        playlist_url: str,
        max_videos: Optional[int] = None,
        mode: str = 'metadata'
    ) -> Dict[str, Any]:
        """
        Process entire YouTube playlist

        Args:
            playlist_url: YouTube playlist URL
            max_videos: Maximum number of videos to process
            mode: Processing mode ('metadata', 'rag', 'full')

        Returns:
            Processing results
        """
        video_urls = self.get_playlist_videos(playlist_url, max_videos)

        if not video_urls:
            return {'error': 'No videos found in playlist'}

        # Extract playlist name
        try:
            playlist = Playlist(playlist_url)
            batch_name = f"playlist_{playlist.title}"
        except:
            batch_name = "playlist_unknown"

        return self.process_batch(video_urls, batch_name)

    def process_channel(
        self,
        channel_id: str,
        max_videos: int = 50,
        mode: str = 'metadata'
    ) -> Dict[str, Any]:
        """
        Process videos from YouTube channel

        Args:
            channel_id: YouTube channel ID or URL
            max_videos: Maximum number of videos to process
            mode: Processing mode ('metadata', 'rag', 'full')

        Returns:
            Processing results
        """
        video_urls = self.get_channel_videos(channel_id, max_videos)

        if not video_urls:
            return {'error': 'No videos found in channel'}

        # Extract channel name
        try:
            if 'youtube.com' in channel_id:
                channel = Channel(channel_id)
            else:
                channel = Channel(f"https://www.youtube.com/channel/{channel_id}")
            batch_name = f"channel_{channel.channel_name}"
        except:
            batch_name = "channel_unknown"

        return self.process_batch(video_urls, batch_name)


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Batch process YouTube videos')
    parser.add_argument('--playlist', help='YouTube playlist URL')
    parser.add_argument('--channel', help='YouTube channel ID or URL')
    parser.add_argument('--max-videos', type=int, help='Maximum videos to process')
    parser.add_argument('--output', default='./batch_output', help='Output directory')
    parser.add_argument('--no-cache', action='store_true', help='Disable cache')
    parser.add_argument('--stop-on-error', action='store_true', help='Stop on first error')

    args = parser.parse_args()

    if not args.playlist and not args.channel:
        print("Error: Must specify --playlist or --channel")
        sys.exit(1)

    # Create processor
    processor = BatchProcessor(
        output_dir=args.output,
        use_cache=not args.no_cache,
        continue_on_error=not args.stop_on_error
    )

    # Process playlist or channel
    if args.playlist:
        results = processor.process_playlist(args.playlist, args.max_videos)
    else:
        results = processor.process_channel(args.channel, args.max_videos or 50)

    # Exit with appropriate code
    stats = results.get('statistics')
    if stats and stats.failed > 0:
        sys.exit(1)
