#!/usr/bin/env python3
"""
Frame Extraction Module for YouTube Video Analysis
Extracts key frames from videos for vision-based analysis

Part of Task 044-1: Frame Extraction + Vision Analysis Implementation
"""

import os
import cv2
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from tqdm import tqdm


class FrameExtractor:
    """Extract key frames from video files at configurable intervals"""

    def __init__(self, output_dir: str = "frames", interval_seconds: int = 30):
        """
        Initialize frame extractor

        Args:
            output_dir: Directory to save extracted frames
            interval_seconds: Time interval between frame extractions (default: 30s)
        """
        self.output_dir = Path(output_dir)
        self.interval_seconds = interval_seconds
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_frames(self, video_path: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Extract frames from video at regular intervals

        Args:
            video_path: Path to video file
            metadata: Optional video metadata (title, duration, etc.)

        Returns:
            List of frame info dicts with path, timestamp, frame_number

        Raises:
            ValueError: If video file doesn't exist or can't be opened
        """
        print("=" * 80)
        print("FRAME EXTRACTION")
        print("=" * 80)
        print()

        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")

        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        frame_interval = int(fps * self.interval_seconds)

        print(f"Video: {video_path}")
        print(f"FPS: {fps:.2f}")
        print(f"Total Frames: {total_frames:,}")
        print(f"Duration: {duration:.1f}s ({duration/60:.1f} minutes)")
        print(f"Extracting every {self.interval_seconds}s (every {frame_interval} frames)")
        print()

        frames = []
        frame_count = 0
        extracted_count = 0

        print("Extracting frames...")

        # Create progress bar
        with tqdm(total=total_frames, desc="Scanning frames", unit="frame", unit_scale=True) as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Extract frame at interval
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    frame_filename = f"frame_{int(timestamp):06d}s.jpg"
                    frame_path = self.output_dir / frame_filename

                    # Save frame as JPEG
                    cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])

                    frames.append({
                        'path': str(frame_path),
                        'filename': frame_filename,
                        'timestamp': timestamp,
                        'frame_number': frame_count,
                        'time_formatted': self._format_timestamp(timestamp)
                    })

                    extracted_count += 1
                    pbar.set_postfix({"extracted": extracted_count}, refresh=False)

                frame_count += 1
                pbar.update(1)

        cap.release()

        print(f"\n\n[OK] Extracted {extracted_count} frames to {self.output_dir}")
        print()

        # Save frame index
        self._save_frame_index(frames, metadata)

        return frames

    def extract_specific_frames(self, video_path: str, timestamps: List[float]) -> List[Dict]:
        """
        Extract frames at specific timestamps

        Args:
            video_path: Path to video file
            timestamps: List of timestamps (in seconds) to extract

        Returns:
            List of frame info dicts
        """
        print("=" * 80)
        print("EXTRACTING SPECIFIC FRAMES")
        print("=" * 80)
        print()

        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = []

        print(f"Extracting {len(timestamps)} frames at specific timestamps...")
        print()

        for timestamp in sorted(timestamps):
            # Seek to timestamp
            frame_number = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            ret, frame = cap.read()
            if ret:
                frame_filename = f"frame_{int(timestamp):06d}s.jpg"
                frame_path = self.output_dir / frame_filename

                cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 85])

                frames.append({
                    'path': str(frame_path),
                    'filename': frame_filename,
                    'timestamp': timestamp,
                    'frame_number': frame_number,
                    'time_formatted': self._format_timestamp(timestamp)
                })

                print(f"  Extracted: {self._format_timestamp(timestamp)} -> {frame_filename}")

        cap.release()

        print(f"\n[OK] Extracted {len(frames)} frames")
        print()

        return frames

    def get_frame_at_time(self, video_path: str, timestamp: float) -> Tuple[Optional[Dict], Optional[object]]:
        """
        Get a single frame at specific timestamp

        Args:
            video_path: Path to video file
            timestamp: Timestamp in seconds

        Returns:
            Tuple of (frame_info, frame_data) or (None, None) if failed
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None, None

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(timestamp * fps)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            return None, None

        frame_info = {
            'timestamp': timestamp,
            'frame_number': frame_number,
            'time_formatted': self._format_timestamp(timestamp)
        }

        return frame_info, frame

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def _save_frame_index(self, frames: List[Dict], metadata: Optional[Dict] = None):
        """Save frame index as JSON for reference"""
        index_path = self.output_dir / "frame_index.json"

        index_data = {
            'extracted_at': datetime.now().isoformat(),
            'interval_seconds': self.interval_seconds,
            'total_frames': len(frames),
            'metadata': metadata or {},
            'frames': frames
        }

        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)

        print(f"[OK] Frame index saved: {index_path}")


def main():
    """CLI interface for frame extraction"""
    import argparse

    parser = argparse.ArgumentParser(description='Extract frames from video for analysis')
    parser.add_argument('video_path', help='Path to video file')
    parser.add_argument('--interval', type=int, default=30,
                       help='Interval between frames in seconds (default: 30)')
    parser.add_argument('--output', default='frames',
                       help='Output directory for frames (default: frames)')
    parser.add_argument('--timestamps', nargs='+', type=float,
                       help='Extract specific timestamps instead of intervals')

    args = parser.parse_args()

    extractor = FrameExtractor(output_dir=args.output, interval_seconds=args.interval)

    if args.timestamps:
        frames = extractor.extract_specific_frames(args.video_path, args.timestamps)
    else:
        frames = extractor.extract_frames(args.video_path)

    print(f"\n✓ Successfully extracted {len(frames)} frames")
    print(f"✓ Frames saved to: {args.output}/")
    print(f"✓ Frame index: {args.output}/frame_index.json")


if __name__ == "__main__":
    main()
