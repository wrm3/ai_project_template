# Deep Research Skill - Setup Guide

## Overview

The Deep Research Skill has two versions:

1. **Simple Research** (Lightweight) - Basic multi-source research
2. **Full Deep Research** (Advanced) - Complete AI agent with all features

## Quick Start - Simple Research (Recommended to Start)

### 1. Install Minimal Dependencies

```bash
cd /mnt/c/git/ai_project_template

# Option A: Install minimal requirements only
pip install requests beautifulsoup4 duckduckgo-search

# Option B: Install from requirements file (includes optional)
pip install -r .claude/skills/deep-research/requirements.txt
```

### 2. Test Simple Research

```bash
python3 .claude/skills/deep-research/scripts/simple_research.py "React hooks" --pages=10
```

This should generate a research report in `docs/research/`.

### 3. Usage

```bash
# Basic usage
python3 .claude/skills/deep-research/scripts/simple_research.py "your topic"

# Specify output
python3 .claude/skills/deep-research/scripts/simple_research.py "your topic" --output=path/to/report.md

# Target more sources
python3 .claude/skills/deep-research/scripts/simple_research.py "your topic" --pages=20
```

## Advanced Setup - Full Deep Research

For the full-featured research engine with:
- Pydantic AI agent (GPT-4o autonomous reasoning)
- PDF parsing
- Perplexity integration
- Multi-phase iterative research (30-50+ pages)
- Citation verification
- Budget tracking

### Prerequisites

1. **OpenAI API Key** (required)
2. **Perplexity API Key** (optional but recommended)
3. **Python 3.10+**

### 1. Set Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
PERPLEXITY_API_KEY=pplx-your-key-here  # Optional
```

Or export directly:

```bash
export OPENAI_API_KEY="sk-your-key-here"
export PERPLEXITY_API_KEY="pplx-your-key-here"  # Optional
```

### 2. Install Full Dependencies

The full research engine requires the MCP deep research implementation:

```bash
cd /mnt/c/git/ai_project_template/research/mcps/fstrent_mcp_deep_research

# Install all dependencies (large list!)
pip install -r requirements.txt

# Or install just the essentials:
pip install pydantic-ai openai requests beautifulsoup4 duckduckgo-search PyMuPDF python-dotenv
```

### 3. Verify Setup

```bash
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "test" --mode=quick
```

If you see the research banner and no dependency errors, you're set!

### 4. Full Usage

```bash
# Quick research (5-10 pages)
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=quick

# Standard research (10-20 pages)
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=standard

# Comprehensive research (20-30 pages)
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=comprehensive

# Iterative research (30-50+ pages) - THE GAME CHANGER!
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=iterative --budget=10.00

# Focused research (deep dive on specific aspect)
python3 .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=focused --focus="specific aspect"
```

## Comparison

| Feature | Simple Research | Full Deep Research |
|---------|----------------|-------------------|
| **Dependencies** | 3 packages | 10+ packages + MCP |
| **Setup Time** | 2 minutes | 10-15 minutes |
| **AI Reasoning** | No | Yes (GPT-4o agent) |
| **Max Pages** | ~10 pages | 50+ pages (iterative) |
| **PDF Parsing** | No | Yes |
| **Citation Verification** | No | Yes |
| **Perplexity Integration** | No | Yes |
| **Cost** | Free (no API) | Requires OpenAI API |
| **Best For** | Quick research, learning | Production, comprehensive analysis |

## Troubleshooting

### Simple Research Issues

**"ModuleNotFoundError: No module named 'requests'"**
```bash
pip install requests beautifulsoup4 duckduckgo-search
```

**"No search results found"**
- Check internet connection
- Try different topic (more specific)
- DuckDuckGo may be rate limiting (wait a minute)

**"Permission denied"**
```bash
chmod +x .claude/skills/deep-research/scripts/simple_research.py
```

### Full Deep Research Issues

**"Deep research tools not available"**
- Check that `research/mcps/fstrent_mcp_deep_research` exists
- Install dependencies: `pip install pydantic-ai openai`
- Set OPENAI_API_KEY environment variable

**"ModuleNotFoundError: No module named 'pydantic_ai'"**
```bash
pip install pydantic-ai
```

**"OPENAI_API_KEY not found"**
```bash
export OPENAI_API_KEY="sk-your-key-here"
# Or add to .env file
```

**"Budget exceeded"**
- Increase budget: `--budget=15.00`
- Use less comprehensive mode: `--mode=standard` instead of `--mode=iterative`

## Recommendations

### For Learning/Testing
Start with **Simple Research**:
- No API keys needed
- Fast setup
- Good for understanding workflows
- Free to use

### For Production Use
Upgrade to **Full Deep Research**:
- AI-powered autonomous reasoning
- Much higher quality reports
- Advanced features (PDF, citations, iterative)
- Worth the API costs for important research

## Next Steps

1. **Start Simple**: Test with simple_research.py
2. **Get API Keys**: Sign up for OpenAI (and optionally Perplexity)
3. **Install Full Version**: Follow advanced setup steps
4. **Run Comprehensive Research**: Use iterative mode for mind-blowing results

## Cost Estimates

### Full Deep Research (with OpenAI API)

- **Quick** mode: ~$0.10 - $0.50
- **Standard** mode: ~$0.50 - $2.00
- **Comprehensive** mode: ~$2.00 - $5.00
- **Iterative** mode: ~$5.00 - $20.00 (set budget limits!)

Costs vary based on topic complexity and content length.

## Support

For issues or questions:
1. Check this SETUP.md
2. Review skill.md for usage guidance
3. Check rules.md for best practices
4. Review error messages carefully

## Version History

- **v1.0**: Simple research (lightweight, no dependencies)
- **v2.0**: Full deep research (AI agent, all features)
