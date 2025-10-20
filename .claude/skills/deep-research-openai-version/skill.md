Base directory for this skill: /mnt/c/git/ai_project_template/.claude/skills/deep-research-openai-version

# AI Deep Research Skill - Mind-Blowingly Competitive

**IMPORTANT: This is NOT a manual research guide. This is an AUTONOMOUS AI RESEARCH ENGINE that conducts comprehensive research FOR YOU.**

## What Makes This Different

This skill wraps a **Pydantic AI-powered research agent** that uses GPT-4o to autonomously:
- Conduct multi-phase research with iterative refinement
- **Break context window limits** to produce 30-50+ page documents
- Search across multiple engines (DuckDuckGo, Perplexity, browser automation)
- Parse PDF documents (regulations, papers, reports)
- Verify citations and assess source quality
- Generate professional markdown research reports

**This is NOT web scraping. This is AI REASONING through research.**

## When to Use This Skill

Use this skill when the user needs:
- **Comprehensive research reports** (10-50+ pages)
- **Technical deep dives** with multiple sources
- **Competitive analysis** across multiple options
- **Regulatory research** requiring PDF parsing
- **Academic literature reviews** with citations
- **Market research** with synthesis and recommendations

**Trigger phrases**: "research", "comprehensive analysis", "deep dive", "literature review", "investigate thoroughly", "analyze extensively"

## Research Modes Available

### 1. Quick Research (5-10 pages, ~5-10 min)
**Good for**: Initial exploration, quick fact-finding, preliminary reports

**When to use**:
- User needs quick overview
- Time-sensitive requests
- Preliminary investigation before deeper work

**Example**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "React best practices 2025" --mode=quick
```

---

### 2. Standard Research (10-20 pages, ~10-20 min)
**Good for**: Most use cases, balanced depth and breadth, professional reports

**When to use**:
- Default mode for most research requests
- Technical documentation needs
- Feature comparison and analysis
- Best practices research

**Example**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "Machine Learning model deployment strategies" --mode=standard
```

---

### 3. Comprehensive Research (20-30 pages, ~20-30 min)
**Good for**: Academic papers, detailed technical docs, thorough investigations

**When to use**:
- User explicitly requests "comprehensive" or "thorough" research
- Academic or scholarly work
- Detailed technical specifications needed
- Multiple perspectives required

**Example**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "Cloud Native Architecture Patterns" --mode=comprehensive
```

---

### 4. **Iterative Research (30-50+ pages, ~30-60 min) - THE GAME CHANGER**
**Good for**: Exhaustive research, books, comprehensive guides, regulatory analysis

**THE INNOVATION**: This mode **breaks through context window limitations** using multi-phase research:

**How it works**:
1. **Phase 1**: Overview Research - Understand the landscape
2. **Phase 2**: Identify Sections - Break into research areas
3. **Phase 3**: Deep Dive Sections - Detailed research per area (each section gets full context!)
4. **Phase 4**: Synthesis - Combine into cohesive 30-50+ page document

**When to use**:
- User needs "exhaustive" or "complete" research
- Regulatory compliance documentation
- Book chapter or whitepaper creation
- Multi-faceted topics requiring deep coverage
- When 20-30 pages isn't enough

**Example**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "US Banking Regulatory Requirements" --mode=iterative --budget=10.00
```

**Budget Control**: Use `--budget=X.XX` to limit API costs (0 = unlimited)

---

### 5. Focused Research (Deep dive on specific aspect, ~10-15 min)
**Good for**: Answering specific questions, drilling into one area

**When to use**:
- User wants deep analysis of ONE specific aspect
- Follow-up research on particular detail
- Targeted investigation

**Example**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "React" --mode=focused --focus="hooks and state management best practices"
```

## How to Use This Skill

### Basic Pattern
1. **User asks for research** on a topic
2. **You determine appropriate mode** based on depth needed
3. **You call the research script** via Bash tool
4. **Script runs autonomously** (AI agent does the work!)
5. **You receive markdown report** and summarize for user

### Step-by-Step Example

**User**: "I need comprehensive research on authentication methods for Next.js applications"

**Your Response**:
```
I'll conduct comprehensive research on authentication methods for Next.js. This will produce a 20-30 page report analyzing multiple solutions with comparisons, code examples, and recommendations.

Let me start the research...
```

**You execute**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "Authentication methods for Next.js applications" --mode=comprehensive --output=docs/research/nextjs_auth_analysis.md
```

**Script runs** (AI agent autonomously):
- Searches multiple sources
- Analyzes options (NextAuth.js, Clerk, Auth0, etc.)
- Compares features, pricing, use cases
- Verifies citations
- Generates 20-30 page markdown report

**You then**:
- Read the generated report
- Summarize key findings for user
- Answer follow-up questions using report as reference

## Research Capabilities

### Multi-Search Strategies
The AI agent automatically uses:
- **DuckDuckGo**: Privacy-focused broad search
- **Perplexity AI**: Real-time information with citations
- **Browser Automation**: When API rate limits hit
- **Alternative Engines**: Fallback strategies

### PDF Document Parsing
Automatically extracts text from:
- Regulatory documents
- Financial forms
- Technical specifications
- Research papers
- Official guidance

### Citation Verification
The agent verifies sources by:
- Checking URL accessibility
- Assessing domain reputation (government, academic, financial trusted domains)
- Categorizing source types
- Providing quality scores

### Structured Output
Every report includes:
- **Executive Summary**: Key findings in 2-3 paragraphs
- **Detailed Analysis**: Comprehensive breakdown
- **Key Findings**: Bulleted insights
- **Official Documents**: Table of authoritative sources
- **Sources and References**: Numbered citations
- **Recommendations**: Actionable guidance
- **Related Topics**: Areas for further research
- **Research Metadata**: AI model, date, transparency info

## Output Format

Reports are saved as professional markdown files with:
- Clear hierarchical structure (H1-H4 headings)
- Tables for comparisons
- Numbered citations
- Code blocks where appropriate
- Metadata footer

**Default location**: `docs/research/<topic>_<timestamp>.md`

**Custom location**: Use `--output=path/to/file.md`

## Environment Requirements

The script requires:
- **OPENAI_API_KEY**: For GPT-4o (Pydantic AI agent)
- **PERPLEXITY_API_KEY** (optional): For Perplexity deep analysis
- Python packages: `pydantic-ai`, `requests`, `beautifulsoup4`, `PyMuPDF` (for PDF parsing), `duckduckgo-search`

**Check if available**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "test" --mode=quick
```

If dependencies missing, script will report what's needed.

## Common Use Cases

### Use Case 1: Technology Comparison
**User**: "Compare state management solutions for React"

**Your action**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "React state management solutions comparison" --mode=comprehensive
```

**Result**: 20-30 page report comparing Redux, MobX, Zustand, Jotai, etc. with pros/cons, use cases, code examples

---

### Use Case 2: Best Practices Research
**User**: "What are the best practices for API design?"

**Your action**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "RESTful API design best practices" --mode=standard
```

**Result**: 10-20 page guide with industry standards, common patterns, anti-patterns, examples

---

### Use Case 3: Regulatory Compliance
**User**: "I need to understand FFIEC-041 reporting requirements"

**Your action**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "FFIEC-041 banking reporting requirements" --mode=iterative --budget=15.00
```

**Result**: 30-50+ page comprehensive guide with:
- Official PDF documents parsed
- Detailed requirements
- Compliance procedures
- Regulatory citations
- Implementation guidance

---

### Use Case 4: Deep Dive on Specific Topic
**User**: "I want to deeply understand React Server Components"

**Your action**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "React" --mode=focused --focus="Server Components architecture and implementation"
```

**Result**: Targeted deep dive on just Server Components with detailed technical analysis

---

### Use Case 5: Academic Literature Review
**User**: "Research the current state of transformer models in NLP"

**Your action**:
```bash
python .claude/skills/deep-research/scripts/ai_deep_research.py "Transformer models in Natural Language Processing 2025" --mode=comprehensive
```

**Result**: 20-30 page literature review with:
- Current state of field
- Key papers and research
- Recent developments
- Citations and references
- Future directions

## Best Practices

### 1. Choose the Right Mode
- **Quick**: When user just needs overview or has time constraints
- **Standard**: Default for most professional research needs
- **Comprehensive**: When detail matters, academic work, thorough analysis
- **Iterative**: When comprehensive isn't enough, need exhaustive coverage
- **Focused**: When diving deep into ONE specific aspect

### 2. Set Expectations
Tell the user:
- How long research will take (~5-60 minutes depending on mode)
- What they'll get (page count, depth)
- That this is AI-powered autonomous research (not manual)

### 3. Use Budget Limits
For iterative mode, set budget to prevent runaway costs:
- `--budget=5.00`: Conservative, might limit depth
- `--budget=10.00`: Reasonable for most topics
- `--budget=15.00`: Generous for complex topics
- `--budget=0`: No limit (use carefully!)

### 4. Custom Output Paths
Organize research by topic or project:
```bash
--output=docs/research/authentication/nextjs_auth_2025.md
--output=projects/myapp/research/architecture_patterns.md
```

### 5. Review Before Sharing
- Read the generated report first
- Summarize key findings for user
- Be ready to answer questions from the report
- Offer to do focused research on specific sections if needed

## Integration with Other Skills

### With Task Management (fstrent-task-management)
Create tasks based on research findings:
```
1. Conduct research
2. Review findings
3. Create implementation tasks from recommendations
```

### With Planning (fstrent-planning)
Use research to inform:
- Feature planning
- Technical architecture decisions
- Risk assessment
- Technology selection

### With Web Tools
- Research identifies specific sites
- Use web-tools for targeted scraping
- Combine with research findings

## Comparison to Other Research Tools

### vs Manual WebSearch/WebFetch
- **Manual**: You search, read, synthesize manually
- **Deep Research**: AI agent does all of this autonomously

### vs Perplexity API Direct
- **Perplexity**: Quick answers with citations (~1 page)
- **Deep Research**: Comprehensive reports (5-50+ pages) with reasoning

### vs GPT-4 with browsing
- **GPT-4**: Limited context, single pass
- **Deep Research**: Multi-phase, breaks context limits, structured output

### vs research-methodology skill
- **Research Methodology**: Manual guide on HOW to research
- **Deep Research**: Automated ENGINE that researches FOR YOU

## Limitations and Considerations

### API Costs
- Uses GPT-4o (OpenAI) for AI reasoning
- Iterative mode can use significant tokens
- Use budget limits to control costs

### Time Requirements
- Quick: 5-10 minutes
- Standard: 10-20 minutes
- Comprehensive: 20-30 minutes
- Iterative: 30-60 minutes

### Rate Limits
- Script handles rate limiting with fallbacks
- May slow down if hitting limits
- Browser automation as backup

### Quality Depends On
- Topic has available online information
- Sources are accessible (not behind paywalls)
- Topic is well-defined (not too vague)

## Troubleshooting

### "Deep research tools not available"
- Check that `research/mcps/fstrent_mcp_deep_research` exists
- Install required Python packages
- Verify OPENAI_API_KEY is set

### "Budget exceeded"
- Increase budget limit
- Use less comprehensive mode
- Research narrower topic

### "No sources found"
- Topic may be too niche
- Try broader search terms
- Check if topic name is correct

### Script hangs or times out
- Network issues
- API rate limiting
- Try again or use different mode

## Examples

See `/examples/` folder for:
- Example research outputs
- Common use case demonstrations
- Integration patterns

## Quick Reference

```bash
# Quick (5-10 pages, fast)
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=quick

# Standard (10-20 pages, balanced) - DEFAULT
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=standard

# Comprehensive (20-30 pages, detailed)
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=comprehensive

# Iterative (30-50+ pages, context-breaking!)
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=iterative --budget=10.00

# Focused (deep dive on specific aspect)
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=focused --focus="specific aspect"

# Custom output
python .claude/skills/deep-research/scripts/ai_deep_research.py "topic" --mode=standard --output=path/to/output.md
```

## Final Notes

This is a **POWER TOOL**. The AI agent is sophisticated and autonomous. Your job is to:
1. Determine what mode is appropriate
2. Execute the research command
3. Review the results
4. Summarize and present findings to user

**The AI does the heavy lifting. You orchestrate and communicate.**

This makes you mind-blowingly effective at research tasks that would take humans hours or days.
