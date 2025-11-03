#!/usr/bin/env python3
"""
Vision Analysis Module for YouTube Video Analysis
Analyzes extracted frames using Claude vision capabilities to extract code, diagrams, and text

Part of Task 044-1: Frame Extraction + Vision Analysis Implementation
"""

import os
import json
import base64
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class VisionAnalyzer:
    """Analyze video frames using Claude vision to extract code, diagrams, and text"""

    def __init__(self, output_dir: str = "vision_results"):
        """
        Initialize vision analyzer

        Args:
            output_dir: Directory to save analysis results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_frame_analysis_prompts(self, frames: List[Dict], transcript_data: Optional[Dict] = None) -> List[Dict]:
        """
        Prepare vision analysis prompts for Claude Code

        This creates structured prompts that Claude Code will execute using its native vision capabilities.

        Args:
            frames: List of frame info dicts from FrameExtractor
            transcript_data: Optional transcript with segments for context

        Returns:
            List of analysis prompt dicts ready for Claude Code vision
        """
        print("=" * 80)
        print("PREPARING VISION ANALYSIS PROMPTS")
        print("=" * 80)
        print()

        prompts = []

        for i, frame in enumerate(frames):
            # Get transcript context if available
            context = self._get_transcript_context(transcript_data, frame['timestamp']) if transcript_data else None

            prompt_data = {
                'frame_number': i + 1,
                'frame_path': frame['path'],
                'timestamp': frame['timestamp'],
                'time_formatted': frame['time_formatted'],
                'transcript_context': context,
                'prompt': self._build_vision_prompt(frame, context)
            }

            prompts.append(prompt_data)

            print(f"Frame {i+1}/{len(frames)}: {frame['time_formatted']} - {frame['filename']}")

        print(f"\n[OK] Prepared {len(prompts)} vision analysis prompts")
        print()

        # Save prompts for reference
        self._save_prompts(prompts)

        return prompts

    def _build_vision_prompt(self, frame: Dict, context: Optional[str]) -> str:
        """Build comprehensive vision analysis prompt"""
        prompt = f"""Analyze this video frame from timestamp {frame['time_formatted']} ({frame['timestamp']}s).

CONTEXT FROM TRANSCRIPT:
{context if context else "No transcript context available"}

EXTRACT THE FOLLOWING (if present in the frame):

1. CODE SNIPPETS:
   - Identify programming language
   - Extract complete code blocks
   - Note any syntax highlighting or comments
   - Describe what the code does

2. DIAGRAMS & ARCHITECTURE:
   - Describe any architecture diagrams, flowcharts, or visualizations
   - Identify components, services, or data flows
   - Note relationships and connections
   - Extract any labels or annotations

3. TEXT CONTENT:
   - Extract text from slides, presentations, or UI elements
   - Note headings, bullet points, or key phrases
   - Capture any URLs, file paths, or technical terms
   - Identify speaker notes or captions if visible

4. UI/TOOL SCREENSHOTS:
   - Identify any IDE, terminal, browser, or tool interfaces
   - Note file structures, folder hierarchies, or navigation
   - Capture command-line commands or tool settings
   - Describe what action is being demonstrated

5. KEY VISUAL ELEMENTS:
   - Highlight important visual cues (arrows, circles, annotations)
   - Note any error messages, warnings, or alerts
   - Identify charts, graphs, or data visualizations

OUTPUT FORMAT (JSON):
{{
  "timestamp": {frame['timestamp']},
  "time_formatted": "{frame['time_formatted']}",
  "has_code": true/false,
  "code_snippets": [
    {{
      "language": "python/javascript/sql/etc",
      "code": "actual code here",
      "description": "what this code does",
      "line_count": number
    }}
  ],
  "has_diagram": true/false,
  "diagrams": [
    {{
      "type": "architecture/flowchart/sequence/etc",
      "description": "detailed description of diagram",
      "components": ["component1", "component2"],
      "relationships": "how components connect"
    }}
  ],
  "text_content": {{
    "headings": ["heading1", "heading2"],
    "bullet_points": ["point1", "point2"],
    "key_phrases": ["phrase1", "phrase2"],
    "urls": ["url1", "url2"],
    "file_paths": ["path1", "path2"]
  }},
  "ui_elements": {{
    "tool_name": "VSCode/Terminal/Browser/etc",
    "visible_files": ["file1.py", "file2.js"],
    "commands": ["command1", "command2"],
    "action_description": "what is being demonstrated"
  }},
  "visual_annotations": {{
    "has_annotations": true/false,
    "annotation_types": ["arrow", "circle", "highlight"],
    "description": "what the annotations emphasize"
  }},
  "importance_score": 1-10,
  "summary": "brief summary of frame content and significance"
}}

Provide detailed, accurate extraction. If elements are not present, mark as false/empty but still include the fields."""

        return prompt

    def _get_transcript_context(self, transcript_data: Optional[Dict], timestamp: float, window: int = 30) -> str:
        """
        Get transcript context around a timestamp

        Args:
            transcript_data: Transcript data with segments
            timestamp: Frame timestamp in seconds
            window: Context window in seconds (±window around timestamp)

        Returns:
            Relevant transcript text or None
        """
        if not transcript_data or 'segments' not in transcript_data:
            return None

        context_segments = []

        for segment in transcript_data['segments']:
            segment_start = segment.get('start', 0)
            segment_end = segment.get('end', 0)

            # Check if segment overlaps with our window
            if (segment_start <= timestamp + window and
                segment_end >= timestamp - window):
                context_segments.append(segment['text'].strip())

        if context_segments:
            return " ".join(context_segments)

        return None

    def analyze_frame_batch(self, prompts: List[Dict], batch_size: int = 10) -> List[Dict]:
        """
        Prepare frames for batch vision analysis

        Note: This prepares prompts for Claude Code to execute.
        Actual vision analysis happens through Claude Code's native capabilities.

        Args:
            prompts: List of prompt dicts from prepare_frame_analysis_prompts
            batch_size: Number of frames to process per batch

        Returns:
            List of prepared batches
        """
        print("=" * 80)
        print("PREPARING VISION ANALYSIS BATCHES")
        print("=" * 80)
        print()

        batches = []
        total_prompts = len(prompts)

        for i in range(0, total_prompts, batch_size):
            batch = prompts[i:i + batch_size]
            batches.append({
                'batch_number': (i // batch_size) + 1,
                'frames': batch,
                'frame_count': len(batch)
            })

        print(f"Prepared {len(batches)} batches ({batch_size} frames per batch)")
        print(f"Total frames: {total_prompts}")
        print()

        return batches

    def save_analysis_results(self, results: List[Dict], video_metadata: Optional[Dict] = None):
        """
        Save vision analysis results to JSON file

        Args:
            results: List of analysis result dicts
            video_metadata: Optional video metadata
        """
        output_path = self.output_dir / "vision_analysis_results.json"

        output_data = {
            'analyzed_at': datetime.now().isoformat(),
            'video_metadata': video_metadata or {},
            'total_frames_analyzed': len(results),
            'frames_with_code': sum(1 for r in results if r.get('has_code', False)),
            'frames_with_diagrams': sum(1 for r in results if r.get('has_diagram', False)),
            'results': results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)

        print(f"\n[OK] Vision analysis results saved: {output_path}")
        print(f"    Total frames: {len(results)}")
        print(f"    Frames with code: {output_data['frames_with_code']}")
        print(f"    Frames with diagrams: {output_data['frames_with_diagrams']}")

    def generate_analysis_summary(self, results: List[Dict]) -> Dict:
        """
        Generate summary statistics from vision analysis results

        Args:
            results: List of analysis result dicts

        Returns:
            Summary statistics dict
        """
        summary = {
            'total_frames': len(results),
            'frames_with_code': 0,
            'frames_with_diagrams': 0,
            'programming_languages': set(),
            'diagram_types': set(),
            'code_snippet_count': 0,
            'important_frames': [],  # importance_score >= 7
            'key_topics': []
        }

        for result in results:
            if result.get('has_code', False):
                summary['frames_with_code'] += 1
                for snippet in result.get('code_snippets', []):
                    summary['code_snippet_count'] += 1
                    if 'language' in snippet:
                        summary['programming_languages'].add(snippet['language'])

            if result.get('has_diagram', False):
                summary['frames_with_diagrams'] += 1
                for diagram in result.get('diagrams', []):
                    if 'type' in diagram:
                        summary['diagram_types'].add(diagram['type'])

            if result.get('importance_score', 0) >= 7:
                summary['important_frames'].append({
                    'timestamp': result['timestamp'],
                    'time_formatted': result['time_formatted'],
                    'importance': result['importance_score'],
                    'summary': result.get('summary', '')
                })

        # Convert sets to sorted lists for JSON serialization
        summary['programming_languages'] = sorted(list(summary['programming_languages']))
        summary['diagram_types'] = sorted(list(summary['diagram_types']))

        return summary

    def _save_prompts(self, prompts: List[Dict]):
        """Save prepared prompts for reference"""
        prompts_path = self.output_dir / "vision_prompts.json"

        with open(prompts_path, 'w', encoding='utf-8') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_prompts': len(prompts),
                'prompts': prompts
            }, f, indent=2)

        print(f"[OK] Prompts saved: {prompts_path}")

    def create_claude_code_workflow(self, frames: List[Dict], output_file: str = "vision_workflow.md"):
        """
        Create a workflow markdown file for Claude Code to execute vision analysis

        This generates instructions that Claude Code can follow to analyze all frames.

        Args:
            frames: List of frame info dicts
            output_file: Name of output workflow file
        """
        workflow_path = self.output_dir / output_file

        workflow = f"""# Vision Analysis Workflow for Claude Code

This workflow guides Claude Code through analyzing {len(frames)} extracted video frames.

## Instructions for Claude Code

For each frame below, please:
1. Open the image file using your native capabilities
2. Analyze the visual content following the structured prompt
3. Extract code snippets, diagrams, text, and UI elements
4. Save your analysis in JSON format

## Frames to Analyze

"""

        for i, frame in enumerate(frames):
            workflow += f"""
### Frame {i+1}/{len(frames)} - {frame['time_formatted']}

**File**: `{frame['path']}`
**Timestamp**: {frame['timestamp']}s
**Frame Number**: {frame['frame_number']}

**Analysis Instructions**:
- Look for code snippets (identify language, extract code)
- Describe any diagrams, architecture, or flowcharts
- Extract text from slides, UI elements, or captions
- Note important visual annotations or highlights
- Rate importance (1-10) based on technical content

**Save Result As**: `vision_results/frame_{i+1:03d}_analysis.json`

---
"""

        workflow += f"""
## After Analysis

Once all frames are analyzed:
1. Combine all individual JSON results
2. Generate summary statistics (total code snippets, languages found, diagram types)
3. Identify most important frames (importance >= 7)
4. Save consolidated results to `vision_results/vision_analysis_results.json`

## Expected Output Format

Each frame analysis should be a JSON file with this structure:
```json
{{
  "timestamp": 123.5,
  "time_formatted": "02:03",
  "has_code": true,
  "code_snippets": [...],
  "has_diagram": true,
  "diagrams": [...],
  "text_content": {{}},
  "ui_elements": {{}},
  "visual_annotations": {{}},
  "importance_score": 8,
  "summary": "Brief description"
}}
```
"""

        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow)

        print(f"\n[OK] Vision analysis workflow created: {workflow_path}")
        print(f"    Claude Code can use this file to systematically analyze all {len(frames)} frames")


def main():
    """CLI interface for vision analysis preparation"""
    import argparse

    parser = argparse.ArgumentParser(description='Prepare frames for Claude vision analysis')
    parser.add_argument('--frames-dir', default='frames',
                       help='Directory containing extracted frames')
    parser.add_argument('--output-dir', default='vision_results',
                       help='Output directory for analysis results')
    parser.add_argument('--transcript', help='Path to transcript JSON file (optional)')
    parser.add_argument('--create-workflow', action='store_true',
                       help='Create Claude Code workflow markdown file')

    args = parser.parse_args()

    # Load frame index
    frame_index_path = Path(args.frames_dir) / 'frame_index.json'
    if not frame_index_path.exists():
        print(f"Error: Frame index not found: {frame_index_path}")
        print("Run frame_extractor.py first to extract frames.")
        return 1

    with open(frame_index_path, 'r', encoding='utf-8') as f:
        frame_data = json.load(f)

    frames = frame_data['frames']

    # Load transcript if provided
    transcript_data = None
    if args.transcript:
        with open(args.transcript, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)

    # Initialize analyzer
    analyzer = VisionAnalyzer(output_dir=args.output_dir)

    # Prepare prompts
    prompts = analyzer.prepare_frame_analysis_prompts(frames, transcript_data)

    # Create workflow for Claude Code
    if args.create_workflow:
        analyzer.create_claude_code_workflow(frames)

    print(f"\n✓ Vision analysis preparation complete")
    print(f"✓ {len(prompts)} prompts prepared")
    print(f"✓ Results will be saved to: {args.output_dir}/")
    print(f"\nNext step: Use Claude Code to analyze the prepared frames")


if __name__ == "__main__":
    main()
