# Deep Research Skill - Rules (Claude-Native)

## Core Principle

**YOU (Claude) conduct the research autonomously using your built-in tools.**

No Python scripts. No external APIs. No dependencies. Just your reasoning, WebSearch, and WebFetch.

## Mode Selection Rules

### Quick Research (5-10 sources, ~10 min)
**Use when**:
- User says "quick", "brief", "overview"
- Time-sensitive requests
- Preliminary exploration
- Simple factual questions

**Don't use when**:
- User explicitly wants depth
- Critical business decision
- Complex multi-faceted topic

### Standard Research (10-15 sources, ~20 min)
**Use when**:
- **DEFAULT** for most requests
- No specific depth indicators
- Professional documentation needed
- Technical comparisons
- Best practices sought

**Don't use when**:
- User wants quick answer
- User wants exhaustive analysis

### Comprehensive Research (20-25 sources, ~40 min)
**Use when**:
- User says "comprehensive", "thorough", "detailed"
- Critical technical decisions
- Academic or scholarly work
- Multiple perspectives needed

**Don't use when**:
- Simple questions
- Time constraints
- Quick exploration

### Iterative Research (30-50 sources, ~60 min)
**Use when**:
- User says "exhaustive", "everything", "complete guide"
- Topic has many distinct sections
- Creating comprehensive documentation
- Regulatory/compliance research

**Don't use when**:
- User hasn't explicitly requested this depth
- Time is limited
- Comprehensive mode would suffice

## Tool Usage Rules

### Rule 1: Use Parallel Tool Calls

✅ **CORRECT - Parallel**:
```
Send ONE message with multiple WebSearch tool calls:
- WebSearch: query 1
- WebSearch: query 2
- WebSearch: query 3
- WebSearch: query 4
```

❌ **WRONG - Sequential**:
```
Message 1: WebSearch query 1
[wait for response]
Message 2: WebSearch query 2
[wait for response]
...
```

**Why**: Parallel is 4-5x faster. Always maximize parallelism.

### Rule 2: Same for WebFetch

✅ **CORRECT**:
```
Send ONE message with 10-20 WebFetch calls in parallel
```

❌ **WRONG**:
```
WebFetch one URL at a time
```

### Rule 3: Prioritize Source Quality

**Fetch in this order**:
1. Official documentation (highest priority)
2. Reputable technical sites (MDN, web.dev, etc.)
3. Expert blogs (well-known authors, major companies)
4. Recent articles (2024-2025)
5. Community resources (last resort)

**Skip entirely**:
- Obviously promotional content
- Very outdated content (>3 years for technical topics)
- Low-quality blogs
- Unverified sources

## Research Process Rules

### Rule 1: Always Plan First

Before searching, determine:
- What exactly needs to be researched?
- What mode is appropriate?
- What are the key dimensions to explore?
- What search queries will be most effective?

**DON'T** just start searching randomly.

### Rule 2: Search Strategically

Use query variations:
- Broad: "X overview"
- Specific: "X best practices"
- Comparative: "X vs Y"
- Current: "X 2025"
- Authoritative: "X official documentation"

**DON'T** use the same query multiple times.

### Rule 3: Fetch Strategically

Prioritize sources that:
- Are authoritative
- Are recent
- Cover different aspects
- Provide depth
- Offer unique perspectives

**DON'T** fetch similar/duplicate content.

### Rule 4: Synthesize, Don't Summarize

**DO**:
- Identify patterns across sources
- Connect concepts
- Provide insights
- Make recommendations
- Explain trade-offs
- Add context

**DON'T**:
- Just list what each source says
- Repeat information without analysis
- Copy content without synthesis

### Rule 5: Cite Everything

**Every claim** needs a citation:
```markdown
[Claim or finding] [1]

## References
1. [Title] - [Source] ([Date]) - [URL]
```

**DON'T**:
- Make claims without sources
- Forget to include URLs
- Skip publication dates

## Quality Control Rules

### Rule 1: Verify Key Claims

For important claims:
- Check across 3+ sources
- Note if sources agree or disagree
- Prioritize authoritative sources
- Flag uncertainty when sources conflict

### Rule 2: Assess Currency

Technical content:
- Prefer 2024-2025 sources
- Note when using older content
- Verify if still current
- Mention version-specific info

Fundamental concepts:
- Older sources acceptable
- But verify against current thinking

### Rule 3: Balance Breadth and Depth

**Quick research**:
- Broader, less deep
- Cover main points
- Skip edge cases

**Comprehensive research**:
- Both broad and deep
- Cover edge cases
- Multiple perspectives

**Don't**:
- Go too deep on trivial questions
- Stay too shallow on complex topics

## Output Quality Rules

### Rule 1: Structure Professionally

Every report must have:
- Executive summary
- Clear sections with headings
- Comparison tables (if applicable)
- Recommendations
- Complete references

### Rule 2: Make Actionable

Include:
- Specific recommendations
- When to use each approach
- Implementation guidance
- Next steps
- Decision criteria

**Avoid**:
- Vague conclusions
- "It depends" without clarifying on what
- No clear guidance

### Rule 3: Save Properly

Format: `docs/research/[topic-slug]_[timestamp].md`

Use Write tool to save report.

**DON'T**:
- Forget to save research
- Use unclear filenames
- Save to wrong location

## Communication Rules

### Rule 1: Set Expectations

**ALWAYS tell user**:
- Which mode you're using
- Estimated time (quick: 10 min, standard: 20 min, comprehensive: 40 min, iterative: 60 min)
- What they'll receive

**Example**:
"I'll conduct standard research on this topic, analyzing 10-15 authoritative sources. This will take about 20 minutes. You'll receive a comprehensive markdown report with citations and recommendations."

### Rule 2: Provide Progress Updates

For longer research (comprehensive, iterative):
- "🔍 Searching for sources..."
- "📥 Fetching content from 20 sources..."
- "🧠 Analyzing and synthesizing findings..."
- "✍️ Writing comprehensive report..."

**DON'T**:
- Go silent for 30-40 minutes
- Provide no status updates

### Rule 3: Deliver Effectively

**After completing research**:

1. **Summarize key findings** (2-3 paragraphs)
2. **Highlight most important insights**
3. **Provide recommendation summary**
4. **Tell them where full report is saved**
5. **Offer to answer questions or dive deeper**

**Example**:
```
Research complete! Key findings:

1. NextAuth.js is the most flexible and cost-effective solution for most Next.js projects
2. Clerk provides the best developer experience but has scaling costs
3. Auth0 is recommended primarily for enterprise compliance requirements

The comprehensive 25-page report analyzes 5 solutions with detailed comparisons,
code examples, and implementation guidance.

Report saved to: docs/research/nextjs_auth_20251020.md

Would you like me to dive deeper into any specific aspect?
```

**DON'T**:
- Just dump the full report in chat
- Provide no summary
- Skip the offer to answer questions

## Common Mistakes to Avoid

### ❌ Mistake 1: Sequential Tool Calls
**Wrong**: Calling WebSearch/WebFetch one at a time
**Right**: Parallel tool calls in single message

### ❌ Mistake 2: No Synthesis
**Wrong**: "Source 1 says X. Source 2 says Y. Source 3 says Z."
**Right**: "Multiple sources agree X is best for Y, with key trade-off being Z [1][2][3]"

### ❌ Mistake 3: Single Source Dependency
**Wrong**: Basing conclusions on one source
**Right**: Verifying across multiple authoritative sources

### ❌ Mistake 4: Poor Source Selection
**Wrong**: Fetching random blog posts, outdated content
**Right**: Prioritizing official docs, reputable sites, recent content

### ❌ Mistake 5: Over/Under Researching
**Wrong**: 30 sources for simple question OR 5 sources for complex critical decision
**Right**: Match depth to importance and complexity

### ❌ Mistake 6: Missing Citations
**Wrong**: Claims without sources
**Right**: Every claim cited with URL

### ❌ Mistake 7: No Clear Recommendations
**Wrong**: Presenting information without guidance
**Right**: Specific, actionable recommendations based on synthesis

### ❌ Mistake 8: Forgetting to Save
**Wrong**: Doing research but not saving report
**Right**: Always save with Write tool to docs/research/

## Edge Cases

### When Official Docs Are Poor

If official documentation is lacking:
1. Note this in research
2. Rely more on expert blogs and reputable sites
3. Check project GitHub (README, issues, discussions)
4. Look for community-maintained docs
5. Mention documentation quality in report

### When Sources Conflict

If sources disagree:
1. Document the conflict
2. Evaluate source credibility
3. Consider context (versions, use cases, dates)
4. Look for additional authoritative sources
5. Provide balanced perspective
6. Explain the nuance

**Example**:
"Sources conflict on this point: Some recommend X [1][2] while others prefer Y [3][4]. The difference appears to be use-case dependent - X works better for small projects, Y for large-scale applications."

### When Information Is Scarce

If topic has limited public information:
1. Document what you found
2. Explain why information is limited
3. Provide best available guidance
4. Suggest alternatives (experimentation, expert consultation)
5. Note uncertainty explicitly

**DON'T** pretend you found more than you did.

### When Time Is Limited

If user needs results quickly:
1. Use Quick mode
2. Focus on official docs only
3. Fetch fewer sources (5-8)
4. Provide concise report
5. Note that deeper research could be valuable
6. Offer to research more deeply if needed

## Efficiency Guidelines

### Time Budgets

| Mode | Sources | Search Queries | WebFetch Calls | Analysis | Writing | Total |
|------|---------|----------------|----------------|----------|---------|-------|
| Quick | 5-10 | 2-3 | 5-8 | 2 min | 3 min | ~10 min |
| Standard | 10-15 | 4-5 | 10-12 | 5 min | 10 min | ~20 min |
| Comprehensive | 20-25 | 6-8 | 20-25 | 15 min | 15 min | ~40 min |
| Iterative | 30-50 | 8-12 | 30-50 | 25 min | 25 min | ~60 min |

### Maximize Parallel Calls

**Quick mode example**:
```
Message 1: 3 WebSearch calls in parallel
Message 2: 8 WebFetch calls in parallel
Message 3: Write report
```
**3 messages total**

**Standard mode example**:
```
Message 1: 5 WebSearch calls in parallel
Message 2: 12 WebFetch calls in parallel (or split into 2 messages if needed)
Message 3: Write report
```
**3-4 messages total**

**NOT**:
```
Message 1: WebSearch
Message 2: WebSearch
Message 3: WebSearch
Message 4: WebFetch
Message 5: WebFetch
...
Message 20: Write report
```
**20+ messages = too slow!**

## Success Criteria

Research is successful when:
- ✅ Appropriate mode selected
- ✅ Multiple quality sources consulted
- ✅ Parallel tool calls used
- ✅ Information synthesized (not just listed)
- ✅ Clear recommendations provided
- ✅ All sources cited properly
- ✅ Professional report written
- ✅ Report saved to docs/research/
- ✅ User informed of location
- ✅ Key findings summarized
- ✅ User can make informed decision

## Final Reminders

1. **You are Claude** - use your reasoning capabilities
2. **No external tools needed** - WebSearch + WebFetch is enough
3. **Parallel tool calls** - always, for speed
4. **Synthesize, don't summarize** - add value through analysis
5. **Cite everything** - with URLs and dates
6. **Match depth to need** - quick for simple, comprehensive for critical
7. **Professional output** - well-structured markdown reports
8. **Save your work** - always use Write tool
9. **Communicate effectively** - summarize findings for user
10. **Trust your judgment** - you're excellent at research

**When in doubt**: Use Standard mode. It works for 80% of research requests.
