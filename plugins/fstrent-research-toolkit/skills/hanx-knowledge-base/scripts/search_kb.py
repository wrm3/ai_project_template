#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Knowledge Base Search Interface

Command-line interface for searching the knowledge base using semantic search.

Usage:
    # Basic search
    python search_kb.py "What is RAG?"

    # Search with filters
    python search_kb.py "machine learning" --category technical --limit 10

    # Get detailed results
    python search_kb.py "vector databases" --verbose

    # Export results to JSON
    python search_kb.py "embeddings" --output results.json
"""

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from knowledge_base import KnowledgeBase
from rag_utils import SearchResult


def format_result(
    result: SearchResult,
    index: int,
    verbose: bool = False
) -> str:
    """
    Format search result for display

    Args:
        result: SearchResult object
        index: Result index (1-based)
        verbose: Show all metadata

    Returns:
        Formatted string
    """
    lines = []
    lines.append(f"\n{'=' * 80}")
    lines.append(f"Result {index}")
    lines.append(f"{'=' * 80}")

    # Relevance score
    score_bar = "█" * int(result.score * 20)
    lines.append(f"Relevance: {result.score:.4f} {score_bar}")

    # Metadata
    metadata = result.metadata
    lines.append(f"Category: {metadata.get('category', 'unknown')}")
    lines.append(f"Source: {metadata.get('file_name', metadata.get('source', 'unknown'))}")

    if verbose:
        lines.append(f"\nMetadata:")
        for key, value in metadata.items():
            if key not in ['category', 'file_name', 'source']:
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 80:
                    value_str = value_str[:77] + "..."
                lines.append(f"  {key}: {value_str}")

    # Content
    lines.append(f"\nContent:")
    lines.append("-" * 80)
    lines.append(result.text)
    lines.append("-" * 80)

    return "\n".join(lines)


def search_knowledge_base(
    kb_path: str,
    query: str,
    category: str = None,
    limit: int = 5,
    min_score: float = 0.0,
    verbose: bool = False,
    output_file: str = None
) -> List[SearchResult]:
    """
    Search knowledge base and display results

    Args:
        kb_path: Path to knowledge base
        query: Search query
        category: Filter by category
        limit: Maximum results
        min_score: Minimum relevance score
        verbose: Show detailed metadata
        output_file: Export results to JSON

    Returns:
        List of search results
    """
    print("=" * 80)
    print("Knowledge Base Search")
    print("=" * 80)
    print()
    print(f"Knowledge Base: {kb_path}")
    print(f"Query: \"{query}\"")
    if category:
        print(f"Category Filter: {category}")
    print(f"Max Results: {limit}")
    if min_score > 0:
        print(f"Min Score: {min_score}")
    print()

    # Initialize knowledge base
    kb = KnowledgeBase(kb_path, auto_load=True)

    # Perform search
    print("[SEARCH] Searching knowledge base...")
    results = kb.search(query, limit=limit, category=category)

    # Filter by minimum score
    if min_score > 0:
        results = [r for r in results if r.score >= min_score]

    print(f"[SEARCH] Found {len(results)} results\n")

    # Display results
    if not results:
        print("No results found.")
        print("\nTry:")
        print("  - Using different keywords")
        print("  - Removing category filter")
        print("  - Lowering minimum score threshold")
        return []

    for i, result in enumerate(results, 1):
        print(format_result(result, i, verbose))

    # Export to JSON if requested
    if output_file:
        export_data = {
            "query": query,
            "category": category,
            "total_results": len(results),
            "results": [
                {
                    "index": i,
                    "score": result.score,
                    "text": result.text,
                    "metadata": result.metadata
                }
                for i, result in enumerate(results, 1)
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        print(f"\n[EXPORT] Results saved to: {output_file}")

    return results


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Search knowledge base using semantic search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python search_kb.py "What is RAG?"

  # Search in specific category
  python search_kb.py "machine learning" --category technical

  # Get more results
  python search_kb.py "vector databases" --limit 10

  # Filter by minimum relevance
  python search_kb.py "embeddings" --min-score 0.7

  # Detailed output
  python search_kb.py "semantic search" --verbose

  # Export results
  python search_kb.py "knowledge base" --output results.json
        """
    )

    parser.add_argument(
        'query',
        help='Search query'
    )

    parser.add_argument(
        '--kb-path',
        default='./data/knowledge_base',
        help='Path to knowledge base (default: ./data/knowledge_base)'
    )

    parser.add_argument(
        '--category',
        help='Filter by category'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='Maximum number of results (default: 5)'
    )

    parser.add_argument(
        '--min-score',
        type=float,
        default=0.0,
        help='Minimum relevance score 0.0-1.0 (default: 0.0)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed metadata'
    )

    parser.add_argument(
        '--output',
        help='Export results to JSON file'
    )

    args = parser.parse_args()

    try:
        results = search_knowledge_base(
            kb_path=args.kb_path,
            query=args.query,
            category=args.category,
            limit=args.limit,
            min_score=args.min_score,
            verbose=args.verbose,
            output_file=args.output
        )

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
