# Claude Skills Implementation Guide

Based on the video "Claude Skills: Glimpse of Continual Learning?" by Prompt Engineering

---

## Quick Reference: When to Use Skills

Use Claude Skills when you need:
- ✅ Repeatable workflows with specific SOPs
- ✅ Domain-specific expertise without model retraining
- ✅ Context-efficient agent customization (vs MCP servers)
- ✅ Cross-platform compatibility (API, Code, Web, Desktop)
- ✅ Hierarchical, multi-step workflows
- ✅ Custom code review templates
- ✅ Brand guideline enforcement
- ✅ Financial analysis patterns
- ✅ Company-specific agent behavior

---

## Skills vs Other Approaches

| Feature | Skills | MCP Servers | Sub-Agents | Slash Commands |
|---------|--------|-------------|------------|----------------|
| **Initial Context** | 100-150 tokens | ~32,000 tokens | Isolated | Variable |
| **Loading Strategy** | Progressive | All upfront | On-demand | Manual |
| **Context Sharing** | Yes | Yes | No | Yes |
| **Workflow Control** | Explicit order | Agent decides | Isolated | Explicit |
| **Composability** | Automatic | Manual | Isolated results | Manual |
| **Cross-platform** | Yes | Platform-specific | Platform-specific | Platform-specific |

---

## Skill Anatomy

### Basic Structure
```
my-skill/
├── skill.md              # Main skill definition (metadata + body)
├── reference/            # Documentation and resources
│   ├── workflow-1.md
│   ├── workflow-2.md
│   └── guidelines.md
├── examples/             # Usage examples
│   └── example-output.md
└── tools/                # Tool implementations (optional)
    └── skill_tools.py
```

### skill.md Template

```markdown
---
name: my-skill-name
description: Brief description for skill selection
triggers: ["keyword1", "keyword2", "pattern"]
---

# Skill Name

## Overview
[What this skill does - 150 tokens max]

## Capabilities
[List of capabilities - 5,000 tokens max]
- Capability 1
- Capability 2
- Capability 3

## How to Use
[Instructions on when and how to use this skill]

### Workflow 1: [Name]
[See reference/workflow-1.md for details]

### Workflow 2: [Name]
[See reference/workflow-2.md for details]

## Input Format
[Expected input structure]

## Output Format
[Expected output structure]

## Examples
[See examples/ folder]

## Available Tools
[If using custom Python functions or MCP servers]
- Tool 1: Description
- Tool 2: Description

## References
- [Workflow 1 Details](reference/workflow-1.md)
- [Workflow 2 Details](reference/workflow-2.md)
- [Guidelines](reference/guidelines.md)
```

---

## Progressive Disclosure Architecture

### Level 1: Metadata (100-150 tokens)
```yaml
---
name: code-reviewer
description: Performs thorough code reviews following company SOPs
triggers: ["review", "code review", "PR review", "quality check"]
---
```

**Purpose:** Help agent decide if skill is relevant

### Level 2: Body (~5,000 tokens)
```markdown
## Capabilities
- Security vulnerability scanning
- Code style compliance
- Performance analysis
- Documentation quality check

## Workflows Available
1. Quick Review (< 500 lines)
2. Thorough Review (any size)
3. Security-Focused Review
4. Performance Review
```

**Purpose:** Understand what the skill can do

### Level 3: Resources (Unlimited tokens)
```markdown
<!-- reference/security-review-workflow.md -->
# Security Review Workflow

## Step 1: Input Validation
Check for:
- SQL injection vulnerabilities
- XSS attack vectors
- Buffer overflow risks
...

[Detailed checklist continues]
```

**Purpose:** Execute the actual workflow

---

## Creating Skills: Two Methods

### Method 1: Use Skill Creator (Recommended for Beginners)

1. In Claude, ensure skill-creator skill is enabled
2. Describe your need:
   ```
   Create a skill for thorough code reviews that checks:
   - Security vulnerabilities
   - Code style (PEP 8 for Python)
   - Performance issues
   - Documentation quality
   ```
3. Skill creator generates skill.md and structure
4. Copy generated folder to your Claude skills directory
5. Test and refine

### Method 2: Manual Creation

1. Create skill directory structure
2. Write skill.md with metadata and body
3. Add reference documentation
4. Add examples
5. Test with sample workflows
6. Iterate based on results

---

## Best Practices

### 1. Keep Metadata Concise
- Max 150 tokens for metadata section
- Clear, specific description
- Good trigger keywords

### 2. Structure Hierarchically
- skill.md → high-level overview
- Reference docs → detailed workflows
- Examples → concrete use cases

### 3. Use Clear Triggers
```yaml
# Good triggers
triggers: ["code review", "PR review", "review code", "security scan"]

# Poor triggers
triggers: ["review", "check"]  # Too generic
```

### 4. Provide Explicit Ordering
```markdown
## Code Review Workflow

Execute in this order:
1. Check syntax and compilation
2. Scan for security vulnerabilities
3. Verify code style compliance
4. Analyze performance patterns
5. Review documentation quality
6. Generate summary report
```

### 5. Include Examples
Show both input and expected output:
```markdown
## Example: Security Review

**Input:**
```python
user_input = request.GET['username']
query = f"SELECT * FROM users WHERE username='{user_input}'"
```

**Expected Output:**
```markdown
❌ SECURITY ISSUE: SQL Injection vulnerability
- Line 2: Direct string interpolation in SQL query
- Recommendation: Use parameterized queries
```
```

---

## Context Optimization Tips

### Calculate Your Savings

**Before (MCP Servers):**
- 3 MCP servers = ~32,000 tokens (16% context)
- Always loaded, whether needed or not

**After (Skills):**
- 5 skills metadata = ~750 tokens (0.4% context)
- Only load what's needed: +5,000 tokens when activated
- Potential savings: 26,250 tokens (13.6% context)

### When to Prefer Skills Over MCP

Choose Skills when:
- You have well-defined workflows
- Steps need to be executed in specific order
- Context efficiency matters
- You want cross-platform compatibility

Stick with MCP when:
- Tools are generic/broadly applicable
- No specific workflow needed
- External service integration is primary goal

---

## Skill Composition Patterns

### Pattern 1: Pure Instructions
```
skill.md → reference docs
No custom tools, just workflows
```
Use for: Code review templates, brand guidelines, SOPs

### Pattern 2: Skills + Tools
```
skill.md → reference docs + Python functions
Custom logic wrapped in skill
```
Use for: Financial analysis, data processing, custom calculations

### Pattern 3: Skills + MCP + Sub-agents
```
skill.md → orchestrates MCP tools + sub-agents
Composite workflow
```
Use for: Complex multi-step processes requiring external services

---

## Testing Your Skill

### Checklist

- [ ] Metadata is under 150 tokens
- [ ] Description clearly states what skill does
- [ ] Triggers are specific and relevant
- [ ] Body section under 5,000 tokens
- [ ] Workflows are clearly ordered
- [ ] Examples show input/output
- [ ] Reference docs are well-organized
- [ ] Skill loads only when relevant
- [ ] Agent follows workflow correctly
- [ ] Output matches expectations

### Test Prompts

Test if skill is properly selected:
```
# Should trigger code review skill
"Please review this Python code for security issues"

# Should NOT trigger code review skill
"Write a new Python function"
```

---

## Common Patterns from Video

### 1. Code Review Skill
```markdown
---
name: code-reviewer
description: Thorough code review following company standards
triggers: ["code review", "PR review", "review code"]
---

Workflows:
1. Security scan
2. Style compliance
3. Performance analysis
4. Documentation check
```

### 2. Brand Guidelines Skill
```markdown
---
name: brand-guidelines
description: Ensure content follows brand voice and style
triggers: ["brand", "style guide", "voice", "marketing copy"]
---

Reference:
- Tone and voice guidelines
- Visual design rules
- Copy templates
- Approved messaging
```

### 3. Financial Analysis Skill
```markdown
---
name: financial-ratio-analysis
description: Comprehensive financial ratio analysis for company evaluation
triggers: ["financial analysis", "ratio analysis", "company evaluation"]
---

Capabilities:
- Profitability ratios
- Liquidity analysis
- Valuation metrics
- Performance comparison
```

---

## Integration with Existing Tools

### Skills Can Include

**MCP Servers:**
```markdown
## Available Tools
This skill uses the following MCP servers:
- database-query: For fetching financial data
- web-scraper: For competitor analysis
```

**Sub-Agents:**
```markdown
## Workflow Step 3: Detailed Analysis
Delegate to financial-modeling sub-agent for:
- DCF valuation
- Scenario analysis
```

**Custom Functions:**
```python
# tools/financial_tools.py
class FinancialAnalyzer:
    def calculate_ratios(self, data):
        # Implementation
        pass
```

---

## Deployment

### Where Skills Work

1. **Claude Code**
   - Copy skill folder to skills directory
   - Restart or reload
   - Skill appears in capabilities

2. **Claude Desktop**
   - Add to skills folder
   - Appears in capabilities menu

3. **Claude Web**
   - Skills section in capabilities
   - Can create/edit online

4. **Claude API**
   - Reference skill in API calls
   - Same skill.md structure

---

## Future-Proofing

### Skill Sharing (Coming Soon?)
The video hints at future skill sharing capabilities:
- Community skill marketplace
- Reusable skill templates
- Collaborative skill development

### Standards Evolution
Keep an eye on:
- Anthropic's skill cookbook updates
- Community best practices
- Integration with other platforms

---

## Quick Start Checklist

Ready to build your first skill?

1. [ ] Identify a repeatable workflow in your work
2. [ ] List the steps in specific order
3. [ ] Gather any reference documentation needed
4. [ ] Use Claude's skill-creator to generate initial structure
5. [ ] Review and customize the generated skill.md
6. [ ] Add specific examples from your domain
7. [ ] Test with real-world use cases
8. [ ] Refine based on results
9. [ ] Document what works/doesn't work
10. [ ] Share learnings with community

---

## Resources

**Official Documentation:**
- https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

**Code Examples:**
- https://github.com/anthropics/claude-cookbooks/tree/main/skills

**Community Analysis:**
- https://simonwillison.net/2025/Oct/16/claude-skills/

---

## Key Takeaways

1. **Context Efficiency:** Skills use 100-150 tokens vs 32,000 tokens for MCP servers
2. **Progressive Disclosure:** Load only what's needed, when it's needed
3. **Workflow Control:** Explicit ordering of steps for repeatable processes
4. **Cross-Platform:** Build once, use everywhere (API, Code, Web, Desktop)
5. **Continual Learning:** Add capabilities without model retraining
6. **Composability:** Skills work together automatically

---

**Status:** Based on video published by Prompt Engineering channel
**Last Updated:** 2025-10-19
**Next Steps:** Experiment with creating custom skills for your workflows
