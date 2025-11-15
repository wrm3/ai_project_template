# Deep Research Skill - Claude-Native Implementation

## Overview

This is a **Claude-native autonomous research methodology** - no external APIs, no Python scripts, no dependencies. Just Claude using its built-in tools (WebSearch, WebFetch) to conduct comprehensive, multi-phase research.

## What This Is

**An autonomous research workflow for Claude** that enables:
- Comprehensive multi-source research
- Professional markdown reports with citations
- Synthesis and analysis (not just summarization)
- Comparison analysis and recommendations
- 5-50+ source analysis depending on mode

## How It Works

When you (Claude) use this skill:

1. **You plan the research** - determine mode, search strategy
2. **You gather information** - WebSearch + WebFetch in parallel
3. **You analyze and synthesize** - connect findings, provide insights
4. **You write professional reports** - structured markdown with citations
5. **You save the research** - Write tool to docs/research/

**No external tools. Just your reasoning + WebSearch + WebFetch.**

## Research Modes

| Mode | Sources | Time | Best For |
|------|---------|------|----------|
| **Quick** | 5-10 | ~10 min | Overviews, quick questions |
| **Standard** | 10-15 | ~20 min | Most requests (DEFAULT) |
| **Comprehensive** | 20-25 | ~40 min | Critical decisions, detailed analysis |
| **Iterative** | 30-50 | ~60 min | Exhaustive research, multi-faceted topics |

## Key Features

### 1. Autonomous Research
- Claude conducts entire research process
- Plans search strategy
- Gathers from multiple sources
- Analyzes and synthesizes
- Writes professional reports

### 2. Multi-Source Analysis
- Parallel web searches (4-8 queries)
- Parallel content fetching (10-50 sources)
- Source quality assessment
- Citation verification
- Cross-source synthesis

### 3. Professional Output
- Executive summaries
- Organized findings by theme
- Comparison tables
- Best practices
- Clear recommendations
- Complete citations

### 4. No Dependencies
- ❌ No Python scripts
- ❌ No external APIs (OpenAI, Perplexity)
- ❌ No API keys needed
- ❌ No installation required
- ✅ Just Claude + WebSearch + WebFetch

## Usage

### For Claude

When user requests research:
1. Read `skill.md` for methodology
2. Read `rules.md` for best practices
3. Execute research workflow
4. Use template from `templates/`

### For Users

Simply ask Claude to research something:

```
"Research React state management solutions comprehensively"
"Deep dive into Next.js authentication best practices"
"Compare task management systems for development teams"
"Investigate Claude Code sub-agents implementation"
```

Claude will:
- Determine appropriate research mode
- Conduct multi-source research
- Analyze and synthesize findings
- Write comprehensive report
- Save to docs/research/
- Summarize key findings

## Files

```
.claude/skills/deep-research/
├── README.md                          # This file
├── skill.md                           # Complete research methodology
├── rules.md                           # Best practices and guidelines
└── templates/
    └── research_report_template.md   # Report structure template
```

## Advantages Over Previous Version

| Aspect | Old (OpenAI-based) | New (Claude-native) |
|--------|-------------------|---------------------|
| **Dependencies** | Pydantic AI, OpenAI, many packages | None - built-in tools |
| **API Keys** | OPENAI_API_KEY required | None required |
| **Cost** | $0.50-$20 per research | Free (Claude is already running) |
| **Setup** | Install dependencies, configure | No setup needed |
| **Execution** | Python script via Bash | Direct Claude execution |
| **Flexibility** | Fixed workflow | Adaptive based on topic |
| **Quality** | GPT-4o reasoning | Claude reasoning (arguably better!) |

## Example Workflow

**User**: "Research API design best practices"

**Claude**:
```
I'll conduct standard research on API design best practices.
This will analyze 10-15 authoritative sources and take about 20 minutes.

🔍 Searching for sources...
[Executes 5 WebSearch queries in parallel]

📥 Fetching content from sources...
[Executes 12 WebFetch calls in parallel]

🧠 Analyzing and synthesizing findings...
[Analyzes content, identifies patterns, synthesizes insights]

✍️ Writing comprehensive report...
[Creates professional markdown report]

✅ Research complete!

Key findings:
1. REST principles remain gold standard for most APIs
2. GraphQL preferred for complex data requirements
3. API versioning critical from day one

Full 15-page report with comparison analysis, best practices, and
recommendations saved to: docs/research/api_design_best_practices_20251020.md

Would you like me to dive deeper into any specific aspect?
```

## Output Quality

Every report includes:
- **Executive Summary** - Key findings in 2-3 paragraphs
- **Research Objective** - What was researched and why
- **Key Findings** - Organized by theme with analysis
- **Comparisons** - Tables comparing options (if applicable)
- **Best Practices** - Industry standards and recommendations
- **Recommendations** - Clear, actionable guidance
- **References** - Complete citations with URLs
- **Metadata** - Research date, mode, confidence levels

## Comparison to Other Approaches

### vs Manual Web Search
- **Manual**: User searches, reads, synthesizes
- **This**: Claude does all of it autonomously

### vs ChatGPT with Browsing
- **ChatGPT**: Single pass, limited context
- **This**: Multi-phase, systematic methodology, structured output

### vs Perplexity
- **Perplexity**: Quick answers (~1-2 pages)
- **This**: Comprehensive reports (5-50 pages) with deep analysis

### vs Research Agents (Pydantic AI, etc.)
- **Agents**: External tools, dependencies, setup
- **This**: Built-in, no setup, Claude-native

## Best Practices

1. **Match mode to need** - Quick for simple, Comprehensive for critical
2. **Use parallel tool calls** - Faster execution
3. **Prioritize source quality** - Official docs > blogs
4. **Synthesize, don't summarize** - Add insights, not just lists
5. **Cite everything** - All claims need sources
6. **Professional output** - Well-structured reports
7. **Save research** - Always use Write tool
8. **Summarize for user** - Don't dump full report

## When to Use

✅ **Use this skill when user needs**:
- Comprehensive analysis
- Technology comparisons
- Best practices research
- Deep technical investigation
- Multi-source verification
- Professional reports

❌ **Don't use when**:
- Simple factual lookup (just answer directly)
- User already knows what they want
- Code-specific questions (search codebase instead)
- Real-time/breaking news only

## Success Metrics

Research is successful when:
- User's question is thoroughly answered
- Multiple authoritative sources consulted
- Information is synthesized with insights
- Recommendations are clear and actionable
- Report is professional and well-organized
- User can make informed decision

## Previous Versions

The OpenAI-based version is archived at:
`.claude/skills/deep-research-openai-version/`

It remains available if you want:
- Pydantic AI agent approach
- PDF parsing capabilities
- Perplexity integration
- Iterative research controller

But requires:
- Python dependencies
- OpenAI API key
- Complex setup

## Philosophy

**Research is a reasoning task, not just information gathering.**

Claude's strength is:
- Synthesizing information across sources
- Identifying patterns and connections
- Providing nuanced analysis
- Making thoughtful recommendations

This skill applies that strength systematically to research tasks.

## Conclusion

This is research **by Claude, for users** - leveraging Claude's built-in tools and reasoning capabilities to deliver comprehensive, professional research reports without any external dependencies.

**Simple. Powerful. Native.**

---

**Created**: 2025-10-20
**Version**: 2.0 (Claude-native)
**Status**: Production-ready
