# AI Project Template

> **This file follows the agents.md standard**  
> **For complete instructions, see [agents.md](agents.md)**

This project now uses the industry-standard **agents.md** format for AI agent instructions.

## Quick Links

- **Full Instructions**: [agents.md](agents.md)
- **SubAgents Guide**: [docs/CLAUDE_SUBAGENTS_GUIDE.md](docs/CLAUDE_SUBAGENTS_GUIDE.md) - **NEW! 15 specialized AI agents**
- **Task List**: [.fstrent_spec_tasks/TASKS.md](.fstrent_spec_tasks/TASKS.md)
- **Project Context**: [.fstrent_spec_tasks/PROJECT_CONTEXT.md](.fstrent_spec_tasks/PROJECT_CONTEXT.md)
- **Project Plan**: [.fstrent_spec_tasks/PLAN.md](.fstrent_spec_tasks/PLAN.md)

## What Changed?

As of October 2025, this project adopted the **agents.md** standard announced by OpenAI and adopted by 20+ major companies including Cursor, Google Jules, Gemini CLI, Factory, and Roo-Code.

**agents.md** provides unified instructions for AI coding agents across all IDEs, eliminating the need for multiple IDE-specific configuration files.

## For Claude Code Users

Claude Code automatically loads this CLAUDE.md file. Since it now references agents.md, you get the benefits of the standardized format while maintaining backward compatibility.

### 🤖 SubAgents System

This project includes **15 specialized SubAgents** for accelerated development:

- **Development**: backend-developer, frontend-developer, full-stack-developer, database-expert
- **Quality**: test-runner (proactive), code-reviewer, debugger, qa-engineer
- **Security/DevOps**: security-auditor (opus), devops-engineer, docker-specialist
- **Documentation**: technical-writer, solution-architect (opus), api-designer
- **Workflow**: task-expander (proactive)

**Benefits**:
- 60-80% reduction in context usage
- 10x faster for multi-component features
- Automatic code reviews and security audits
- Parallel processing of complex tasks

See the [SubAgents Guide](docs/CLAUDE_SUBAGENTS_GUIDE.md) for complete documentation.

## For Other IDE Users

Your IDE will look for agents.md directly and use the standardized format.

## Migration

All content from the original CLAUDE.md has been incorporated into agents.md with enhanced best practices from industry research. Nothing was lost - everything was improved!

**Original CLAUDE.md backed up as**: `CLAUDE.md.backup`

---

**Standard**: [agents.md](https://agents.md) - August 2025  
**See**: [agents.md](agents.md) for complete instructions

