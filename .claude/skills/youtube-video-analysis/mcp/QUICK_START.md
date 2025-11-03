# YouTube Intel MCP Server - Quick Start Guide

Get up and running with YouTube Intelligence in Claude Desktop in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
cd /mnt/c/git/ai_project_template/.claude/skills/youtube-video-analysis/mcp

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Configure Environment (1 minute)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key (minimum required)
nano .env
```

**Minimum required**:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Optional** (for semantic search):
```env
SUPABASE_HOST=db.your-project.supabase.co
SUPABASE_PASSWORD=your-password
```

## Step 3: Test the Server (1 minute)

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector python server.py
```

This will open a web UI at `http://localhost:5173` where you can test all 5 tools.

## Step 4: Add to Claude Desktop (1 minute)

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "youtube-intel": {
      "command": "python",
      "args": [
        "/mnt/c/git/ai_project_template/.claude/skills/youtube-video-analysis/mcp/server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here"
      }
    }
  }
}
```

**Important**: Adjust the path to `server.py` based on your system:
- **Windows**: `C:/git/ai_project_template/.claude/skills/youtube-video-analysis/mcp/server.py`
- **macOS/Linux**: `/path/to/ai_project_template/.claude/skills/youtube-video-analysis/mcp/server.py`

## Step 5: Restart Claude Desktop

Close and reopen Claude Desktop. You should now see "youtube-intel" in the available tools.

## Quick Test in Claude Desktop

Try these commands:

### Test 1: Get Transcript
```
Get the transcript for this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Test 2: Analyze Video
```
Analyze this Python tutorial in comprehensive mode:
https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

### Test 3: Extract Code
```
Extract all Python code from this tutorial:
https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

## Success Indicators

✅ **Working correctly** if you see:
- Tool calls in Claude Desktop chat
- Transcript appears in response
- Files created in `./output/<video_id>/` directory
- Server logs in `./logs/youtube_intel_mcp_YYYY_MM_DD.log`

❌ **Not working** if you see:
- "Tool not found" errors
- "Connection failed" errors
- No logs generated

## Troubleshooting

### Issue: "Command not found: python"

**Solution**: Use `python3` instead:
```json
"command": "python3",
```

### Issue: "OpenAI API key not found"

**Solution**: Verify your API key in the config:
```json
"env": {
  "OPENAI_API_KEY": "sk-..."  // Must start with "sk-"
}
```

### Issue: "Module not found"

**Solution**: Install dependencies with full path to Python:
```bash
/path/to/python -m pip install -r requirements.txt
```

### Issue: "FFmpeg not found"

**Solution**: Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html and add to PATH
```

## Optional: Enable Semantic Search (RAG)

If you want to use the `search_videos` tool:

1. **Create Supabase account**: https://supabase.com
2. **Create new project** and note the connection details
3. **Run database setup**:
   ```bash
   cd ../../youtube-rag-storage/
   python scripts/setup_database.py
   ```
4. **Add to Claude Desktop config**:
   ```json
   "env": {
     "OPENAI_API_KEY": "sk-...",
     "SUPABASE_HOST": "db.your-project.supabase.co",
     "SUPABASE_PASSWORD": "your-password"
   }
   ```

## Next Steps

Once working:

1. **Ingest videos** to build searchable knowledge base
2. **Use semantic search** to find specific topics across videos
3. **Compare videos** to evaluate different tutorials
4. **Extract code** for quick reference
5. **Automate analysis** of entire playlists

## Support

- **README.md**: Full documentation
- **Logs**: Check `./logs/` for errors
- **MCP Inspector**: Test tools at `http://localhost:5173`
- **GitHub Issues**: Report problems

---

**Time to first working command**: ~5 minutes
**Time to full setup with RAG**: ~15 minutes
