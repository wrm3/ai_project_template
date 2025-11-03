---
name: hanx-youtube-researcher
description: Specialized YouTube video analysis with domain-specific templates (general, trading strategy, framework/tool). Extends youtube-video-analysis with structured analysis prompts from hanx YouTube Researcher Agent.
---

# Hanx YouTube Researcher Skill

Perform specialized YouTube video analysis using domain-specific prompt templates. This skill extends the base `youtube-video-analysis` skill with three powerful analysis modes optimized for different video types.

## Overview

This skill provides three specialized analysis templates that extract structured, domain-specific insights from YouTube videos:

1. **General Analysis** - Comprehensive video analysis for any content
2. **Trading Strategy Analysis** - Structured extraction of trading methodologies
3. **Framework/Tool Analysis** - Technical documentation extraction from tutorials

Each analysis type uses carefully crafted prompts to extract specific information in JSON format, making the output immediately actionable.

## When to Use This Skill

### Automatic Triggers
- User provides YouTube URL with "analyze for trading strategy"
- User mentions "extract framework details from video"
- User asks for "structured analysis of video"
- User wants "trading strategy breakdown"

### Manual Invocation
```bash
# General analysis
python specialized_analyzer.py --url https://youtu.be/example --type general

# Trading strategy analysis
python specialized_analyzer.py --url https://youtu.be/example --type trading

# Framework/tool analysis
python specialized_analyzer.py --url https://youtu.be/example --type framework
```

## Three Analysis Types

### 1. General Analysis

**Best For:**
- Educational content
- Conference talks
- Interviews
- Product demos
- General knowledge extraction

**Extracts:**
- Summary (concise overview)
- Key points (main arguments/ideas)
- Topics covered (list of subjects)
- Insights (notable takeaways)
- Questions answered (what problems this solves)
- References (external sources mentioned)

**Output Format:** JSON with structured fields

**Use Case:** "Analyze this Python conference talk and extract the key insights"

### 2. Trading Strategy Analysis

**Best For:**
- Trading strategy tutorials
- Market analysis videos
- Technical indicator guides
- Backtesting discussions
- Risk management content

**Extracts:**
- Strategy name
- Markets (crypto, forex, stocks, etc.)
- Timeframes (1H, 4H, daily, etc.)
- Indicators (RSI, MACD, EMA, etc.)
- Entry conditions (specific rules)
- Exit conditions (specific rules)
- Risk management (position sizing, stops)
- Backtest results (performance data)
- Pros and cons (advantages/disadvantages)
- Key insights (important notes)

**Output Format:** JSON with trading-specific fields

**Use Case:** "Extract the trading strategy from this video and give me the entry/exit rules"

### 3. Framework/Tool Analysis

**Best For:**
- Framework tutorials
- Tool demonstrations
- Installation guides
- Technical documentation
- Library/package overviews

**Extracts:**
- Tool/framework name
- Purpose (problem it solves)
- Target users (who should use it)
- Key features (main capabilities)
- Installation process (setup steps)
- Basic usage (getting started)
- Advanced features (power user capabilities)
- Limitations (constraints/drawbacks)
- Alternatives (competing solutions)
- Resources (docs, links, repos)

**Output Format:** JSON with technical documentation fields

**Use Case:** "Watch this FastAPI tutorial and create a setup guide with all features listed"

## Integration with Existing Skills

### Leverages youtube-video-analysis

This skill is a **lightweight extension** that focuses only on specialized analysis. It delegates to the existing `youtube-video-analysis` skill for:

- Video downloading (pytubefix)
- Audio extraction (ffmpeg/moviepy)
- Transcription (Whisper AI)

**Architecture:**
```
User Request
    ↓
hanx-youtube-researcher (specialized analysis)
    ↓
youtube-video-analysis (transcript extraction)
    ↓
Structured JSON + Markdown Report
```

### Optional RAG Integration

If `youtube-rag-storage` skill is available, analysis results can be stored in the knowledge base for future retrieval.

## Workflow Example

### Complete Analysis Flow

```bash
# Step 1: User provides video URL
$ python specialized_analyzer.py --url https://youtu.be/dQw4w9WgXcQ --type trading

# Step 2: Tool uses youtube-video-analysis to get transcript
Downloading video...
Extracting audio...
Transcribing with Whisper (base model)...
Transcript ready (5,432 characters)

# Step 3: Tool applies trading strategy prompt template
Analyzing transcript with trading strategy template...
Querying LLM...

# Step 4: Tool outputs structured JSON
{
  "strategy_name": "RSI Divergence Reversal",
  "markets": ["Crypto", "Forex"],
  "timeframes": ["1H", "4H"],
  "indicators": ["RSI (14)", "Volume", "Support/Resistance"],
  "entry_conditions": [
    "RSI shows bullish divergence (higher lows while price makes lower lows)",
    "Price reaches support level",
    "Volume confirmation on reversal candle"
  ],
  "exit_conditions": [
    "RSI reaches overbought (>70)",
    "Price hits resistance level",
    "Stop loss at 2% below entry"
  ],
  "risk_management": [
    "2% maximum risk per trade",
    "1:2 minimum risk/reward ratio"
  ],
  "backtest_results": "67% win rate over 100 trades, 1:2.3 avg R:R",
  "pros": ["Simple to identify", "Works in trending markets"],
  "cons": ["False signals in choppy markets", "Requires discipline"],
  "key_insights": ["Works best on H4 timeframe", "Combine with volume confirmation"]
}

# Step 5: Tool generates markdown report
Saved: output/RSI_Divergence_Reversal_analysis.md
Saved: output/RSI_Divergence_Reversal_analysis.json
```

## Usage Instructions

### Basic Usage

```python
from specialized_analyzer import SpecializedAnalyzer

# Initialize analyzer
analyzer = SpecializedAnalyzer()

# Analyze video
result = analyzer.analyze(
    url="https://youtu.be/example",
    analysis_type="general"
)

print(result['summary'])
print(result['key_points'])
```

### Command-Line Usage

```bash
# General analysis
python specialized_analyzer.py \
    --url https://youtu.be/example \
    --type general

# Trading analysis with output directory
python specialized_analyzer.py \
    --url https://youtu.be/example \
    --type trading \
    --output ./trading_analysis

# Framework analysis with custom model
python specialized_analyzer.py \
    --url https://youtu.be/example \
    --type framework \
    --model small \
    --output ./framework_docs
```

### Advanced Usage

```python
# Custom LLM provider
result = analyzer.analyze(
    url="https://youtu.be/example",
    analysis_type="trading",
    llm_provider="anthropic",
    llm_model="claude-sonnet-4"
)

# Save to multiple formats
analyzer.save_results(
    result,
    formats=["json", "markdown", "yaml"],
    output_dir="./analysis"
)

# Integrate with RAG
if has_rag_integration:
    analyzer.store_in_rag(result)
```

## Output Formats

### JSON Output

```json
{
  "video_id": "dQw4w9WgXcQ",
  "video_url": "https://youtu.be/dQw4w9WgXcQ",
  "analysis_type": "trading",
  "timestamp": "2025-11-01T12:00:00Z",
  "analysis": {
    "strategy_name": "RSI Divergence Reversal",
    "markets": ["Crypto", "Forex"],
    "timeframes": ["1H", "4H"],
    "indicators": ["RSI (14)", "Volume"],
    "entry_conditions": ["..."],
    "exit_conditions": ["..."],
    "risk_management": ["..."],
    "backtest_results": "...",
    "pros": ["..."],
    "cons": ["..."],
    "key_insights": ["..."]
  }
}
```

### Markdown Output

See `templates/` folder for formatted markdown templates:
- `general_analysis_template.md`
- `trading_analysis_template.md`
- `framework_analysis_template.md`

## Technical Details

### Dependencies

Inherits dependencies from `youtube-video-analysis`:
- `pytubefix>=6.0.0` - YouTube downloading
- `openai-whisper>=20231117` - Transcription
- `moviepy>=1.0.3` - Audio extraction

Additional dependencies:
- `requests>=2.31.0` - LLM API calls
- `python-dotenv>=1.0.0` - API key management

### Architecture

**Modular Design:**
```
specialized_analyzer.py (main CLI)
    ↓
analyze_general()      - General analysis
analyze_trading()      - Trading analysis
analyze_framework()    - Framework analysis
    ↓
get_transcript()       - Calls youtube-video-analysis
    ↓
query_llm()           - LLM API integration
    ↓
format_output()       - JSON + Markdown generation
```

**Key Functions:**
- `analyze_general(url, transcript)` - Apply general analysis prompt
- `analyze_trading(url, transcript)` - Apply trading strategy prompt
- `analyze_framework(url, transcript)` - Apply framework/tool prompt
- `get_transcript(url)` - Delegate to youtube-video-analysis
- `query_llm(prompt, provider)` - Call LLM API with prompt
- `format_output(analysis, template)` - Generate markdown report

### Prompt Templates

The three prompt templates are extracted directly from the hanx YouTube Researcher Agent (lines 109-199 of `agent_youtube_researcher.py`):

1. **GENERAL_PROMPT** - Comprehensive video analysis
2. **TRADING_STRATEGY_PROMPT** - Trading methodology extraction
3. **FRAMEWORK_TOOL_PROMPT** - Technical documentation extraction

These prompts are optimized for structured JSON output with specific fields for each analysis type.

## Best Practices

### Choosing Analysis Type

**General Analysis:**
- ✅ Use for: Educational content, talks, interviews
- ✅ When: You want broad understanding
- ❌ Avoid: Highly technical content (use framework instead)

**Trading Analysis:**
- ✅ Use for: Trading strategies, market analysis
- ✅ When: You need specific entry/exit rules
- ❌ Avoid: General financial news (use general instead)

**Framework Analysis:**
- ✅ Use for: Tool tutorials, installation guides
- ✅ When: You need technical documentation
- ❌ Avoid: Conceptual discussions (use general instead)

### Quality Tips

- **Clear Audio** - Better transcription = better analysis
- **Longer Videos** - More content = richer analysis
- **Focused Content** - Single topic videos work best
- **Technical Content** - Framework/trading types excel here

### Performance Optimization

- **Model Selection** - Use `base` Whisper model for speed
- **Caching** - Store transcripts to avoid re-processing
- **Batch Processing** - Analyze multiple videos in one session
- **LLM Provider** - Choose provider based on cost/quality needs

## Limitations

### Current Limitations

- **Language** - Best results with English content
- **Audio Quality** - Poor audio affects transcription accuracy
- **Video Length** - Very long videos (>2 hours) may need chunking
- **Specialized Domains** - May miss domain-specific jargon

### Not Supported

- ❌ Real-time analysis (must download first)
- ❌ Live streams (must be recorded)
- ❌ Age-restricted videos (requires auth)
- ❌ Private videos (requires auth)

## Troubleshooting

### Common Issues

**Issue**: "Failed to get transcript"
- **Solution**: Ensure youtube-video-analysis skill is installed
- **Solution**: Check video URL is valid and accessible

**Issue**: "LLM API error"
- **Solution**: Verify API key is set in environment
- **Solution**: Check API provider is supported

**Issue**: "Invalid analysis type"
- **Solution**: Must be one of: general, trading, framework

**Issue**: "JSON parsing error"
- **Solution**: LLM response may not be valid JSON
- **Solution**: Check raw response in output file

## Future Enhancements

### Planned Features

- [ ] Support for additional analysis types (security, architecture, etc.)
- [ ] Multi-language support with automatic detection
- [ ] Batch video processing
- [ ] Custom prompt templates via configuration
- [ ] Integration with fstrent_spec_tasks for task generation
- [ ] RAG integration for knowledge persistence

### Potential Improvements

- [ ] Automatic analysis type detection based on video content
- [ ] Confidence scores for extracted information
- [ ] Cross-video comparison and aggregation
- [ ] Export to additional formats (YAML, CSV, etc.)

## Resources

### Documentation
- See `reference/prompt_templates.md` for full prompt text
- See `reference/output_schemas.md` for JSON schema definitions
- See `examples/` for workflow demonstrations

### Example Files
- `examples/general_analysis_example.md` - General analysis workflow
- `examples/trading_analysis_example.md` - Trading strategy extraction
- `examples/framework_analysis_example.md` - Framework documentation

### Related Skills
- `youtube-video-analysis` - Base video processing (required)
- `youtube-rag-storage` - Knowledge persistence (optional)

---

**Version**: 1.0.0
**Created**: 2025-11-01
**Source**: Hanx YouTube Researcher Agent
**Maintainer**: AI Project Template Team
**Status**: Active Development
