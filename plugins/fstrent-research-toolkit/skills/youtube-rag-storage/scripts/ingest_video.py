"""
YouTube Video Ingestion Pipeline for RAG Storage

Complete workflow from YouTube URL to searchable vector database:
1. Download and transcribe video (youtube-video-analysis)
2. Chunk transcript intelligently (Dockling)
3. Generate embeddings (OpenAI)
4. Store in Supabase vector database

Usage:
    python ingest_video.py https://www.youtube.com/watch?v=VIDEO_ID

    python ingest_video.py URL --output-dir ./data --whisper-model medium
"""

import sys
import os
import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional
import json

# Add parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent))

# Import from youtube-video-analysis skill
try:
    from youtube_video_analysis.scripts.analyze_video import (
        download_video,
        extract_audio,
        transcribe_audio,
        extract_video_id
    )
except ImportError:
    print("[ERROR] Could not import youtube-video-analysis skill")
    print("[HELP] Ensure youtube-video-analysis skill is installed")
    sys.exit(1)

# Import Dockling chunker (from Task 044-5)
try:
    # Assuming dockling_chunker is available
    # If not, we'll implement a simple chunker
    from dockling_chunker import chunk_transcript_with_dockling
    HAS_DOCKLING = True
except ImportError:
    HAS_DOCKLING = False
    print("[WARNING] Dockling chunker not found, using simple chunker")

# Import database client (from Task 044-4)
try:
    from db_client import SupabaseClient
except ImportError:
    print("[ERROR] Database client not found")
    print("[HELP] Ensure db_client.py exists (from Task 044-4)")
    sys.exit(1)

# Import embeddings
from embeddings import EmbeddingGenerator


def simple_chunk_transcript(
    transcript: str,
    metadata: Dict,
    chunk_size: int = 512,
    overlap: int = 128
) -> List[Dict]:
    """
    Simple chunking fallback if Dockling is not available

    Args:
        transcript: Full transcript text
        metadata: Video metadata
        chunk_size: Target tokens per chunk
        overlap: Overlap tokens between chunks

    Returns:
        List of chunk dictionaries
    """
    words = transcript.split()
    chunks = []
    chunk_index = 0

    # Approximate: 1 token ≈ 0.75 words
    words_per_chunk = int(chunk_size * 0.75)
    words_overlap = int(overlap * 0.75)

    for i in range(0, len(words), words_per_chunk - words_overlap):
        chunk_words = words[i:i + words_per_chunk]
        chunk_text = " ".join(chunk_words)

        if not chunk_text.strip():
            continue

        chunks.append({
            'chunk_text': chunk_text,
            'chunk_index': chunk_index,
            'chunk_type': 'transcript',
            'word_count': len(chunk_words),
            'char_count': len(chunk_text),
            'has_code': False,
            'has_diagram': False,
            'metadata': {}
        })

        chunk_index += 1

    return chunks


def ingest_video(
    video_url: str,
    output_dir: str = "youtube_analysis/output",
    whisper_model: str = "base",
    skip_download: bool = False,
    embedding_model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> Dict:
    """
    Complete video ingestion pipeline

    Args:
        video_url: YouTube video URL
        output_dir: Directory for downloaded files
        whisper_model: Whisper model size
        skip_download: Skip download if files exist
        embedding_model: OpenAI embedding model
        batch_size: Embedding batch size

    Returns:
        Ingestion statistics and results
    """
    print("=" * 80)
    print("YouTube RAG Ingestion Pipeline")
    print("=" * 80)
    print()
    print(f"Video URL: {video_url}")
    print(f"Output directory: {output_dir}")
    print(f"Whisper model: {whisper_model}")
    print(f"Embedding model: {embedding_model}")
    print()

    start_time = time.time()

    # Extract video ID
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {video_url}")

    print(f"Video ID: {video_id}")
    print()

    # ==========================
    # STEP 1: Download & Transcribe
    # ==========================
    print("=" * 80)
    print("STEP 1: Download & Transcribe")
    print("=" * 80)
    print()

    step1_start = time.time()

    # Download video
    print("[1/3] Downloading video...")
    video_path, metadata = download_video(video_url, output_dir)
    print(f"[OK] Downloaded: {metadata['title']}")
    print(f"[OK] Author: {metadata['author']}")
    print(f"[OK] Duration: {metadata['duration_minutes']:.1f} minutes ({metadata['duration_seconds']}s)")
    print()

    # Extract audio
    print("[2/3] Extracting audio...")
    audio_path = extract_audio(video_path, output_dir)
    print(f"[OK] Audio extracted: {audio_path}")
    print()

    # Transcribe
    print(f"[3/3] Transcribing with Whisper ({whisper_model} model)...")
    transcript = transcribe_audio(audio_path, model_size=whisper_model)
    print(f"[OK] Transcribed: {len(transcript)} characters")
    print(f"[OK] Words: ~{len(transcript.split())} words")
    print()

    step1_time = time.time() - step1_start
    print(f"Step 1 complete in {step1_time:.1f}s\n")

    # ==========================
    # STEP 2: Intelligent Chunking
    # ==========================
    print("=" * 80)
    print("STEP 2: Intelligent Chunking")
    print("=" * 80)
    print()

    step2_start = time.time()

    if HAS_DOCKLING:
        print("[CHUNKING] Using Dockling HybridChunker (document-aware)")
        chunks = chunk_transcript_with_dockling(transcript, metadata)
    else:
        print("[CHUNKING] Using simple chunker (fallback)")
        chunks = simple_chunk_transcript(transcript, metadata)

    print(f"[OK] Created {len(chunks)} chunks")

    # Count chunk types
    chunk_types = {}
    for chunk in chunks:
        chunk_type = chunk.get('chunk_type', 'unknown')
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1

    print(f"[TYPES] Chunk breakdown:")
    for chunk_type, count in chunk_types.items():
        print(f"        - {count} {chunk_type} chunks")
    print()

    step2_time = time.time() - step2_start
    print(f"Step 2 complete in {step2_time:.1f}s\n")

    # ==========================
    # STEP 3: Generate Embeddings
    # ==========================
    print("=" * 80)
    print("STEP 3: Generate Embeddings")
    print("=" * 80)
    print()

    step3_start = time.time()

    # Extract text from chunks
    chunk_texts = [chunk['chunk_text'] for chunk in chunks]

    # Generate embeddings
    generator = EmbeddingGenerator(model=embedding_model)
    embeddings, stats = generator.generate_embeddings_batch(
        chunk_texts,
        batch_size=batch_size,
        show_progress=True
    )

    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, embeddings):
        chunk['embedding'] = embedding.tolist()  # Convert numpy array to list for JSON

    step3_time = time.time() - step3_start
    print(f"Step 3 complete in {step3_time:.1f}s\n")

    # ==========================
    # STEP 4: Store in Database
    # ==========================
    print("=" * 80)
    print("STEP 4: Store in Vector Database")
    print("=" * 80)
    print()

    step4_start = time.time()

    # Prepare video data
    video_data = {
        'video_id': video_id,
        'url': video_url,
        'title': metadata['title'],
        'author': metadata.get('author'),
        'duration_seconds': metadata.get('duration_seconds'),
        'views': metadata.get('views'),
        'description': metadata.get('description'),
        'transcript_full': transcript,
        'metadata': metadata
    }

    # Insert into database
    print("[1/2] Inserting video metadata...")
    client = SupabaseClient()

    try:
        video_uuid = client.insert_video(video_data)
        print(f"[OK] Video inserted with UUID: {video_uuid}")
        print()

        print(f"[2/2] Inserting {len(chunks)} chunks with embeddings...")
        client.insert_chunks(video_uuid, chunks)
        print(f"[OK] All chunks stored successfully")
        print()

    finally:
        client.close()

    step4_time = time.time() - step4_start
    print(f"Step 4 complete in {step4_time:.1f}s\n")

    # ==========================
    # Summary
    # ==========================
    total_time = time.time() - start_time

    print("=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)
    print()
    print(f"✅ Video ID: {video_id}")
    print(f"✅ Title: {metadata['title']}")
    print(f"✅ Duration: {metadata['duration_minutes']:.1f} minutes")
    print()
    print(f"📊 Statistics:")
    print(f"   - Chunks created: {len(chunks)}")
    print(f"   - Embeddings generated: {len(embeddings)}")
    print(f"   - Total tokens: {stats.total_tokens:,}")
    print(f"   - Embedding cost: ${stats.cost_usd:.6f}")
    print(f"   - Video UUID: {video_uuid}")
    print()
    print(f"⏱️  Time breakdown:")
    print(f"   - Download & Transcribe: {step1_time:.1f}s")
    print(f"   - Chunking: {step2_time:.1f}s")
    print(f"   - Embeddings: {step3_time:.1f}s")
    print(f"   - Database Storage: {step4_time:.1f}s")
    print(f"   - TOTAL: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print()
    print("=" * 80)
    print("Ready for semantic search!")
    print(f"Try: python search_content.py \"your query here\"")
    print("=" * 80)
    print()

    return {
        'video_id': video_id,
        'video_uuid': str(video_uuid),
        'title': metadata['title'],
        'chunks_created': len(chunks),
        'embeddings_generated': len(embeddings),
        'total_tokens': stats.total_tokens,
        'embedding_cost_usd': stats.cost_usd,
        'total_time_seconds': total_time,
        'steps': {
            'download_transcribe': step1_time,
            'chunking': step2_time,
            'embeddings': step3_time,
            'database': step4_time
        }
    }


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Ingest YouTube video into RAG vector database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python ingest_video.py https://www.youtube.com/watch?v=VIDEO_ID

  # Custom settings
  python ingest_video.py URL --output-dir ./data --whisper-model medium

  # Skip download if already exists
  python ingest_video.py URL --skip-download

  # Use larger embedding model (higher quality, 6.5x cost)
  python ingest_video.py URL --embedding-model text-embedding-3-large
        """
    )

    parser.add_argument(
        'url',
        help='YouTube video URL'
    )
    parser.add_argument(
        '--output-dir',
        default='youtube_analysis/output',
        help='Output directory for downloaded files (default: youtube_analysis/output)'
    )
    parser.add_argument(
        '--whisper-model',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base',
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip download if video already exists'
    )
    parser.add_argument(
        '--embedding-model',
        choices=['text-embedding-3-small', 'text-embedding-3-large'],
        default='text-embedding-3-small',
        help='OpenAI embedding model (default: text-embedding-3-small)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Embedding batch size (default: 100)'
    )
    parser.add_argument(
        '--output-json',
        help='Save statistics to JSON file'
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
        # Run ingestion
        results = ingest_video(
            video_url=args.url,
            output_dir=args.output_dir,
            whisper_model=args.whisper_model,
            skip_download=args.skip_download,
            embedding_model=args.embedding_model,
            batch_size=args.batch_size
        )

        # Save JSON output if requested
        if args.output_json:
            with open(args.output_json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"[SAVED] Statistics saved to: {args.output_json}")

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n[CANCELLED] Ingestion cancelled by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
