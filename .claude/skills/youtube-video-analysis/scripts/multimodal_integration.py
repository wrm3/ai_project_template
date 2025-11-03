#!/usr/bin/env python3
"""
Multi-Modal Integration Module for YouTube Video Analysis
Combines visual analysis (frames) and transcript analysis into unified comprehensive output

Part of Task 044-3: Multi-Modal Integration
Aligns frame timestamps with transcript segments, merges insights, identifies gaps, and generates comprehensive outputs
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
from tqdm import tqdm


class MultiModalIntegrator:
    """
    Integrate visual (frame) and audio (transcript) analysis into comprehensive multi-modal output
    """

    def __init__(self, output_dir: str = "multimodal_output"):
        """
        Initialize multi-modal integrator

        Args:
            output_dir: Directory to save integrated analysis results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Configuration
        self.alignment_window = 30  # ±30 seconds for transcript alignment
        self.avg_words_per_second = 150 / 60  # ~2.5 words/second (150 WPM)

    def align_frames_with_transcript(
        self,
        frames: List[Dict],
        transcript: str,
        window_seconds: int = 30
    ) -> List[Dict]:
        """
        Align extracted frames with transcript segments

        For each frame, find transcript text within ±window_seconds window

        Args:
            frames: List of frame dicts from frame extractor
            transcript: Full video transcript (plain text or with timing)
            window_seconds: Time window in seconds (default: 30)

        Returns:
            List of aligned data: [{timestamp, frame_data, transcript_segment}]
        """
        print("=" * 80)
        print("TIMESTAMP ALIGNMENT")
        print("=" * 80)
        print()

        print(f"Aligning {len(frames)} frames with transcript...")
        print(f"Alignment window: ±{window_seconds} seconds")
        print()

        aligned_data = []

        # Get total transcript duration (estimate from last frame)
        total_duration = frames[-1]['timestamp'] if frames else 0

        # Create progress bar for alignment
        with tqdm(total=len(frames), desc="Aligning timestamps", unit="frame") as pbar:
            for i, frame_data in enumerate(frames):
                timestamp = frame_data['timestamp']

                # Extract transcript segment for this time window
                transcript_segment = self._extract_transcript_segment(
                    transcript,
                    start_time=max(0, timestamp - window_seconds),
                    end_time=min(total_duration, timestamp + window_seconds),
                    total_duration=total_duration
                )

                aligned_item = {
                    'timestamp': timestamp,
                    'frame': {
                        'path': frame_data['path'],
                        'filename': frame_data['filename'],
                        'frame_number': frame_data['frame_number'],
                        'time_formatted': frame_data['time_formatted'],
                        'code_score': frame_data.get('code_score', 0),
                        'diagram_score': frame_data.get('diagram_score', 0),
                        'scene_change_score': frame_data.get('scene_change_score', 0),
                        'reasons': frame_data.get('reasons', []),
                        'has_code': frame_data.get('has_code', False),
                        'has_diagram': frame_data.get('has_diagram', False),
                        'priority': frame_data.get('priority', 0)
                    },
                    'transcript': transcript_segment
                }

                aligned_data.append(aligned_item)
                pbar.update(1)

        print(f"\n\n[OK] Aligned {len(aligned_data)} frames with transcript segments")
        print()

        return aligned_data

    def _extract_transcript_segment(
        self,
        transcript: str,
        start_time: float,
        end_time: float,
        total_duration: float
    ) -> Dict:
        """
        Extract transcript text for a time range

        Uses word-based estimation for plain text transcripts

        Args:
            transcript: Full transcript text
            start_time: Start time in seconds
            end_time: End time in seconds
            total_duration: Total video duration in seconds

        Returns:
            Dict with text, start, end, word_count
        """
        words = transcript.split()
        total_words = len(words)

        if total_words == 0:
            return {
                'text': '',
                'start': start_time,
                'end': end_time,
                'word_count': 0
            }

        # Calculate word positions based on time
        # Assume uniform word distribution across video duration
        words_per_second = total_words / total_duration if total_duration > 0 else 0

        start_word_idx = int(start_time * words_per_second)
        end_word_idx = int(end_time * words_per_second)

        # Ensure indices are within bounds
        start_word_idx = max(0, min(start_word_idx, total_words))
        end_word_idx = max(0, min(end_word_idx, total_words))

        segment_words = words[start_word_idx:end_word_idx]

        return {
            'text': ' '.join(segment_words),
            'start': start_time,
            'end': end_time,
            'word_count': len(segment_words)
        }

    def merge_multimodal_insights(
        self,
        aligned_data: List[Dict],
        video_metadata: Dict
    ) -> Dict:
        """
        Merge visual and audio insights into comprehensive analysis

        Args:
            aligned_data: List of aligned frame + transcript segments
            video_metadata: Video metadata (title, duration, etc.)

        Returns:
            Comprehensive analysis dict with merged segments, summary, statistics, gaps
        """
        print("=" * 80)
        print("MULTI-MODAL INSIGHT MERGER")
        print("=" * 80)
        print()

        print(f"Merging {len(aligned_data)} segments...")
        print()

        merged_segments = []

        # Create progress bar for merging
        with tqdm(total=len(aligned_data), desc="Merging insights", unit="segment") as pbar:
            for item in aligned_data:
                timestamp = item['timestamp']
                frame_data = item['frame']
                transcript_data = item['transcript']

                # Determine segment type based on visual + audio content
                segment_type = self._determine_segment_type(frame_data, transcript_data)

                # Generate insights about alignment
                insights = self._generate_segment_insights(frame_data, transcript_data)

                # Create merged segment
                segment = {
                    'timestamp': timestamp,
                    'timestamp_formatted': frame_data['time_formatted'],
                    'type': segment_type,
                    'visual_content': {
                        'has_code': frame_data['has_code'],
                        'has_diagram': frame_data['has_diagram'],
                        'code_score': frame_data['code_score'],
                        'diagram_score': frame_data['diagram_score'],
                        'frame_path': frame_data['path'],
                        'detection_reasons': frame_data['reasons'],
                        'priority': frame_data['priority']
                    },
                    'audio_content': {
                        'text': transcript_data['text'],
                        'word_count': transcript_data['word_count'],
                        'time_window': f"{transcript_data['start']:.1f}s - {transcript_data['end']:.1f}s"
                    },
                    'insights': insights,
                    'alignment_quality': self._assess_alignment_quality(frame_data, transcript_data)
                }

                merged_segments.append(segment)
                pbar.update(1)

        # Generate comprehensive analysis
        print("Generating comprehensive analysis...")

        comprehensive_analysis = {
            'video_metadata': video_metadata,
            'analysis_metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_segments': len(merged_segments),
                'alignment_window': self.alignment_window
            },
            'segments': merged_segments,
            'summary': self._generate_multimodal_summary(merged_segments, video_metadata),
            'statistics': self._calculate_multimodal_stats(merged_segments),
            'gaps': self._identify_gaps(merged_segments)
        }

        print(f"[OK] Multi-modal analysis complete")
        print(f"    Total segments: {len(merged_segments)}")
        print(f"    Code segments: {comprehensive_analysis['statistics']['code_segments']}")
        print(f"    Diagram segments: {comprehensive_analysis['statistics']['diagram_segments']}")
        print(f"    Gaps identified: {comprehensive_analysis['statistics']['gaps_count']}")
        print()

        return comprehensive_analysis

    def _determine_segment_type(self, frame_data: Dict, transcript_data: Dict) -> str:
        """
        Classify segment based on visual and audio content

        Args:
            frame_data: Frame analysis data
            transcript_data: Transcript segment data

        Returns:
            Segment type string
        """
        has_code = frame_data['has_code']
        has_diagram = frame_data['has_diagram']
        has_substantial_text = transcript_data['word_count'] > 20
        has_some_text = transcript_data['word_count'] > 5

        # Check for technical keywords in transcript
        transcript_lower = transcript_data['text'].lower()
        has_code_keywords = any(kw in transcript_lower for kw in [
            'code', 'function', 'method', 'class', 'variable', 'programming',
            'implement', 'algorithm', 'syntax'
        ])
        has_architecture_keywords = any(kw in transcript_lower for kw in [
            'architecture', 'diagram', 'system', 'component', 'service',
            'design', 'structure', 'flow'
        ])

        # Classify based on combinations
        if has_code and has_substantial_text and has_code_keywords:
            return 'code_explanation'
        elif has_diagram and has_substantial_text and has_architecture_keywords:
            return 'architecture_overview'
        elif has_code and not has_some_text:
            return 'code_only'
        elif has_diagram and not has_some_text:
            return 'diagram_only'
        elif has_substantial_text and not (has_code or has_diagram):
            return 'spoken_only'
        elif has_code and has_substantial_text:
            return 'code_with_discussion'
        elif has_diagram and has_substantial_text:
            return 'diagram_with_discussion'
        else:
            return 'general'

    def _generate_segment_insights(self, frame_data: Dict, transcript_data: Dict) -> List[str]:
        """
        Generate insights about what's shown vs what's said

        Args:
            frame_data: Frame analysis data
            transcript_data: Transcript segment data

        Returns:
            List of insight strings
        """
        insights = []
        transcript_lower = transcript_data['text'].lower()

        # Positive alignments
        if frame_data['has_code'] and transcript_data['word_count'] > 20:
            insights.append("✅ Code shown on screen with spoken explanation")

        if frame_data['has_diagram'] and transcript_data['word_count'] > 20:
            insights.append("✅ Visual diagram with accompanying narration")

        # Check for specific technical content
        if 'python' in transcript_lower and frame_data['has_code']:
            insights.append("🐍 Python code segment")
        elif 'javascript' in transcript_lower and frame_data['has_code']:
            insights.append("📜 JavaScript code segment")
        elif 'sql' in transcript_lower and frame_data['has_code']:
            insights.append("🗄️ SQL code segment")

        # Gaps and warnings
        if frame_data['has_code'] and transcript_data['word_count'] < 10:
            insights.append("⚠️ Code shown but minimal verbal explanation")

        if frame_data['has_diagram'] and transcript_data['word_count'] < 10:
            insights.append("⚠️ Diagram shown but not explained verbally")

        # Check for code discussion without visual
        code_keywords = ['code', 'function', 'implement', 'programming', 'syntax']
        if any(kw in transcript_lower for kw in code_keywords) and frame_data['code_score'] < 0.3:
            insights.append("⚠️ Code concepts discussed but not shown visually")

        # Check for architecture discussion without visual
        arch_keywords = ['architecture', 'diagram', 'system', 'component']
        if any(kw in transcript_lower for kw in arch_keywords) and frame_data['diagram_score'] < 0.3:
            insights.append("⚠️ Architecture discussed but no diagram shown")

        # High priority content
        if frame_data['priority'] >= 0.7:
            insights.append("🎯 High priority visual content")

        return insights

    def _assess_alignment_quality(self, frame_data: Dict, transcript_data: Dict) -> str:
        """
        Assess how well visual and audio content are aligned

        Args:
            frame_data: Frame analysis data
            transcript_data: Transcript segment data

        Returns:
            Quality rating: 'excellent', 'good', 'fair', 'poor'
        """
        score = 0
        transcript_lower = transcript_data['text'].lower()

        # Score alignment indicators
        if frame_data['has_code'] and any(kw in transcript_lower for kw in ['code', 'function', 'implement']):
            score += 3
        if frame_data['has_diagram'] and any(kw in transcript_lower for kw in ['diagram', 'architecture', 'system']):
            score += 3
        if transcript_data['word_count'] > 30:
            score += 2
        if frame_data['priority'] >= 0.5:
            score += 1

        # Penalize misalignments
        if frame_data['has_code'] and transcript_data['word_count'] < 10:
            score -= 2
        if transcript_data['word_count'] > 50 and not (frame_data['has_code'] or frame_data['has_diagram']):
            score -= 1

        # Convert to quality rating
        if score >= 6:
            return 'excellent'
        elif score >= 4:
            return 'good'
        elif score >= 2:
            return 'fair'
        else:
            return 'poor'

    def _generate_multimodal_summary(self, segments: List[Dict], video_metadata: Dict) -> str:
        """
        Generate high-level summary of multi-modal analysis

        Args:
            segments: List of merged segments
            video_metadata: Video metadata

        Returns:
            Summary text
        """
        total = len(segments)
        code_segments = sum(1 for s in segments if s['visual_content']['has_code'])
        diagram_segments = sum(1 for s in segments if s['visual_content']['has_diagram'])

        well_aligned = sum(1 for s in segments if s['alignment_quality'] in ['excellent', 'good'])
        alignment_pct = (well_aligned / total * 100) if total > 0 else 0

        summary = f"""This multi-modal analysis combines visual frame analysis with transcript narration for the video "{video_metadata.get('title', 'Unknown')}".

Analyzed {total} key moments across {video_metadata.get('duration', 0) // 60} minutes:
- {code_segments} segments contain code snippets ({code_segments / total * 100:.1f}%)
- {diagram_segments} segments show diagrams or architecture ({diagram_segments / total * 100:.1f}%)
- {well_aligned} segments demonstrate excellent visual-audio alignment ({alignment_pct:.1f}%)

The analysis identifies where visual content (code, diagrams) aligns with spoken explanations, as well as gaps where content is shown but not explained or discussed but not visualized.
"""
        return summary

    def _calculate_multimodal_stats(self, segments: List[Dict]) -> Dict:
        """
        Calculate comprehensive statistics across all segments

        Args:
            segments: List of merged segments

        Returns:
            Statistics dict
        """
        stats = {
            'total_segments': len(segments),
            'code_segments': 0,
            'diagram_segments': 0,
            'code_and_diagram': 0,
            'spoken_only': 0,
            'visual_only': 0,
            'well_aligned': 0,
            'gaps_count': 0,
            'avg_alignment_quality': 0,
            'segment_types': {},
            'alignment_distribution': {
                'excellent': 0,
                'good': 0,
                'fair': 0,
                'poor': 0
            }
        }

        total_quality_score = 0

        for segment in segments:
            # Count segment types
            seg_type = segment['type']
            stats['segment_types'][seg_type] = stats['segment_types'].get(seg_type, 0) + 1

            # Count content types
            if segment['visual_content']['has_code']:
                stats['code_segments'] += 1
            if segment['visual_content']['has_diagram']:
                stats['diagram_segments'] += 1
            if segment['visual_content']['has_code'] and segment['visual_content']['has_diagram']:
                stats['code_and_diagram'] += 1

            # Count alignment quality
            quality = segment['alignment_quality']
            stats['alignment_distribution'][quality] += 1

            # Map quality to score for average
            quality_scores = {'excellent': 4, 'good': 3, 'fair': 2, 'poor': 1}
            total_quality_score += quality_scores.get(quality, 0)

            if quality in ['excellent', 'good']:
                stats['well_aligned'] += 1

            # Count gaps (segments with warnings in insights)
            if any('⚠️' in insight for insight in segment['insights']):
                stats['gaps_count'] += 1

        # Calculate averages
        if stats['total_segments'] > 0:
            stats['avg_alignment_quality'] = total_quality_score / stats['total_segments']

        return stats

    def _identify_gaps(self, segments: List[Dict]) -> Dict:
        """
        Find discrepancies between visual and audio content

        Args:
            segments: List of merged segments

        Returns:
            Dict with visual_not_explained, explained_not_shown, misalignments lists
        """
        gaps = {
            'visual_not_explained': [],
            'explained_not_shown': [],
            'high_value_content': [],
            'recommendations': []
        }

        for segment in segments:
            timestamp = segment['timestamp_formatted']
            segment_type = segment['type']
            visual = segment['visual_content']
            audio = segment['audio_content']

            # Gap 1: Visual content without explanation
            if segment_type in ['code_only', 'diagram_only']:
                gap_entry = {
                    'timestamp': timestamp,
                    'content': 'Code shown on screen' if visual['has_code'] else 'Diagram shown on screen',
                    'suggestion': 'Consider adding verbal explanation of what is shown',
                    'priority': visual['priority']
                }
                gaps['visual_not_explained'].append(gap_entry)

            # Gap 2: Explained but not shown
            if segment_type == 'spoken_only':
                transcript_lower = audio['text'].lower()
                keywords = {
                    'code': ['code', 'function', 'implement', 'programming'],
                    'architecture': ['architecture', 'diagram', 'system', 'component']
                }

                for content_type, kws in keywords.items():
                    if any(kw in transcript_lower for kw in kws):
                        gap_entry = {
                            'timestamp': timestamp,
                            'content': f'{content_type.title()} concepts discussed',
                            'suggestion': f'Consider adding visual {content_type} example',
                            'transcript_excerpt': audio['text'][:100] + '...'
                        }
                        gaps['explained_not_shown'].append(gap_entry)
                        break

            # Identify high-value content for recommendations
            if visual['priority'] >= 0.7 and segment['alignment_quality'] == 'excellent':
                gaps['high_value_content'].append({
                    'timestamp': timestamp,
                    'type': segment_type,
                    'reason': 'High quality multi-modal segment worth highlighting',
                    'insights': segment['insights']
                })

        # Generate overall recommendations
        if len(gaps['visual_not_explained']) > len(segments) * 0.2:
            gaps['recommendations'].append(
                'Consider adding more verbal explanations for visual content (20%+ of frames lack narration)'
            )

        if len(gaps['explained_not_shown']) > len(segments) * 0.15:
            gaps['recommendations'].append(
                'Consider adding more visual examples for technical concepts (15%+ mentioned without visuals)'
            )

        if len(gaps['high_value_content']) > 5:
            gaps['recommendations'].append(
                f'Excellent multi-modal alignment found in {len(gaps["high_value_content"])} segments - these are reference quality'
            )

        return gaps

    def generate_multimodal_output(
        self,
        comprehensive_analysis: Dict,
        output_dir: Optional[Path] = None
    ) -> Dict[str, str]:
        """
        Generate comprehensive multi-modal analysis in multiple formats

        Args:
            comprehensive_analysis: Complete analysis dict from merge_multimodal_insights
            output_dir: Optional output directory (defaults to self.output_dir)

        Returns:
            Dict mapping format names to file paths
        """
        print("=" * 80)
        print("GENERATING MULTI-MODAL OUTPUT")
        print("=" * 80)
        print()

        if output_dir is None:
            output_dir = self.output_dir

        output_files = {}

        # 1. JSON (structured data)
        print("1. Generating JSON output...")
        json_path = output_dir / 'MULTIMODAL_ANALYSIS.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_analysis, f, indent=2, ensure_ascii=False)
        output_files['json'] = str(json_path)
        print(f"   [OK] {json_path}")

        # 2. Markdown (human-readable)
        print("2. Generating Markdown output...")
        md_path = output_dir / 'MULTIMODAL_ANALYSIS.md'
        markdown_content = self._format_as_markdown(comprehensive_analysis)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        output_files['markdown'] = str(md_path)
        print(f"   [OK] {md_path}")

        # 3. Comparison Table (Visual vs Audio)
        print("3. Generating comparison table...")
        table_path = output_dir / 'COMPARISON_TABLE.md'
        comparison_table = self._generate_comparison_table(comprehensive_analysis)
        with open(table_path, 'w', encoding='utf-8') as f:
            f.write(comparison_table)
        output_files['comparison'] = str(table_path)
        print(f"   [OK] {table_path}")

        # 4. Timeline View (HTML)
        print("4. Generating HTML timeline...")
        html_path = output_dir / 'TIMELINE.html'
        timeline_html = self._generate_timeline_html(comprehensive_analysis)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(timeline_html)
        output_files['timeline'] = str(html_path)
        print(f"   [OK] {html_path}")

        # 5. Claude Code Analysis Prompt
        print("5. Generating Claude Code prompt...")
        prompt_path = output_dir / 'PROMPT_MULTIMODAL.txt'
        multimodal_prompt = self._prepare_multimodal_prompt(comprehensive_analysis)
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(multimodal_prompt)
        output_files['prompt'] = str(prompt_path)
        print(f"   [OK] {prompt_path}")

        print()
        print("=" * 80)
        print("MULTI-MODAL OUTPUT COMPLETE")
        print("=" * 80)
        print()
        print("Generated files:")
        for format_name, file_path in output_files.items():
            print(f"  - {format_name}: {file_path}")
        print()

        return output_files

    def _format_as_markdown(self, analysis: Dict) -> str:
        """Format comprehensive analysis as Markdown"""
        md = []

        # Header
        md.append(f"# Multi-Modal Video Analysis\n\n")
        md.append(f"**Video**: {analysis['video_metadata'].get('title', 'Unknown')}\n\n")
        md.append(f"**Duration**: {analysis['video_metadata'].get('duration', 0) // 60} minutes\n\n")
        md.append(f"**Author**: {analysis['video_metadata'].get('author', 'Unknown')}\n\n")
        md.append(f"**Analyzed**: {analysis['analysis_metadata']['generated_at']}\n\n")
        md.append("---\n\n")

        # Summary
        md.append("## Executive Summary\n\n")
        md.append(f"{analysis['summary']}\n\n")

        # Statistics
        md.append("## Statistics\n\n")
        stats = analysis['statistics']
        md.append(f"- **Total Segments**: {stats['total_segments']}\n")
        md.append(f"- **Code Segments**: {stats['code_segments']} ({stats['code_segments'] / max(stats['total_segments'], 1) * 100:.1f}%)\n")
        md.append(f"- **Diagram Segments**: {stats['diagram_segments']} ({stats['diagram_segments'] / max(stats['total_segments'], 1) * 100:.1f}%)\n")
        md.append(f"- **Well-Aligned Segments**: {stats['well_aligned']} ({stats['well_aligned'] / max(stats['total_segments'], 1) * 100:.1f}%)\n")
        md.append(f"- **Gaps Identified**: {stats['gaps_count']}\n")
        md.append(f"- **Average Alignment Quality**: {stats['avg_alignment_quality']:.2f}/4.0\n\n")

        # Alignment distribution
        md.append("### Alignment Quality Distribution\n\n")
        for quality, count in stats['alignment_distribution'].items():
            md.append(f"- **{quality.title()}**: {count}\n")
        md.append("\n")

        # Segment types
        md.append("### Segment Types\n\n")
        for seg_type, count in sorted(stats['segment_types'].items(), key=lambda x: -x[1]):
            md.append(f"- **{seg_type.replace('_', ' ').title()}**: {count}\n")
        md.append("\n")

        # Detailed segments
        md.append("## Detailed Segments\n\n")
        for i, segment in enumerate(analysis['segments']):
            md.append(f"### {i + 1}. {segment['timestamp_formatted']} - {segment['type'].replace('_', ' ').title()}\n\n")

            # Visual content
            visual = segment['visual_content']
            md.append(f"**Visual Content**:\n")
            if visual['has_code']:
                md.append(f"- ✅ Code detected (score: {visual['code_score']:.2f})\n")
            if visual['has_diagram']:
                md.append(f"- ✅ Diagram detected (score: {visual['diagram_score']:.2f})\n")
            if visual['detection_reasons']:
                md.append(f"- Detection: {', '.join(visual['detection_reasons'])}\n")
            md.append(f"- Priority: {visual['priority']:.2f}\n")
            md.append("\n")

            # Audio content
            audio = segment['audio_content']
            md.append(f"**Transcript** ({audio['word_count']} words):\n")
            md.append(f"> {audio['text'][:300]}{'...' if len(audio['text']) > 300 else ''}\n\n")

            # Alignment quality
            md.append(f"**Alignment Quality**: {segment['alignment_quality'].title()}\n\n")

            # Insights
            if segment['insights']:
                md.append("**Insights**:\n")
                for insight in segment['insights']:
                    md.append(f"- {insight}\n")
                md.append("\n")

            md.append("---\n\n")

        # Gaps analysis
        md.append("## Gap Analysis\n\n")
        gaps = analysis['gaps']

        if gaps['visual_not_explained']:
            md.append("### Visual Content Not Explained\n\n")
            md.append("These segments show technical content (code/diagrams) without verbal explanation:\n\n")
            for gap in gaps['visual_not_explained'][:10]:  # Top 10
                md.append(f"- **{gap['timestamp']}**: {gap['content']}\n")
                md.append(f"  - *Suggestion*: {gap['suggestion']}\n")
            if len(gaps['visual_not_explained']) > 10:
                md.append(f"\n*...and {len(gaps['visual_not_explained']) - 10} more*\n")
            md.append("\n")

        if gaps['explained_not_shown']:
            md.append("### Concepts Explained But Not Shown\n\n")
            md.append("These segments discuss technical concepts without visual examples:\n\n")
            for gap in gaps['explained_not_shown'][:10]:  # Top 10
                md.append(f"- **{gap['timestamp']}**: {gap['content']}\n")
                md.append(f"  - *Excerpt*: \"{gap['transcript_excerpt']}\"\n")
                md.append(f"  - *Suggestion*: {gap['suggestion']}\n")
            if len(gaps['explained_not_shown']) > 10:
                md.append(f"\n*...and {len(gaps['explained_not_shown']) - 10} more*\n")
            md.append("\n")

        if gaps['high_value_content']:
            md.append("### High-Value Multi-Modal Segments\n\n")
            md.append("These segments demonstrate excellent alignment of visual and audio content:\n\n")
            for content in gaps['high_value_content'][:10]:
                md.append(f"- **{content['timestamp']}** ({content['type'].replace('_', ' ').title()})\n")
                md.append(f"  - {content['reason']}\n")
            md.append("\n")

        # Recommendations
        if gaps['recommendations']:
            md.append("### Recommendations\n\n")
            for rec in gaps['recommendations']:
                md.append(f"- {rec}\n")
            md.append("\n")

        return ''.join(md)

    def _generate_comparison_table(self, analysis: Dict) -> str:
        """Generate comparison table: Visual vs Audio"""
        table = []

        table.append("# Visual vs Audio Comparison\n\n")
        table.append(f"**Video**: {analysis['video_metadata'].get('title', 'Unknown')}\n\n")
        table.append("This table compares what is shown visually versus what is explained verbally.\n\n")
        table.append("| Timestamp | Visual Content | Audio Content | Alignment | Type |\n")
        table.append("|-----------|----------------|---------------|-----------|------|\n")

        for segment in analysis['segments']:
            timestamp = segment['timestamp_formatted']

            # Visual content
            visual_parts = []
            if segment['visual_content']['has_code']:
                visual_parts.append(f"Code ({segment['visual_content']['code_score']:.2f})")
            if segment['visual_content']['has_diagram']:
                visual_parts.append(f"Diagram ({segment['visual_content']['diagram_score']:.2f})")
            visual_str = ", ".join(visual_parts) if visual_parts else "None"

            # Audio content
            audio_text = segment['audio_content']['text'][:60]
            if len(segment['audio_content']['text']) > 60:
                audio_text += "..."
            audio_str = f"{audio_text} ({segment['audio_content']['word_count']} words)"

            # Alignment indicator
            quality = segment['alignment_quality']
            alignment_icons = {
                'excellent': '✅✅',
                'good': '✅',
                'fair': '⚠️',
                'poor': '❌'
            }
            alignment_str = f"{alignment_icons.get(quality, '?')} {quality.title()}"

            # Segment type
            seg_type = segment['type'].replace('_', ' ').title()

            table.append(f"| {timestamp} | {visual_str} | {audio_str} | {alignment_str} | {seg_type} |\n")

        table.append("\n## Legend\n\n")
        table.append("- ✅✅ Excellent - Perfect alignment of visual and audio\n")
        table.append("- ✅ Good - Strong alignment\n")
        table.append("- ⚠️ Fair - Some alignment issues\n")
        table.append("- ❌ Poor - Significant misalignment or gaps\n")

        return ''.join(table)

    def _generate_timeline_html(self, analysis: Dict) -> str:
        """Generate interactive HTML timeline"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Modal Timeline - {analysis['video_metadata'].get('title', 'Video Analysis')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .metadata {{
            color: #666;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        .timeline {{
            position: relative;
            padding-left: 30px;
        }}
        .timeline:before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: #ddd;
        }}
        .timeline-item {{
            position: relative;
            margin-bottom: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
        }}
        .timeline-item.code {{
            border-left-color: #4CAF50;
        }}
        .timeline-item.diagram {{
            border-left-color: #FF9800;
        }}
        .timeline-item.gap {{
            border-left-color: #f44336;
        }}
        .timeline-marker {{
            position: absolute;
            left: -36px;
            top: 20px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #2196F3;
            border: 3px solid white;
            box-shadow: 0 0 0 2px #2196F3;
        }}
        .timestamp {{
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        }}
        .segment-type {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976D2;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            margin-bottom: 10px;
        }}
        .alignment-quality {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            margin-left: 10px;
        }}
        .quality-excellent {{ background: #c8e6c9; color: #2e7d32; }}
        .quality-good {{ background: #fff9c4; color: #f57f17; }}
        .quality-fair {{ background: #ffccbc; color: #d84315; }}
        .quality-poor {{ background: #ffcdd2; color: #c62828; }}
        .content-section {{
            margin-top: 15px;
        }}
        .content-label {{
            font-weight: 600;
            color: #555;
            margin-bottom: 5px;
        }}
        .visual-indicators {{
            margin: 10px 0;
        }}
        .indicator {{
            display: inline-block;
            padding: 4px 10px;
            margin-right: 8px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .has-code {{
            background: #c8e6c9;
            color: #2e7d32;
        }}
        .has-diagram {{
            background: #ffe0b2;
            color: #e65100;
        }}
        .transcript {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 0.95em;
            line-height: 1.6;
            color: #444;
            border-left: 3px solid #ddd;
        }}
        .insights {{
            margin-top: 10px;
            padding: 10px;
            background: white;
            border-radius: 6px;
        }}
        .insight {{
            padding: 5px 0;
            font-size: 0.9em;
        }}
        .filter-bar {{
            margin-bottom: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 8px;
        }}
        .filter-btn {{
            padding: 8px 16px;
            margin-right: 10px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
        }}
        .filter-btn.active {{
            background: #2196F3;
            color: white;
            border-color: #2196F3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{analysis['video_metadata'].get('title', 'Multi-Modal Video Analysis')}</h1>
        <div class="metadata">
            <strong>Author:</strong> {analysis['video_metadata'].get('author', 'Unknown')} |
            <strong>Duration:</strong> {analysis['video_metadata'].get('duration', 0) // 60} minutes |
            <strong>Analyzed:</strong> {analysis['analysis_metadata']['generated_at'][:10]}
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Segments</div>
                <div class="stat-value">{analysis['statistics']['total_segments']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Code Segments</div>
                <div class="stat-value">{analysis['statistics']['code_segments']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Diagram Segments</div>
                <div class="stat-value">{analysis['statistics']['diagram_segments']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Well Aligned</div>
                <div class="stat-value">{analysis['statistics']['well_aligned']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Gaps Identified</div>
                <div class="stat-value">{analysis['statistics']['gaps_count']}</div>
            </div>
        </div>

        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterSegments('all')">All</button>
            <button class="filter-btn" onclick="filterSegments('code')">Code Only</button>
            <button class="filter-btn" onclick="filterSegments('diagram')">Diagrams Only</button>
            <button class="filter-btn" onclick="filterSegments('gaps')">Gaps</button>
        </div>

        <div class="timeline">
"""

        # Add timeline items
        for i, segment in enumerate(analysis['segments']):
            visual = segment['visual_content']
            audio = segment['audio_content']

            # Determine classes
            classes = ['timeline-item']
            if visual['has_code']:
                classes.append('code')
                classes.append('data-code')
            if visual['has_diagram']:
                classes.append('diagram')
                classes.append('data-diagram')
            if any('⚠️' in insight for insight in segment['insights']):
                classes.append('gap')
                classes.append('data-gap')

            html += f"""
            <div class="{' '.join(classes)}">
                <div class="timeline-marker"></div>
                <div class="timestamp">{segment['timestamp_formatted']}</div>
                <span class="segment-type">{segment['type'].replace('_', ' ').title()}</span>
                <span class="alignment-quality quality-{segment['alignment_quality']}">{segment['alignment_quality'].title()}</span>

                <div class="visual-indicators">
"""
            if visual['has_code']:
                html += f'                    <span class="indicator has-code">Code: {visual["code_score"]:.2f}</span>\n'
            if visual['has_diagram']:
                html += f'                    <span class="indicator has-diagram">Diagram: {visual["diagram_score"]:.2f}</span>\n'

            html += """                </div>

                <div class="content-section">
                    <div class="content-label">Transcript:</div>
                    <div class="transcript">
"""
            html += f'                        {audio["text"][:500]}{"..." if len(audio["text"]) > 500 else ""}\n'
            html += """                    </div>
                </div>
"""

            if segment['insights']:
                html += """
                <div class="insights">
                    <div class="content-label">Insights:</div>
"""
                for insight in segment['insights']:
                    html += f'                    <div class="insight">{insight}</div>\n'
                html += """                </div>
"""

            html += """            </div>
"""

        html += """        </div>
    </div>

    <script>
        function filterSegments(type) {
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            // Filter timeline items
            const items = document.querySelectorAll('.timeline-item');
            items.forEach(item => {
                if (type === 'all') {
                    item.style.display = 'block';
                } else if (type === 'code' && item.classList.contains('data-code')) {
                    item.style.display = 'block';
                } else if (type === 'diagram' && item.classList.contains('data-diagram')) {
                    item.style.display = 'block';
                } else if (type === 'gaps' && item.classList.contains('data-gap')) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""

        return html

    def _prepare_multimodal_prompt(self, analysis: Dict) -> str:
        """Prepare comprehensive prompt for Claude Code to analyze both modalities"""

        prompt = f"""Analyze this YouTube video using BOTH visual and audio content (Multi-Modal Analysis).

═══════════════════════════════════════════════════════════════════════════════
VIDEO METADATA
═══════════════════════════════════════════════════════════════════════════════

Title: {analysis['video_metadata'].get('title', 'Unknown')}
Duration: {analysis['video_metadata'].get('duration', 0) // 60} minutes ({analysis['video_metadata'].get('duration', 0)} seconds)
Author: {analysis['video_metadata'].get('author', 'Unknown')}

═══════════════════════════════════════════════════════════════════════════════
MULTI-MODAL CONTENT OVERVIEW
═══════════════════════════════════════════════════════════════════════════════

We have extracted {analysis['statistics']['total_segments']} key segments combining visual frames and transcript:

Visual Content:
- {analysis['statistics']['code_segments']} segments with code snippets
- {analysis['statistics']['diagram_segments']} segments with diagrams/architecture
- {analysis['statistics']['well_aligned']} segments well-aligned with audio

Audio Content:
- Full transcript aligned with visual frames
- ±{analysis['analysis_metadata']['alignment_window']} second windows around each frame

Alignment Quality:
- Excellent: {analysis['statistics']['alignment_distribution']['excellent']}
- Good: {analysis['statistics']['alignment_distribution']['good']}
- Fair: {analysis['statistics']['alignment_distribution']['fair']}
- Poor: {analysis['statistics']['alignment_distribution']['poor']}

═══════════════════════════════════════════════════════════════════════════════
MULTI-MODAL SEGMENTS (Top 20)
═══════════════════════════════════════════════════════════════════════════════

"""

        # Include top 20 segments (or all if fewer)
        for i, segment in enumerate(analysis['segments'][:20]):
            visual = segment['visual_content']
            audio = segment['audio_content']

            prompt += f"""
────────────────────────────────────────────────────────────────────────────────
Segment {i + 1}: {segment['timestamp_formatted']} - {segment['type'].replace('_', ' ').upper()}
────────────────────────────────────────────────────────────────────────────────

Alignment Quality: {segment['alignment_quality'].upper()}

VISUAL CONTENT:
"""
            if visual['has_code']:
                prompt += f"  ✓ Code Present (score: {visual['code_score']:.2f})\n"
            if visual['has_diagram']:
                prompt += f"  ✓ Diagram Present (score: {visual['diagram_score']:.2f})\n"
            if visual['detection_reasons']:
                prompt += f"  - Detection: {', '.join(visual['detection_reasons'])}\n"
            prompt += f"  - Priority: {visual['priority']:.2f}\n"
            prompt += f"  - Frame: {visual['frame_path']}\n"

            prompt += f"\nTRANSCRIPT ({audio['word_count']} words):\n"
            prompt += f'  "{audio["text"][:400]}{"..." if len(audio["text"]) > 400 else ""}"\n'

            if segment['insights']:
                prompt += f"\nINSIGHTS:\n"
                for insight in segment['insights']:
                    prompt += f"  - {insight}\n"

        if len(analysis['segments']) > 20:
            prompt += f"\n... and {len(analysis['segments']) - 20} more segments (see MULTIMODAL_ANALYSIS.json for complete data)\n"

        prompt += f"""

═══════════════════════════════════════════════════════════════════════════════
GAP ANALYSIS
═══════════════════════════════════════════════════════════════════════════════

Visual Content Not Explained: {len(analysis['gaps']['visual_not_explained'])}
"""
        for gap in analysis['gaps']['visual_not_explained'][:5]:
            prompt += f"  - [{gap['timestamp']}] {gap['content']}\n"

        prompt += f"\nConcepts Explained But Not Shown: {len(analysis['gaps']['explained_not_shown'])}\n"
        for gap in analysis['gaps']['explained_not_shown'][:5]:
            prompt += f"  - [{gap['timestamp']}] {gap['content']}\n"

        if analysis['gaps']['recommendations']:
            prompt += f"\nRecommendations:\n"
            for rec in analysis['gaps']['recommendations']:
                prompt += f"  - {rec}\n"

        prompt += f"""

═══════════════════════════════════════════════════════════════════════════════
ANALYSIS REQUEST
═══════════════════════════════════════════════════════════════════════════════

Please provide a COMPREHENSIVE multi-modal analysis leveraging BOTH visual and audio insights:

1. **Executive Summary**
   - What is this video about (using both visual and audio evidence)?
   - Key value proposition or main message
   - Target audience

2. **Core Technical Concepts**
   - Main concepts explained (from transcript)
   - Visual examples/demonstrations (from frames)
   - How visual and audio complement each other

3. **Code Analysis** (if applicable)
   - Programming languages identified (from frames)
   - Code patterns and techniques shown
   - Relationship between code shown and code discussed
   - Notable code snippets worth extracting

4. **Architecture & System Design** (if applicable)
   - Diagrams and architecture visualizations identified
   - System components and their relationships
   - How architecture explanations align with visuals

5. **Multi-Modal Insights**
   - What insights ONLY emerge from combining both modalities?
   - Where does visual content enhance understanding?
   - Where does narration provide crucial context?
   - Examples of excellent visual-audio alignment

6. **Gap Analysis Review**
   - Validate identified gaps (visual not explained, explained not shown)
   - Additional gaps or misalignments you notice
   - Suggestions for improvement

7. **Actionable Takeaways**
   - Key implementation steps (from both visual examples and explanations)
   - Code patterns to adopt
   - Architecture patterns to consider
   - Tools, libraries, or frameworks mentioned

8. **Reference Quality Assessment**
   - Which segments are reference quality (excellent alignment)?
   - Which concepts are explained most clearly?
   - What makes this content valuable?

9. **Follow-Up Questions**
   - What needs clarification?
   - What would benefit from deeper exploration?
   - Related topics to research

═══════════════════════════════════════════════════════════════════════════════

IMPORTANT: Focus on insights that emerge from COMBINING both visual and audio modalities.
Highlight where the multi-modal approach provides richer understanding than either modality alone.

For detailed segment data, frame paths, and complete transcripts, see:
- MULTIMODAL_ANALYSIS.json (complete structured data)
- MULTIMODAL_ANALYSIS.md (human-readable report)
- COMPARISON_TABLE.md (visual vs audio comparison)
- TIMELINE.html (interactive timeline view)
"""

        return prompt

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp as HH:MM:SS or MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"


def main():
    """CLI interface for multi-modal integration"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Multi-Modal Integration: Combine visual frames and transcript analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--frames-index', required=True,
                       help='Path to frame_index.json from smart frame selection')
    parser.add_argument('--transcript', required=True,
                       help='Path to transcript.txt file')
    parser.add_argument('--metadata', required=True,
                       help='Path to video metadata.json file')
    parser.add_argument('--output', default='multimodal_output',
                       help='Output directory for multi-modal analysis (default: multimodal_output)')
    parser.add_argument('--window', type=int, default=30,
                       help='Alignment window in seconds (default: 30)')

    args = parser.parse_args()

    # Load frame index
    print("Loading frame data...")
    with open(args.frames_index, 'r', encoding='utf-8') as f:
        frame_data = json.load(f)
    frames = frame_data['frames']
    print(f"[OK] Loaded {len(frames)} frames")

    # Load transcript
    print("Loading transcript...")
    with open(args.transcript, 'r', encoding='utf-8') as f:
        transcript = f.read()
    print(f"[OK] Loaded transcript ({len(transcript)} characters)")

    # Load metadata
    print("Loading video metadata...")
    with open(args.metadata, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    print(f"[OK] Loaded metadata for: {metadata.get('title', 'Unknown')}")
    print()

    # Initialize integrator
    integrator = MultiModalIntegrator(output_dir=args.output)
    integrator.alignment_window = args.window

    # Step 1: Align frames with transcript
    aligned_data = integrator.align_frames_with_transcript(
        frames=frames,
        transcript=transcript,
        window_seconds=args.window
    )

    # Step 2: Merge insights
    comprehensive_analysis = integrator.merge_multimodal_insights(
        aligned_data=aligned_data,
        video_metadata=metadata
    )

    # Step 3: Generate outputs
    output_files = integrator.generate_multimodal_output(comprehensive_analysis)

    print("=" * 80)
    print("✓ MULTI-MODAL INTEGRATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Analyzed {len(frames)} segments across {metadata.get('duration', 0) // 60} minutes")
    print()
    print("Generated files:")
    for format_name, file_path in output_files.items():
        print(f"  - {format_name.upper()}: {file_path}")
    print()
    print("Next step: Use PROMPT_MULTIMODAL.txt with Claude Code for comprehensive analysis")
    print()


if __name__ == "__main__":
    main()
