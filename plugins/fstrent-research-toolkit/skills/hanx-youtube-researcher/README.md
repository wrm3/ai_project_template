# Hanx YouTube Researcher Skill

Specialized YouTube video analysis using domain-specific prompt templates from the hanx YouTube Researcher Agent.

## Quick Start

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# General analysis
python scripts/specialized_analyzer.py \
    --url https://youtu.be/example \
    --type general

# Trading strategy analysis
python scripts/specialized_analyzer.py \
    --url https://youtu.be/example \
    --type trading

# Framework/tool analysis
python scripts/specialized_analyzer.py \
    --url https://youtu.be/example \
    --type framework
```

## Three Analysis Types

1. **General** - Comprehensive video analysis (summary, key points, topics, insights)
2. **Trading** - Trading strategy extraction (entry/exit rules, indicators, risk management)
3. **Framework** - Technical documentation (installation, features, usage, limitations)

## Directory Structure

```
hanx-youtube-researcher/
├── SKILL.md                    # Complete skill documentation
├── README.md                   # This file (quick reference)
├── rules.md                    # Best practices and integration patterns
├── scripts/
│   ├── specialized_analyzer.py # Main CLI tool (415 lines)
│   └── requirements.txt        # Python dependencies
├── templates/
│   ├── general_analysis_template.md
│   ├── trading_analysis_template.md
│   └── framework_analysis_template.md
├── examples/
│   ├── general_analysis_example.md
│   ├── trading_analysis_example.md
│   └── framework_analysis_example.md
└── reference/
    └── prompt_templates.md     # Complete prompt template reference
```

## Integration

### Required: youtube-video-analysis

This skill delegates video downloading, audio extraction, and transcription to the `youtube-video-analysis` skill. Make sure it's installed first.

### Optional: youtube-rag-storage

If available, analysis results can be stored in the RAG system for future retrieval.

## Key Features

- **Domain-Specific Prompts** - Three specialized templates optimized for different content types
- **Structured JSON Output** - Consistent schema for easy parsing and automation
- **Markdown Reports** - Human-readable formatted reports
- **LLM Provider Flexibility** - Works with OpenAI, Anthropic, and hanx_tools LLM APIs
- **Lightweight Architecture** - Delegates infrastructure to existing skills

## Examples

See the `examples/` directory for complete workflow demonstrations:
- General analysis of Python conference talk
- Trading strategy extraction from RSI divergence video
- Framework documentation from FastAPI tutorial

## Documentation

- **SKILL.md** - Complete skill documentation (600+ lines)
- **rules.md** - Best practices and integration patterns (500+ lines)
- **reference/prompt_templates.md** - Complete prompt template reference

## Requirements

- Python 3.8+
- youtube-video-analysis skill (for transcript extraction)
- LLM API access (OpenAI or Anthropic recommended)

## Output Formats

- **JSON** - Structured data with consistent schema
- **Markdown** - Formatted reports using templates
- **YAML** - Optional (requires PyYAML)

## Command-Line Options

```
--url URL              YouTube video URL (required)
--type TYPE            Analysis type: general, trading, framework (required)
--output DIR           Output directory (default: ./output)
--model SIZE           Whisper model size (default: base)
--formats FORMAT+      Output formats: json, markdown, yaml (default: json markdown)
--provider PROVIDER    LLM provider (default: openai)
```

## Version

**Version:** 1.0.0
**Created:** 2025-11-01
**Source:** Hanx YouTube Researcher Agent
**Status:** Active Development

---

**Need Help?** See SKILL.md for complete documentation, rules.md for best practices, or examples/ for workflow demonstrations.
