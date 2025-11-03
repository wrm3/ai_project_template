#!/usr/bin/env python3
"""
Test script for frame extraction functionality
Tests frame_extractor.py and vision_analyzer.py modules
"""

import os
import sys
from pathlib import Path

def test_frame_extractor():
    """Test FrameExtractor class"""
    print("=" * 80)
    print("TEST: Frame Extractor")
    print("=" * 80)
    print()

    try:
        from frame_extractor import FrameExtractor
        print("✓ Successfully imported FrameExtractor")

        # Check if test video exists
        test_video = "output/video.mp4"
        if not os.path.exists(test_video):
            print(f"⚠ Test video not found: {test_video}")
            print("  Run analyze_video.py first to download a test video")
            return False

        # Create test extractor
        extractor = FrameExtractor(output_dir="test_frames", interval_seconds=60)
        print("✓ Created FrameExtractor instance")

        # Test extraction (just first 60s to keep it fast)
        print("\nExtracting test frames...")
        frames = extractor.extract_frames(test_video)
        print(f"✓ Extracted {len(frames)} frames")

        if len(frames) > 0:
            print(f"✓ First frame: {frames[0]}")
            return True
        else:
            print("✗ No frames extracted")
            return False

    except ImportError as e:
        print(f"✗ Failed to import FrameExtractor: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during frame extraction: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vision_analyzer():
    """Test VisionAnalyzer class"""
    print()
    print("=" * 80)
    print("TEST: Vision Analyzer")
    print("=" * 80)
    print()

    try:
        from vision_analyzer import VisionAnalyzer
        print("✓ Successfully imported VisionAnalyzer")

        # Create test analyzer
        analyzer = VisionAnalyzer(output_dir="test_vision")
        print("✓ Created VisionAnalyzer instance")

        # Test with mock frame data
        mock_frames = [
            {
                'path': 'test_frames/frame_000000s.jpg',
                'filename': 'frame_000000s.jpg',
                'timestamp': 0.0,
                'frame_number': 0,
                'time_formatted': '00:00'
            },
            {
                'path': 'test_frames/frame_000060s.jpg',
                'filename': 'frame_000060s.jpg',
                'timestamp': 60.0,
                'frame_number': 1800,
                'time_formatted': '01:00'
            }
        ]

        print("\nPreparing vision analysis prompts...")
        prompts = analyzer.prepare_frame_analysis_prompts(mock_frames)
        print(f"✓ Prepared {len(prompts)} prompts")

        if len(prompts) == 2:
            print("✓ Correct number of prompts generated")
            return True
        else:
            print(f"✗ Expected 2 prompts, got {len(prompts)}")
            return False

    except ImportError as e:
        print(f"✗ Failed to import VisionAnalyzer: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during vision analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_opencv_installation():
    """Test if OpenCV is properly installed"""
    print()
    print("=" * 80)
    print("TEST: OpenCV Installation")
    print("=" * 80)
    print()

    try:
        import cv2
        print(f"✓ OpenCV installed: version {cv2.__version__}")
        return True
    except ImportError:
        print("✗ OpenCV not installed")
        print("  Install with: pip install opencv-python>=4.8.0")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("█" * 80)
    print("  FRAME EXTRACTION TEST SUITE")
    print("█" * 80)
    print()

    results = {}

    # Test 1: OpenCV installation
    results['opencv'] = test_opencv_installation()

    # Test 2: Frame extractor module
    results['frame_extractor'] = test_frame_extractor()

    # Test 3: Vision analyzer module
    results['vision_analyzer'] = test_vision_analyzer()

    # Summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}  {test_name}")

    print()

    all_passed = all(results.values())
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
