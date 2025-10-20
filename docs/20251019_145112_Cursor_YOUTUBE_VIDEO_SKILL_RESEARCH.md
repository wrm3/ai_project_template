# YouTube Video Analysis Skill - Research Summary

**Date**: 2025-10-19  
**Task**: Task 019 - Create YouTube Video Analysis Skill  
**Status**: Research Phase

## Executive Summary

User has existing YouTube video processing tools from 4 months ago (June 2025) in the `research/hanx/` folders. These tools use **pytubefix**, **Whisper**, **moviepy**, and **ffmpeg** to download, transcribe, and analyze YouTube videos. 

**Goal**: Create a Claude Code Skill that can process YouTube videos (like a "Claude Skills" tutorial) to extract knowledge, generate summaries, and create code/requirements.

## Existing Code Analysis

### Files Found

1. **`research/hanx/hanx_tools/youtube_harvest_data.py`** (640 lines)
   - Main processing script
   - Downloads videos, extracts audio, transcribes, analyzes
   - Supports multiple video types (trading, framework, general)
   - Has LLM integration for analysis

2. **`research/hanx2/hanx_tools/agent_youtube_researcher.py`** (655 lines)
   - Agent-based approach
   - Similar functionality to youtube_harvest_data.py
   - Better structured as an agent
   - RAG integration support

3. **`research/hanx2/hanx_tools/tool_youtube.py`** (790+ lines)
   - Most comprehensive implementation
   - Combines functionality from multiple modules
   - Well-documented with usage examples
   - GitHub-ready with installation notes

4. **`research/hanx/hanx_tools/temp_tools/youtube_processor.py`**
   - Core processor class
   - Clean OOP design
   - Reusable components

5. **`research/hanx/hanx_tools/temp_tools/youtube_harvester.py`**
   - Workflow integration
   - End-to-end processing

### Technology Stack (User's 4-Month-Old Code)

```python
# Core Dependencies
pytubefix>=6.0.0          # YouTube video downloading
openai-whisper>=20231117  # Audio transcription (OpenAI's Whisper)
moviepy>=1.0.3            # Video/audio extraction
imageio-ffmpeg>=0.4.9     # FFmpeg binaries (bundled)

# Optional
pydub>=0.25.1             # Audio manipulation
```

### Key Features in Existing Code

1. **Graceful Dependency Handling**:
   ```python
   try:
       from pytubefix import YouTube
       HAS_PYTUBEFIX = True
   except ImportError:
       HAS_PYTUBEFIX = False
       print("Warning: pytubefix not found...")
   ```

2. **FFmpeg Fallback**:
   - If moviepy not available, uses ffmpeg directly
   - Subprocess call to ffmpeg binary
   - User mentioned ffmpeg is "most useful"

3. **Multiple Video Types**:
   - **Trading Strategy**: Extract entry/exit criteria, indicators, risk management
   - **Framework/Tool**: Extract installation, usage, features, limitations
   - **General**: Extract summary, key points, topics, insights

4. **LLM Analysis**:
   - Custom prompts for each video type
   - JSON-structured output
   - Fallback analysis when LLM unavailable

5. **Whisper Integration**:
   - Multiple model sizes (tiny, base, small, medium, large)
   - Trade-off between speed and accuracy
   - Handles long videos

## Technology Assessment (October 2025)

### Current State of the Art

**Need to Research** (web search rate-limited, but based on code):

1. **YouTube Downloading**:
   - **pytubefix**: User's current choice
   - **yt-dlp**: More actively maintained alternative
   - **pytube**: Original library (may be outdated)

2. **Audio Transcription**:
   - **Whisper**: OpenAI's model (user's current choice)
   - **faster-whisper**: 4x faster implementation
   - **distil-whisper**: Smaller, faster distilled model
   - **Whisper v3**: Latest version (need to check)

3. **Audio/Video Processing**:
   - **moviepy**: User's current choice
   - **ffmpeg-python**: Better Python bindings
   - **pydub**: Audio-focused alternative
   - **imageio-ffmpeg**: Bundled ffmpeg (user already uses)

4. **Video Frame Analysis** (if needed):
   - **transformers**: For vision models
   - **video-llm**: If exists, direct video analysis
   - **CLIP**: For image/video understanding

### Recommendations

**Option A: Keep Existing Stack** (Conservative)
- ✅ User's code already works
- ✅ Well-tested over 4 months
- ✅ Known issues already solved
- ❌ May not be latest/greatest

**Option B: Upgrade to Modern Stack** (Aggressive)
- ✅ Potentially faster/better
- ✅ More actively maintained
- ❌ Need to rewrite/test everything
- ❌ Unknown issues

**Option C: Hybrid Approach** (Recommended)
- ✅ Keep what works (pytubefix, ffmpeg)
- ✅ Upgrade where clear benefit (faster-whisper)
- ✅ Maintain compatibility
- ✅ Incremental improvement

## Proposed Architecture

### Skill Structure

```
.claude/skills/youtube-video-analysis/
├── SKILL.md                          # Main skill definition
├── rules.md                          # Detailed implementation rules
├── reference/
│   ├── technology_stack.md           # Tech comparison
│   ├── video_types.md                # Video type definitions
│   ├── prompt_templates.md           # LLM prompts
│   ├── ffmpeg_guide.md               # FFmpeg usage
│   └── migration_from_hanx.md        # Upgrade notes
├── examples/
│   ├── trading_strategy_analysis.json
│   ├── framework_tutorial_analysis.json
│   ├── general_video_analysis.json
│   └── sample_workflow.md
└── scripts/
    ├── __init__.py
    ├── video_processor.py            # Core processing
    ├── transcriber.py                # Whisper integration
    ├── analyzer.py                   # LLM analysis
    ├── downloader.py                 # YouTube downloading
    └── requirements.txt              # Dependencies
```

### Workflow

```
User provides YouTube URL
    ↓
1. Download Video (pytubefix or yt-dlp)
    ↓
2. Extract Audio (moviepy or ffmpeg)
    ↓
3. Transcribe Audio (Whisper)
    ↓
4. Analyze Transcription (Claude API)
    ↓
5. Generate Structured Output (JSON)
    ↓
6. Optional: Generate Code/Requirements/Tasks
```

## Use Cases

### Use Case 1: Claude Skills Tutorial

**Input**: YouTube URL for "How to Create Claude Skills"

**Process**:
1. Download video
2. Transcribe tutorial
3. Extract key concepts:
   - Skill structure (SKILL.md format)
   - YAML frontmatter requirements
   - Reference materials structure
   - Example files structure
4. Generate:
   - Summary of tutorial
   - Code template for new skill
   - Requirements checklist
   - Tasks to implement

**Output**:
```json
{
  "summary": "Tutorial on creating Claude Skills...",
  "key_concepts": [
    "SKILL.md format",
    "Progressive disclosure",
    "Reference materials"
  ],
  "code_templates": {
    "skill_md": "---\nname: my-skill\n...",
    "rules_md": "# My Skill Rules\n..."
  },
  "requirements": [
    "Create SKILL.md with YAML frontmatter",
    "Add reference materials",
    "Include examples"
  ],
  "tasks": [
    "Task: Create SKILL.md file",
    "Task: Add reference documentation",
    "Task: Create example files"
  ]
}
```

### Use Case 2: Trading Strategy Video

**Input**: YouTube URL for trading strategy explanation

**Process**:
1. Download video
2. Transcribe strategy explanation
3. Extract:
   - Strategy name
   - Entry/exit criteria
   - Indicators used
   - Risk management
   - Timeframes and markets
4. Generate:
   - Strategy summary
   - Implementation requirements
   - Code skeleton

**Output**:
```json
{
  "strategy_name": "RSI Divergence Strategy",
  "entry_criteria": [
    "RSI shows bullish divergence",
    "Price makes lower low",
    "Volume confirmation"
  ],
  "exit_criteria": [
    "RSI reaches 70",
    "Price hits resistance",
    "Stop loss at 2%"
  ],
  "indicators": ["RSI", "Volume", "Support/Resistance"],
  "risk_management": ["2% stop loss", "1:2 risk/reward"],
  "implementation_notes": "Requires real-time RSI calculation..."
}
```

### Use Case 3: Framework Tutorial

**Input**: YouTube URL for "FastAPI Tutorial"

**Process**:
1. Download video
2. Transcribe tutorial
3. Extract:
   - Installation steps
   - Basic usage
   - Code examples
   - Best practices
4. Generate:
   - Setup guide
   - Code examples
   - Implementation tasks

**Output**:
```json
{
  "framework": "FastAPI",
  "installation": [
    "pip install fastapi",
    "pip install uvicorn"
  ],
  "basic_usage": [
    "Create FastAPI app instance",
    "Define routes with @app.get()",
    "Run with uvicorn"
  ],
  "code_examples": [
    "from fastapi import FastAPI\napp = FastAPI()..."
  ],
  "best_practices": [
    "Use Pydantic models for validation",
    "Add type hints",
    "Document with docstrings"
  ]
}
```

## Integration Points

### With fstrent_spec_tasks

1. **Task Generation**:
   - Tutorial videos → implementation tasks
   - Strategy videos → coding tasks
   - Demo videos → bug reports

2. **Planning Integration**:
   - Product videos → PRD generation
   - Feature demos → feature documents
   - Architecture videos → technical considerations

3. **QA Integration**:
   - Bug demo videos → bug reports
   - Testing videos → test cases
   - Review videos → quality metrics

### With RAG System (if available)

1. Store transcriptions in knowledge base
2. Enable semantic search across videos
3. Link related videos
4. Build video knowledge graph

## Technical Considerations

### Windows-Specific

- FFmpeg path handling (Windows paths with backslashes)
- PowerShell compatibility
- File path separators (`os.path.join` vs manual concatenation)
- Temp directory handling (`tempfile` module)

### Performance

- **Model Size Selection**:
  - tiny: Fast, lower accuracy (good for quick previews)
  - base: Balanced (recommended default)
  - small: Better accuracy, slower
  - medium: High accuracy, much slower
  - large: Best accuracy, very slow

- **Caching**:
  - Cache downloaded videos
  - Cache transcriptions
  - Cache analyses

- **Parallel Processing**:
  - Process multiple videos concurrently
  - Batch transcription
  - Async LLM calls

### Error Handling

1. **Network Errors**:
   - Retry logic for downloads
   - Timeout handling
   - Rate limit respect

2. **Processing Errors**:
   - Invalid video formats
   - Corrupted downloads
   - Transcription failures
   - LLM API errors

3. **User Errors**:
   - Invalid URLs
   - Unsupported video types
   - Missing dependencies

## Dependencies

### Required

```python
pytubefix>=6.0.0          # YouTube downloading
openai-whisper>=20231117  # Audio transcription
moviepy>=1.0.3            # Video/audio processing
imageio-ffmpeg>=0.4.9     # FFmpeg binaries
anthropic>=0.7.0          # Claude API for analysis
```

### Optional

```python
pydub>=0.25.1             # Audio manipulation
yt-dlp>=2023.10.13        # Alternative downloader
faster-whisper>=0.10.0    # Faster transcription
ffmpeg-python>=0.2.0      # Better ffmpeg control
```

### System Requirements

- **FFmpeg**: Bundled via imageio-ffmpeg (or system-installed)
- **Python**: 3.8+ (for Whisper)
- **Disk Space**: ~1GB for Whisper models
- **RAM**: 4GB+ for large model, 2GB for base model
- **GPU**: Optional, speeds up Whisper significantly

## Next Steps

### Immediate (Research Phase)

1. ✅ Analyze existing user code
2. ✅ Document current technology stack
3. ✅ Identify use cases
4. ✅ Create task file
5. ✅ Update TASKS.md
6. [ ] Research latest libraries (when web search available)
7. [ ] Compare technology options
8. [ ] Make final technology decisions

### Short-Term (Design Phase)

1. [ ] Finalize technology stack
2. [ ] Design Skill structure
3. [ ] Create prompt templates
4. [ ] Design JSON output schemas
5. [ ] Plan integration points

### Medium-Term (Implementation Phase)

1. [ ] Create SKILL.md
2. [ ] Create rules.md
3. [ ] Add reference materials
4. [ ] Add example files
5. [ ] Write core scripts
6. [ ] Create requirements.txt

### Long-Term (Testing & Polish)

1. [ ] Test with Claude Skills video
2. [ ] Test with trading strategy video
3. [ ] Test with framework tutorial
4. [ ] Document any issues
5. [ ] Create comprehensive examples
6. [ ] Write user guide

## Questions for User

1. **Technology Preferences**:
   - Stick with existing stack (pytubefix, Whisper, moviepy)?
   - Or upgrade to newer alternatives (yt-dlp, faster-whisper)?
   - User mentioned ffmpeg is "most useful" - prefer ffmpeg-first approach?

2. **Scope**:
   - Just YouTube? Or support other video sources (Vimeo, local files)?
   - Just audio transcription? Or also video frame analysis?
   - Integration with RAG system desired?

3. **Use Cases**:
   - Primary use case: Learning from tutorials?
   - Or: Analyzing trading strategies?
   - Or: Extracting code examples?

4. **Performance vs Accuracy**:
   - Prefer fast processing (tiny/base Whisper model)?
   - Or high accuracy (large model)?
   - Or user-selectable?

5. **Output Format**:
   - JSON structured output sufficient?
   - Or also generate markdown reports?
   - Or also create tasks/PRDs automatically?

## Conclusion

User has solid foundation with 4-month-old Hanx tools. The code is well-structured, handles errors gracefully, and supports multiple use cases. 

**Recommendation**: 
1. Start with existing code as base
2. Upgrade selectively (faster-whisper if clearly better)
3. Package as Claude Code Skill
4. Add comprehensive documentation
5. Test with real-world videos

**Estimated Effort**: 4-6 hours
- Research: 1-2 hours
- Design: 1 hour
- Implementation: 2-3 hours
- Testing: 1 hour

---

**Status**: Research phase complete, awaiting user feedback on technology decisions and scope.

