# Cursor Architecture

**Last Updated**: 2025-10-26
**Official Website**: https://cursor.com
**Version Documented**: Cursor IDE (Standalone IDE based on VSCode)

## Overview
Cursor is an AI-first IDE built as a fork of VSCode. It uses **rules** (`.mdc` files) for AI behavior customization, supports MCP integration, and provides AI-powered code editing with context awareness.

## Directory Structure

```
.cursor/
├── rules/                     # AI behavior rules
│   ├── global_rule.mdc       # Global rules
│   ├── project_specific/     # Project-specific rules
│   │   ├── rule1.mdc
│   │   └── rule2.mdc
│   └── fstrent_spec_tasks/   # Task management system rules
│       ├── rules/
│       │   ├── rules.mdc     # Main rules
│       │   ├── plans.mdc     # Planning rules
│       │   ├── qa.mdc        # QA rules
│       │   └── workflow.mdc  # Workflow rules
│       └── commands/
│           └── *.md          # Command definitions
└── .cursorrules               # Optional: Single-file rules (deprecated)
```

## Rules System

### .mdc File Format
```yaml
---
description: Brief description of what this rule does
globs:                         # Optional file patterns
  - "**/*.ts"
  - "**/*.tsx"
alwaysApply: true             # Apply to all files (optional)
---

# Rule Title

## Rule Content
[Markdown content with instructions, examples, and guidelines]

### Sub-sections
[Organize content with headers]

## Code Examples
```language
code examples
```

## Best Practices
- Bullet points
- Guidelines
- Standards
```

### Key Features
- **File Type**: `.mdc` (Markdown Cursor) - **UNIQUE TO CURSOR**
- **YAML Frontmatter**: Required for metadata
- **Glob Patterns**: Target specific file types
- **alwaysApply**: Make rule global across project
- **Subfolder Support**: ✅ Yes (organize rules in subdirectories)

### Rule Types

1. **Global Rules** (`alwaysApply: true`)
   - Applied to all AI interactions
   - Located in `.cursor/rules/`
   - Use for project-wide standards

2. **File-Specific Rules** (with `globs`)
   - Applied only to matching files
   - Target specific languages/file types
   - Use for language-specific conventions

3. **Feature-Specific Rules**
   - Organized in subfolders
   - Applied when working on specific features
   - Use for domain-specific logic

### Example Rule Structure
```
.cursor/rules/
├── coding_standards.mdc       # Always apply
├── typescript/
│   ├── react_rules.mdc       # For .tsx files
│   └── testing_rules.mdc     # For .test.ts files
└── fstrent_spec_tasks/
    └── rules/
        ├── rules.mdc          # Task management
        ├── plans.mdc          # Planning system
        └── qa.mdc             # QA system
```

## Commands

### Command Files (.md)
Located in `.cursor/rules/*/commands/` folders:

```markdown
# Command Name

Brief description

## Usage
```
@command-name [arguments]
```

## What it does
- Action 1
- Action 2
- Action 3
```

### Key Features
- **Invocation**: Use `@` prefix (e.g., `@fstrent_spec_tasks_plan`)
- **Format**: Plain markdown (.md files)
- **Location**: Can be in subdirectories under rules/
- **Arguments**: Support for command arguments

## MCP (Model Context Protocol)

### Configuration Location
- **No Built-in MCP UI** (as of late 2024)
- MCP servers configured via VSCode settings since Cursor is VSCode-based
- May require manual MCP server integration

### Expected MCP Format (VSCode-style)
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["/path/to/server/index.js"]
    }
  }
}
```

**Note**: Cursor's MCP support may differ from Claude Code. Verify current implementation.

## Project Organization

### Recommended Structure
Cursor works well with organized project structures:

```
project-root/
├── .cursor/
│   └── rules/
│       ├── coding_standards.mdc
│       ├── project_specific/
│       │   └── custom_rules.mdc
│       └── commands/
│           └── custom_commands.md
├── src/                  # Source code
├── docs/                 # Documentation
├── tests/                # Test files
└── README.md             # Project documentation
```

### Custom Instructions
Create `.mdc` files in `.cursor/rules/` to customize AI behavior:

```yaml
---
description: Project-specific coding standards
alwaysApply: true
---

# Project Standards

## Code Style
[Your standards here]

## Best Practices
[Your practices here]
```

## File Naming Conventions

### Rules
- **File Extension**: `.mdc` (NOT .md) ⚠️ CRITICAL
- **Naming**: `kebab-case-name.mdc`
- **Location**: `.cursor/rules/` or subfolders
- **Example**: `coding-standards.mdc`, `typescript-rules.mdc`

### Commands
- **File Extension**: `.md`
- **Naming**: `command_name.md` or `kebab-case.md`
- **Location**: `.cursor/rules/*/commands/`
- **Example**: `format-code.md`, `run-tests.md`

### Project Files
- **Documentation**: Use standard markdown `.md`
- **Configuration**: JSON, YAML, or platform-specific formats
- **Source Code**: Follow language conventions

## Best Practices

### 1. Rule Organization
```
✅ Use .mdc extension for all rules
✅ Include YAML frontmatter with description
✅ Use alwaysApply: true for global rules
✅ Organize related rules in subfolders
✅ Keep rules focused and modular
```

### 2. Project Structure
```
✅ Keep .cursor/ folder in project root
✅ Use subfolders for organization
✅ Document custom rules in README
✅ Version control .cursor/ folder
✅ Share rules with team via git
```

### 3. File Placement
```
✅ Rules: .cursor/rules/*.mdc
✅ Commands: .cursor/rules/*/commands/*.md
✅ Docs: docs/ or documentation/ folder
✅ Tests: tests/ or __tests__/ folder
✅ Source: src/ or lib/ folder
```

## Unique Cursor Features

### 1. .mdc File Format
- **Only Cursor uses .mdc** for rules
- Other platforms use .md
- Must use .mdc in Cursor or rules won't load

### 2. @ Command Prefix
- Cursor uses `@` for commands
- Claude Code uses `/`
- Different invocation syntax

### 3. Composer Feature
- Multi-file editing in single view
- Context-aware code generation
- Inline AI suggestions

### 4. Chat with Codebase
- Natural language queries about code
- Context from entire codebase
- Different from Claude Code's SubAgents

## Cross-Platform Compatibility

### Cursor → Claude Code Migration
```
1. Rename rules:
   .cursor/rules/*.mdc → .claude/skills/*/SKILL.md

2. Convert format:
   - Keep YAML frontmatter
   - Adapt content to Skill format
   - Add triggers if needed

3. Commands:
   .cursor/rules/*/commands/*.md → .claude/commands/*.md
   Change @ to / for invocation

4. Project files:
   - Keep standard markdown documentation
   - No changes needed for source code
```

### Cursor → Windsurf/Cline Migration
```
1. Convert rules to markdown:
   .cursor/rules/*.mdc → .windsurf/rules/*.md (or equivalent)

2. Update YAML frontmatter:
   - Check platform-specific requirements
   - Adapt metadata fields as needed

3. Test commands:
   - Command syntax may differ
   - Verify invocation method
   - Update documentation
```

## Troubleshooting

### Rules Not Loading
1. ✅ Verify .mdc extension (NOT .md)
2. ✅ Check YAML frontmatter is valid
3. ✅ Ensure alwaysApply: true for global rules
4. ✅ Restart Cursor IDE
5. ✅ Check Cursor settings for rule directories

### Commands Not Working
1. ✅ Verify command is in commands/ subfolder
2. ✅ Use @ prefix (not /)
3. ✅ Check command file is .md format
4. ✅ Reload Cursor window

### Custom Instructions Not Working
1. ✅ Verify files are in .cursor/rules/
2. ✅ Check YAML frontmatter is valid
3. ✅ Ensure alwaysApply is set if needed
4. ✅ Reload Cursor window

## Official Resources

- **Website**: https://cursor.com
- **Docs**: https://docs.cursor.com
- **Discord**: Cursor community Discord
- **Forum**: https://forum.cursor.com

## Version History

- **2025-10-26**: Initial documentation
  - Documented .mdc file format requirement
  - Explained fstrent_spec_tasks integration
  - Added task status indicator system
  - Documented @ command prefix
  - Cross-platform migration notes

---

**Critical Notes**:
1. **MUST use .mdc extension** for rules in Cursor (not .md)
2. **Use @ prefix** for commands (not /)
3. **YAML frontmatter required** for all rules
4. Check Cursor docs quarterly for platform updates
