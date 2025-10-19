---
name: youtube-video-analysis
description: Download, transcribe, and analyze YouTube videos to extract knowledge, generate summaries, and create code/requirements. Use when user provides a YouTube URL or wants to process video content for information extraction. Supports trading strategies, framework tutorials, and general content analysis.
---

# YouTube Video Analysis Skill

Extract knowledge from YouTube videos through automated downloading, transcription, and LLM-powered analysis. Transform video content into actionable summaries, code templates, requirements documents, and structured data.

## Overview

This Skill provides end-to-end YouTube video processing capabilities:

1. **Download**: Fetch YouTube videos by URL or ID
2. **Extract**: Pull audio tracks from videos
3. **Transcribe**: Convert audio to text using Whisper AI
4. **Analyze**: Extract structured information using Claude
5. **Generate**: Create summaries, code, requirements, or tasks

## When to Use This Skill

### Automatic Triggers
- User provides a YouTube URL
- User mentions "analyze this video"
- User asks to "extract information from video"
- User wants to "learn from tutorial video"
- User requests "video summary" or "video transcript"

### Manual Invocation
```
/analyze-youtube https://youtu.be/example
/transcribe-video https://youtu.be/example
/extract-from-video https://youtu.be/example --type trading_strategy
```

## Supported Video Types

### 1. Trading Strategy Videos
Extract structured trading information:
- Strategy name and overview
- Entry and exit criteria
- Technical indicators used
- Risk management rules
- Timeframes and markets
- Backtest results
- Pros and cons

**Example Use Case**: "Analyze this RSI divergence strategy video and create implementation requirements"

### 2. Framework/Tool Tutorials
Extract technical documentation:
- Tool/framework name and purpose
- Installation steps
- Basic and advanced usage
- Code examples
- Best practices
- Limitations and alternatives
- Resources and documentation

**Example Use Case**: "Watch this FastAPI tutorial and generate a setup guide with code examples"

### 3. General Educational Content
Extract key insights:
- Content summary
- Main topics covered
- Key points and takeaways
- Questions answered
- References and resources
- Action items

**Example Use Case**: "Summarize this Claude Skills tutorial and create tasks for implementation"

## Core Capabilities

### Video Acquisition
- **YouTube URLs**: Full URLs, shortened URLs (youtu.be), or video IDs
- **Quality Selection**: Automatically selects highest quality available
- **Format Support**: MP4, WebM, and other common formats
- **Playlist Support**: Process individual videos or entire playlists
- **Local Files**: Also supports local video files

### Audio Processing
- **Extraction**: Pull audio track from video using ffmpeg
- **Format Conversion**: Convert to MP3 for optimal transcription
- **Quality Optimization**: Balance file size and audio quality
- **Multi-language**: Support for various audio languages

### Transcription
- **Whisper AI**: OpenAI's state-of-the-art speech recognition
- **Model Selection**: Choose from tiny, base, small, medium, large
  - **tiny**: Fastest, lower accuracy (~1GB RAM)
  - **base**: Balanced, recommended default (~2GB RAM)
  - **small**: Better accuracy (~5GB RAM)
  - **medium**: High accuracy (~10GB RAM)
  - **large**: Best accuracy (~20GB RAM)
- **Timestamp Support**: Optional timestamps for segments
- **Speaker Detection**: Identify different speakers (if available)

### Analysis
- **LLM-Powered**: Uses Claude for intelligent content analysis
- **Structured Output**: JSON format for easy parsing
- **Custom Prompts**: Tailored analysis based on video type
- **Fallback Analysis**: Basic extraction if LLM unavailable
- **Multi-pass**: Can analyze same content multiple ways

### Output Generation
- **Summaries**: Concise overviews of video content
- **Code Templates**: Extract and format code examples
- **Requirements**: Generate PRD-style requirement documents
- **Tasks**: Create actionable task lists
- **Knowledge Base**: Format for RAG system integration

## Workflow Examples

### Example 1: Learning from Tutorial

**User**: "I found this great video on Claude Skills: https://youtu.be/example. Can you watch it and help me implement what it teaches?"

**Skill Actions**:
1. Download video
2. Extract audio
3. Transcribe content
4. Analyze tutorial structure
5. Extract key concepts
6. Generate implementation tasks
7. Create code templates

**Output**:
```json
{
  "video_title": "How to Create Claude Skills",
  "summary": "Tutorial covering Claude Skills creation...",
  "key_concepts": [
    "SKILL.md structure with YAML frontmatter",
    "Progressive disclosure pattern",
    "Reference materials organization"
  ],
  "code_templates": {
    "skill_md": "---\nname: my-skill\ndescription: ...\n---\n\n# My Skill\n..."
  },
  "implementation_tasks": [
    "Create SKILL.md with proper YAML frontmatter",
    "Add reference documentation in reference/ folder",
    "Create example files in examples/ folder",
    "Write implementation rules in rules.md"
  ],
  "requirements": [
    "Skill must have clear description",
    "Must include usage examples",
    "Should follow progressive disclosure pattern"
  ]
}
```

### Example 2: Trading Strategy Analysis

**User**: "Analyze this trading strategy video: https://youtu.be/example"

**Skill Actions**:
1. Download and transcribe video
2. Identify strategy components
3. Extract entry/exit rules
4. Document indicators and timeframes
5. Generate implementation requirements

**Output**:
```json
{
  "strategy_name": "RSI Divergence Strategy",
  "summary": "Momentum reversal strategy using RSI divergence...",
  "entry_criteria": [
    "RSI shows bullish divergence (higher lows while price makes lower lows)",
    "Price reaches support level",
    "Volume confirmation on reversal candle"
  ],
  "exit_criteria": [
    "RSI reaches overbought (>70)",
    "Price hits resistance level",
    "Stop loss at 2% below entry"
  ],
  "indicators": ["RSI (14)", "Volume", "Support/Resistance"],
  "timeframes": ["1-hour", "4-hour", "Daily"],
  "markets": ["Crypto", "Forex", "Stocks"],
  "risk_management": [
    "2% maximum risk per trade",
    "1:2 minimum risk/reward ratio",
    "Position sizing based on volatility"
  ],
  "implementation_notes": "Requires real-time RSI calculation, support/resistance detection, and volume analysis"
}
```

### Example 3: Framework Tutorial

**User**: "I need to learn FastAPI. Can you watch this tutorial and create a setup guide? https://youtu.be/example"

**Skill Actions**:
1. Download and transcribe tutorial
2. Extract installation steps
3. Identify code examples
4. Document best practices
5. Generate setup guide

**Output**:
```json
{
  "framework": "FastAPI",
  "summary": "Modern Python web framework for building APIs...",
  "installation": [
    "pip install fastapi",
    "pip install uvicorn[standard]"
  ],
  "basic_usage": [
    "Create FastAPI app instance",
    "Define routes using decorators",
    "Add request/response models with Pydantic",
    "Run with uvicorn"
  ],
  "code_examples": [
    "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}"
  ],
  "best_practices": [
    "Use Pydantic models for validation",
    "Add type hints for better IDE support",
    "Document endpoints with docstrings",
    "Use dependency injection for shared logic"
  ],
  "setup_guide": "1. Install FastAPI and uvicorn\n2. Create main.py with app instance\n3. Define routes\n4. Run with: uvicorn main:app --reload"
}
```

## Integration with fstrent_spec_tasks

### Automatic Task Generation
When analyzing tutorial videos, the Skill can automatically create tasks:

```markdown
# Generated from video: "How to Create Claude Skills"

## Task: Implement Claude Skill Structure
- [ ] Create SKILL.md with YAML frontmatter
- [ ] Add skill description and usage examples
- [ ] Define when skill should be triggered

## Task: Add Reference Materials
- [ ] Create reference/ folder
- [ ] Add technology documentation
- [ ] Include schema definitions

## Task: Create Examples
- [ ] Add example inputs/outputs
- [ ] Document common use cases
- [ ] Provide code templates
```

### PRD Generation
For product or feature videos, generate Product Requirements Documents:

```markdown
# PRD: [Feature from Video]

## Overview
[Extracted from video summary]

## Goals
[Extracted from video objectives]

## Features
[Extracted from video feature descriptions]

## Technical Considerations
[Extracted from implementation details]
```

### Bug Documentation
For bug demo or issue videos, create bug reports:

```markdown
# Bug: [Issue from Video]

## Description
[Extracted from video problem description]

## Reproduction Steps
[Extracted from video demonstration]

## Expected Behavior
[Extracted from video expectations]

## Actual Behavior
[Extracted from video observations]
```

## Technical Details

### Dependencies
```python
pytubefix>=6.0.0          # YouTube downloading
openai-whisper>=20231117  # Audio transcription
moviepy>=1.0.3            # Video/audio processing
imageio-ffmpeg>=0.4.9     # FFmpeg binaries (bundled)
anthropic>=0.7.0          # Claude API for analysis
```

### FFmpeg Integration
This Skill uses ffmpeg for audio/video processing. FFmpeg is bundled via `imageio-ffmpeg`, but you can also use a system-installed version:

**Bundled** (automatic):
```python
import imageio_ffmpeg
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
```

**System-installed** (manual):
```bash
# Windows: Add to PATH or specify full path
C:\path\to\ffmpeg\bin\ffmpeg.exe

# Mac: brew install ffmpeg
# Linux: apt-get install ffmpeg
```

**Project-specific** (recommended for this project):
```
research/ffmpeg-2025-03-27-git-114fccc4a5-full_build/bin/ffmpeg.exe
```

### Performance Considerations

**Model Size vs Speed**:
- **tiny**: ~32x realtime (10min video = 20sec processing)
- **base**: ~16x realtime (10min video = 40sec processing) ✅ Recommended
- **small**: ~6x realtime (10min video = 100sec processing)
- **medium**: ~2x realtime (10min video = 5min processing)
- **large**: ~1x realtime (10min video = 10min processing)

**Memory Requirements**:
- **tiny**: ~1GB RAM
- **base**: ~2GB RAM ✅ Recommended
- **small**: ~5GB RAM
- **medium**: ~10GB RAM
- **large**: ~20GB RAM

**GPU Acceleration**:
- CUDA-enabled GPU can speed up Whisper 5-10x
- Automatic detection and usage if available
- CPU fallback if GPU unavailable

### Error Handling

The Skill handles common errors gracefully:

1. **Network Errors**: Retry logic for downloads, timeout handling
2. **Invalid URLs**: Clear error messages with suggestions
3. **Processing Errors**: Fallback to simpler methods
4. **Missing Dependencies**: Helpful installation instructions
5. **API Errors**: Graceful degradation, fallback analysis

## Usage Instructions

### Basic Usage

```python
# Simple analysis
result = analyze_youtube_video("https://youtu.be/example")

# With video type
result = analyze_youtube_video(
    "https://youtu.be/example",
    video_type="trading_strategy"
)

# With custom model
result = analyze_youtube_video(
    "https://youtu.be/example",
    model_size="small",  # Better accuracy
    video_type="framework_tool"
)
```

### Advanced Usage

```python
# Multi-pass analysis
result = analyze_youtube_video(
    "https://youtu.be/example",
    analysis_types=["summary", "code_extraction", "task_generation"]
)

# Save intermediate files
result = analyze_youtube_video(
    "https://youtu.be/example",
    save_video=True,
    save_audio=True,
    save_transcript=True,
    output_dir="./youtube_analysis"
)

# Custom prompt
result = analyze_youtube_video(
    "https://youtu.be/example",
    custom_prompt="Extract all Python code examples and explain each one"
)
```

### Command-Line Usage

```bash
# Basic analysis
python -m youtube_video_analysis https://youtu.be/example

# With options
python -m youtube_video_analysis https://youtu.be/example \
    --type trading_strategy \
    --model base \
    --output ./analysis

# Multiple videos
python -m youtube_video_analysis \
    https://youtu.be/example1 \
    https://youtu.be/example2 \
    --type general
```

## Output Formats

### JSON (Default)
```json
{
  "video_id": "example",
  "video_url": "https://youtu.be/example",
  "title": "Video Title",
  "duration": "15:30",
  "transcription": "Full transcription text...",
  "analysis": {
    "summary": "...",
    "key_points": ["...", "..."],
    "topics": ["...", "..."]
  },
  "metadata": {
    "processed_at": "2025-10-19T14:30:00Z",
    "model_size": "base",
    "processing_time": "45.2s"
  }
}
```

### Markdown
```markdown
# Video Analysis: [Title]

## Summary
[Summary text]

## Key Points
- Point 1
- Point 2

## Topics Covered
- Topic 1
- Topic 2

## Transcription
[Full transcription]
```

### Tasks (fstrent_spec_tasks format)
```yaml
---
id: 020
title: 'Implement [Feature from Video]'
type: feature
status: pending
priority: medium
source: youtube_video
video_url: https://youtu.be/example
---

# Task: Implement [Feature]

## Objective
[Extracted from video]

## Acceptance Criteria
- [ ] [Criterion 1 from video]
- [ ] [Criterion 2 from video]

## Implementation Notes
[Extracted from video technical details]
```

## Best Practices

### Video Selection
- ✅ Choose high-quality audio (clear speech, minimal background noise)
- ✅ Prefer shorter videos (<30 minutes) for faster processing
- ✅ Ensure video language matches Whisper model language
- ❌ Avoid videos with heavy music or sound effects
- ❌ Avoid videos with multiple simultaneous speakers

### Model Selection
- **Quick preview**: Use `tiny` model
- **General use**: Use `base` model (recommended)
- **Important content**: Use `small` or `medium` model
- **Critical accuracy**: Use `large` model (slow)

### Analysis Quality
- Provide video type for better analysis
- Use custom prompts for specific extraction needs
- Review and refine output as needed
- Combine with manual review for critical content

### Resource Management
- Cache downloaded videos to avoid re-downloading
- Clean up temporary files after processing
- Use appropriate model size for available RAM
- Consider batch processing for multiple videos

## Limitations

### Current Limitations
- **Language**: Best results with English audio (Whisper supports 99 languages but accuracy varies)
- **Accuracy**: Transcription accuracy depends on audio quality and accents
- **Speed**: Large models can be slow without GPU
- **Video Length**: Very long videos (>2 hours) may require chunking
- **Content Type**: Works best with clear, structured content

### Not Supported
- ❌ Live streams (must be recorded first)
- ❌ Age-restricted videos (requires authentication)
- ❌ Private videos (requires authentication)
- ❌ DRM-protected content
- ❌ Real-time processing (must download first)

## Troubleshooting

### Common Issues

**Issue**: "Failed to download video"
- **Solution**: Check URL is valid, video is public, network connection is stable

**Issue**: "Whisper model not found"
- **Solution**: First run downloads model (~1GB), ensure sufficient disk space

**Issue**: "Out of memory"
- **Solution**: Use smaller Whisper model (tiny or base), close other applications

**Issue**: "Audio extraction failed"
- **Solution**: Ensure ffmpeg is installed and accessible, check video format

**Issue**: "Transcription is inaccurate"
- **Solution**: Use larger model, ensure good audio quality, check language setting

## Future Enhancements

### Planned Features
- [ ] Video frame analysis (extract diagrams, code screenshots)
- [ ] Multi-language support with automatic detection
- [ ] Playlist processing with batch analysis
- [ ] Real-time streaming support
- [ ] Speaker diarization (identify who said what)
- [ ] Automatic chapter detection
- [ ] Integration with RAG system for knowledge base
- [ ] Web interface for easy access

### Potential Improvements
- [ ] Faster transcription with faster-whisper
- [ ] Better code extraction with syntax highlighting
- [ ] Automatic diagram extraction from video frames
- [ ] Integration with Anki for flashcard generation
- [ ] Automatic quiz generation from content

## Resources

### Documentation
- [pytubefix Documentation](https://github.com/JuanBindez/pytubefix)
- [Whisper Documentation](https://github.com/openai/whisper)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [moviepy Documentation](https://zulko.github.io/moviepy/)

### Reference Materials
- See `reference/technology_stack.md` for detailed tech stack information
- See `reference/video_types.md` for video type definitions and prompts
- See `reference/prompt_templates.md` for LLM prompt templates
- See `reference/ffmpeg_guide.md` for FFmpeg usage and commands

### Example Files
- See `examples/` folder for sample analysis outputs
- See `examples/sample_workflow.md` for step-by-step examples

### Scripts
- See `scripts/` folder for Python implementation
- See `scripts/requirements.txt` for dependency list

---

**Version**: 1.0.0  
**Created**: 2025-10-19  
**Last Updated**: 2025-10-19  
**Maintainer**: Richard (Pied Piper)  
**Status**: Active Development

