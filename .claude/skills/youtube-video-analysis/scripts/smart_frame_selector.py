#!/usr/bin/env python3
"""
Smart Frame Selection Module for YouTube Video Analysis
Implements intelligent frame selection using scene change detection and content heuristics

Part of Task 044-2: Smart Frame Selection + Code Detection
Reduces frame extraction by 70-80% while maintaining quality
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
from tqdm import tqdm


class SmartFrameSelector:
    """
    Intelligent frame selection using:
    1. Scene change detection (histogram comparison)
    2. Code presence heuristics (OCR + pattern matching)
    3. Diagram/slide detection (edge detection + contours)
    """

    def __init__(self, output_dir: str = "smart_frames"):
        """
        Initialize smart frame selector

        Args:
            output_dir: Directory to save selected frames
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Detection thresholds
        self.scene_change_threshold = 0.70  # Correlation threshold (lower = more different)
        self.code_score_threshold = 0.5     # Minimum score to consider frame has code
        self.diagram_score_threshold = 0.5  # Minimum score to consider frame has diagram

    def select_frames(
        self,
        video_path: str,
        metadata: Optional[Dict] = None,
        enable_ocr: bool = True
    ) -> List[Dict]:
        """
        Main smart frame selection pipeline

        Args:
            video_path: Path to video file
            metadata: Optional video metadata
            enable_ocr: Enable OCR-based content detection (slower but more accurate)

        Returns:
            List of selected frame info dicts
        """
        print("=" * 80)
        print("SMART FRAME SELECTION")
        print("=" * 80)
        print()

        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")

        # Step 1: Detect scene changes
        print("Step 1: Detecting scene changes...")
        scene_frames = self._detect_scene_changes(video_path)
        print(f"[OK] Found {len(scene_frames)} scene changes")
        print()

        # Step 2: Analyze content (code, diagrams, text)
        print("Step 2: Analyzing frame content...")
        selected_frames = self._analyze_and_filter_frames(scene_frames, enable_ocr)
        print(f"[OK] Selected {len(selected_frames)} important frames")
        print()

        # Step 3: Save selected frames
        print("Step 3: Saving selected frames...")
        saved_frames = self._save_frames(selected_frames, metadata)
        print(f"[OK] Saved {len(saved_frames)} frames to {self.output_dir}")
        print()

        # Calculate statistics
        reduction_percent = 100 * (1 - len(saved_frames) / max(len(scene_frames), 1))
        print("=" * 80)
        print("SMART SELECTION SUMMARY")
        print("=" * 80)
        print()
        print(f"Scene changes detected: {len(scene_frames)}")
        print(f"Frames selected: {len(saved_frames)}")
        print(f"Reduction: {reduction_percent:.1f}%")
        print()

        return saved_frames

    def _detect_scene_changes(self, video_path: str) -> List[Dict]:
        """
        Detect scene changes using histogram comparison

        Args:
            video_path: Path to video file

        Returns:
            List of frames with significant scene changes
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        print(f"Video: {video_path}")
        print(f"FPS: {fps:.2f}")
        print(f"Total Frames: {total_frames:,}")
        print(f"Duration: {duration:.1f}s ({duration/60:.1f} minutes)")
        print()

        prev_hist = None
        scene_frames = []
        frame_count = 0
        min_frame_gap = int(fps * 5)  # Minimum 5 seconds between scene changes

        print("Scanning for scene changes...")

        # Create progress bar
        with tqdm(total=total_frames, desc="Detecting scenes", unit="frame", unit_scale=True) as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Skip frames too close to previous scene change
                if scene_frames and (frame_count - scene_frames[-1]['frame_number']) < min_frame_gap:
                    frame_count += 1
                    pbar.update(1)
                    continue

                # Convert to HSV for better color comparison
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Calculate histogram
                hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
                hist = cv2.normalize(hist, hist).flatten()

                # Compare with previous frame
                if prev_hist is not None:
                    # Use correlation (1.0 = identical, 0.0 = completely different)
                    correlation = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)

                    # Detect significant change
                    if correlation < self.scene_change_threshold:
                        timestamp = frame_count / fps
                        scene_frames.append({
                            'frame': frame.copy(),
                            'timestamp': timestamp,
                            'frame_number': frame_count,
                            'time_formatted': self._format_timestamp(timestamp),
                            'scene_change_score': 1.0 - correlation,  # Higher = more different
                            'reason': 'scene_change'
                        })

                        pbar.set_postfix({"scenes": len(scene_frames)}, refresh=False)

                prev_hist = hist
                frame_count += 1
                pbar.update(1)

        cap.release()
        print("\n")

        return scene_frames

    def _analyze_and_filter_frames(self, frames: List[Dict], enable_ocr: bool = True) -> List[Dict]:
        """
        Analyze frame content and filter based on importance

        Args:
            frames: List of candidate frames from scene detection
            enable_ocr: Enable OCR-based detection

        Returns:
            Filtered list of important frames
        """
        selected = []

        # Create progress bar for content analysis
        with tqdm(total=len(frames), desc="Analyzing content", unit="frame") as pbar:
            for i, frame_data in enumerate(frames):
                frame = frame_data['frame']

                # Analyze content
                code_result = self._detect_code_presence(frame, enable_ocr)
                diagram_result = self._detect_diagrams_slides(frame)

                # Calculate priority score
                priority = max(
                    code_result['score'],
                    diagram_result['score'],
                    frame_data.get('scene_change_score', 0) * 0.5  # Scene changes are less important
                )

                # Combine reasons
                reasons = []
                if code_result['has_code']:
                    reasons.extend(code_result['reasons'])
                if diagram_result['has_diagram_slide']:
                    reasons.extend(diagram_result['reasons'])
                if frame_data.get('scene_change_score', 0) > 0.5:
                    reasons.append('major_scene_change')

                # Select frame if it meets criteria
                if priority >= 0.4 or len(reasons) >= 2:  # Lower threshold or multiple indicators
                    frame_data['code_score'] = code_result['score']
                    frame_data['diagram_score'] = diagram_result['score']
                    frame_data['priority'] = priority
                    frame_data['reasons'] = reasons
                    frame_data['has_code'] = code_result['has_code']
                    frame_data['has_diagram'] = diagram_result['has_diagram_slide']

                    selected.append(frame_data)

                    pbar.set_postfix({"selected": len(selected)}, refresh=False)

                pbar.update(1)

        return selected

    def _detect_code_presence(self, frame: np.ndarray, enable_ocr: bool = True) -> Dict:
        """
        Detect if frame likely contains code using visual heuristics

        Args:
            frame: Video frame (BGR image)
            enable_ocr: Enable OCR-based text analysis (slower)

        Returns:
            Dict with score, reasons, and has_code boolean
        """
        score = 0.0
        reasons = []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Heuristic 1: Dark background (common for code editors)
        avg_brightness = np.mean(gray)
        if avg_brightness < 80:  # Dark background
            score += 0.3
            reasons.append('dark_background')

        # Heuristic 2: High contrast text (monospace fonts)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.count_nonzero(edges) / edges.size
        if 0.05 < edge_density < 0.3:  # Moderate edge density (text but not cluttered)
            score += 0.2
            reasons.append('text_pattern')

        # Heuristic 3: Rectangular regions (code editor windows)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large_rects = [c for c in contours if cv2.contourArea(c) > 10000]
        if len(large_rects) >= 1:
            score += 0.2
            reasons.append('editor_window')

        # Heuristic 4: OCR-based keyword detection (if enabled)
        if enable_ocr:
            try:
                import pytesseract
                text = pytesseract.image_to_string(gray, config='--psm 6')

                # Code keywords
                code_keywords = [
                    'def ', 'class ', 'import ', 'function', 'const ', 'let ', 'var ',
                    'return', 'if ', 'for ', 'while ', 'public ', 'private ', 'void ',
                    'int ', 'string ', 'async ', 'await ', 'SELECT ', 'FROM ', 'WHERE '
                ]
                keyword_count = sum(1 for kw in code_keywords if kw.lower() in text.lower())

                if keyword_count >= 2:
                    score += 0.4
                    reasons.append(f'{keyword_count}_code_keywords')

                # Special characters common in code
                import re
                special_chars = re.findall(r'[{}()\[\];:=<>]', text)
                if len(special_chars) >= 5:
                    score += 0.2
                    reasons.append('code_symbols')

            except ImportError:
                pass  # pytesseract not available
            except Exception:
                pass  # OCR failed

        return {
            'score': min(score, 1.0),
            'reasons': reasons,
            'has_code': score >= self.code_score_threshold
        }

    def _detect_diagrams_slides(self, frame: np.ndarray) -> Dict:
        """
        Detect diagrams and presentation slides using edge detection

        Args:
            frame: Video frame (BGR image)

        Returns:
            Dict with score, reasons, and has_diagram_slide boolean
        """
        score = 0.0
        reasons = []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Detect geometric shapes (diagrams)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Count rectangles and polygons (boxes in diagrams)
        rectangles = []
        for c in contours:
            perimeter = cv2.arcLength(c, True)
            if perimeter < 100:  # Skip very small contours
                continue
            approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
            if len(approx) >= 4:  # Rectangles or polygons
                rectangles.append(c)

        if len(rectangles) >= 3:
            score += 0.4
            reasons.append(f'{len(rectangles)}_shapes')

        # Detect lines (arrows/connections in diagrams)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
        if lines is not None and len(lines) >= 5:
            score += 0.3
            reasons.append(f'{len(lines)}_lines')

        # Detect text regions (slides often have text)
        # Simple heuristic: check if there's organized text (not too dense)
        edge_density = np.count_nonzero(edges) / edges.size
        if 0.02 < edge_density < 0.15:  # Moderate density suggests organized content
            score += 0.2
            reasons.append('organized_content')

        # Check for high contrast (slides often have clear text on background)
        avg_brightness = np.mean(gray)
        std_brightness = np.std(gray)
        if std_brightness > 60 and (avg_brightness > 150 or avg_brightness < 80):
            score += 0.2
            reasons.append('high_contrast_slide')

        return {
            'score': min(score, 1.0),
            'reasons': reasons,
            'has_diagram_slide': score >= self.diagram_score_threshold
        }

    def _save_frames(self, frames: List[Dict], metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Save selected frames to disk

        Args:
            frames: List of frame dicts with frame data
            metadata: Optional video metadata

        Returns:
            List of saved frame info dicts
        """
        saved_frames = []

        for frame_data in frames:
            timestamp = frame_data['timestamp']
            frame_filename = f"frame_{int(timestamp):06d}s.jpg"
            frame_path = self.output_dir / frame_filename

            # Save frame
            cv2.imwrite(str(frame_path), frame_data['frame'], [cv2.IMWRITE_JPEG_QUALITY, 85])

            # Create frame info (without the actual frame data)
            saved_info = {
                'path': str(frame_path),
                'filename': frame_filename,
                'timestamp': timestamp,
                'frame_number': frame_data['frame_number'],
                'time_formatted': frame_data['time_formatted'],
                'priority': frame_data.get('priority', 0),
                'code_score': frame_data.get('code_score', 0),
                'diagram_score': frame_data.get('diagram_score', 0),
                'scene_change_score': frame_data.get('scene_change_score', 0),
                'reasons': frame_data.get('reasons', []),
                'has_code': frame_data.get('has_code', False),
                'has_diagram': frame_data.get('has_diagram', False)
            }

            saved_frames.append(saved_info)

        # Save frame index
        self._save_frame_index(saved_frames, metadata)

        return saved_frames

    def _save_frame_index(self, frames: List[Dict], metadata: Optional[Dict] = None):
        """Save frame index with selection metadata"""
        index_path = self.output_dir / "frame_index.json"

        # Calculate statistics
        total_frames = len(frames)
        frames_with_code = sum(1 for f in frames if f.get('has_code', False))
        frames_with_diagrams = sum(1 for f in frames if f.get('has_diagram', False))
        avg_priority = sum(f.get('priority', 0) for f in frames) / max(total_frames, 1)

        index_data = {
            'selected_at': datetime.now().isoformat(),
            'selection_method': 'smart_selection',
            'total_frames': total_frames,
            'frames_with_code': frames_with_code,
            'frames_with_diagrams': frames_with_diagrams,
            'average_priority': avg_priority,
            'metadata': metadata or {},
            'frames': frames
        }

        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)

        print(f"[OK] Frame index saved: {index_path}")

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


def main():
    """CLI interface for smart frame selection"""
    import argparse

    parser = argparse.ArgumentParser(description='Smart frame selection with scene detection and content analysis')
    parser.add_argument('video_path', help='Path to video file')
    parser.add_argument('--output', default='smart_frames',
                       help='Output directory for selected frames (default: smart_frames)')
    parser.add_argument('--no-ocr', action='store_true',
                       help='Disable OCR-based code detection (faster but less accurate)')
    parser.add_argument('--scene-threshold', type=float, default=0.70,
                       help='Scene change correlation threshold 0-1 (default: 0.70)')

    args = parser.parse_args()

    selector = SmartFrameSelector(output_dir=args.output)
    selector.scene_change_threshold = args.scene_threshold

    frames = selector.select_frames(
        video_path=args.video_path,
        enable_ocr=not args.no_ocr
    )

    print(f"\n✓ Smart selection complete")
    print(f"✓ Selected {len(frames)} frames")
    print(f"✓ Frames saved to: {args.output}/")
    print(f"✓ Frame index: {args.output}/frame_index.json")


if __name__ == "__main__":
    main()
