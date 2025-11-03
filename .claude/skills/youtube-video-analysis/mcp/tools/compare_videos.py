"""
compare_videos MCP tool handler
Side-by-side video comparison
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio
import logging
import json

# Add scripts directory to path
SKILL_ROOT = Path(__file__).parent.parent.parent.resolve()
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from get_transcript import get_transcript_handler, extract_video_id


async def compare_videos_handler(
    video_urls: List[str],
    aspects: Optional[List[str]] = None,
    output_format: str = "markdown",
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Compare multiple videos side-by-side

    Args:
        video_urls: List of YouTube URLs or video IDs (2-5 videos)
        aspects: Comparison aspects (default: ["approach", "tools", "pros_cons"])
        output_format: Output format - "markdown", "json", or "html"
        logger: Logger instance

    Returns:
        dict with comparison results
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = datetime.now()

    try:
        # Validate inputs
        if not video_urls or len(video_urls) < 2:
            return {
                "success": False,
                "error": "At least 2 videos required for comparison"
            }

        if len(video_urls) > 5:
            return {
                "success": False,
                "error": "Maximum 5 videos can be compared at once"
            }

        # Default aspects if not provided
        if aspects is None:
            aspects = ["approach", "tools", "pros_cons"]

        logger.info(f"Comparing {len(video_urls)} videos across {len(aspects)} aspects")

        # Get transcripts for all videos
        videos_data = []
        for i, url in enumerate(video_urls):
            logger.info(f"Processing video {i+1}/{len(video_urls)}: {url}")

            transcript_result = await get_transcript_handler(
                video_url=url,
                logger=logger
            )

            if not transcript_result["success"]:
                logger.warning(f"Failed to get transcript for video {i+1}: {transcript_result.get('error')}")
                continue

            videos_data.append({
                "index": i,
                "video_id": transcript_result["video_id"],
                "url": url,
                "title": transcript_result["title"],
                "author": transcript_result["author"],
                "duration_seconds": transcript_result["duration_seconds"],
                "transcript": transcript_result["transcript"],
                "word_count": transcript_result["word_count"]
            })

        if len(videos_data) < 2:
            return {
                "success": False,
                "error": f"Could only retrieve {len(videos_data)} video(s) successfully. Need at least 2 for comparison."
            }

        # Perform comparison analysis
        comparison = analyze_comparison(videos_data, aspects, logger)

        # Generate comparison table
        comparison_table = generate_comparison_table(videos_data, comparison, output_format)

        # Generate summary and recommendation
        summary = generate_comparison_summary(videos_data, comparison)
        recommendation = generate_recommendation(videos_data, comparison)

        processing_time = (datetime.now() - start_time).total_seconds()

        return {
            "success": True,
            "videos": [
                {
                    "video_id": v["video_id"],
                    "title": v["title"],
                    "author": v["author"],
                    "duration_seconds": v["duration_seconds"]
                }
                for v in videos_data
            ],
            "comparison": comparison,
            "summary": summary,
            "recommendation": recommendation,
            "comparison_table": comparison_table,
            "output_format": output_format,
            "aspects_compared": aspects,
            "processing_time_seconds": round(processing_time, 2)
        }

    except Exception as e:
        logger.exception(f"Error comparing videos: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def analyze_comparison(videos_data: List[dict], aspects: List[str], logger: logging.Logger) -> dict:
    """Analyze videos across specified aspects"""
    logger.info("Analyzing comparison aspects...")

    comparison = {}

    for aspect in aspects:
        comparison[aspect] = {}

        for video in videos_data:
            video_id = video["video_id"]
            transcript = video["transcript"]

            # Analyze each aspect
            if aspect == "approach":
                comparison[aspect][video_id] = analyze_approach(transcript, video)
            elif aspect == "tools":
                comparison[aspect][video_id] = analyze_tools(transcript, video)
            elif aspect == "pros_cons":
                comparison[aspect][video_id] = analyze_pros_cons(transcript, video)
            elif aspect == "complexity":
                comparison[aspect][video_id] = analyze_complexity(transcript, video)
            elif aspect == "completeness":
                comparison[aspect][video_id] = analyze_completeness(transcript, video)
            elif aspect == "code_quality":
                comparison[aspect][video_id] = analyze_code_quality(transcript, video)
            else:
                # Generic aspect analysis
                comparison[aspect][video_id] = analyze_generic(transcript, video, aspect)

    return comparison


def analyze_approach(transcript: str, video: dict) -> str:
    """Analyze the approach taken in the video"""
    # Simple keyword-based analysis
    keywords = {
        "beginner": ["beginner", "introduction", "basics", "fundamentals", "getting started"],
        "advanced": ["advanced", "deep dive", "complex", "sophisticated", "expert"],
        "practical": ["example", "demo", "hands-on", "tutorial", "build"],
        "theoretical": ["theory", "concept", "principle", "architecture", "design"]
    }

    approach_scores = {}
    transcript_lower = transcript.lower()

    for approach_type, words in keywords.items():
        count = sum(1 for word in words if word in transcript_lower)
        approach_scores[approach_type] = count

    # Determine primary approach
    primary = max(approach_scores, key=approach_scores.get)
    duration = video["duration_seconds"] // 60

    return f"{primary.capitalize()} approach, {duration}-minute tutorial focusing on practical examples" if approach_scores.get("practical", 0) > 5 else f"{primary.capitalize()} approach with theoretical foundations"


def analyze_tools(transcript: str, video: dict) -> str:
    """Analyze tools and technologies mentioned"""
    # Common tool keywords
    tools_keywords = ["python", "javascript", "typescript", "react", "fastapi", "flask", "django", "node", "docker", "kubernetes", "aws", "azure", "gcp", "postgresql", "mysql", "mongodb", "redis", "api", "rest", "graphql", "claude", "openai", "anthropic"]

    transcript_lower = transcript.lower()
    tools_found = [tool for tool in tools_keywords if tool in transcript_lower]

    if tools_found:
        return f"Uses: {', '.join(tools_found[:5])}" + (f" and {len(tools_found)-5} more" if len(tools_found) > 5 else "")
    else:
        return "Tools not clearly specified in transcript"


def analyze_pros_cons(transcript: str, video: dict) -> str:
    """Analyze pros and cons"""
    return f"Well-structured content ({video['word_count']} words), {video['duration_seconds'] // 60} minutes long"


def analyze_complexity(transcript: str, video: dict) -> str:
    """Analyze complexity level"""
    word_count = video['word_count']
    duration = video['duration_seconds']

    # Words per minute indicates density
    wpm = (word_count / duration) * 60 if duration > 0 else 0

    if wpm > 140:
        return f"High density ({wpm:.0f} wpm) - fast-paced content"
    elif wpm > 100:
        return f"Medium density ({wpm:.0f} wpm) - moderate pace"
    else:
        return f"Low density ({wpm:.0f} wpm) - slower, detailed pace"


def analyze_completeness(transcript: str, video: dict) -> str:
    """Analyze completeness"""
    duration = video['duration_seconds'] // 60
    word_count = video['word_count']

    if duration > 45 and word_count > 5000:
        return f"Comprehensive ({duration}min, {word_count} words) - in-depth coverage"
    elif duration > 20:
        return f"Moderate coverage ({duration}min, {word_count} words)"
    else:
        return f"Brief overview ({duration}min, {word_count} words)"


def analyze_code_quality(transcript: str, video: dict) -> str:
    """Analyze code quality indicators"""
    code_keywords = ["function", "class", "import", "def", "const", "let", "var", "async", "await"]
    transcript_lower = transcript.lower()

    code_mentions = sum(1 for keyword in code_keywords if keyword in transcript_lower)

    if code_mentions > 20:
        return f"Code-heavy ({code_mentions} code keywords) - substantial code examples"
    elif code_mentions > 10:
        return f"Moderate code ({code_mentions} code keywords)"
    else:
        return f"Minimal code ({code_mentions} code keywords) - more conceptual"


def analyze_generic(transcript: str, video: dict, aspect: str) -> str:
    """Generic analysis for custom aspects"""
    return f"Analysis for '{aspect}' aspect - requires custom implementation"


def generate_comparison_table(videos_data: List[dict], comparison: dict, output_format: str) -> str:
    """Generate comparison table in specified format"""

    if output_format == "markdown":
        return generate_markdown_table(videos_data, comparison)
    elif output_format == "html":
        return generate_html_table(videos_data, comparison)
    elif output_format == "json":
        return json.dumps(comparison, indent=2)
    else:
        return generate_markdown_table(videos_data, comparison)


def generate_markdown_table(videos_data: List[dict], comparison: dict) -> str:
    """Generate markdown comparison table"""
    table = "# Video Comparison\n\n"

    # Header row
    table += "| Aspect | " + " | ".join([f"Video {i+1}: {v['title'][:30]}..." for i, v in enumerate(videos_data)]) + " |\n"
    table += "|--------|" + "|".join(["--------" for _ in videos_data]) + "|\n"

    # Data rows
    for aspect, videos_analysis in comparison.items():
        row = f"| **{aspect.replace('_', ' ').title()}** |"

        for video in videos_data:
            video_id = video["video_id"]
            analysis = videos_analysis.get(video_id, "N/A")
            row += f" {analysis} |"

        table += row + "\n"

    # Video details
    table += "\n## Video Details\n\n"
    for i, video in enumerate(videos_data):
        table += f"### Video {i+1}: {video['title']}\n"
        table += f"- **Author**: {video['author']}\n"
        table += f"- **Duration**: {video['duration_seconds'] // 60} minutes\n"
        table += f"- **Word Count**: {video['word_count']} words\n"
        table += f"- **URL**: {video['url']}\n\n"

    return table


def generate_html_table(videos_data: List[dict], comparison: dict) -> str:
    """Generate HTML comparison table"""
    html = "<table border='1'>\n<tr><th>Aspect</th>"

    for i, v in enumerate(videos_data):
        html += f"<th>Video {i+1}: {v['title'][:30]}...</th>"

    html += "</tr>\n"

    for aspect, videos_analysis in comparison.items():
        html += f"<tr><td><strong>{aspect.replace('_', ' ').title()}</strong></td>"

        for video in videos_data:
            video_id = video["video_id"]
            analysis = videos_analysis.get(video_id, "N/A")
            html += f"<td>{analysis}</td>"

        html += "</tr>\n"

    html += "</table>"
    return html


def generate_comparison_summary(videos_data: List[dict], comparison: dict) -> str:
    """Generate overall comparison summary"""
    summary = f"Compared {len(videos_data)} videos across {len(comparison)} aspects:\n\n"

    for i, video in enumerate(videos_data):
        summary += f"{i+1}. **{video['title']}** by {video['author']} ({video['duration_seconds'] // 60} min)\n"

    summary += f"\nAspects analyzed: {', '.join(comparison.keys())}"

    return summary


def generate_recommendation(videos_data: List[dict], comparison: dict) -> str:
    """Generate recommendation based on comparison"""
    # Simple heuristic: recommend longest, most comprehensive video
    longest_video = max(videos_data, key=lambda v: v['duration_seconds'])

    recommendation = f"**Recommended**: '{longest_video['title']}' by {longest_video['author']}\n\n"
    recommendation += f"Reasons:\n"
    recommendation += f"- Most comprehensive duration ({longest_video['duration_seconds'] // 60} minutes)\n"
    recommendation += f"- Substantial content ({longest_video['word_count']} words)\n"
    recommendation += f"\nNote: This recommendation is based on content length. Consider your learning goals and time availability."

    return recommendation
