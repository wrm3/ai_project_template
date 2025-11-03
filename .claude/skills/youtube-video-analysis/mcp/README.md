# YouTube Intel MCP Server

**Model Context Protocol (MCP) server that exposes YouTube intelligence capabilities to Claude Desktop and other MCP clients.**

## Overview

The YouTube Intel MCP server provides 5 powerful tools for working with YouTube content:

1. **`get_transcript`** - Download and transcribe YouTube videos
2. **`analyze_video`** - Comprehensive analysis (quick/comprehensive/multimodal modes)
3. **`search_videos`** - Semantic search across ingested videos (RAG database)
4. **`compare_videos`** - Side-by-side video comparison
5. **`extract_code`** - Extract code snippets from videos

## Features

- **Automatic transcription** using OpenAI Whisper AI
- **Multi-modal analysis** combining transcript + visual frames
- **Semantic search** across video content using vector embeddings
- **Code extraction** from both transcripts and video frames (OCR)
- **Video comparison** for evaluating different tutorials
- **RAG integration** for building searchable video knowledge bases
- **Caching** to avoid re-downloading/re-transcribing

## Installation

### Prerequisites

- Python 3.10 or higher
- Claude Desktop (for MCP integration)
- FFmpeg (for video/audio processing)
- Tesseract OCR (optional, for code extraction from frames)

### 1. Install Dependencies

```bash
cd /mnt/c/git/ai_project_template/.claude/skills/youtube-video-analysis/mcp

# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

Required environment variables:
- `OPENAI_API_KEY` - For embeddings and Whisper transcription
- `SUPABASE_HOST` - For RAG database (semantic search)
- `SUPABASE_PASSWORD` - Database password

Optional:
- `ANTHROPIC_API_KEY` - For Claude-powered analysis
- `TESSERACT_CMD` - Path to Tesseract OCR executable

### 3. Set Up RAG Database (Optional)

If you want to use semantic search (`search_videos` tool), set up Supabase:

1. Create a Supabase project at https://supabase.com
2. Run the database migration:
   ```bash
   cd ../../../.claude/skills/youtube-rag-storage/
   python scripts/setup_database.py
   ```
3. Add Supabase credentials to `.env`

## Claude Desktop Integration

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "youtube-intel": {
      "command": "python",
      "args": [
        "/mnt/c/git/ai_project_template/.claude/skills/youtube-video-analysis/mcp/server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key",
        "SUPABASE_HOST": "db.your-project.supabase.co",
        "SUPABASE_PASSWORD": "your-password"
      }
    }
  }
}
```

**Note**: Adjust the path to `server.py` based on your system.

After adding this configuration, restart Claude Desktop.

## Testing

### Test the MCP Server

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector python server.py

# The inspector will start at http://localhost:5173
# You can interact with all 5 tools through the web UI
```

### Test Individual Tools

```bash
# Test transcript tool
python -c "import asyncio; from tools.get_transcript import get_transcript_handler; print(asyncio.run(get_transcript_handler('dQw4w9WgXcQ', logger=None)))"
```

## Usage Examples

### In Claude Desktop

Once configured, you can use these tools directly in Claude Desktop conversations:

#### Example 1: Get Transcript

```
User: "Get the transcript for https://www.youtube.com/watch?v=dQw4w9WgXcQ"

Claude Desktop → youtube-intel.get_transcript → Returns full transcript
```

#### Example 2: Comprehensive Analysis

```
User: "Analyze this FastAPI tutorial: https://youtube.com/watch?v=VIDEO_ID"

Claude Desktop → youtube-intel.analyze_video(mode="comprehensive") → Returns detailed analysis
```

#### Example 3: Semantic Search

```
User: "Search my video knowledge base for RAG implementation examples"

Claude Desktop → youtube-intel.search_videos(query="RAG implementation") → Returns top 10 matches
```

#### Example 4: Compare Videos

```
User: "Compare these two Python tutorials:"
User: "1. https://youtube.com/watch?v=VIDEO_1"
User: "2. https://youtube.com/watch?v=VIDEO_2"

Claude Desktop → youtube-intel.compare_videos → Returns comparison table
```

#### Example 5: Extract Code

```
User: "Extract all Python code from this tutorial: https://youtube.com/watch?v=VIDEO_ID"

Claude Desktop → youtube-intel.extract_code(language="python") → Returns all code snippets
```

## Tool Documentation

### 1. get_transcript

**Description**: Download and transcribe YouTube video using Whisper AI

**Parameters**:
- `video_url` (required): YouTube URL or video ID
- `output_dir` (optional): Output directory (default: `./output/<video_id>/`)
- `force_redownload` (optional): Re-download even if cached (default: `false`)

**Returns**:
```json
{
  "success": true,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "author": "Channel Name",
  "duration_seconds": 212,
  "transcript": "Full transcript text...",
  "transcript_length": 5430,
  "word_count": 892,
  "cached": false,
  "output_dir": "./output/dQw4w9WgXcQ/",
  "processing_time_seconds": 45.2
}
```

### 2. analyze_video

**Description**: Comprehensive video analysis with multiple modes

**Parameters**:
- `video_url` (required): YouTube URL or video ID
- `mode` (optional): Analysis mode - "quick", "comprehensive", or "multimodal" (default: "comprehensive")
- `output_dir` (optional): Output directory
- `save_to_rag` (optional): Ingest to RAG database (default: `false`)

**Modes**:
- **quick**: Fast summary, keyword extraction
- **comprehensive**: Detailed insights, quotes, technical details
- **multimodal**: Full analysis combining transcript + visual frames

**Returns**:
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "title": "Video Title",
  "mode": "comprehensive",
  "analysis": {
    "summary": "...",
    "key_insights": ["insight1", "insight2"],
    "technical_details": {...},
    "quotes": ["quote1", "quote2"],
    "action_items": ["item1", "item2"]
  },
  "output_files": ["analysis.json", "ANALYSIS.md"],
  "processing_time_seconds": 120.5
}
```

### 3. search_videos

**Description**: Semantic search across all ingested videos in RAG database

**Parameters**:
- `query` (required): Natural language search query
- `limit` (optional): Max results (default: 10)
- `min_similarity` (optional): Minimum similarity threshold 0.0-1.0 (default: 0.7)
- `video_id` (optional): Limit to specific video
- `chunk_type` (optional): Filter by type ("transcript", "code", etc.)

**Returns**:
```json
{
  "success": true,
  "query": "RAG implementation",
  "results": [
    {
      "video_id": "VIDEO_ID",
      "video_title": "Title",
      "video_author": "Author",
      "chunk_text": "Content snippet...",
      "similarity": 0.89,
      "timestamp_start": 125.5,
      "chunk_type": "transcript",
      "has_code": true
    }
  ],
  "total_results": 10,
  "search_time_ms": 87.3
}
```

### 4. compare_videos

**Description**: Side-by-side comparison of multiple videos

**Parameters**:
- `video_urls` (required): Array of 2-5 YouTube URLs
- `aspects` (optional): Comparison aspects (default: ["approach", "tools", "pros_cons"])
- `output_format` (optional): "markdown", "json", or "html" (default: "markdown")

**Aspects**: `approach`, `tools`, `pros_cons`, `complexity`, `completeness`, `code_quality`, or custom

**Returns**:
```json
{
  "success": true,
  "videos": [{"video_id": "...", "title": "..."}],
  "comparison": {
    "approach": {
      "VIDEO_1": "Beginner-friendly approach...",
      "VIDEO_2": "Advanced deep dive..."
    }
  },
  "summary": "Compared 2 videos...",
  "recommendation": "Recommended: Video 1 because...",
  "comparison_table": "| Aspect | Video 1 | Video 2 |\n|..."
}
```

### 5. extract_code

**Description**: Extract all code snippets from video (transcript + frames)

**Parameters**:
- `video_url` (required): YouTube URL or video ID
- `language` (optional): Filter by language ("python", "javascript", etc.)
- `include_frames` (optional): Extract from video frames using OCR (default: `true`)
- `output_dir` (optional): Output directory

**Returns**:
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "code_snippets": [
    {
      "snippet_id": 1,
      "language": "python",
      "source": "transcript",
      "code": "def example():\n    return True",
      "timestamp": 125.5,
      "line_count": 2,
      "has_imports": false,
      "has_functions": true,
      "has_classes": false
    }
  ],
  "summary": {
    "total_snippets": 15,
    "languages_found": ["python", "javascript"],
    "snippets_by_source": {"transcript": 10, "frame": 5},
    "total_lines_of_code": 245
  },
  "output_files": ["snippet_001.py", "snippet_002.js"],
  "output_directory": "./output/VIDEO_ID/code/"
}
```

## Architecture

```
youtube-intel-mcp/
├── server.py                     # Main MCP server (FastMCP)
├── tools/
│   ├── get_transcript.py         # Tool 1: Get video transcript
│   ├── analyze_video.py          # Tool 2: Comprehensive analysis
│   ├── search_videos.py          # Tool 3: Semantic search (RAG)
│   ├── compare_videos.py         # Tool 4: Video comparison
│   └── extract_code.py           # Tool 5: Code extraction
├── logs/                         # Server logs (auto-generated)
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project metadata
├── .env.example                  # Environment template
└── README.md                     # This file
```

## Integration with Existing Skills

This MCP server integrates with:

1. **youtube-video-analysis** skill - Uses `analyze_video.py` for transcription
2. **youtube-rag-storage** skill - Uses RAG database for semantic search
3. **dockling_chunker** - Intelligent transcript chunking
4. **multimodal_integration** - Combines visual + audio analysis

## Performance

**Typical Processing Times**:
- **Transcript** (1-hour video): ~2-3 minutes
- **Quick analysis**: <5 seconds
- **Comprehensive analysis**: <10 seconds
- **Multimodal analysis**: ~5-8 minutes (includes frame extraction)
- **Semantic search**: <100ms
- **Code extraction**: ~30 seconds - 2 minutes

**Caching**:
- Transcripts are cached locally
- Re-requesting same video returns instantly from cache
- Use `force_redownload=true` to bypass cache

## Cost Estimates

**OpenAI API Costs** (per video):
- **Transcription** (Whisper): FREE (local processing)
- **Embeddings** (for RAG): ~$0.001 - $0.004 per video
- **Total**: ~$0.004 per video (essentially FREE!)

**Supabase Storage**:
- **Free tier**: 500MB database (sufficient for ~150 videos)
- **Pro tier**: $25/month for 8GB (~2,400 videos)

## Troubleshooting

### Issue: "OpenAI API key not found"

```bash
# Solution: Set environment variable
export OPENAI_API_KEY=sk-your-api-key
# Or add to .env file
```

### Issue: "Database connection failed"

```bash
# Solution: Verify Supabase credentials
python -c "from tools.search_videos import *; test_connection()"
```

### Issue: "ModuleNotFoundError: No module named 'X'"

```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

### Issue: "FFmpeg not found"

```bash
# Solution: Install FFmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Issue: "Tesseract not found" (for code extraction)

```bash
# Solution: Install Tesseract OCR

# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Logs

Server logs are automatically written to:
```
./logs/youtube_intel_mcp_YYYY_MM_DD.log
```

Check logs for debugging:
```bash
tail -f logs/youtube_intel_mcp_$(date +%Y_%m_%d).log
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run specific test
pytest tests/test_get_transcript.py -v
```

### Adding New Tools

1. Create new handler in `tools/new_tool.py`
2. Import and register in `server.py`:
   ```python
   from tools.new_tool import new_tool_handler

   @mcp.tool(name="new_tool")
   async def run_new_tool(...):
       return await new_tool_handler(...)
   ```
3. Update README with tool documentation

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Related Projects

- **Task 044-6**: YouTube RAG Storage Skill
- **Task 044-10**: YouTube Researcher SubAgent
- **youtube-video-analysis**: Core transcription skill
- **FastMCP**: Model Context Protocol implementation

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review server logs

---

**Version**: 1.0.0
**Created**: 2025-11-01
**Task**: 044-11
**Status**: Production Ready
