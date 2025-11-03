# Claude Code Documentation

**Last Updated**: 2025-10-29
**Purpose**: Comprehensive Claude Code platform documentation and research

---

## Overview

This folder contains in-depth documentation for Anthropic's Claude Code AI coding assistant. Documentation is organized into focused files covering architecture, research topics, and platform-specific details.

---

## Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Complete architectural deep dive | ✅ Complete |
| [RESEARCH_TOPICS.md](RESEARCH_TOPICS.md) | Active research tracking | 🔍 Living Document |
| [PLATFORM_OVERVIEW.md](PLATFORM_OVERVIEW.md) | Quick reference guide | ✅ Complete |

---

## Quick Links

### For New Users
Start here: [PLATFORM_OVERVIEW.md](PLATFORM_OVERVIEW.md)

### For Developers Building Skills/SubAgents
Read: [ARCHITECTURE.md](ARCHITECTURE.md) - Sections 3-4

### For Advanced Workflows
Read: [ARCHITECTURE.md](ARCHITECTURE.md) - Sections 7-10

### For Research Contributors
Check: [RESEARCH_TOPICS.md](RESEARCH_TOPICS.md) - Priority Queue

---

## What's Documented

### ✅ Fully Documented
- **Skills System**: Structure, activation, organization
- **SubAgents**: Architecture, tool scoping, model selection
- **Commands**: Creation and invocation
- **MCP Integration**: Configuration and usage
- **Workflow Patterns**: 6 common patterns with examples
- **Component Interactions**: How everything works together
- **Best Practices**: Design guidelines for each component

### 🔍 Research In Progress
- Plugin development details
- Security considerations
- Performance optimization
- Team collaboration patterns
- CI/CD integration
- Cross-platform portability

### ❓ Needs Research
- CLI version (if exists)
- Mobile apps (if exist)
- Enterprise/cloud versions
- Skills marketplace
- Advanced SubAgent communication
- Token usage optimization

---

## File Structure

```
Claude_Code/
├── README.md                    # This file - Navigation guide
├── ARCHITECTURE.md              # Complete architectural reference
├── RESEARCH_TOPICS.md           # Active research tracking
└── PLATFORM_OVERVIEW.md         # Quick reference (moved from parent)
```

---

## How to Use This Documentation

### Scenario 1: First Time Setup
1. Read **PLATFORM_OVERVIEW.md** for basics
2. Follow setup instructions
3. Create your first Skill
4. Test with simple examples

### Scenario 2: Building Complex Workflows
1. Review **ARCHITECTURE.md** Section 7 (Workflow Patterns)
2. Identify pattern matching your use case
3. Review Section 10 (Advanced Use Cases) for examples
4. Implement following best practices in Section 9

### Scenario 3: Creating SubAgents
1. Read **ARCHITECTURE.md** Section 4 (SubAgents)
2. Choose appropriate model (haiku/sonnet/opus)
3. Define tool scope
4. Test activation triggers
5. Follow SubAgent Design Best Practices

### Scenario 4: Contributing Research
1. Check **RESEARCH_TOPICS.md** Priority Queue
2. Select high-priority topic
3. Follow Research Workflow
4. Document findings
5. Update status and link to detailed docs

---

## Key Concepts at a Glance

### Skills
- **What**: Reusable knowledge modules
- **When**: Domain-specific expertise needed
- **Where**: `.claude/skills/skill-name/SKILL.md`
- **How**: Auto-activates via triggers or manual invocation

### SubAgents
- **What**: Specialized AI agents with isolated context
- **When**: Specialized tasks requiring focus
- **Where**: `.claude/agents/agent-name.md`
- **How**: Invoked by main Claude or auto-triggered

### Commands
- **What**: Pre-defined workflow templates
- **When**: Repeatable processes
- **Where**: `.claude/commands/command-name.md`
- **How**: User types `/command-name [args]`

### MCP Tools
- **What**: External system integrations
- **When**: Need database, browser, or other external tools
- **Where**: `.claude/settings.local.json`
- **How**: Called by Claude or SubAgents

---

## Quick Reference

### Create a Skill

```bash
mkdir -p .claude/skills/my-skill
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: What this skill does
triggers:
  - keyword1
  - keyword2
---

# My Skill

## Overview
[Description]

## When to Use
[Conditions]

## Capabilities
[What it can do]
EOF
```

### Create a SubAgent

```bash
cat > .claude/agents/my-agent.md << 'EOF'
---
name: my-agent
description: Specializes in X. Use PROACTIVELY for Y.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

# My Agent

## Specialization
[What makes this agent unique]

## When to Use
[Invocation conditions]
EOF
```

### Create a Command

```bash
cat > .claude/commands/my-command.md << 'EOF'
# my-command

Brief description of what this command does.

## Usage
```
/my-command [arg1] [arg2]
```

## What it does
1. Step one
2. Step two
3. Step three

## When to use
- Use case 1
- Use case 2
EOF
```

---

## Common Questions

### Q: Skills vs SubAgents - When to use which?

**Use Skills when**: You need domain knowledge that enhances Claude's understanding
**Use SubAgents when**: You need isolated context or specialized focus on a task

### Q: Can SubAgents use Skills?

**Yes**: SubAgents can reference Skills in their context, and main Claude can load Skills before invoking SubAgents.

### Q: How do I choose between haiku/sonnet/opus?

**haiku**: Fast, simple tasks (formatting, simple refactoring)
**sonnet**: Most development tasks (default choice)
**opus**: Complex architecture, difficult debugging

### Q: Can I use MCP tools in SubAgents?

**Yes**: Omit the `tools` field in the SubAgent YAML frontmatter to inherit all MCP tools.

### Q: How do I debug Skills/SubAgents not working?

1. Check YAML frontmatter syntax
2. Verify file naming and location
3. Test with explicit invocation first
4. Review Claude Code logs
5. Restart VSCode

---

## Contributing to Documentation

### Found Something Missing?
1. Check [RESEARCH_TOPICS.md](RESEARCH_TOPICS.md)
2. Add topic if not listed
3. Mark as high priority if critical
4. Start research or request help

### Discovered New Information?
1. Update relevant .md file
2. Add date and source
3. Update status indicators
4. Link related documentation

### Want to Share Examples?
1. Add to appropriate section in ARCHITECTURE.md
2. Use clear code blocks
3. Explain context and use case
4. Test before committing

---

## External Resources

- **Official Docs**: https://docs.claude.com/en/docs/claude-code
- **MCP Protocol**: https://modelcontextprotocol.io/
- **VSCode Marketplace**: Search "Claude Code"
- **Anthropic API**: https://docs.anthropic.com/
- **Community**: Check Discord/forums

---

## Version History

- **2025-10-29**: Initial Claude_Code folder structure
  - Created ARCHITECTURE.md (comprehensive)
  - Created RESEARCH_TOPICS.md (23 topics)
  - Created README.md (this file)
  - Moved CLAUDE_CODE.md to PLATFORM_OVERVIEW.md

---

## Next Steps

1. **Immediate**: Complete plugin development research (RESEARCH_TOPICS 2.2)
2. **This Week**: Document security considerations (RESEARCH_TOPICS 5.2)
3. **This Month**: Web interface comparison (RESEARCH_TOPICS 1.3)
4. **Ongoing**: Collect community best practices (RESEARCH_TOPICS 7.2)

---

**Maintained By**: Template maintainers and community
**Review Schedule**: Monthly for research topics, quarterly for architecture
**Status**: Active development and documentation

