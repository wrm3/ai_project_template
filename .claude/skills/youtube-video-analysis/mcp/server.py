#!/usr/bin/env python3
"""
YouTube Intelligence MCP Server
Exposes YouTube video analysis capabilities to Claude Desktop and other MCP clients

Features:
- Get video transcripts
- Comprehensive video analysis (quick/comprehensive/multimodal modes)
- Semantic search across ingested videos (RAG)
- Video comparison
- Code extraction from videos

Dependencies:
- FastMCP for MCP protocol
- OpenAI for embeddings
- Supabase for RAG database
- youtube-video-analysis skill for transcription
- youtube-rag-storage skill for RAG search
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
import logging
import sys
import os

# --- Logging Setup ---
PROJECT_ROOT_FOR_LOG = Path(__file__).parent.resolve()
LOG_DIR = PROJECT_ROOT_FOR_LOG / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILENAME = f"youtube_intel_mcp_{datetime.now().strftime('%Y_%m_%d')}.log"
LOG_FILE = LOG_DIR / LOG_FILENAME

# Configure logging
log_root = logging.getLogger()
for handler in log_root.handlers[:]:
    log_root.removeHandler(handler)
    handler.close()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"--- YouTube Intel MCP Server Started --- Log file: {LOG_FILE} ---")

# Create FastMCP server
mcp = FastMCP("youtube-intel")
logger.info("FastMCP instance created for YouTube Intelligence")

# Define paths to skill modules
SKILL_ROOT = Path(__file__).parent.parent.resolve()
SCRIPTS_DIR = SKILL_ROOT / "scripts"
RAG_SKILL_ROOT = SKILL_ROOT.parent / "youtube-rag-storage"
RAG_SCRIPTS_DIR = RAG_SKILL_ROOT / "scripts"

logger.info(f"Skill Root: {SKILL_ROOT}")
logger.info(f"Scripts Directory: {SCRIPTS_DIR}")
logger.info(f"RAG Skill Root: {RAG_SKILL_ROOT}")

# Add scripts to Python path
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(RAG_SCRIPTS_DIR))

# Import tool handlers
from tools.get_transcript import get_transcript_handler
from tools.analyze_video import analyze_video_handler
from tools.search_videos import search_videos_handler
from tools.compare_videos import compare_videos_handler
from tools.extract_code import extract_code_handler


@mcp.tool(name="get_transcript")
async def run_get_transcript(
    video_url: str,
    output_dir: Optional[str] = None,
    force_redownload: bool = False
) -> dict:
    """
    Get full transcript of a YouTube video.

    Downloads the video, extracts audio, and transcribes using Whisper AI.
    Results are cached for future requests unless force_redownload is True.

    Args:
        video_url (str): YouTube URL or video ID (e.g., "https://youtube.com/watch?v=VIDEO_ID" or "VIDEO_ID")
        output_dir (str, optional): Directory to save results. Defaults to ./output/<video_id>/
        force_redownload (bool): If True, re-downloads and re-transcribes even if cached. Default: False

    Returns:
        dict: {
            "success": bool,
            "video_id": str,
            "title": str,
            "author": str,
            "duration_seconds": int,
            "transcript": str (full transcript text),
            "transcript_length": int (character count),
            "word_count": int,
            "cached": bool (whether result was from cache),
            "output_dir": str,
            "error": str (if success=False)
        }

    Example:
        # Get transcript
        result = await get_transcript("https://youtube.com/watch?v=dQw4w9WgXcQ")
        print(result["transcript"])

        # Force fresh download
        result = await get_transcript("dQw4w9WgXcQ", force_redownload=True)
    """
    logger.info(f"Tool 'get_transcript' called for URL: {video_url}")

    try:
        return await get_transcript_handler(
            video_url=video_url,
            output_dir=output_dir,
            force_redownload=force_redownload,
            logger=logger
        )
    except Exception as e:
        logger.exception(f"Error in get_transcript tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(name="analyze_video")
async def run_analyze_video(
    video_url: str,
    mode: str = "comprehensive",
    output_dir: Optional[str] = None,
    save_to_rag: bool = False
) -> dict:
    """
    Comprehensive analysis of a YouTube video.

    Modes:
    - "quick": Fast summary (transcript only, no visual analysis)
    - "comprehensive": Detailed analysis with key insights, quotes, technical details
    - "multimodal": Full analysis combining transcript + visual frames (code screenshots, diagrams)

    Args:
        video_url (str): YouTube URL or video ID
        mode (str): Analysis mode - "quick", "comprehensive", or "multimodal". Default: "comprehensive"
        output_dir (str, optional): Directory to save results. Defaults to ./output/<video_id>/
        save_to_rag (bool): If True, ingests video into RAG database for semantic search. Default: False

    Returns:
        dict: {
            "success": bool,
            "video_id": str,
            "title": str,
            "mode": str,
            "analysis": {
                "summary": str,
                "key_insights": list[str],
                "technical_details": dict,
                "quotes": list[str],
                "action_items": list[str],
                "code_examples": list[dict] (if multimodal),
                "diagrams": list[dict] (if multimodal)
            },
            "rag_ingestion": dict (if save_to_rag=True),
            "output_files": list[str],
            "processing_time_seconds": float,
            "error": str (if success=False)
        }

    Example:
        # Quick summary
        result = await analyze_video("https://youtube.com/watch?v=VIDEO_ID", mode="quick")

        # Comprehensive analysis + save to RAG
        result = await analyze_video("VIDEO_ID", mode="comprehensive", save_to_rag=True)

        # Multi-modal with visual analysis
        result = await analyze_video("VIDEO_ID", mode="multimodal")
    """
    logger.info(f"Tool 'analyze_video' called for URL: {video_url}, mode: {mode}")

    try:
        return await analyze_video_handler(
            video_url=video_url,
            mode=mode,
            output_dir=output_dir,
            save_to_rag=save_to_rag,
            logger=logger
        )
    except Exception as e:
        logger.exception(f"Error in analyze_video tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(name="search_videos")
async def run_search_videos(
    query: str,
    limit: int = 10,
    min_similarity: float = 0.7,
    video_id: Optional[str] = None,
    chunk_type: Optional[str] = None
) -> dict:
    """
    Semantic search across all videos in the RAG database.

    Uses OpenAI embeddings and vector similarity to find relevant content
    across all ingested YouTube videos. Search is semantic, not keyword-based.

    Args:
        query (str): Natural language search query (e.g., "RAG implementation best practices")
        limit (int): Maximum number of results to return. Default: 10
        min_similarity (float): Minimum cosine similarity threshold (0.0-1.0). Default: 0.7
        video_id (str, optional): Limit search to specific video ID
        chunk_type (str, optional): Filter by chunk type - "transcript", "code", "heading", etc.

    Returns:
        dict: {
            "success": bool,
            "query": str,
            "results": list[{
                "video_id": str,
                "video_title": str,
                "video_author": str,
                "chunk_text": str,
                "similarity": float,
                "timestamp_start": float (seconds into video),
                "chunk_type": str,
                "chunk_index": int,
                "has_code": bool,
                "has_diagram": bool
            }],
            "total_results": int,
            "search_time_ms": float,
            "error": str (if success=False)
        }

    Example:
        # General search
        results = await search_videos("How to implement RAG with Claude")

        # Search within specific video
        results = await search_videos(
            "vector database setup",
            video_id="dQw4w9WgXcQ",
            limit=5
        )

        # Search for code examples only
        results = await search_videos(
            "Python FastAPI example",
            chunk_type="code",
            min_similarity=0.75
        )
    """
    logger.info(f"Tool 'search_videos' called with query: {query[:100]}")

    try:
        return await search_videos_handler(
            query=query,
            limit=limit,
            min_similarity=min_similarity,
            video_id=video_id,
            chunk_type=chunk_type,
            logger=logger
        )
    except Exception as e:
        logger.exception(f"Error in search_videos tool: {e}")
        return {
            "success": False,
            "error": str(e),
            "results": []
        }


@mcp.tool(name="compare_videos")
async def run_compare_videos(
    video_urls: list,
    aspects: Optional[list] = None,
    output_format: str = "markdown"
) -> dict:
    """
    Compare multiple YouTube videos side-by-side.

    Analyzes and compares videos across specified aspects such as approach,
    tools used, complexity, performance, etc. Useful for evaluating different
    tutorials or implementations.

    Args:
        video_urls (list[str]): List of 2-5 YouTube URLs or video IDs to compare
        aspects (list[str], optional): Comparison aspects. Examples:
            - "approach" - How the topic is approached
            - "tools" - Technologies and tools used
            - "complexity" - Level of complexity
            - "completeness" - How thorough the content is
            - "code_quality" - Quality of code examples
            - "performance" - Performance considerations discussed
            If None, uses default aspects: ["approach", "tools", "pros_cons"]
        output_format (str): Output format - "markdown", "json", or "html". Default: "markdown"

    Returns:
        dict: {
            "success": bool,
            "videos": list[{
                "video_id": str,
                "title": str,
                "author": str,
                "duration_seconds": int
            }],
            "comparison": {
                "aspect_1": {
                    "video_1": str (description),
                    "video_2": str (description),
                    ...
                },
                ...
            },
            "summary": str (overall comparison summary),
            "recommendation": str (which video to watch and why),
            "comparison_table": str (formatted comparison table),
            "output_format": str,
            "error": str (if success=False)
        }

    Example:
        # Compare two FastAPI tutorials
        result = await compare_videos(
            video_urls=[
                "https://youtube.com/watch?v=VIDEO_1",
                "https://youtube.com/watch?v=VIDEO_2"
            ],
            aspects=["approach", "code_quality", "completeness"]
        )

        # Compare with default aspects
        result = await compare_videos([
            "VIDEO_ID_1",
            "VIDEO_ID_2",
            "VIDEO_ID_3"
        ])

        print(result["comparison_table"])
    """
    logger.info(f"Tool 'compare_videos' called for {len(video_urls)} videos")

    try:
        return await compare_videos_handler(
            video_urls=video_urls,
            aspects=aspects,
            output_format=output_format,
            logger=logger
        )
    except Exception as e:
        logger.exception(f"Error in compare_videos tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool(name="extract_code")
async def run_extract_code(
    video_url: str,
    language: Optional[str] = None,
    include_frames: bool = True,
    output_dir: Optional[str] = None
) -> dict:
    """
    Extract all code snippets from a YouTube video.

    Combines transcript analysis (code blocks in description/transcript)
    with optional frame analysis (OCR on code screenshots) to extract
    all programming code from the video.

    Args:
        video_url (str): YouTube URL or video ID
        language (str, optional): Filter by programming language (e.g., "python", "javascript", "sql")
        include_frames (bool): If True, also extracts code from video frames using OCR. Default: True
        output_dir (str, optional): Directory to save code files. Defaults to ./output/<video_id>/code/

    Returns:
        dict: {
            "success": bool,
            "video_id": str,
            "video_title": str,
            "code_snippets": list[{
                "snippet_id": int,
                "language": str,
                "source": str ("transcript", "description", "frame", "auto-detected"),
                "code": str,
                "timestamp": float (seconds, if available),
                "frame_number": int (if from frame),
                "context": str (surrounding text),
                "line_count": int,
                "has_imports": bool,
                "has_functions": bool,
                "has_classes": bool
            }],
            "summary": {
                "total_snippets": int,
                "languages_found": list[str],
                "snippets_by_source": dict,
                "total_lines_of_code": int
            },
            "output_files": list[str] (saved code files),
            "error": str (if success=False)
        }

    Example:
        # Extract all code
        result = await extract_code("https://youtube.com/watch?v=VIDEO_ID")

        # Extract only Python code from transcript
        result = await extract_code(
            "VIDEO_ID",
            language="python",
            include_frames=False
        )

        # Get code with frame analysis
        result = await extract_code("VIDEO_ID", include_frames=True)

        # Save to specific directory
        for snippet in result["code_snippets"]:
            print(f"--- {snippet['language']} at {snippet['timestamp']}s ---")
            print(snippet['code'])
    """
    logger.info(f"Tool 'extract_code' called for URL: {video_url}")

    try:
        return await extract_code_handler(
            video_url=video_url,
            language=language,
            include_frames=include_frames,
            output_dir=output_dir,
            logger=logger
        )
    except Exception as e:
        logger.exception(f"Error in extract_code tool: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    logger.info("Starting YouTube Intel MCP server via Stdio...")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.exception("Fatal error running MCP server")
    finally:
        logger.info("YouTube Intel MCP server stopped.")
