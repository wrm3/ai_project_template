#!/usr/bin/env python3
"""
RAG Workflow Example: Complete pipeline for ingesting YouTube videos into vector databases

This example demonstrates:
1. Download and transcribe video
2. Extract frames with smart selection
3. Generate embeddings
4. Store in vector database (Supabase pgvector, Chroma, Pinecone, or Weaviate)
5. Query and retrieve similar content

Requirements:
    pip install openai anthropic sentence-transformers supabase chromadb pinecone-client weaviate-client

Usage:
    # Ingest a single video
    python rag_workflow_example.py --video-url "https://youtube.com/watch?v=..." --vector-db supabase

    # Query the knowledge base
    python rag_workflow_example.py --query "How do I use React hooks?" --vector-db supabase

    # Batch ingest from playlist
    python rag_workflow_example.py --playlist-url "https://youtube.com/playlist?list=..." --vector-db supabase
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_video import download_video, extract_audio, transcribe_audio
from frame_extractor import FrameExtractor
from smart_frame_selector import SmartFrameSelector
from tqdm import tqdm


class VideoRAGPipeline:
    """
    Complete RAG pipeline for YouTube videos

    Features:
    - Download and transcribe videos
    - Extract key frames
    - Generate embeddings (OpenAI, local, or Anthropic)
    - Store in vector database
    - Semantic search and retrieval
    """

    def __init__(
        self,
        vector_db_type: str = "supabase",
        embedding_model: str = "openai",
        output_dir: str = "./rag_output"
    ):
        """
        Initialize RAG pipeline

        Args:
            vector_db_type: Type of vector database ("supabase", "chroma", "pinecone", "weaviate")
            embedding_model: Embedding model ("openai", "local", "anthropic")
            output_dir: Output directory for intermediate files
        """
        self.vector_db_type = vector_db_type
        self.embedding_model = embedding_model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize vector database client
        self.vector_db = self._initialize_vector_db()

        # Initialize embedding model
        self.embedder = self._initialize_embedder()

    def _initialize_vector_db(self):
        """Initialize vector database client"""
        if self.vector_db_type == "supabase":
            from supabase import create_client
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")
            return create_client(url, key)

        elif self.vector_db_type == "chroma":
            import chromadb
            return chromadb.Client()

        elif self.vector_db_type == "pinecone":
            import pinecone
            api_key = os.getenv("PINECONE_API_KEY")
            if not api_key:
                raise ValueError("PINECONE_API_KEY must be set in environment")
            pinecone.init(api_key=api_key, environment=os.getenv("PINECONE_ENV", "us-west1-gcp"))
            return pinecone

        elif self.vector_db_type == "weaviate":
            import weaviate
            url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
            return weaviate.Client(url)

        else:
            raise ValueError(f"Unsupported vector database: {self.vector_db_type}")

    def _initialize_embedder(self):
        """Initialize embedding model"""
        if self.embedding_model == "openai":
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY must be set in environment")
            return openai

        elif self.embedding_model == "local":
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer('all-MiniLM-L6-v2')

        elif self.embedding_model == "anthropic":
            import anthropic
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY must be set in environment")
            return anthropic.Anthropic(api_key=api_key)

        else:
            raise ValueError(f"Unsupported embedding model: {self.embedding_model}")

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        print(f"Generating embeddings for {len(texts)} text chunks...")
        embeddings = []

        if self.embedding_model == "openai":
            # OpenAI embeddings (batch processing)
            for i in tqdm(range(0, len(texts), 100), desc="Embedding chunks"):
                batch = texts[i:i+100]
                response = self.embedder.Embedding.create(
                    model="text-embedding-ada-002",
                    input=batch
                )
                embeddings.extend([item['embedding'] for item in response['data']])

        elif self.embedding_model == "local":
            # Local sentence-transformers
            embeddings = self.embedder.encode(texts, show_progress_bar=True).tolist()

        elif self.embedding_model == "anthropic":
            # Anthropic embeddings (when available)
            # Note: As of 2025-11, Anthropic doesn't have a public embeddings API
            # This is a placeholder for future implementation
            raise NotImplementedError("Anthropic embeddings not yet available")

        print(f"[OK] Generated {len(embeddings)} embeddings")
        return embeddings

    def chunk_transcript(self, transcript: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """
        Split transcript into chunks with overlap

        Args:
            transcript: Full transcript text
            chunk_size: Number of words per chunk
            overlap: Number of words to overlap between chunks

        Returns:
            List of chunk dicts with text and metadata
        """
        words = transcript.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)

            chunks.append({
                'text': chunk_text,
                'start_word': i,
                'end_word': i + len(chunk_words),
                'chunk_index': len(chunks)
            })

        print(f"[OK] Split transcript into {len(chunks)} chunks")
        return chunks

    def ingest_video(
        self,
        video_url: str,
        video_type: str = "general",
        extract_frames: bool = True,
        smart_frames: bool = True,
        collection_name: str = "youtube_videos"
    ) -> Dict[str, Any]:
        """
        Complete RAG ingestion pipeline for a single video

        Args:
            video_url: YouTube video URL
            video_type: Type of video (for metadata)
            extract_frames: Whether to extract frames
            smart_frames: Use smart frame selection
            collection_name: Vector database collection name

        Returns:
            Ingestion result dict
        """
        print("=" * 80)
        print(f"RAG INGESTION PIPELINE")
        print("=" * 80)
        print()
        print(f"Video URL: {video_url}")
        print(f"Vector DB: {self.vector_db_type}")
        print(f"Embedding Model: {self.embedding_model}")
        print(f"Collection: {collection_name}")
        print()

        start_time = datetime.now()
        video_output_dir = self.output_dir / f"video_{int(start_time.timestamp())}"
        video_output_dir.mkdir(exist_ok=True)

        # Step 1: Download video
        print("Step 1: Downloading video...")
        video_path, metadata = download_video(video_url, str(video_output_dir))
        video_id = video_url.split('=')[-1].split('&')[0]

        # Step 2: Extract audio
        print("\nStep 2: Extracting audio...")
        audio_path = extract_audio(video_path, str(video_output_dir))

        # Step 3: Transcribe
        print("\nStep 3: Transcribing...")
        transcript = transcribe_audio(audio_path, model_size="base")

        # Step 4: Extract frames (if requested)
        frames_data = []
        if extract_frames:
            print("\nStep 4: Extracting frames...")
            frames_dir = video_output_dir / "frames"

            if smart_frames:
                selector = SmartFrameSelector(output_dir=str(frames_dir))
                frames = selector.select_frames(video_path, metadata, enable_ocr=True)
            else:
                extractor = FrameExtractor(output_dir=str(frames_dir), interval_seconds=30)
                frames = extractor.extract_frames(video_path, metadata)

            frames_data = frames
            print(f"[OK] Extracted {len(frames)} frames")

        # Step 5: Chunk transcript
        print("\nStep 5: Chunking transcript...")
        chunks = self.chunk_transcript(transcript, chunk_size=500, overlap=50)

        # Step 6: Generate embeddings
        print("\nStep 6: Generating embeddings...")
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = self.generate_embeddings(chunk_texts)

        # Step 7: Store in vector database
        print("\nStep 7: Storing in vector database...")
        self._store_in_vector_db(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings,
            metadata={
                'video_id': video_id,
                'video_url': video_url,
                'video_title': metadata.get('title', 'Unknown'),
                'video_type': video_type,
                'duration': metadata.get('duration', 0),
                'author': metadata.get('author', 'Unknown'),
                'processed_at': start_time.isoformat(),
                'frames_count': len(frames_data)
            }
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print()
        print("=" * 80)
        print("INGESTION COMPLETE")
        print("=" * 80)
        print()
        print(f"Video: {metadata.get('title', 'Unknown')}")
        print(f"Duration: {metadata.get('duration', 0)} seconds")
        print(f"Chunks: {len(chunks)}")
        print(f"Frames: {len(frames_data)}")
        print(f"Processing Time: {duration:.1f} seconds")
        print()

        return {
            'video_id': video_id,
            'video_url': video_url,
            'metadata': metadata,
            'chunks_count': len(chunks),
            'frames_count': len(frames_data),
            'processing_time': duration,
            'collection': collection_name
        }

    def _store_in_vector_db(
        self,
        collection_name: str,
        chunks: List[Dict],
        embeddings: List[List[float]],
        metadata: Dict
    ):
        """Store chunks and embeddings in vector database"""

        if self.vector_db_type == "supabase":
            # Supabase pgvector storage
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                self.vector_db.table('youtube_chunks').insert({
                    'content': chunk['text'],
                    'embedding': embedding,
                    'metadata': {**metadata, **chunk},
                    'collection': collection_name
                }).execute()

        elif self.vector_db_type == "chroma":
            # ChromaDB storage
            collection = self.vector_db.get_or_create_collection(collection_name)
            collection.add(
                documents=[chunk['text'] for chunk in chunks],
                embeddings=embeddings,
                metadatas=[{**metadata, **chunk} for chunk in chunks],
                ids=[f"{metadata['video_id']}_chunk_{i}" for i in range(len(chunks))]
            )

        elif self.vector_db_type == "pinecone":
            # Pinecone storage
            index_name = collection_name.replace('_', '-')  # Pinecone naming rules
            if index_name not in self.vector_db.list_indexes():
                self.vector_db.create_index(index_name, dimension=len(embeddings[0]))

            index = self.vector_db.Index(index_name)
            vectors = [
                (f"{metadata['video_id']}_chunk_{i}", embedding, {**metadata, **chunk})
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
            ]
            index.upsert(vectors)

        elif self.vector_db_type == "weaviate":
            # Weaviate storage
            class_name = collection_name.title().replace('_', '')

            # Create schema if not exists
            if not self.vector_db.schema.exists(class_name):
                self.vector_db.schema.create_class({
                    'class': class_name,
                    'vectorizer': 'none',
                    'properties': [
                        {'name': 'content', 'dataType': ['text']},
                        {'name': 'metadata', 'dataType': ['object']}
                    ]
                })

            # Add vectors
            with self.vector_db.batch as batch:
                for chunk, embedding in zip(chunks, embeddings):
                    batch.add_data_object(
                        {
                            'content': chunk['text'],
                            'metadata': {**metadata, **chunk}
                        },
                        class_name,
                        vector=embedding
                    )

        print(f"[OK] Stored {len(chunks)} chunks in {self.vector_db_type}")

    def query(
        self,
        query_text: str,
        collection_name: str = "youtube_videos",
        top_k: int = 5
    ) -> List[Dict]:
        """
        Query the vector database for similar content

        Args:
            query_text: Query string
            collection_name: Collection to search
            top_k: Number of results to return

        Returns:
            List of result dicts with content and metadata
        """
        print(f"Querying: {query_text}")

        # Generate query embedding
        query_embedding = self.generate_embeddings([query_text])[0]

        # Search vector database
        if self.vector_db_type == "supabase":
            # Supabase pgvector search
            results = self.vector_db.rpc('match_youtube_chunks', {
                'query_embedding': query_embedding,
                'match_count': top_k,
                'filter': {'collection': collection_name}
            }).execute()

            return [
                {
                    'content': r['content'],
                    'metadata': r['metadata'],
                    'similarity': r['similarity']
                }
                for r in results.data
            ]

        elif self.vector_db_type == "chroma":
            # ChromaDB search
            collection = self.vector_db.get_collection(collection_name)
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            return [
                {
                    'content': doc,
                    'metadata': meta,
                    'similarity': 1 - dist  # Convert distance to similarity
                }
                for doc, meta, dist in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )
            ]

        elif self.vector_db_type == "pinecone":
            # Pinecone search
            index_name = collection_name.replace('_', '-')
            index = self.vector_db.Index(index_name)
            results = index.query(query_embedding, top_k=top_k, include_metadata=True)

            return [
                {
                    'content': match['metadata'].get('text', ''),
                    'metadata': match['metadata'],
                    'similarity': match['score']
                }
                for match in results['matches']
            ]

        elif self.vector_db_type == "weaviate":
            # Weaviate search
            class_name = collection_name.title().replace('_', '')
            results = (
                self.vector_db.query
                .get(class_name, ['content', 'metadata'])
                .with_near_vector({'vector': query_embedding})
                .with_limit(top_k)
                .with_additional(['distance'])
                .do()
            )

            return [
                {
                    'content': r['content'],
                    'metadata': r['metadata'],
                    'similarity': 1 - r['_additional']['distance']
                }
                for r in results['data']['Get'][class_name]
            ]


def main():
    """CLI interface for RAG workflow"""
    parser = argparse.ArgumentParser(description='YouTube Video RAG Workflow')

    # Mode selection
    parser.add_argument('--video-url', help='Single video URL to ingest')
    parser.add_argument('--playlist-url', help='Playlist URL for batch ingestion')
    parser.add_argument('--query', help='Query string to search knowledge base')

    # Configuration
    parser.add_argument('--vector-db', default='supabase',
                       choices=['supabase', 'chroma', 'pinecone', 'weaviate'],
                       help='Vector database type')
    parser.add_argument('--embedding-model', default='openai',
                       choices=['openai', 'local', 'anthropic'],
                       help='Embedding model')
    parser.add_argument('--collection', default='youtube_videos',
                       help='Collection name in vector database')
    parser.add_argument('--output-dir', default='./rag_output',
                       help='Output directory')
    parser.add_argument('--no-frames', action='store_true',
                       help='Skip frame extraction')
    parser.add_argument('--basic-frames', action='store_true',
                       help='Use basic frame extraction (not smart selection)')
    parser.add_argument('--top-k', type=int, default=5,
                       help='Number of results for query')

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = VideoRAGPipeline(
        vector_db_type=args.vector_db,
        embedding_model=args.embedding_model,
        output_dir=args.output_dir
    )

    # Execute based on mode
    if args.video_url:
        # Ingest single video
        result = pipeline.ingest_video(
            video_url=args.video_url,
            extract_frames=not args.no_frames,
            smart_frames=not args.basic_frames,
            collection_name=args.collection
        )
        print(f"\n✓ Video ingested successfully!")
        print(f"✓ Video ID: {result['video_id']}")
        print(f"✓ Chunks: {result['chunks_count']}")
        print(f"✓ Frames: {result['frames_count']}")

    elif args.playlist_url:
        # Batch ingestion
        from batch_processor import BatchProcessor

        def process_func(video_url, output_dir):
            return pipeline.ingest_video(
                video_url=video_url,
                extract_frames=not args.no_frames,
                smart_frames=not args.basic_frames,
                collection_name=args.collection
            )

        processor = BatchProcessor(
            output_dir=args.output_dir,
            process_function=process_func
        )
        results = processor.process_playlist(args.playlist_url)

        print(f"\n✓ Batch ingestion complete!")
        print(f"✓ Total videos: {results['statistics'].total_videos}")
        print(f"✓ Successful: {results['statistics'].successful}")
        print(f"✓ Failed: {results['statistics'].failed}")

    elif args.query:
        # Query knowledge base
        results = pipeline.query(
            query_text=args.query,
            collection_name=args.collection,
            top_k=args.top_k
        )

        print(f"\n✓ Found {len(results)} results:\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['similarity']:.3f}] {result['metadata'].get('video_title', 'Unknown')}")
            print(f"   {result['content'][:200]}...")
            print()

    else:
        print("Error: Must specify --video-url, --playlist-url, or --query")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
