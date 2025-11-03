# YouTube Video Analysis - Caching System

Multi-layer caching system to avoid redundant downloads, transcriptions, and embeddings.

## Quick Start

```bash
# Install dependencies
pip install tqdm

# Process a video with automatic caching
python ../analyze_with_cache.py VIDEO_URL

# Process a playlist with caching
python ../analyze_with_cache.py --playlist PLAYLIST_URL --max-videos 10

# View cache statistics
python ../cache_cli.py stats
```

## Cache Structure

```
.cache/
├── transcripts/        # Video transcripts (TEXT)
│   └── VIDEO_ID.txt
├── embeddings/         # Vector embeddings (PICKLE)
│   └── VIDEO_ID_embeddings.pkl
├── frames/             # Extracted frames (JPEG)
│   └── VIDEO_ID/
│       ├── frame_0.jpg
│       └── frame_30.jpg
├── analysis/           # Analysis results (JSON with TTL)
│   └── VIDEO_ID_analysis.json
└── cache_stats.json    # Cache statistics
```

## Cache Manager API

```python
from cache.cache_manager import CacheManager

# Initialize
cache = CacheManager(cache_dir=".cache", ttl_hours=168)

# Check cache
if cache.has_transcript(video_id):
    transcript = cache.get_transcript(video_id)
else:
    transcript = generate_transcript()
    cache.save_transcript(video_id, transcript)

# Statistics
cache.print_stats()
```

## CLI Commands

```bash
# Show statistics
python cache_cli.py stats

# Show cache sizes
python cache_cli.py size

# List cached videos
python cache_cli.py list

# Validate cache integrity
python cache_cli.py validate

# Clear specific video
python cache_cli.py clear VIDEO_ID

# Clear all cache (with confirmation)
python cache_cli.py clear

# Remove expired entries (>7 days)
python cache_cli.py prune
```

## Performance

### Without Cache (First Run)
- Download: 30-120s
- Transcription: 120-300s
- Frame extraction: 60-180s
- **Total: 3-10 minutes**

### With Cache (Second Run)
- Cache lookup: <1s
- Load transcript: <1s
- Load frames: 1-3s
- **Total: <5s (98% time savings)**

### Playlist (10 videos, 50% cached)
- Cached videos (5): ~25s total
- New videos (5): ~30-50 minutes total
- **Time savings: ~25 minutes (45%)**

## Cache TTL

Analysis cache has a 7-day TTL (time-to-live). Other cache types are permanent until manually cleared.

To customize TTL:
```python
cache = CacheManager(ttl_hours=72)  # 3 days
```

## Cache Validation

```bash
python cache_cli.py validate
```

Checks for:
- Empty transcript files
- Corrupted pickle files
- Empty frame directories
- Invalid JSON in analysis cache
- Expired analysis entries

## Batch Processing Integration

The cache system is automatically integrated with batch processing:

```bash
# Process playlist with caching
python analyze_with_cache.py --playlist PLAYLIST_URL

# Output shows cache utilization:
# Cached: 7 (70.0%)
# Time savings: ~35 minutes
```

## Thread Safety

The cache manager is **not** thread-safe. For concurrent access, use file locking or separate cache directories per process.

## Disk Space

Monitor cache size with:
```bash
python cache_cli.py size
```

Typical sizes:
- Transcript: 10-50 KB per video
- Embeddings: 500 KB - 2 MB per video
- Frames: 1-10 MB per video (depends on count)
- Analysis: 5-20 KB per video

## Troubleshooting

### Cache not working
1. Check cache directory exists and is writable
2. Verify video ID extraction: `python -c "from cache.cache_manager import CacheManager; print(CacheManager.extract_video_id('YOUR_URL'))"`

### Cache statistics reset
- Stats are stored in `.cache/cache_stats.json`
- If file is deleted, stats reset to zero
- This doesn't affect cached content

### Expired analysis cache
- Analysis cache uses TTL (default: 7 days)
- Run `python cache_cli.py prune` to remove expired entries
- Or increase TTL: `CacheManager(ttl_hours=336)`  # 14 days

## See Also

- Main script: `analyze_with_cache.py`
- Batch processor: `batch_processor.py`
- CLI tool: `cache_cli.py`
- Documentation: `/docs/TASK044-8_BATCH_CACHING_COMPLETION.md`
