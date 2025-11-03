# YouTube Video Ingestion Workflow Template

This template provides a step-by-step workflow for ingesting YouTube videos into the RAG system.

**Author**: AI Project Template Team
**Created**: 2025-10-28
**Task**: 044-6

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Environment Variables Set**:
  - `OPENAI_API_KEY` - OpenAI API key for embeddings
  - `SUPABASE_HOST` - Supabase database host
  - `SUPABASE_PASSWORD` - Supabase database password

- [ ] **Dependencies Installed**:
  ```bash
  pip install openai psycopg2-binary pgvector python-dotenv pytubefix openai-whisper moviepy dockling
  ```

- [ ] **Database Setup Complete**:
  - Supabase project created
  - pgvector extension enabled
  - Migrations run (001_initial_schema.sql)

- [ ] **Test Connection**:
  ```bash
  python scripts/db/test_connection.py
  ```

---

## Workflow Steps

### Step 1: Prepare YouTube Video URL

**Action**: Identify the YouTube video you want to ingest

**Valid URL formats**:
- Full URL: `https://www.youtube.com/watch?v=VIDEO_ID`
- Short URL: `https://youtu.be/VIDEO_ID`
- Video ID only: `VIDEO_ID` (11 characters)

**Example**:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Considerations**:
- Ensure video is public (not private or unlisted)
- Check video length (>2 hours may take longer to process)
- Verify audio quality is clear for accurate transcription

---

### Step 2: Run Ingestion Pipeline

**Command**:
```bash
python scripts/rag/ingest_video.py <YOUTUBE_URL>
```

**Full example**:
```bash
python scripts/rag/ingest_video.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**With custom output directory**:
```bash
python scripts/rag/ingest_video.py https://youtu.be/dQw4w9WgXcQ ./my_videos/video1
```

**Without keeping files** (clean up after ingestion):
```bash
python scripts/rag/ingest_video.py https://youtu.be/dQw4w9WgXcQ --no-keep-files
```

---

### Step 3: Monitor Progress

The pipeline will show progress for each step:

**Expected output**:
```
================================================================================
YouTube RAG Ingestion Pipeline
================================================================================

Video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Output Directory: ./youtube_rag_data/dQw4w9WgXcQ
Timestamp: 2025-10-28 14:30:00

================================================================================
STEP 1: Download & Transcribe
================================================================================

Video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Downloading... 100.0%

Title: Example Video Title
Author: Example Channel
Duration: 180 seconds (3 minutes)
Views: 100,000

[OK] Downloaded: ./youtube_rag_data/dQw4w9WgXcQ/video.mp4

================================================================================
STEP 2: Extract Audio
================================================================================

[OK] Audio extracted (moviepy): ./youtube_rag_data/dQw4w9WgXcQ/audio.mp3

================================================================================
STEP 3: Transcribe Audio
================================================================================

Loading Whisper model (base)...
Transcribing audio (this may take a few minutes)...
[OK] Transcription complete!
   Length: 5420 characters

================================================================================
STEP 2: Intelligent Chunking
================================================================================

[OK] Created 12 chunks using Dockling

Chunking Statistics:
  Total chunks: 12
  Average chunk size: 145.2 words
  Min/Max size: 85/230 words
  Chunks with code: 0
  Chunk type distribution:
    - transcript: 10
    - heading: 2

================================================================================
STEP 3: Generate Embeddings
================================================================================

[INFO] Estimated cost: $0.000024 (1,744 tokens)

[OK] Batch 1/1: 12 texts, 1,744 tokens, $0.000035

[OK] Generated 12 embeddings

================================================================================
EMBEDDING COST SUMMARY
================================================================================
Model: text-embedding-3-small
Total tokens: 1,744
Total cost: $0.000035
Average cost per 1K tokens: $0.00002006
================================================================================

================================================================================
STEP 4: Store in Database
================================================================================

[INFO] Inserting video metadata...
[OK] Inserted/updated video: dQw4w9WgXcQ (UUID: a1b2c3d4-...)
[OK] Video UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
[INFO] Inserting 12 chunks with embeddings...
[OK] Inserted 12 chunks for video a1b2c3d4-...
[OK] Stored 12 chunks

================================================================================
INGESTION COMPLETE
================================================================================

Video ID: dQw4w9WgXcQ
Video UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Title: Example Video Title
Duration: 3 minutes
Chunks stored: 12
Embedding cost: $0.000035
Processing time: 125.3 seconds (2.1 minutes)

Ready for semantic search!
```

---

### Step 4: Verify Ingestion

**Check database**:
```bash
python scripts/db/test_connection.py
```

**Query video**:
```python
from scripts.db.db_client import SupabaseClient

client = SupabaseClient()
video = client.get_video_by_id('dQw4w9WgXcQ')
print(f"Title: {video['title']}")
print(f"Chunks: {len(client.get_chunks_by_video(video['id']))}")
client.close()
```

**Expected output**:
```
Title: Example Video Title
Chunks: 12
```

---

### Step 5: Test Search

**Run a test search**:
```bash
python scripts/rag/semantic_search.py "main topics covered"
```

**Expected output**:
```
================================================================================
📺 Search Results for: "main topics covered"
================================================================================

Found 3 results:

1. Example Video Title by Example Channel
   Similarity: 0.847 (Very Good)
   Timestamp: 00:30
   Type: transcript
   In this video, we'll cover three main topics: first, the fundamentals...

2. Example Video Title by Example Channel
   Similarity: 0.782 (Good)
   Timestamp: 01:45
   Type: heading
   # Main Topics

3. Example Video Title by Example Channel
   Similarity: 0.734 (Good)
   Timestamp: 02:30
   Type: transcript
   To summarize the key points we discussed...

================================================================================
```

---

## Common Issues & Solutions

### Issue 1: "OpenAI API key not found"

**Solution**:
```bash
# Set environment variable
export OPENAI_API_KEY=sk-your-api-key-here

# Or add to .env file
echo "OPENAI_API_KEY=sk-your-api-key-here" >> .env
```

### Issue 2: "Database connection failed"

**Solution**:
1. Check Supabase credentials in `.env`
2. Verify Supabase project is running
3. Test connection: `python scripts/db/test_connection.py`

### Issue 3: "Failed to download video"

**Possible causes**:
- Video is private or unlisted
- Network connection issues
- Invalid URL format

**Solution**:
- Verify video is public
- Check URL is correct
- Try again with stable network

### Issue 4: "Whisper model not found"

**Solution**:
```bash
# First run downloads Whisper model (~1GB)
# Ensure sufficient disk space and wait for download to complete
```

### Issue 5: "Out of memory during transcription"

**Solution**:
```bash
# Use smaller Whisper model
# Edit scripts/rag/ingest_video.py, line 157:
# Change: transcribe_audio(audio_path, model_size='tiny')  # Instead of 'base'
```

---

## Batch Ingestion Workflow

To ingest multiple videos:

### Create video list file

**videos.txt**:
```
https://www.youtube.com/watch?v=VIDEO1
https://www.youtube.com/watch?v=VIDEO2
https://www.youtube.com/watch?v=VIDEO3
```

### Run batch script

```bash
# Bash/Linux/Mac
for url in $(cat videos.txt); do
    python scripts/rag/ingest_video.py "$url"
done

# Windows PowerShell
Get-Content videos.txt | ForEach-Object {
    python scripts/rag/ingest_video.py $_
}
```

### Track progress

Create a batch ingestion log:

```bash
for url in $(cat videos.txt); do
    echo "Processing: $url" >> ingestion.log
    python scripts/rag/ingest_video.py "$url" >> ingestion.log 2>&1
    echo "Completed: $url" >> ingestion.log
    echo "---" >> ingestion.log
done
```

---

## Cost Estimation

### Before ingestion

**Estimate costs for a video**:

```python
from scripts.rag.generate_embeddings import EmbeddingGenerator

# Assume 1-hour video = ~30K words = ~40K tokens
# Chunks: ~500 chunks × 130 tokens avg = 65K tokens

generator = EmbeddingGenerator()
tokens = 65000  # Estimated

cost = (tokens / 1_000_000) * 0.020  # $0.020 per 1M tokens
print(f"Estimated cost: ${cost:.6f}")  # $0.0013
```

### After ingestion

**Check actual costs**:
- View cost summary in ingestion output
- Check OpenAI usage dashboard: https://platform.openai.com/usage

---

## Post-Ingestion Tasks

### 1. Document ingested videos

Create a log of ingested videos:

```bash
echo "$(date) - Ingested: VIDEO_TITLE (VIDEO_ID)" >> ingestion_log.txt
```

### 2. Test search quality

Run test queries to verify content is searchable:

```bash
python scripts/rag/semantic_search.py "key topic from video"
```

### 3. Backup database

Regularly backup Supabase database:
- Use Supabase dashboard → Database → Backups
- Or export to SQL: `pg_dump`

### 4. Monitor storage usage

Check Supabase storage:
- Dashboard → Database → Usage
- Free tier: 500MB limit
- Upgrade if approaching limit

---

## Next Steps

After successful ingestion:

1. **Explore search features**: Try different queries
2. **Ingest more videos**: Build your knowledge base
3. **Create SubAgent**: Use Task 044-10 to build a YouTube Researcher
4. **Set up MCP server**: Task 044-11 for Claude Desktop integration
5. **Optimize performance**: Tune indexes and query parameters

---

## Resources

- **Ingestion Script**: `scripts/rag/ingest_video.py`
- **Database Client**: `scripts/db/db_client.py`
- **Chunking Module**: `scripts/chunking/dockling_chunker.py`
- **Embedding Generator**: `scripts/rag/generate_embeddings.py`
- **Search Interface**: `scripts/rag/semantic_search.py`

---

**Workflow complete!** Your video is now searchable in the RAG system.