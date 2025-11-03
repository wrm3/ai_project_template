#!/usr/bin/env python3
"""
Cache Management CLI for YouTube Video Analysis
Manage cache with stats, validation, clearing, and pruning operations.

Usage:
    python cache_cli.py stats                    # Show cache statistics
    python cache_cli.py clear                    # Clear all cache
    python cache_cli.py clear VIDEO_ID           # Clear specific video
    python cache_cli.py prune                    # Remove expired entries
    python cache_cli.py validate                 # Validate cache integrity
    python cache_cli.py size                     # Show cache sizes
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from cache.cache_manager import CacheManager
except ImportError:
    print("[ERROR] Could not import CacheManager")
    print("Make sure you're running from the scripts directory")
    sys.exit(1)


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} TB"


def cmd_stats(cache_manager: CacheManager, args):
    """Show cache statistics"""
    cache_manager.print_stats()


def cmd_clear(cache_manager: CacheManager, args):
    """Clear cache (all or specific video)"""
    if args.video_id:
        # Clear specific video
        video_id = cache_manager.extract_video_id(args.video_id)
        print(f"\n[INFO] Clearing cache for video: {video_id}")

        deleted = cache_manager.clear_video(video_id)

        if deleted > 0:
            print(f"[OK] Deleted {deleted} cache entries")
        else:
            print(f"[INFO] No cache found for video: {video_id}")
    else:
        # Clear all
        if not args.force:
            confirm = input("\n⚠️  This will delete ALL cached data. Continue? (y/N): ")
            if confirm.lower() != 'y':
                print("[CANCELLED] Cache clear cancelled")
                return

        print("\n[INFO] Clearing all cache...")
        deleted = cache_manager.clear_all()
        print(f"[OK] Deleted {deleted} cache entries")


def cmd_prune(cache_manager: CacheManager, args):
    """Remove expired cache entries"""
    print(f"\n[INFO] Pruning expired cache (TTL: {cache_manager.ttl_hours} hours)")

    deleted = cache_manager.prune_expired()

    if deleted > 0:
        print(f"[OK] Deleted {deleted} expired entries")
    else:
        print(f"[INFO] No expired entries found")


def cmd_validate(cache_manager: CacheManager, args):
    """Validate cache integrity"""
    print("\n" + "=" * 80)
    print("CACHE VALIDATION")
    print("=" * 80)
    print()

    report = cache_manager.validate_cache()

    # Print summary
    if report['valid']:
        print("✓ Cache is valid")
    else:
        print("✗ Cache has issues")

    print()

    # Transcripts
    print(f"Transcripts: {report['transcripts']['count']} total")
    if report['transcripts']['invalid']:
        print(f"  ✗ {len(report['transcripts']['invalid'])} invalid:")
        for item in report['transcripts']['invalid']:
            print(f"    - {item}")

    # Embeddings
    print(f"\nEmbeddings: {report['embeddings']['count']} total")
    if report['embeddings']['invalid']:
        print(f"  ✗ {len(report['embeddings']['invalid'])} invalid:")
        for item in report['embeddings']['invalid']:
            print(f"    - {item}")

    # Frames
    print(f"\nFrames: {report['frames']['count']} total")
    if report['frames']['invalid']:
        print(f"  ✗ {len(report['frames']['invalid'])} invalid:")
        for item in report['frames']['invalid']:
            print(f"    - {item}")

    # Analysis
    print(f"\nAnalysis: {report['analysis']['count']} total")
    if report['analysis']['invalid']:
        print(f"  ✗ {len(report['analysis']['invalid'])} invalid:")
        for item in report['analysis']['invalid']:
            print(f"    - {item}")
    if report['analysis']['expired']:
        print(f"  ⚠️  {len(report['analysis']['expired'])} expired:")
        for item in report['analysis']['expired']:
            print(f"    - {item}")

    print()


def cmd_size(cache_manager: CacheManager, args):
    """Show cache sizes"""
    print("\n" + "=" * 80)
    print("CACHE SIZE BREAKDOWN")
    print("=" * 80)
    print()

    sizes = cache_manager.get_cache_size()

    # Print each category
    for category, size in sorted(sizes.items()):
        if category != 'total':
            print(f"{category.capitalize():15} {format_bytes(size):>12}")

    print("-" * 30)
    print(f"{'TOTAL':15} {format_bytes(sizes['total']):>12}")
    print()


def cmd_list(cache_manager: CacheManager, args):
    """List cached videos"""
    print("\n" + "=" * 80)
    print("CACHED VIDEOS")
    print("=" * 80)
    print()

    # Get unique video IDs from all cache types
    video_ids = set()

    # From transcripts
    for file in cache_manager.transcript_dir.glob("*.txt"):
        video_ids.add(file.stem)

    # From embeddings
    for file in cache_manager.embedding_dir.glob("*.pkl"):
        video_id = file.stem.replace('_embeddings', '')
        video_ids.add(video_id)

    # From frames
    for dir in cache_manager.frame_dir.iterdir():
        if dir.is_dir():
            video_ids.add(dir.name)

    # From analysis
    for file in cache_manager.analysis_dir.glob("*.json"):
        video_id = file.stem.replace('_analysis', '')
        video_ids.add(video_id)

    if not video_ids:
        print("No cached videos found")
        print()
        return

    # Print table
    print(f"{'Video ID':15} {'Transcript':12} {'Embeddings':12} {'Frames':12} {'Analysis':12}")
    print("-" * 63)

    for video_id in sorted(video_ids):
        has_transcript = cache_manager.has_transcript(video_id)
        has_embeddings = cache_manager.has_embeddings(video_id)
        has_frames = cache_manager.has_frames(video_id)
        has_analysis = cache_manager.has_analysis(video_id)

        print(f"{video_id:15} "
              f"{'✓' if has_transcript else '-':^12} "
              f"{'✓' if has_embeddings else '-':^12} "
              f"{'✓' if has_frames else '-':^12} "
              f"{'✓' if has_analysis else '-':^12}")

    print()
    print(f"Total: {len(video_ids)} videos")
    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Cache Management CLI for YouTube Video Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Show cache statistics
  python cache_cli.py stats

  # Show cache sizes
  python cache_cli.py size

  # List all cached videos
  python cache_cli.py list

  # Validate cache integrity
  python cache_cli.py validate

  # Clear specific video cache
  python cache_cli.py clear FOqbS_llAms

  # Clear ALL cache (with confirmation)
  python cache_cli.py clear

  # Remove expired entries
  python cache_cli.py prune

  # Clear cache without confirmation
  python cache_cli.py clear --force
        '''
    )

    parser.add_argument('--cache-dir', default='.cache',
                       help='Cache directory (default: .cache)')
    parser.add_argument('--ttl', type=int,
                       help='TTL for analysis cache in hours (default: 168)')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # stats command
    subparsers.add_parser('stats', help='Show cache statistics')

    # clear command
    clear_parser = subparsers.add_parser('clear', help='Clear cache')
    clear_parser.add_argument('video_id', nargs='?',
                             help='Video ID or URL to clear (omit to clear all)')
    clear_parser.add_argument('--force', action='store_true',
                             help='Skip confirmation prompt')

    # prune command
    subparsers.add_parser('prune', help='Remove expired cache entries')

    # validate command
    subparsers.add_parser('validate', help='Validate cache integrity')

    # size command
    subparsers.add_parser('size', help='Show cache sizes')

    # list command
    subparsers.add_parser('list', help='List cached videos')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Create cache manager
    cache_kwargs = {'cache_dir': args.cache_dir}
    if args.ttl:
        cache_kwargs['ttl_hours'] = args.ttl

    cache_manager = CacheManager(**cache_kwargs)

    # Execute command
    commands = {
        'stats': cmd_stats,
        'clear': cmd_clear,
        'prune': cmd_prune,
        'validate': cmd_validate,
        'size': cmd_size,
        'list': cmd_list
    }

    try:
        commands[args.command](cache_manager, args)
    except KeyboardInterrupt:
        print("\n[CANCELLED] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
