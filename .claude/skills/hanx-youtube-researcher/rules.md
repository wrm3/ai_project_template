# Hanx YouTube Researcher - Rules and Best Practices

## Overview

This file defines the rules, best practices, and integration patterns for the Hanx YouTube Researcher skill. This skill extends youtube-video-analysis with specialized domain-specific analysis capabilities.

## Core Principles

### 1. Lightweight Extension Philosophy

**Do:**
- Delegate video downloading to youtube-video-analysis
- Delegate audio extraction to youtube-video-analysis
- Delegate transcription to youtube-video-analysis
- Focus ONLY on the specialized analysis layer

**Don't:**
- Duplicate video downloading logic
- Reimplement audio extraction
- Reimplement transcription
- Create monolithic all-in-one solution

**Rationale:** This skill adds value through specialized prompt templates, not by reimplementing infrastructure.

### 2. Structured Output First

**Do:**
- Always return JSON with consistent schema
- Use exact field names from prompt templates
- Provide fallback for non-JSON responses
- Include metadata in all outputs

**Don't:**
- Return unstructured text
- Vary field names between runs
- Skip error handling for malformed responses
- Omit timestamp and source information

**Rationale:** Structured output enables automation, validation, and downstream processing.

### 3. Domain-Specific Expertise

**Do:**
- Use appropriate analysis type for content
- Provide clear guidance on type selection
- Extract domain-specific fields accurately
- Include domain context in outputs

**Don't:**
- Apply general analysis to trading videos
- Mix analysis types
- Skip domain-specific fields
- Lose technical details in summarization

**Rationale:** Domain-specific analysis provides more actionable insights than generic summaries.

## Analysis Type Selection Rules

### When to Use General Analysis

**Use for:**
- Educational content (conference talks, tutorials)
- Interviews and podcasts
- Product demonstrations
- General knowledge videos
- Multi-topic discussions

**Avoid for:**
- Trading strategy videos (use trading analysis)
- Framework tutorials (use framework analysis)
- Highly technical content with specific methodologies

**Quality Indicators:**
- Video covers multiple topics
- Content is conceptual rather than procedural
- Goal is knowledge extraction, not implementation
- Audience is general rather than specialist

### When to Use Trading Strategy Analysis

**Use for:**
- Trading strategy explanations
- Technical analysis tutorials
- Indicator usage guides
- Backtesting discussions
- Risk management content
- Market analysis with specific rules

**Avoid for:**
- General financial news
- Economic theory discussions
- Company analysis (fundamental analysis)
- General investment advice

**Quality Indicators:**
- Video presents specific entry/exit rules
- Technical indicators are mentioned
- Risk/reward ratios discussed
- Timeframes and markets specified
- Backtest results provided

### When to Use Framework/Tool Analysis

**Use for:**
- Framework tutorials (FastAPI, React, etc.)
- Library demonstrations
- Tool installation guides
- Technical documentation videos
- Software setup walkthroughs

**Avoid for:**
- Conceptual programming discussions
- Algorithm explanations
- General coding tutorials without specific tools
- Theory-focused content

**Quality Indicators:**
- Video demonstrates specific tool/framework
- Installation steps are provided
- Code examples are shown
- Features are enumerated
- Alternatives are mentioned

## Integration Patterns

### With youtube-video-analysis Skill

**Required Integration:**

```python
# Call youtube-video-analysis for transcript
from youtube_video_analysis import analyze_video

result = analyze_video(url, model_size="base")
transcript = result["transcript"]
metadata = result["metadata"]

# Then apply specialized analysis
analysis = analyze_trading(transcript)
```

**Best Practices:**
- Always check if youtube-video-analysis is available
- Provide clear error message if not found
- Pass through Whisper model size parameter
- Reuse transcript for multiple analysis types
- Cache transcript to avoid re-processing

### With youtube-rag-storage Skill (Optional)

**Optional Integration:**

```python
# After analysis, store in RAG if available
if has_rag_integration:
    store_in_rag(
        content=analysis,
        metadata={
            "source": "youtube",
            "analysis_type": analysis_type,
            "video_url": url
        }
    )
```

**Best Practices:**
- Make RAG integration optional
- Don't fail if RAG not available
- Include analysis type in metadata
- Store structured JSON, not markdown
- Tag with appropriate categories

### With fstrent_spec_tasks (Future)

**Potential Integration:**

```python
# Generate tasks from framework analysis
if analysis_type == "framework":
    generate_tasks_from_framework_analysis(analysis)
    # Creates tasks like:
    # - "Install FastAPI"
    # - "Implement basic endpoint"
    # - "Add authentication"
```

**Best Practices:**
- Make task generation opt-in
- Use analysis fields to create specific tasks
- Include video URL as reference
- Set appropriate priority/status

## Prompt Template Rules

### Template Maintenance

**Do:**
- Keep prompts synchronized with source (agent_youtube_researcher.py)
- Use exact JSON schema from prompts
- Test prompts with various LLM providers
- Version prompts if modified

**Don't:**
- Modify prompts without testing
- Remove fields from JSON schema
- Add fields without updating templates
- Skip documentation of changes

### Template Usage

**Do:**
- Format transcript into prompt template
- Validate LLM response against schema
- Handle JSON parsing errors gracefully
- Provide raw response on parse failure

**Don't:**
- Send transcript without template
- Assume response is valid JSON
- Fail silently on parse errors
- Lose information in error cases

## Output Format Rules

### JSON Output

**Required Fields:**
```json
{
  "video_url": "string",
  "analysis_type": "general|trading|framework",
  "timestamp": "ISO8601 datetime",
  "metadata": {},
  "analysis": {}
}
```

**Best Practices:**
- Always include all required fields
- Use ISO8601 for timestamps
- Include original video URL
- Preserve metadata from youtube-video-analysis
- Use UTF-8 encoding
- Pretty-print with 2-space indent

### Markdown Output

**Best Practices:**
- Use templates for consistent formatting
- Include video metadata at top
- Format lists as bullet points
- Add disclaimer for trading analysis
- Include generation timestamp
- Link to source video

### File Naming

**Pattern:**
```
{analysis_type}_analysis_{timestamp}.{extension}
```

**Examples:**
- `trading_analysis_20251101_140000.json`
- `framework_analysis_20251101_160000.md`
- `general_analysis_20251101_120000.yaml`

## Error Handling Rules

### Dependency Errors

**When youtube-video-analysis not found:**
```python
raise FileNotFoundError(
    "youtube-video-analysis skill not found. "
    "Please install youtube-video-analysis skill first."
)
```

**When LLM API not available:**
```python
print("[WARN] LLM API not available")
print("Please ensure you have either:")
print("  1. hanx_tools/hanx_apis installed, OR")
print("  2. openai package + OPENAI_API_KEY environment variable")
raise
```

### Processing Errors

**When transcript extraction fails:**
- Show clear error message
- Include URL in error message
- Suggest troubleshooting steps
- Exit with non-zero status code

**When LLM response is invalid JSON:**
- Print warning
- Save raw response to file
- Return fallback structure with raw_response field
- Continue processing

**When analysis type is invalid:**
- Print available types
- Show usage examples
- Exit with error message

## Performance Best Practices

### Caching Strategy

**Do:**
- Cache transcripts for reuse
- Store intermediate results
- Reuse transcript for multiple analysis types
- Clean up temporary files after completion

**Don't:**
- Re-download video for each analysis
- Re-transcribe for each analysis type
- Keep large video files indefinitely
- Fill up disk with temporary files

### Batch Processing

**Do:**
- Support analyzing multiple videos
- Process transcripts in parallel if possible
- Show progress indicators
- Handle partial failures gracefully

**Don't:**
- Fail entire batch on single error
- Block on sequential processing
- Skip error reporting
- Lose successful results on failure

## Security Best Practices

### API Key Management

**Do:**
- Load API keys from environment variables
- Use .env files (not committed to git)
- Provide clear setup instructions
- Support multiple LLM providers

**Don't:**
- Hardcode API keys
- Commit API keys to repository
- Log API keys in output
- Share API keys in examples

### Input Validation

**Do:**
- Validate YouTube URLs
- Check analysis type is valid
- Sanitize file paths
- Validate model size parameter

**Don't:**
- Trust user input without validation
- Allow arbitrary file paths
- Execute user-provided code
- Skip input sanitization

## Quality Assurance Rules

### Testing Requirements

**Must Test:**
- All three analysis types
- Error handling (missing dependencies, invalid URLs, API errors)
- Output format validation (JSON schema, markdown structure)
- Integration with youtube-video-analysis
- Multiple LLM providers

**Should Test:**
- Various video lengths
- Different audio quality levels
- Multiple languages (if supported)
- Edge cases (very short/long videos)

### Documentation Requirements

**Must Document:**
- All three analysis types with examples
- Integration with youtube-video-analysis
- LLM API setup and configuration
- Output format specifications
- Error messages and troubleshooting

**Should Document:**
- Choosing appropriate analysis type
- Performance characteristics
- Limitations and known issues
- Future enhancement plans

## Version Compatibility

### youtube-video-analysis Compatibility

**Required:**
- youtube-video-analysis must provide transcript
- Must support command-line invocation
- Must save transcript to predictable location

**Recommended:**
- Version >= 1.0.0
- Supports --skip-download and --skip-transcription flags
- Provides metadata in JSON format

### LLM Provider Compatibility

**Supported Providers:**
- OpenAI (gpt-4, gpt-3.5-turbo)
- Anthropic (claude-3, claude-2)
- Any provider supported by hanx_tools/hanx_apis

**Required API Features:**
- Chat completion endpoint
- JSON mode or reliable JSON output
- Reasonable context window (8K+ tokens)

## Maintenance Rules

### Prompt Template Updates

**When to Update:**
- Source prompts change in agent_youtube_researcher.py
- LLM providers change capabilities
- JSON schema needs expansion
- Quality issues identified

**How to Update:**
- Update all three prompts together
- Test with sample videos
- Update examples and documentation
- Version the change

### Code Maintenance

**Regular Tasks:**
- Update dependencies
- Test with latest youtube-video-analysis
- Verify LLM provider compatibility
- Update examples with current videos
- Check for deprecated APIs

**Best Practices:**
- Follow Python style guide (PEP 8)
- Add type hints to functions
- Document all public APIs
- Keep dependencies minimal
- Write self-documenting code

---

**Last Updated:** 2025-11-01
**Skill Version:** 1.0.0
**Compatible With:** youtube-video-analysis >= 1.0.0
