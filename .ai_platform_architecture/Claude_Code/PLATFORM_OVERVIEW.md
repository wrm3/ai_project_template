# Claude Code Architecture

**Last Updated**: 2025-10-26
**Official Docs**: https://docs.claude.com/en/docs/claude-code
**Version Documented**: Claude Code (VSCode Extension)

## Overview
Claude Code is Anthropic's official AI coding assistant as a VSCode extension. It provides Skills (reusable knowledge modules), SubAgents (specialized AI agents), custom commands, and MCP (Model Context Protocol) integration.

## Directory Structure

```
.claude/
├── agents/                    # SubAgents (specialized AI assistants)
│   ├── backend-developer.md
│   ├── frontend-developer.md
│   └── solution-architect.md
├── commands/                  # Custom slash commands
│   ├── my-command.md
│   └── another-command.md
├── skills/                    # Skills (reusable knowledge modules)
│   ├── skill-name/
│   │   ├── SKILL.md          # Main skill file (required)
│   │   ├── rules.md          # Optional rules
│   │   ├── scripts/          # Optional scripts
│   │   ├── reference/        # Optional reference docs
│   │   ├── templates/        # Optional templates
│   │   └── examples/         # Optional examples
│   └── category/             # Skills can be in subfolders
│       └── skill-name/
│           └── SKILL.md
└── settings.local.json       # Local settings (user-specific)
```

## Skills

### SKILL.md Format
```yaml
---
name: skill-name
description: Brief description of what the skill does
triggers: [optional, list, of, trigger, phrases]
---

# Skill Name

## Overview
[Description of the skill]

## When to Use This Skill
[Trigger conditions]

## Capabilities
[What the skill can do]

## Usage Examples
[Examples with code]

## Reference Materials
[Links to additional resources]
```

### Key Features
- **Subfolder Support**: ✅ Yes (proven with document-skills/)
- **File Types**: Markdown (.md)
- **YAML Frontmatter**: Required
- **Triggers**: Optional keywords that auto-activate skill
- **Scripts**: Can include Python/Bash scripts in scripts/ folder
- **Reference Materials**: Can include documentation in reference/ folder

### Example Skill Structure
```
.claude/skills/my-skill/
├── SKILL.md               # Required
├── rules.md               # Optional - additional rules
├── scripts/
│   ├── helper.py
│   └── requirements.txt
├── reference/
│   └── api_docs.md
├── templates/
│   └── template.md
└── examples/
    └── example_usage.md
```

## SubAgents

### Agent File Format (.md)
```yaml
---
name: agent-name
description: What this agent specializes in. Use PROACTIVELY if should auto-trigger.
tools: Read, Edit, Write, Bash, Grep, Glob  # Or omit for all tools
model: sonnet                                # sonnet, opus, haiku
---

# Agent Name

## Specialization
[What this agent is expert in]

## When to Use
[When to invoke this agent]

## Tool Access
[Which tools this agent can use]

## Examples
[Usage examples]
```

### Key Features
- **Proactive Triggers**: Use "PROACTIVELY" in description for auto-activation
- **Tool Scoping**: Can restrict tools (Read, Edit, Write, Bash, Grep, Glob)
- **Model Selection**: Choose sonnet (default), opus (complex), haiku (fast)
- **MCP Integration**: Omit tools field to inherit all MCP tools
- **Isolated Context**: Each agent has independent context window

### Agent Types
1. **Read-Only Agents**: `tools: Read, Grep, Glob` (reviewers, analyzers)
2. **Full-Access Agents**: `tools: Read, Edit, Write, Bash, Grep, Glob` (implementers)
3. **MCP-Enabled Agents**: Omit tools field (inherits all MCP tools)

## Commands

### Command File Format (.md)
```markdown
# command-name

Brief description of what this command does.

## Usage
```
/command-name [arguments]
```

## Description
Detailed explanation of the command behavior.

## What it does
- Bullet points of actions
- Step-by-step process
- Expected outcomes

## When to use
- Use case 1
- Use case 2
```

### Key Features
- **Slash Commands**: Invoke with `/command-name`
- **Simple Format**: Plain markdown, no YAML frontmatter
- **Arguments**: Can accept arguments after command name
- **Expansion**: Command content becomes prompt for Claude

## MCP (Model Context Protocol)

### Configuration Location
- File: `.claude/settings.local.json` (user-specific, gitignored)
- OR: Project settings in VSCode settings.json

### MCP Server Configuration Format
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": [
        "/path/to/mcp/server/build/index.js"
      ],
      "env": {
        "API_KEY": "value"
      }
    },
    "python-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/server",
        "run",
        "server-name"
      ]
    }
  }
}
```

### MCP Tool Access
- **From Main Claude**: Automatic access to all MCP tools
- **From SubAgents**: Omit `tools` field in agent YAML to inherit MCP tools
- **Tool Discovery**: Claude Code auto-discovers MCP tools on startup

### Supported MCP Servers
- Custom Node.js MCP servers
- Python MCP servers (via uv)
- FastMCP servers (Python)
- Any MCP-compliant server

## File Naming Conventions

### Skills
- Folder: `kebab-case-name/`
- Main file: `SKILL.md` (uppercase)
- Other files: `lowercase-with-hyphens.md`

### SubAgents
- File: `kebab-case-name.md`
- Location: `.claude/agents/`

### Commands
- File: `command-name.md`
- Location: `.claude/commands/`
- Invoke: `/command-name`

## Best Practices

### 1. Skills Organization
```
✅ Use subfolders for logical grouping (category/skill-name/)
✅ Include YAML frontmatter with name, description, triggers
✅ Provide usage examples and reference materials
✅ Keep skills focused on single domain
```

### 2. SubAgents Design
```
✅ Use descriptive names that indicate specialization
✅ Scope tool access appropriately (security)
✅ Use "PROACTIVELY" for auto-triggering agents
✅ Choose appropriate model (sonnet, opus, haiku)
✅ Test agent invocation before deploying
```

### 3. Commands
```
✅ Keep commands simple and focused
✅ Document arguments and usage clearly
✅ Use descriptive command names
✅ Provide examples of invocation
```

### 4. MCP Integration
```
✅ Use settings.local.json for user-specific MCP configs
✅ Document required environment variables
✅ Test MCP tools before relying on them
✅ Handle MCP tool failures gracefully
```

## Cross-Platform Compatibility

### What's Unique to Claude Code
- ✅ Skills system (other platforms don't have this)
- ✅ SubAgents with isolated context
- ✅ MCP integration built-in
- ✅ Custom slash commands
- ✅ YAML frontmatter in agent files

### What's Similar to Other Platforms
- ✅ Markdown-based configuration (.md files)
- ✅ Folder-based organization
- ✅ Tool access control concepts
- ✅ Custom instructions/rules concept (though format differs)

## Migration Notes

### From Cursor
- Cursor uses `.mdc` files for rules → Claude Code uses `.md` for Skills
- Cursor rules in `.cursor/rules/` → Claude Code Skills in `.claude/skills/`
- Both support similar concepts but different file formats

### To Windsurf/Cline/Roo-Code
- Skills system is Claude-specific → May need to recreate as rules/instructions
- SubAgents concept may not exist → Adapt to single-agent workflows
- MCP integration may differ → Check platform-specific MCP support

## Troubleshooting

### Skills Not Activating
1. Check YAML frontmatter is valid
2. Verify SKILL.md exists (case-sensitive)
3. Check triggers are defined if using auto-activation
4. Reload VSCode window

### SubAgents Not Working
1. Verify YAML frontmatter format
2. Check agent file is in `.claude/agents/`
3. Ensure tools field is correct (or omit for MCP access)
4. Test with explicit invocation first

### MCP Tools Not Available
1. Check settings.local.json syntax
2. Verify MCP server path is correct
3. Restart VSCode to reload MCP servers
4. Check MCP server logs for errors

## Official Resources

- **Docs**: https://docs.claude.com/en/docs/claude-code
- **GitHub**: https://github.com/anthropics/claude-code
- **MCP Docs**: https://modelcontextprotocol.io/
- **Skills Examples**: Check `.claude/skills/` in this project

## Version History

- **2025-10-26**: Initial documentation
  - Documented Skills, SubAgents, Commands, MCP
  - Confirmed subfolder support for Skills
  - Added YAML frontmatter requirements
  - Documented tool scoping and model selection

---

**Note**: This documentation should be updated when Claude Code releases new features or changes existing behavior. Check official docs quarterly for updates.
