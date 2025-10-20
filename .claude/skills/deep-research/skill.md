Base directory for this skill: /mnt/c/git/ai_project_template/.claude/skills/deep-research

# Deep Research Skill - Claude-Native Autonomous Research

**THIS IS AN AUTONOMOUS RESEARCH METHODOLOGY FOR CLAUDE**

You (Claude) conduct comprehensive, multi-phase research using your built-in tools (WebSearch, WebFetch). No external APIs, no Python scripts, no dependencies - just your own reasoning and research capabilities.

## Core Concept

When a user needs comprehensive research:
1. **You conduct the research** using WebSearch and WebFetch
2. **You analyze and synthesize** using your reasoning
3. **You write professional reports** using Write tool
4. **You cite sources properly** with verification

**This is NOT manual research guidance. This IS your autonomous research workflow.**

## When to Use This Skill

Activate when user requests:
- "Research X comprehensively"
- "Deep dive into Y"
- "Compare multiple options for Z"
- "I need a detailed analysis of..."
- "Investigate A thoroughly"
- "Literature review on B"

**Trigger phrases**: research, investigate, analyze, deep dive, comprehensive, comparison, literature review

## Research Modes

### Quick Research (5-10 sources, ~10 minutes)
**Use when**: User needs quick overview or has time constraints
**Process**: 2-3 WebSearch queries, 5-8 WebFetch calls, basic synthesis

### Standard Research (10-15 sources, ~20 minutes)
**Use when**: Most research requests (DEFAULT)
**Process**: 4-5 WebSearch queries, 10-12 WebFetch calls, detailed synthesis

### Comprehensive Research (20-30 sources, ~40 minutes)
**Use when**: User explicitly requests "comprehensive", "thorough", "detailed"
**Process**: 6-8 WebSearch queries, 20-25 WebFetch calls, exhaustive synthesis

### Iterative Research (30+ sources, ~60 minutes)
**Use when**: User requests "exhaustive", "complete guide", "everything about X"
**Process**: Multi-phase research with section-based deep dives

## Phase 1: Research Planning

### Step 1: Understand the Request
Clarify:
- **What exactly** needs to be researched?
- **How deep** should the research be? (mode selection)
- **What output** does the user expect?
- **Any specific focus** areas or constraints?

**Ask clarifying questions if needed**, but don't over-clarify obvious requests.

### Step 2: Break Down the Topic
Identify research dimensions:
- **Core concepts**: What are the fundamental aspects?
- **Key questions**: What specific questions need answering?
- **Comparison factors**: If comparing options, what criteria matter?
- **Information sources**: What types of sources are most valuable?

### Step 3: Plan Search Strategy
Create search query variations:
- **Broad queries**: "X overview", "what is X"
- **Specific queries**: "X best practices", "X vs Y", "X tutorial"
- **Current queries**: "X 2025", "X latest", "X recent updates"
- **Authoritative queries**: "X official documentation", "X specification"
- **Problem-focused**: "X challenges", "X pitfalls", "X comparison"

**Example for "React state management"**:
- "React state management overview"
- "React state management best practices 2025"
- "Redux vs MobX vs Zustand comparison"
- "React state management official documentation"
- "React state management patterns"

## Phase 2: Information Gathering

### Step 1: Execute Multi-Search Strategy

**DO THIS** (parallel searches for efficiency):
```
Use WebSearch tool multiple times in PARALLEL with different queries:
- Query 1: Broad overview
- Query 2: Best practices/recent
- Query 3: Comparison/alternatives
- Query 4: Official documentation
- Query 5: Specific aspect (if needed)
```

**From each search**:
- Note promising URLs (official docs, reputable sites, recent articles)
- Identify key themes appearing across results
- Skip obviously low-quality sources

### Step 2: Fetch Detailed Content

**Prioritize sources** in this order:
1. **Official documentation** (.org, official project sites)
2. **Reputable technical sites** (MDN, CSS-Tricks, Smashing Magazine, web.dev)
3. **Well-known blogs** (Vercel, Netlify, major tech companies)
4. **Recent articles** (2024-2025)
5. **Community resources** (GitHub discussions, Stack Overflow)

**Use WebFetch in PARALLEL** for top 10-25 sources (based on mode):
```
Fetch multiple URLs simultaneously:
- Official docs (highest priority)
- 3-5 reputable technical articles
- 2-3 comparison/analysis pieces
- 2-3 recent articles (currency)
- 1-2 community discussions (real-world perspective)
```

**Extract from each fetch**:
- Key points and insights
- Quotes worth citing
- Code examples (if relevant)
- Author/publication date
- URL for citation

### Step 3: Assess Source Quality

For each source, note:
- **Authority**: Official docs > Expert blogs > Community content
- **Currency**: Recent (2024-2025) > Older content
- **Depth**: Detailed analysis > Surface-level overviews
- **Objectivity**: Balanced perspective > Promotional content

**Trust indicators**:
- .gov, .edu, .org domains
- Official project documentation
- Recognized expert authors
- Recent publication dates
- Multiple corroborating sources

## Phase 3: Analysis and Synthesis

### Step 1: Organize Findings

Group information by themes:
- **Core concepts**: Fundamental understanding
- **Approaches/Options**: Different ways to solve the problem
- **Best practices**: Recommended patterns
- **Common pitfalls**: What to avoid
- **Real-world usage**: How it's used in practice
- **Tradeoffs**: Pros and cons of different approaches

### Step 2: Identify Patterns

Look for:
- **Consensus**: What do multiple sources agree on?
- **Disagreements**: Where do sources conflict?
- **Evolution**: How has thinking changed over time?
- **Trends**: What's emerging or declining?
- **Gaps**: What information is missing?

### Step 3: Synthesize Insights

**Your job** (Claude's unique value):
- **Connect dots**: Link concepts across sources
- **Provide context**: Explain why things matter
- **Identify trade-offs**: Weigh pros and cons
- **Give perspective**: What's most important?
- **Make recommendations**: Based on synthesis

**Don't just summarize** - add value through:
- Cross-source analysis
- Pattern identification
- Contextual understanding
- Nuanced recommendations

## Phase 4: Report Generation

### Structure Your Report

Every research report should include:

#### 1. Executive Summary (2-3 paragraphs)
- What was researched
- Key findings in brief
- Main recommendation
- Critical takeaways

#### 2. Research Objective
- What question was answered
- Why this research was needed
- Scope boundaries

#### 3. Key Findings (Organized by Theme)

**For each theme**:
```markdown
### Finding 1: [Theme Name]

[Detailed explanation of finding]

**Key Points**:
- Point 1 [Source 1]
- Point 2 [Source 2]
- Point 3 [Source 3]

**Analysis**: [Your synthesis and insights]
```

#### 4. Comparisons (if applicable)

Create comparison tables:
```markdown
| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Complexity | Low | Medium | High |
| Performance | Good | Excellent | Fair |
| Use Cases | Small projects | Large apps | Specific needs |
```

#### 5. Best Practices
- Recommended approaches
- Industry standards
- Common patterns
- Expert advice

#### 6. Recommendations
- Primary recommendation with rationale
- Alternative approaches
- When to use each
- Implementation guidance

#### 7. Sources and References

**Citation format**:
```markdown
## References

1. [Title] - [Author/Organization] ([Date]) - [URL]
2. [Title] - [Author/Organization] ([Date]) - [URL]
```

**Example**:
```markdown
1. "React State Management Guide" - React Team (2025) - https://react.dev/learn/managing-state
2. "Redux vs Zustand: A Comparison" - Lee Robinson (2024) - https://vercel.com/blog/redux-zustand
```

#### 8. Metadata
```markdown
---

**Research Date**: [Date]
**Researcher**: Claude Code
**Sources Consulted**: [Number]
**Research Mode**: [Quick/Standard/Comprehensive/Iterative]
**Confidence Level**: [High/Medium/Low]
```

### Use the Write Tool

**Save research to**:
```
docs/research/[topic-slug]_[timestamp].md
```

**Example**:
```
docs/research/react_state_management_20251020_143022.md
```

## Research Workflow Examples

### Example 1: Technology Comparison

**User**: "Compare React state management solutions"

**Your Process**:

1. **Plan** (30 seconds):
   - Research Redux, Zustand, Jotai, MobX, React Context
   - Compare: complexity, performance, use cases, ecosystem
   - Mode: Comprehensive (user wants thorough comparison)

2. **Search** (5 minutes):
   ```
   WebSearch in parallel:
   - "React state management comparison 2025"
   - "Redux vs Zustand vs Jotai"
   - "React state management best practices"
   - "React state management official documentation"
   - "React state management performance"
   ```

3. **Fetch** (15 minutes):
   ```
   WebFetch in parallel (top 20 sources):
   - Official React docs on state
   - Redux official docs
   - Zustand GitHub + docs
   - Jotai docs
   - 5-8 comparison articles
   - 3-4 recent blog posts
   - 2-3 GitHub discussions
   ```

4. **Analyze** (10 minutes):
   - Create comparison matrix
   - Identify use cases for each
   - Note pros/cons
   - Synthesize recommendations

5. **Write Report** (10 minutes):
   - Executive summary
   - Detailed comparison
   - Comparison table
   - Recommendations by use case
   - 20+ citations

**Output**: 15-20 page comprehensive comparison report

---

### Example 2: Best Practices Research

**User**: "Research API design best practices"

**Your Process**:

1. **Plan**:
   - Research REST, GraphQL, design patterns
   - Find industry standards
   - Mode: Standard (typical request)

2. **Search**:
   ```
   - "API design best practices 2025"
   - "REST API design principles"
   - "API design patterns"
   - "API security best practices"
   ```

3. **Fetch** (12 sources):
   - Industry standards (OpenAPI, JSON:API)
   - Expert blog posts
   - Company engineering blogs
   - Official documentation

4. **Analyze**:
   - Identify common patterns
   - Note industry consensus
   - Extract specific guidelines

5. **Write Report**:
   - Best practices by category
   - Code examples
   - Anti-patterns to avoid
   - Recommendations

**Output**: 10-15 page best practices guide

---

### Example 3: Deep Dive Technical Topic

**User**: "Deep dive into React Server Components"

**Your Process**:

1. **Plan**:
   - Understand architecture
   - How they work
   - Use cases and benefits
   - Mode: Comprehensive

2. **Search**:
   ```
   - "React Server Components explained"
   - "React Server Components architecture"
   - "React Server Components vs Client Components"
   - "React Server Components use cases"
   - "React Server Components Next.js"
   ```

3. **Fetch** (20 sources):
   - Official React docs (primary)
   - React team blog posts
   - Next.js documentation
   - Technical deep dives
   - Real-world examples

4. **Analyze**:
   - How RSC works (architecture)
   - Benefits and trade-offs
   - Use cases
   - Integration patterns

5. **Write Report**:
   - Technical architecture explanation
   - Conceptual diagrams (text)
   - Code examples
   - Best practices
   - Common patterns

**Output**: 20-25 page technical deep dive

## Iterative Research Mode (Advanced)

For exhaustive research (30+ sources, 60+ minutes):

### Phase 1: Overview Research
1. Broad searches to understand landscape
2. Fetch 5-8 overview sources
3. Identify main topic areas/sections

### Phase 2: Section Identification
Based on overview, identify 4-6 major sections:
- Example for "Banking Regulations":
  - Section 1: Regulatory Framework
  - Section 2: Compliance Requirements
  - Section 3: Reporting Standards
  - Section 4: Security Requirements
  - Section 5: Audit Procedures

### Phase 3: Deep Dive Each Section
For each section:
1. Targeted searches
2. Fetch 5-8 sources per section
3. Detailed analysis
4. Section write-up

### Phase 4: Synthesis
1. Combine all sections
2. Add cross-references
3. Create comprehensive document
4. Final review and polish

**Result**: 30-50+ page exhaustive research document

## Quality Standards

### Every Research Report Must Have

✅ **Multiple Sources**:
- Minimum 5 sources for quick research
- Minimum 10 sources for standard
- Minimum 20 sources for comprehensive

✅ **Proper Citations**:
- All claims cited
- URLs included
- Publication dates noted
- Sources verified

✅ **Synthesis, Not Just Summary**:
- Your analysis and insights
- Connections across sources
- Pattern identification
- Recommendations

✅ **Professional Structure**:
- Clear headings
- Logical organization
- Executive summary
- Actionable recommendations

✅ **Source Quality**:
- Prioritize authoritative sources
- Recent content preferred
- Multiple perspectives
- Fact-checked where possible

### Self-Check Before Delivering

- [ ] Research question clearly answered?
- [ ] Multiple credible sources consulted?
- [ ] Information organized logically?
- [ ] Synthesis provided (not just lists)?
- [ ] Recommendations are actionable?
- [ ] All sources properly cited?
- [ ] Report is professional quality?
- [ ] Appropriate depth for request?

## Efficiency Tips

### Use Parallel Tool Calls
**DO THIS**:
```
Send one message with multiple WebSearch calls
Send one message with multiple WebFetch calls
```

**DON'T DO THIS**:
```
WebSearch, wait for results
WebSearch again, wait for results
WebSearch again, wait for results
(Sequential = slow!)
```

### Prioritize Ruthlessly
Focus on:
- Official documentation first
- Most reputable sources
- Recent content
- Directly relevant material

Skip:
- Obviously low-quality content
- Outdated information
- Promotional material
- Tangentially related topics

### Know When to Stop
Research has diminishing returns:
- **Quick**: 5-10 sources is enough
- **Standard**: 10-15 sources
- **Comprehensive**: 20-25 sources
- **Iterative**: 30-50 sources

**More sources ≠ better research**. Quality over quantity.

## Common Pitfalls to Avoid

### ❌ Don't: Just Summarize Sources
**Wrong**: "Source 1 says X. Source 2 says Y. Source 3 says Z."
**Right**: "Multiple sources agree that X is best for Y use case, though Z has advantages for specific scenarios [1][2][3]. The key trade-off is..."

### ❌ Don't: Single Source Dependency
**Wrong**: Base conclusions on one source
**Right**: Verify important claims across 3+ sources

### ❌ Don't: Ignore Currency
**Wrong**: Use 2019 article about 2025 technology
**Right**: Prioritize 2024-2025 content, note when using older sources

### ❌ Don't: Skip Synthesis
**Wrong**: List findings without analysis
**Right**: Connect findings, identify patterns, provide insights

### ❌ Don't: Forget Citations
**Wrong**: Make claims without sources
**Right**: Cite everything [1]

### ❌ Don't: Over-Research Trivial Questions
**Wrong**: 30 sources for "What is React?"
**Right**: 5 sources for simple questions

## Integration with Other Skills

### With Task Management
1. Research technology options
2. Create tasks based on research findings
3. Link research report in task notes

### With Planning
1. Research before feature planning
2. Use findings to inform PRD
3. Base technical decisions on research

### With Code Implementation
1. Research best practices
2. Implement based on findings
3. Reference research in code comments

## Example Research Report Template

See `templates/research_report_template.md` for a complete example.

## Success Metrics

Research is successful when:
- ✅ User's question is thoroughly answered
- ✅ Multiple authoritative sources consulted
- ✅ Information is synthesized with insights
- ✅ Recommendations are clear and actionable
- ✅ Citations are complete and accurate
- ✅ Report is professional and well-organized
- ✅ Appropriate depth for importance of decision
- ✅ User can make informed decision

## Final Checklist

Before delivering research:
- [ ] Conducted multi-source search
- [ ] Fetched and analyzed quality sources
- [ ] Synthesized findings (not just summarized)
- [ ] Created comparison tables (if applicable)
- [ ] Provided clear recommendations
- [ ] Cited all sources properly
- [ ] Wrote professional report
- [ ] Saved to docs/research/
- [ ] Summarized key findings for user
- [ ] Offered to answer follow-up questions

---

## Remember

**You are Claude** - you have excellent research and synthesis capabilities. This skill is just a methodology to apply your abilities systematically. Trust your judgment, be thorough, and provide value through your unique insights and analysis.

**No external tools needed** - you have WebSearch and WebFetch. That's all you need for comprehensive research.

**Quality over quantity** - Better to deeply analyze 10 sources than superficially scan 50.

**Add value through synthesis** - Anyone can collect information. You provide insights, connections, and recommendations.

**This is your superpower** - Comprehensive, autonomous research that would take a human days, you do in minutes.
