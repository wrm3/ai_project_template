"""
search_videos MCP tool handler
Semantic search across RAG database
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio
import logging

# Add scripts directory to path
SKILL_ROOT = Path(__file__).parent.parent.parent.resolve()
RAG_SKILL_ROOT = SKILL_ROOT.parent / "youtube-rag-storage"
RAG_SCRIPTS_DIR = RAG_SKILL_ROOT / "scripts"
sys.path.insert(0, str(RAG_SCRIPTS_DIR))


async def search_videos_handler(
    query: str,
    limit: int = 10,
    min_similarity: float = 0.7,
    video_id: Optional[str] = None,
    chunk_type: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Search across videos in RAG database using semantic similarity

    Args:
        query: Natural language search query
        limit: Maximum number of results
        min_similarity: Minimum cosine similarity threshold (0.0-1.0)
        video_id: Optional filter by video ID
        chunk_type: Optional filter by chunk type
        logger: Logger instance

    Returns:
        dict with search results
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = datetime.now()

    try:
        # Import search functionality
        from search_content import semantic_search

        logger.info(f"Searching videos for: '{query[:100]}'")
        logger.info(f"Parameters: limit={limit}, min_similarity={min_similarity}, video_id={video_id}, chunk_type={chunk_type}")

        # Perform semantic search
        results = await asyncio.to_thread(
            semantic_search,
            query=query,
            limit=limit,
            min_similarity=min_similarity,
            video_id=video_id,
            chunk_type=chunk_type
        )

        search_time = (datetime.now() - start_time).total_seconds() * 1000  # Convert to milliseconds

        logger.info(f"Search complete: Found {len(results)} results in {search_time:.2f}ms")

        # Format results
        formatted_results = []
        for r in results:
            formatted_results.append({
                "video_id": r.get("video_id", "unknown"),
                "video_title": r.get("video_title", "Unknown"),
                "video_author": r.get("video_author", "Unknown"),
                "chunk_text": r.get("chunk_text", ""),
                "similarity": round(r.get("similarity", 0.0), 4),
                "timestamp_start": r.get("timestamp_start"),
                "chunk_type": r.get("chunk_type", "transcript"),
                "chunk_index": r.get("chunk_index", 0),
                "has_code": r.get("has_code", False),
                "has_diagram": r.get("has_diagram", False)
            })

        return {
            "success": True,
            "query": query,
            "results": formatted_results,
            "total_results": len(formatted_results),
            "search_time_ms": round(search_time, 2),
            "parameters": {
                "limit": limit,
                "min_similarity": min_similarity,
                "video_id": video_id,
                "chunk_type": chunk_type
            }
        }

    except ImportError as e:
        logger.error(f"RAG search module not available: {e}")
        return {
            "success": False,
            "error": "RAG search functionality not available. Ensure youtube-rag-storage skill is properly installed and configured.",
            "details": str(e),
            "results": [],
            "suggestion": "Run ingest_video first to populate the RAG database"
        }

    except Exception as e:
        logger.exception(f"Error searching videos: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "results": []
        }
