"""
Semantic Search Interface for YouTube RAG Content

Search YouTube content using natural language queries with vector similarity.

Usage:
    # Basic search
    python search_content.py "How to implement RAG with Claude"

    # Search with filters
    python search_content.py "vector database" --limit 20 --min-similarity 0.75

    # Search within specific video
    python search_content.py "Python examples" --video-id VIDEO_ID

    # JSON output for AI agents
    python search_content.py "query" --format json > results.json
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import timedelta

# Add parent directories to path
sys.path.append(str(Path(__file__).parent))

# Import database client
try:
    from db_client import SupabaseClient
except ImportError:
    print("[ERROR] Database client not found")
    print("[HELP] Ensure db_client.py exists (from Task 044-4)")
    sys.exit(1)

# Import embeddings
from embeddings import generate_embedding_single


def format_timestamp(seconds: Optional[float]) -> str:
    """
    Format timestamp seconds as HH:MM:SS

    Args:
        seconds: Timestamp in seconds

    Returns:
        Formatted timestamp string
    """
    if seconds is None:
        return "N/A"

    td = timedelta(seconds=int(seconds))
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def format_similarity_bar(similarity: float, width: int = 20) -> str:
    """
    Create visual similarity bar

    Args:
        similarity: Similarity score 0-1
        width: Bar width in characters

    Returns:
        Visual bar representation
    """
    filled = int(similarity * width)
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {similarity:.3f}"


def search_youtube_content(
    query: str,
    limit: int = 10,
    min_similarity: float = 0.7,
    video_id: Optional[str] = None,
    chunk_type: Optional[str] = None,
    show_context: bool = False,
    embedding_model: str = "text-embedding-3-small"
) -> List[Dict]:
    """
    Search YouTube content using semantic similarity

    Args:
        query: Search query (natural language)
        limit: Maximum number of results
        min_similarity: Minimum similarity threshold (0-1)
        video_id: Filter by specific video ID
        chunk_type: Filter by chunk type (transcript, code, etc.)
        show_context: Include surrounding chunks for context
        embedding_model: OpenAI embedding model

    Returns:
        List of search results with metadata
    """
    # Generate query embedding
    print(f"[SEARCH] Generating query embedding...")
    query_embedding = generate_embedding_single(query, model=embedding_model)

    # Search database
    print(f"[SEARCH] Searching vector database...")
    client = SupabaseClient()

    try:
        results = client.semantic_search(
            query_embedding=query_embedding.tolist(),
            limit=limit,
            min_similarity=min_similarity,
            video_id=video_id,
            chunk_type=chunk_type
        )

        # Add context if requested
        if show_context:
            for result in results:
                # Get surrounding chunks
                chunk_id = result['chunk_id']
                chunk_index = result['chunk_index']

                # Get previous and next chunks
                prev_chunk = client.get_chunk_by_index(
                    result['video_uuid'],
                    chunk_index - 1
                )
                next_chunk = client.get_chunk_by_index(
                    result['video_uuid'],
                    chunk_index + 1
                )

                result['context'] = {
                    'previous': prev_chunk['chunk_text'] if prev_chunk else None,
                    'next': next_chunk['chunk_text'] if next_chunk else None
                }

    finally:
        client.close()

    return results


def display_results_text(query: str, results: List[Dict], show_context: bool = False):
    """
    Display search results in human-readable text format

    Args:
        query: Original search query
        results: Search results
        show_context: Show surrounding chunks
    """
    print()
    print("=" * 80)
    print(f"📺 Search Results for: \"{query}\"")
    print("=" * 80)
    print()

    if not results:
        print("No results found. Try:")
        print("  - Lowering --min-similarity threshold")
        print("  - Using different search terms")
        print("  - Checking if videos have been ingested")
        print()
        return

    print(f"Found {len(results)} result(s)\n")

    for idx, result in enumerate(results, 1):
        # Header
        print(f"{'─' * 80}")
        print(f"Result {idx}: {result['title']}")
        print(f"{'─' * 80}")

        # Metadata
        print(f"Author: {result.get('author', 'Unknown')}")
        print(f"Video ID: {result['video_id']}")

        if result.get('timestamp_start') is not None:
            timestamp = format_timestamp(result['timestamp_start'])
            print(f"Timestamp: {timestamp}")
            print(f"URL: https://youtube.com/watch?v={result['video_id']}&t={int(result['timestamp_start'])}s")

        print(f"Chunk Type: {result['chunk_type']}")
        print(f"Similarity: {format_similarity_bar(result['similarity'])}")
        print()

        # Content
        if show_context and result.get('context'):
            # Show previous chunk (dimmed)
            if result['context']['previous']:
                print("┌─ Previous chunk ─────────────────────────────────────────────┐")
                prev_text = result['context']['previous'][:150]
                print(f"│ {prev_text}{'...' if len(result['context']['previous']) > 150 else ''}")
                print("└──────────────────────────────────────────────────────────────┘")
                print()

        # Main content
        print("Content:")
        print(f"{result['chunk_text']}")
        print()

        if show_context and result.get('context'):
            # Show next chunk (dimmed)
            if result['context']['next']:
                print("┌─ Next chunk ─────────────────────────────────────────────────┐")
                next_text = result['context']['next'][:150]
                print(f"│ {next_text}{'...' if len(result['context']['next']) > 150 else ''}")
                print("└──────────────────────────────────────────────────────────────┘")
                print()

    print("=" * 80)
    print(f"Total results: {len(results)}")
    print("=" * 80)
    print()


def display_results_json(results: List[Dict]):
    """
    Display search results in JSON format

    Args:
        results: Search results
    """
    # Remove binary data for JSON serialization
    clean_results = []
    for result in results:
        clean = {k: v for k, v in result.items() if k not in ['embedding']}
        clean_results.append(clean)

    print(json.dumps(clean_results, indent=2, default=str))


def display_results_markdown(query: str, results: List[Dict]):
    """
    Display search results in Markdown format

    Args:
        query: Original search query
        results: Search results
    """
    print(f"# Search Results: \"{query}\"\n")

    if not results:
        print("*No results found.*\n")
        return

    print(f"**Found {len(results)} result(s)**\n")

    for idx, result in enumerate(results, 1):
        print(f"## {idx}. {result['title']}\n")
        print(f"- **Author**: {result.get('author', 'Unknown')}")
        print(f"- **Video ID**: `{result['video_id']}`")

        if result.get('timestamp_start') is not None:
            timestamp = format_timestamp(result['timestamp_start'])
            url = f"https://youtube.com/watch?v={result['video_id']}&t={int(result['timestamp_start'])}s"
            print(f"- **Timestamp**: [{timestamp}]({url})")

        print(f"- **Similarity**: {result['similarity']:.3f}")
        print(f"- **Type**: {result['chunk_type']}\n")

        # Content
        if result['chunk_type'] == 'code':
            print(f"```\n{result['chunk_text']}\n```\n")
        else:
            print(f"{result['chunk_text']}\n")

        print("---\n")


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Semantic search for YouTube RAG content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python search_content.py "How to implement RAG with Claude"

  # Search with custom limit and threshold
  python search_content.py "vector databases" --limit 20 --min-similarity 0.75

  # Search within specific video
  python search_content.py "Python code" --video-id dQw4w9WgXcQ

  # Filter by chunk type
  python search_content.py "examples" --chunk-type code

  # JSON output for AI agents
  python search_content.py "query" --format json > results.json

  # Show surrounding chunks for context
  python search_content.py "RAG" --show-context --limit 5
        """
    )

    parser.add_argument(
        'query',
        help='Search query (natural language)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of results (default: 10)'
    )
    parser.add_argument(
        '--min-similarity',
        type=float,
        default=0.7,
        help='Minimum similarity threshold 0-1 (default: 0.7)'
    )
    parser.add_argument(
        '--video-id',
        help='Filter by specific video ID'
    )
    parser.add_argument(
        '--chunk-type',
        choices=['transcript', 'code', 'heading', 'diagram'],
        help='Filter by chunk type'
    )
    parser.add_argument(
        '--show-context',
        action='store_true',
        help='Show surrounding chunks for context'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--embedding-model',
        choices=['text-embedding-3-small', 'text-embedding-3-large'],
        default='text-embedding-3-small',
        help='OpenAI embedding model (default: text-embedding-3-small)'
    )

    args = parser.parse_args()

    # Validate environment
    if not os.getenv('OPENAI_API_KEY'):
        print("[ERROR] OPENAI_API_KEY environment variable not set")
        print("[HELP] Set it with: export OPENAI_API_KEY=sk-...")
        sys.exit(1)

    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'):
        print("[ERROR] Supabase credentials not set")
        print("[HELP] Set environment variables:")
        print("       export SUPABASE_URL=https://your-project.supabase.co")
        print("       export SUPABASE_KEY=your-service-role-key")
        sys.exit(1)

    try:
        # Perform search
        results = search_youtube_content(
            query=args.query,
            limit=args.limit,
            min_similarity=args.min_similarity,
            video_id=args.video_id,
            chunk_type=args.chunk_type,
            show_context=args.show_context,
            embedding_model=args.embedding_model
        )

        # Display results in requested format
        if args.format == 'json':
            display_results_json(results)
        elif args.format == 'markdown':
            display_results_markdown(args.query, results)
        else:  # text
            display_results_text(args.query, results, show_context=args.show_context)

        # Exit code based on results
        sys.exit(0 if results else 1)

    except KeyboardInterrupt:
        print("\n[CANCELLED] Search cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Search failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
