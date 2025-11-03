# Sample Ingestion Example

This document shows a complete example of ingesting a YouTube video into the RAG system, including all outputs and verification steps.

**Author**: AI Project Template Team
**Created**: 2025-10-28
**Task**: 044-6
**Example Video**: Sample tutorial on RAG implementation (simulated)

---

## Scenario

**Goal**: Ingest a technical tutorial video about RAG (Retrieval-Augmented Generation) implementation

**Video Details**:
- **URL**: `https://www.youtube.com/watch?v=example123` (simulated)
- **Title**: "Building Production RAG Systems with Claude"
- **Author**: "AI Engineer"
- **Duration**: 45 minutes (2700 seconds)
- **Content**: Technical tutorial covering RAG architecture, vector databases, chunking strategies, and Claude integration

---

## Step 1: Pre-Ingestion Setup

### Environment Check

```bash
# Verify environment variables
$ env | grep -E '(OPENAI|SUPABASE)'
OPENAI_API_KEY=sk-proj-abc123...
SUPABASE_HOST=db.xxxxxxxxxxxx.supabase.co
SUPABASE_PASSWORD=your-secure-password
```

### Dependencies Check

```bash
# Test imports
$ python -c "import openai, psycopg2, dockling; print('✓ All dependencies installed')"
✓ All dependencies installed
```

### Database Connection Test

```bash
$ python scripts/db/test_connection.py
Testing Supabase connection...
[OK] Connected to Supabase database (pool: 1-10 connections)
✓ Successfully connected to Supabase!
✓ PostgreSQL version: PostgreSQL 15.6 on x86_64-pc-linux-gnu
✓ pgvector version: 0.5.1
✓ Tables found: transcript_chunks, visual_content, youtube_videos

✓ All tests passed! Database is ready.
[OK] Database connection pool closed
```

---

## Step 2: Run Ingestion

### Command

```bash
$ python scripts/rag/ingest_video.py https://www.youtube.com/watch?v=example123
```

### Complete Output

```
================================================================================
YouTube RAG Ingestion Pipeline
================================================================================

Video URL: https://www.youtube.com/watch?v=example123
Output Directory: ./youtube_rag_data/example123
Timestamp: 2025-10-28 14:35:22

================================================================================
STEP 1: Download & Transcribe
================================================================================

Video URL: https://www.youtube.com/watch?v=example123
Downloading... 100.0%

Title: Building Production RAG Systems with Claude
Author: AI Engineer
Duration: 2700 seconds (45 minutes)
Views: 125,430

[OK] Downloaded: ./youtube_rag_data/example123/video.mp4

================================================================================
STEP 2: Extract Audio
================================================================================

Trying moviepy for audio extraction...
[OK] Audio extracted (moviepy): ./youtube_rag_data/example123/audio.mp3

================================================================================
STEP 3: Transcribe Audio
================================================================================

Loading Whisper model (base)...
Transcribing audio (this may take a few minutes)...
[OK] Transcription complete!
   Length: 45,820 characters

First 500 characters:
--------------------------------------------------------------------------------
In this video, I'll walk you through building a production-ready RAG system
using Claude and pgvector. We'll cover everything from setting up your vector
database, to chunking strategies, to integrating with Claude for intelligent
retrieval. By the end of this tutorial, you'll have a fully functional RAG
system that can answer questions based on your knowledge base. Let's start
with the architecture overview. A RAG system consists of three main components:
a document store, a vector database, and a large language model...
--------------------------------------------------------------------------------

================================================================================
STEP 2: Intelligent Chunking
================================================================================

[OK] Created 87 chunks using Dockling

Chunking Statistics:
  Total chunks: 87
  Average chunk size: 168.4 words
  Min/Max size: 52/245 words
  Chunks with code: 23
  Chunks with headings: 8
  Chunk type distribution:
    - transcript: 56
    - code: 23
    - heading: 8

================================================================================
STEP 3: Generate Embeddings
================================================================================

[INFO] Estimated cost: $0.000294 (14,655 tokens)

[INFO] Generating embeddings for 87 texts in 1 batches...
[OK] Batch 1/1: 87 texts, 14,892 tokens, $0.000298

[OK] Generated 87 embeddings

================================================================================
EMBEDDING COST SUMMARY
================================================================================
Model: text-embedding-3-small
Total tokens: 14,892
Total cost: $0.000298
Average cost per 1K tokens: $0.00002000
================================================================================

================================================================================
STEP 4: Store in Database
================================================================================

[INFO] Inserting video metadata...
[OK] Inserted/updated video: example123 (UUID: 7c8f3d2e-1a4b-5c6d-9e7f-8a9b0c1d2e3f)
[OK] Video UUID: 7c8f3d2e-1a4b-5c6d-9e7f-8a9b0c1d2e3f
[INFO] Inserting 87 chunks with embeddings...
[OK] Inserted 87 chunks for video 7c8f3d2e-1a4b-5c6d-9e7f-8a9b0c1d2e3f
[OK] Stored 87 chunks
[OK] Database connection pool closed

================================================================================
INGESTION COMPLETE
================================================================================

Video ID: example123
Video UUID: 7c8f3d2e-1a4b-5c6d-9e7f-8a9b0c1d2e3f
Title: Building Production RAG Systems with Claude
Duration: 45 minutes
Chunks stored: 87
Embedding cost: $0.000298
Processing time: 287.5 seconds (4.8 minutes)

Ready for semantic search!

[INFO] Saved ingestion result to: ./youtube_rag_data/example123/ingestion_result.json
```

---

## Step 3: Verify Ingestion

### Check Database Entry

```python
from scripts.db.db_client import SupabaseClient

client = SupabaseClient()

# Get video by ID
video = client.get_video_by_id('example123')
print(f"Video UUID: {video['id']}")
print(f"Title: {video['title']}")
print(f"Author: {video['author']}")
print(f"Duration: {video['duration_seconds']} seconds")
print(f"Chunks: {video['transcript_full'][:100]}...")

# Get chunks
chunks = client.get_chunks_by_video(video['id'], limit=5)
print(f"\nFirst 5 chunks:")
for i, chunk in enumerate(chunks, 1):
    print(f"\n{i}. Type: {chunk['chunk_type']}, Index: {chunk['chunk_index']}")
    print(f"   Text: {chunk['chunk_text'][:100]}...")
    print(f"   Embedding dims: {len(chunk.get('embedding', []))}")

client.close()
```

**Output**:
```
[OK] Connected to Supabase database (pool: 1-10 connections)
Video UUID: 7c8f3d2e-1a4b-5c6d-9e7f-8a9b0c1d2e3f
Title: Building Production RAG Systems with Claude
Author: AI Engineer
Duration: 2700 seconds
Chunks: In this video, I'll walk you through building a production-ready RAG system using Claude and p...

First 5 chunks:

1. Type: heading, Index: 0
   Text: # Introduction to RAG Systems

   In this comprehensive tutorial, we'll explore how to build produ...
   Embedding dims: 1536

2. Type: transcript, Index: 1
   Text: A RAG system combines the power of large language models with external knowledge retrieval. T...
   Embedding dims: 1536

3. Type: code, Index: 2
   Text: ```python
   from openai import OpenAI
   import anthropic

   # Initialize clients
   openai_client = OpenAI()
   ...
   Embedding dims: 1536

4. Type: transcript, Index: 3
   Text: The key advantage of RAG is that it allows the LLM to access up-to-date information without...
   Embedding dims: 1536

5. Type: heading, Index: 4
   Text: ## Setting Up Your Vector Database

   For this tutorial, we'll use PostgreSQL with pgvector...
   Embedding dims: 1536

[OK] Database connection pool closed
```

---

## Step 4: Test Semantic Search

### Search Query 1: "How do I set up pgvector?"

```bash
$ python scripts/rag/semantic_search.py "How do I set up pgvector?"
```

**Output**:
```
[INFO] Generating query embedding...
[INFO] Searching database...

================================================================================
📺 Search Results for: "How do I set up pgvector?"
================================================================================

Found 10 results:

1. Building Production RAG Systems with Claude by AI Engineer
   Similarity: 0.894 (Excellent)
   Timestamp: 12:45
   Type: heading
   ## Setting Up Your Vector Database

   For this tutorial, we'll use PostgreSQL with pgvector. First, you need to
   install the extension...

2. Building Production RAG Systems with Claude by AI Engineer
   Similarity: 0.872 (Very Good)
   Timestamp: 13:20
   Type: code
   ```sql
   -- Enable pgvector extension
   CREATE EXTENSION IF NOT EXISTS vector;

   -- Create table with vector column
   CREATE TABLE embeddings (
       id UUID PRIMARY KEY,
       content TEXT,
       embedding vector(1536)
   );
   ```

3. Building Production RAG Systems with Claude by AI Engineer
   Similarity: 0.845 (Very Good)
   Timestamp: 14:10
   Type: transcript
   After enabling the extension, you'll want to create an index for faster
   similarity searches. The IVFFlat index works well for most use cases...

[7 more results...]

================================================================================
```

### Search Query 2: "Claude integration code examples"

```bash
$ python scripts/rag/semantic_search.py "Claude integration code examples" --chunk-type code --limit 5
```

**Output**:
```
[INFO] Generating query embedding...
[INFO] Searching database...

================================================================================
📺 Search Results for: "Claude integration code examples"
================================================================================

Found 5 results:

1. Building Production RAG Systems with Claude by AI Engineer
   Similarity: 0.911 (Excellent)
   Timestamp: 28:30
   Type: code
   ```python
   from anthropic import Anthropic

   client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

   def query_with_context(query: str, context: str):
       message = client.messages.create(
           model="claude-3-5-sonnet-20241022",
           max_tokens=1024,
           messages=[{
               "role": "user",
               "content": f"Context: {context}\n\nQuestion: {query}"
           }]
       )
       return message.content[0].text
   ```

2. Building Production RAG Systems with Claude by AI Engineer
   Similarity: 0.887 (Excellent)
   Timestamp: 31:15
   Type: code
   ```python
   def rag_query(query: str, limit: int = 5):
       # 1. Generate query embedding
       query_embedding = generate_embedding(query)

       # 2. Search vector database
       results = search_database(query_embedding, limit=limit)

       # 3. Build context from results
       context = "\n\n".join([r['text'] for r in results])

       # 4. Query Claude with context
       response = query_with_context(query, context)
       return response
   ```

[3 more results...]

================================================================================
```

---

## Step 5: Advanced Search Examples

### Multi-Video Search (After Ingesting Multiple Videos)

```bash
# Search across all videos
$ python scripts/rag/semantic_search.py "best practices for chunking strategies"
```

**Result**: Returns relevant chunks from multiple videos, ranked by similarity

### Search with Similarity Threshold

```bash
# Only show high-quality matches
$ python scripts/rag/semantic_search.py "vector database performance" --min-similarity 0.8
```

**Result**: Filters out results below 0.8 similarity (Very Good or Excellent only)

### Export Search Results

```bash
# Export to JSON for further processing
$ python scripts/rag/semantic_search.py "RAG architecture patterns" --export results.json --limit 20
```

**result.json**:
```json
{
  "query": "RAG architecture patterns",
  "limit": 20,
  "num_results": 18,
  "filters": {},
  "results": [
    {
      "id": "chunk-uuid-1",
      "chunk_text": "The fundamental RAG architecture consists of...",
      "similarity": 0.892,
      "title": "Building Production RAG Systems with Claude",
      "author": "AI Engineer",
      "timestamp_start": 8.5,
      "chunk_type": "transcript"
    },
    ...
  ]
}
```

---

## Performance Metrics

### Ingestion Performance

| Metric | Value |
|--------|-------|
| Video Duration | 45 minutes |
| Download Time | ~30 seconds |
| Transcription Time | ~180 seconds (3 min) |
| Chunking Time | <1 second |
| Embedding Generation | ~5 seconds |
| Database Storage | ~2 seconds |
| **Total Time** | **~287 seconds (4.8 min)** |

### Cost Breakdown

| Item | Cost |
|------|------|
| OpenAI Embeddings | $0.000298 |
| Supabase Storage (3.4MB) | $0 (free tier) |
| **Total Cost** | **$0.000298** |

### Storage Usage

| Component | Size |
|-----------|------|
| Video metadata | ~8 KB |
| Full transcript | ~45 KB |
| Chunks (87 × 500 bytes) | ~43 KB |
| Embeddings (87 × 6 KB) | ~522 KB |
| **Total per video** | **~618 KB** |

### Search Performance

| Metric | Value |
|--------|-------|
| Query embedding generation | ~200ms |
| Vector similarity search | ~85ms |
| Result formatting | ~5ms |
| **Total query time** | **~290ms** |

---

## Files Created

```
./youtube_rag_data/example123/
├── video.mp4              # Downloaded video
├── audio.mp3              # Extracted audio
├── metadata.json          # Video metadata
├── transcript.txt         # Full transcript
├── ingestion_result.json  # Ingestion summary
└── README.md             # Navigation guide
```

---

## Summary

**Ingestion Successful** ✓

- **Video**: "Building Production RAG Systems with Claude" (45 min)
- **Chunks Created**: 87 (56 transcript, 23 code, 8 headings)
- **Embeddings Generated**: 87 vectors (1536 dimensions each)
- **Database Storage**: Complete (video + chunks + embeddings)
- **Cost**: $0.000298 (essentially FREE!)
- **Time**: 4.8 minutes (6.4x faster than video length)
- **Search Quality**: Excellent (0.85+ similarity for relevant queries)

**Next Steps**:
1. Ingest more videos to build knowledge base
2. Experiment with different search queries
3. Try filtered searches (by video, chunk type, etc.)
4. Build SubAgent for complex research tasks (Task 044-10)

---

**Example complete!** This video is now fully searchable in the RAG system.