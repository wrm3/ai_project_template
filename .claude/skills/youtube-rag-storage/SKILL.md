---
name: youtube-rag-storage
description: Ingest YouTube content into vector database with embeddings for semantic search and RAG. Combines video download, transcription, chunking, embedding generation, and Supabase storage for intelligent content retrieval.
triggers:
  - "ingest this YouTube video into RAG"
  - "store YouTube content for semantic search"
  - "add this video to the knowledge base"
  - "search my YouTube knowledge base"
  - "find videos about"
dependencies:
  - youtube-video-analysis (download + transcribe)
  - dockling_chunker (intelligent chunking)
  - db_client (Supabase storage)
  - openai (embeddings)
version: 1.0.0
---

# YouTube RAG Storage Skill

Store YouTube video content in a vector database with semantic embeddings for intelligent search and retrieval-augmented generation (RAG).

## Overview

This skill provides end-to-end RAG storage for YouTube videos:

1. **Download & Transcribe**: Uses youtube-video-analysis skill to get video content
2. **Intelligent Chunking**: Uses Dockling to preserve code blocks, headings, and structure
3. **Generate Embeddings**: Creates 1536-dimension vectors using OpenAI text-embedding-3-small
4. **Store in Supabase**: Saves chunks + embeddings in PostgreSQL + pgvector database
5. **Semantic Search**: Query content using natural language vector similarity

## When to Use This Skill

### Automatic Triggers
- User says "ingest this YouTube video" or "add to RAG"
- User wants to "search across multiple videos"
- User requests "semantic search" or "find similar content"
- User mentions "build a knowledge base from YouTube"

### Manual Invocation
```bash
# Ingest a single video
python scripts/rag/ingest_video.py https://youtu.be/VIDEO_ID

# Search across all ingested content
python scripts/rag/semantic_search.py "RAG implementation best practices"

# Search within specific video
python scripts/rag/semantic_search.py "vector database" --video-id VIDEO_ID
```

## Core Capabilities

### 1. Video Ingestion Pipeline

**Complete workflow from URL to searchable content:**

```
YouTube URL
    ↓
[Download + Transcribe] (youtube-video-analysis)
    ↓
[Intelligent Chunking] (dockling_chunker)
    ↓
[Generate Embeddings] (OpenAI API)
    ↓
[Store in Supabase] (db_client)
    ↓
Searchable Vector Database
```

**Features:**
- Automatic video metadata extraction
- Transcript-aware chunking (preserves code blocks, headings)
- Batch embedding generation (efficient API usage)
- Atomic database transactions
- Progress tracking and error recovery
- Cost estimation and tracking

### 2. Embedding Generation

**OpenAI text-embedding-3-small specifications:**
- **Dimensions**: 1536
- **Cost**: $0.020 per 1M tokens
- **Performance**: ~130 tokens per chunk average
- **Quality**: State-of-the-art semantic similarity

**Batch processing:**
- Processes up to 2048 texts per API request
- Automatic retry logic for transient failures
- Token counting and cost estimation
- Progress indicators for large batches

### 3. Semantic Search

**Vector similarity using cosine distance:**

```python
# Search by natural language query
results = semantic_search(
    query="How to implement RAG with Claude",
    limit=10,
    min_similarity=0.7
)

# Filter by video or chunk type
results = semantic_search(
    query="Python code examples",
    video_id="dQw4w9WgXcQ",
    chunk_type="code",
    limit=5
)
```

**Search capabilities:**
- Semantic similarity (not just keyword matching)
- Filter by video, author, chunk type, date range
- Minimum similarity threshold
- Ranked results with similarity scores
- Includes context (timestamps, video metadata)

### 4. Multi-Modal Content Support

**Handles diverse content types:**
- **Transcript chunks**: Regular spoken content
- **Code blocks**: Programming examples preserved with syntax
- **Diagrams**: Visual content descriptions (when available)
- **Mixed content**: Combined text + code sections

**Metadata preserved:**
- Video title, author, duration, views
- Chunk timestamps (when in video)
- Word/character counts
- Structural information (headings, lists)
- Custom metadata (tags, notes)

## Workflow Examples

### Example 1: Ingest Tutorial Video

**User**: "Ingest this FastAPI tutorial into the knowledge base: https://youtu.be/example"

**Skill Actions**:
1. Download video and transcribe (uses youtube-video-analysis)
2. Chunk transcript with Dockling (preserves code blocks)
3. Generate embeddings for each chunk (OpenAI API)
4. Store in Supabase with full metadata
5. Report ingestion stats (chunks, cost, time)

**Output**:
```
================================================================================
YouTube RAG Ingestion Pipeline
================================================================================

STEP 1: Download & Transcribe
[OK] Downloaded: FastAPI Complete Tutorial by TechWithTim
[OK] Duration: 45:30 (2730 seconds)
[OK] Transcribed: 18,500 characters

STEP 2: Intelligent Chunking
[OK] Created 48 chunks using Dockling
     - 32 transcript chunks
     - 12 code chunks
     - 4 heading chunks

STEP 3: Generate Embeddings
[OK] Generated 48 embeddings (1536 dimensions each)
     - Processed: 6,240 tokens
     - Cost: $0.00012

STEP 4: Store in Database
[OK] Inserted video metadata
[OK] Stored 48 chunks with embeddings
     - Video UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

================================================================================
INGESTION COMPLETE
================================================================================

Video ID: dQw4w9WgXcQ
Chunks stored: 48
Total cost: $0.00012
Processing time: 2m 15s
Ready for semantic search!
```

### Example 2: Semantic Search

**User**: "Search my knowledge base for: implementing RAG with vector databases"

**Skill Actions**:
1. Generate query embedding (OpenAI API)
2. Search Supabase using vector similarity
3. Retrieve top K most relevant chunks
4. Format results with context

**Output**:
```
📺 Search Results for: "implementing RAG with vector databases"

================================================================================

1. Building Production RAG Systems by AI Jason (0.892 similarity)
   Timestamp: 12:45
   Type: transcript
   "When implementing RAG, you need three core components: a vector database
   like Supabase with pgvector, an embedding model like OpenAI's
   text-embedding-3-small, and a chunking strategy that preserves context..."

2. Vector Databases Explained by Coding with Cole (0.874 similarity)
   Timestamp: 08:20
   Type: code
   ```python
   def semantic_search(query: str, limit: int = 10):
       # Generate query embedding
       embedding = openai.Embedding.create(
           model="text-embedding-3-small",
           input=query
       )
       # Search database with cosine similarity
       results = db.query(embedding, limit=limit)
       return results
   ```

3. RAG Tutorial: From Zero to Production by Tech Lead (0.856 similarity)
   Timestamp: 25:10
   Type: transcript
   "The key insight is that vector databases use approximate nearest neighbor
   search algorithms like IVFFlat or HNSW to find similar embeddings quickly.
   For a dataset of 100K chunks, search takes under 100ms..."

[7 more results...]

Total results: 10
Search time: 87ms
```

### Example 3: Multi-Video Research

**User**: "Find all mentions of 'Claude API integration' across my entire knowledge base"

**Skill Actions**:
1. Search across all stored videos
2. Group results by video
3. Show relevant sections with timestamps

**Output**:
```
📺 Found mentions in 4 videos:

Video 1: "Claude API Tutorial" by Anthropic Docs (3 mentions)
  - 05:30: Setting up authentication with API keys
  - 12:45: Streaming responses with Claude 3.5 Sonnet
  - 28:10: Error handling and retry logic

Video 2: "Building AI Agents" by AI Engineer (2 mentions)
  - 18:20: Integrating Claude into agent workflows
  - 35:50: Tool use and function calling with Claude

Video 3: "FastAPI + Claude" by Python Tutorial (2 mentions)
  - 09:15: Creating API endpoints for Claude integration
  - 22:40: Async request handling

Video 4: "Production AI Apps" by Tech With Tim (1 mention)
  - 41:05: Deploying Claude-powered applications
```

## Integration with Existing Systems

### YouTube Video Analysis Skill
```python
from youtube_video_analysis import download_video, extract_audio, transcribe_audio

# Reuse existing functionality
video_path, metadata = download_video(url, output_dir)
audio_path = extract_audio(video_path, output_dir)
transcript = transcribe_audio(audio_path, model_size='base')
```

### Dockling Chunker
```python
from dockling_chunker import chunk_transcript_with_dockling

# Intelligent structure-aware chunking
chunks = chunk_transcript_with_dockling(
    transcript=transcript,
    video_metadata=metadata,
    min_chunk_size=400,
    max_chunk_size=1000,
    overlap_tokens=50
)
```

### Supabase Database Client
```python
from db_client import SupabaseClient

client = SupabaseClient()
video_uuid = client.insert_video(video_data)
client.insert_chunks(video_uuid, chunks)
results = client.semantic_search(query_embedding, limit=10)
client.close()
```

### OpenAI Embeddings
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)
embeddings = [e.embedding for e in response.data]
```

## Technical Specifications

### Embedding Model
- **Model**: text-embedding-3-small
- **Dimensions**: 1536
- **Context Window**: 8192 tokens
- **Pricing**: $0.020 per 1M tokens
- **Performance**: 300K+ tokens per minute

### Database Schema
```sql
-- Video metadata
CREATE TABLE youtube_videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    duration_seconds INTEGER,
    views BIGINT,
    description TEXT,
    transcript_full TEXT,
    visual_analysis JSONB,
    metadata JSONB,
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Transcript chunks with embeddings
CREATE TABLE transcript_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id UUID REFERENCES youtube_videos(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_type TEXT NOT NULL,
    timestamp_start NUMERIC,
    timestamp_end NUMERIC,
    embedding vector(1536) NOT NULL,
    word_count INTEGER,
    char_count INTEGER,
    has_code BOOLEAN DEFAULT FALSE,
    has_diagram BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(video_id, chunk_index)
);

-- Vector similarity index (IVFFlat)
CREATE INDEX idx_chunks_embedding ON transcript_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Performance Characteristics

**Ingestion Performance** (1-hour video):
- Download: ~30 seconds (depends on network)
- Transcription: ~90 seconds (base model, CPU)
- Chunking: <1 second
- Embedding generation: ~5 seconds
- Database storage: ~2 seconds
- **Total**: ~2-3 minutes

**Search Performance**:
- Query embedding generation: ~200ms
- Vector search (100K chunks): <100ms
- Result formatting: <10ms
- **Total query time**: ~300ms

**Storage Requirements** (per 1-hour video):
- Video metadata: ~10KB
- Full transcript: ~100KB
- Chunks (avg 500): 500 × 500 bytes = 250KB
- Embeddings (500 × 1536 × 4 bytes): 3.07MB
- **Total per video**: ~3.4MB

### Cost Analysis

**OpenAI Embeddings** (per video):
```
1-hour video:
- Transcript: ~30K words = 40K tokens
- Chunked into: ~500 chunks
- Embedding tokens: 500 chunks × 130 tokens avg = 65K tokens
- Cost: 65K × $0.020 / 1M = $0.0013

3-hour video:
- Embedding tokens: ~195K tokens
- Cost: $0.0039

Cost per video: ~$0.001 to $0.004 (essentially FREE!)
```

**Supabase Storage**:
```
Free Tier: 500MB database storage
- ~147 videos at 3.4MB each
- Sufficient for prototyping and small-scale use

Pro Tier: $25/month for 8GB
- ~2,400 videos
- Production-ready scale
```

**Total Cost** (100 videos):
- Embeddings: 100 × $0.002 = **$0.20**
- Storage: **$0** (free tier)
- **Total**: ~$0.20

## Usage Instructions

### Setup (One-time)

1. **Install Dependencies**:
```bash
pip install openai psycopg2-binary pgvector python-dotenv
```

2. **Configure Environment**:
```bash
# .env file
OPENAI_API_KEY=sk-your-openai-api-key
SUPABASE_HOST=db.xxxxxxxxxxxx.supabase.co
SUPABASE_PASSWORD=your-supabase-password
```

3. **Verify Setup**:
```bash
python scripts/db/test_connection.py
```

### Ingest Videos

**Single video**:
```bash
python scripts/rag/ingest_video.py https://youtu.be/VIDEO_ID
```

**Multiple videos**:
```bash
# Create a list of URLs
echo "https://youtu.be/VIDEO1" >> videos.txt
echo "https://youtu.be/VIDEO2" >> videos.txt

# Batch ingest
for url in $(cat videos.txt); do
    python scripts/rag/ingest_video.py "$url"
done
```

**With custom settings**:
```bash
python scripts/rag/ingest_video.py \
    https://youtu.be/VIDEO_ID \
    --output-dir ./data/youtube \
    --model-size small \
    --min-chunk-size 400 \
    --max-chunk-size 1000
```

### Search Content

**Basic search**:
```bash
python scripts/rag/semantic_search.py "RAG implementation with Claude"
```

**Advanced search**:
```bash
# Search with filters
python scripts/rag/semantic_search.py \
    "Python code examples" \
    --limit 20 \
    --min-similarity 0.7 \
    --chunk-type code

# Search within specific video
python scripts/rag/semantic_search.py \
    "vector database setup" \
    --video-id dQw4w9WgXcQ \
    --limit 5
```

**Programmatic usage**:
```python
from scripts.rag.semantic_search import search_youtube_content

results = search_youtube_content(
    query="How to implement RAG",
    limit=10,
    min_similarity=0.7,
    video_id=None  # Search all videos
)

for result in results:
    print(f"Video: {result['title']}")
    print(f"Similarity: {result['similarity']:.3f}")
    print(f"Text: {result['chunk_text'][:200]}...")
```

## Best Practices

### Video Selection
- ✅ Choose high-quality educational content
- ✅ Prefer structured tutorials and technical videos
- ✅ Ensure clear audio for accurate transcription
- ❌ Avoid music videos or entertainment content
- ❌ Skip videos with poor audio quality

### Chunking Strategy
- **Default settings work well** for most content
- Increase `max_chunk_size` for longer, detailed explanations
- Decrease `min_chunk_size` for short, dense content
- Use `overlap_tokens` to maintain context between chunks

### Embedding Quality
- **Text-embedding-3-small** is optimal for cost/performance
- Chunk size affects semantic coherence (400-1000 words ideal)
- Include video metadata in search context for better relevance

### Search Optimization
- Use specific queries for better results
- Adjust `min_similarity` threshold (0.7 is good default)
- Filter by `chunk_type` for code vs text searches
- Combine semantic search with metadata filters (author, date)

### Cost Management
- Embeddings are cheap (~$0.002 per video)
- Main cost is Supabase storage at scale
- Cache embeddings to avoid regeneration
- Use free tier (500MB) for prototyping

## Limitations

### Current Limitations
- **Visual content**: Only transcripts, no frame analysis (yet)
- **Timestamps**: Chunk-level only (no word-level alignment)
- **Languages**: Best results with English content
- **Real-time**: Must download and process first (no streaming)
- **Authentication**: Public videos only (no private content)

### Performance Constraints
- Large videos (>3 hours) may need chunking optimization
- Search performance degrades beyond 1M chunks (add sharding)
- Embedding generation limited by OpenAI API rate limits
- Database connection pool may need tuning for high concurrency

## Troubleshooting

### Common Issues

**Issue**: "OpenAI API key not found"
```bash
# Solution: Set environment variable
export OPENAI_API_KEY=sk-your-api-key-here
# Or add to .env file
```

**Issue**: "Database connection failed"
```bash
# Solution: Check Supabase credentials
python scripts/db/test_connection.py
```

**Issue**: "Embedding dimension mismatch"
```python
# Solution: Ensure using text-embedding-3-small (1536 dimensions)
# Check model name in generate_embeddings.py
```

**Issue**: "Out of memory during embedding generation"
```python
# Solution: Reduce batch size
# In generate_embeddings.py, change batch_size from 2048 to 100
```

**Issue**: "Search returns no results"
```bash
# Solution: Lower similarity threshold
python scripts/rag/semantic_search.py "query" --min-similarity 0.5
```

## Future Enhancements

### Planned Features (Task 044 Roadmap)
- [ ] **Multi-modal analysis**: Extract code from video frames (Task 044-1)
- [ ] **Smart frame selection**: Detect code/diagram screenshots (Task 044-2)
- [ ] **Voice input**: Search with spoken queries (Task 044-7)
- [ ] **Batch processing**: Ingest entire playlists efficiently (Task 044-8)
- [ ] **Progress indicators**: Real-time status updates (Task 044-9)
- [ ] **SubAgent integration**: Complex multi-video research (Task 044-10)
- [ ] **MCP server**: Expose to Claude Desktop (Task 044-11)

### Potential Improvements
- [ ] Automatic chapter detection and segmentation
- [ ] Speaker diarization (who said what)
- [ ] Multi-language support with translation
- [ ] Real-time streaming ingestion
- [ ] Automatic tag generation
- [ ] Content recommendation engine
- [ ] Duplicate detection across videos
- [ ] Incremental updates (only new content)

## Reference Documentation

- **[Embedding Guide](reference/embedding_guide.md)**: Deep dive into OpenAI embeddings
- **[Semantic Search Guide](reference/semantic_search_guide.md)**: Vector similarity techniques
- **[Database Schema](reference/database_schema.md)**: Complete schema documentation
- **[Supabase Setup](../../docs/SUPABASE_SETUP_GUIDE.md)**: Database setup instructions

## Examples

- **[Ingestion Workflow](examples/sample_ingestion.md)**: Step-by-step ingestion example
- **[Search Examples](examples/search_examples.md)**: Various search patterns
- **[Cost Analysis](examples/cost_analysis.md)**: Detailed cost breakdown

## Scripts

- **[ingest_video.py](../../scripts/rag/ingest_video.py)**: Main ingestion pipeline
- **[generate_embeddings.py](../../scripts/rag/generate_embeddings.py)**: Embedding generation
- **[semantic_search.py](../../scripts/rag/semantic_search.py)**: Search interface

---

**Version**: 1.0.0
**Created**: 2025-10-28
**Status**: Production Ready
**Task**: 044-6
**Dependencies**: youtube-video-analysis, dockling_chunker, db_client, openai
