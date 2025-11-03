# AI Platform Architecture Comparison

**Last Updated**: 2025-10-28
**Purpose**: Cross-platform compatibility guide for maintaining AI project templates

## TL;DR - The Simple Truth

**Three unique architectures, not six:**

1. **Claude Code** = Unique (Skills + SubAgents + complex structure)
2. **Gemini** = Unique (Hierarchical GEMINI.md cascade + 3 integrated systems)
3. **Everyone Else** = Nearly identical (rules-based, simple structure)

**The ONLY real difference between Cursor/Windsurf/Cline/Roo-Code:**
- Cursor uses `.mdc` file extension
- Others use `.md` file extension
- Everything else is the same pattern!

**Migration between non-Claude platforms is trivial:**
```bash
# Cursor → Windsurf/Cline/Roo-Code
cp -r .cursor .windsurf  # Copy folder
cd .windsurf/rules
rename 's/\.mdc$/.md/' *.mdc  # Rename extensions
# Done!
```

---

## Quick Reference Table

| Feature | Claude Code | Gemini | Cursor | Windsurf | Cline | Roo-Code |
|---------|-------------|--------|---------|-----------|-------|----------|
| **Type** | VSCode Ext | CLI + VSCode + Cloud | Standalone IDE | Standalone IDE | VSCode Ext | VSCode Ext |
| **Rules File Format** | `.md` | `GEMINI.md` ⚠️ | `.mdc` ⚠️ | `.md` (?) | `.md` (?) | `.md` (?) |
| **Rules Location** | `.claude/skills/` | Hierarchical cascade | `.cursor/rules/` | `.windsurf/` (?) | TBD | TBD |
| **Skills Support** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **SubAgents** | ✅ Yes | ❌ No | ❌ No | ❌ No (?) | ❌ No (?) | ❌ No (?) |
| **Hierarchical Context** | ❌ No | ✅ Yes ⚠️ | ❌ No | ❌ No | ❌ No | ❌ No |
| **Commands** | ✅ `/command` | ✅ `/command` | ✅ `@command` | ❓ Unknown | ❓ Unknown | ❓ Unknown |
| **MCP Integration** | ✅ Built-in | ❓ Unknown | ✅ Via VSCode | ❓ Unknown | ✅ Via VSCode | ✅ Via VSCode |
| **YAML Frontmatter** | ✅ Required | ❌ Optional | ✅ Required | ❓ Unknown | ❓ Unknown | ❓ Unknown |
| **Subfolder Support** | ✅ Yes | ✅ Yes | ✅ Yes | ❓ Unknown | ❓ Unknown | ❓ Unknown |
| **Task Management** | ✅ Compatible | ✅ Compatible | ✅ Compatible | ❓ Needs Test | ❓ Needs Test | ❓ Needs Test |

**Legend**:
- ✅ Confirmed working
- ❌ Confirmed not supported
- ❓ Unknown/needs verification
- ⚠️ Platform-specific difference

## Platform Architecture Patterns

### Two Main Architectures

**1. Claude Code (Unique Architecture)**
- **Skills & SubAgents** - Sophisticated multi-agent system
- **Directory**: `.claude/` with `skills/`, `agents/`, `commands/`
- **File Format**: `.md` with YAML frontmatter
- **Commands**: `/command` prefix

**2. Everyone Else (Similar Architecture)**
- **Rules-Based** - Single AI with custom instructions
- **Directory**: `.cursor/`, `.windsurf/`, `.cline/`, `.roo/` (platform-specific)
- **File Format**: `.md` (except Cursor uses `.mdc`)
- **Commands**: Varies by platform (`@` for Cursor, TBD for others)

### Critical Difference: Cursor's .mdc Extension

**The ONLY major difference between non-Claude platforms**:

```
Cursor:       .mdc (Markdown Cursor) ← UNIQUE FILE EXTENSION
Windsurf:     .md  (standard markdown)
Cline:        .md  (standard markdown)
Roo-Code:     .md  (standard markdown)
```

**Impact**: Cursor rules need file extension change for other platforms!

**Why This Matters**:
- Cursor → Windsurf/Cline/Roo-Code: Just rename `.mdc` → `.md`
- Same YAML frontmatter format
- Same rule structure
- Same markdown syntax
- Minimal migration effort!

**Migration**:
```bash
# Cursor → Other Platforms
find .cursor/rules -name "*.mdc" -exec sh -c 'mv "$1" "${1%.mdc}.md"' _ {} \;

# Other Platforms → Cursor
find .platform/rules -name "*.md" -exec sh -c 'mv "$1" "${1%.md}.mdc"' _ {} \;
```

### Directory Structures by Architecture

**Claude Code (Unique)**:
```
.claude/
├── agents/          # SubAgents (unique to Claude Code)
├── commands/        # Slash commands (/)
├── skills/          # Skills (unique to Claude Code)
│   └── skill-name/
│       ├── SKILL.md
│       ├── reference/
│       └── examples/
└── settings.local.json
```

**Non-Claude Platforms (Similar Pattern)**:
```
.{platform}/         # .cursor, .windsurf, .cline, .roo
└── rules/           # Custom instructions
    ├── *.{ext}      # .mdc (Cursor) or .md (others)
    └── commands/    # Optional custom commands
```

**Key Insight**: Once you understand one non-Claude platform (like Cursor), you understand them all! Just change:
1. Folder name (`.cursor/` → `.windsurf/`)
2. File extension (`.mdc` → `.md` for non-Cursor)
3. Command prefix (if applicable)

### 3. Skills/SubAgents Support

**Only Claude Code has Skills & SubAgents**

```
Claude Code: ✅
  - .claude/skills/      # Knowledge modules
  - .claude/agents/      # Specialized AI agents

All Others: ❌
  - Must use rules/instructions instead
  - No SubAgent equivalent
  - Single AI assistant model
```

**Migration Strategy**:
- Claude Code Skills → Convert to platform rules
- Claude Code SubAgents → Merge into main AI instructions
- Document what functionality is lost

### 4. Command Invocation

```
Claude Code:  /command-name
Cursor:       @command-name
Windsurf:     [Unknown]
Cline:        [Unknown]
Roo-Code:     [Unknown]
```

**Impact**: Commands need different prefixes per platform

**Cross-Platform Solution**:
```markdown
# In command documentation
Usage:
- Claude Code: /command-name
- Cursor: @command-name
- Others: [Check platform docs]
```

### 5. MCP Integration

```
Claude Code:  Built-in UI, settings.local.json
Cursor:       Via VSCode settings (VSCode fork)
Windsurf:     Unknown
Cline:        Via VSCode settings (VSCode extension)
Roo-Code:     Via VSCode settings (VSCode extension)
```

**Compatibility**: VSCode-based platforms likely share MCP configuration

## Universal Features (Work Everywhere)

### Markdown-Based Configuration ✅

All platforms support markdown for custom instructions:
- **File Format**: `.md` files (except Cursor uses `.mdc`)
- **YAML Frontmatter**: Widely supported for metadata
- **Code Blocks**: All platforms render code examples
- **Formatting**: Headers, lists, tables work everywhere
- **Documentation**: Standard markdown for project docs

**Example Universal Rule**:
```yaml
---
description: Project coding standards
---

# Coding Standards

## Style Guide
- Use consistent indentation
- Follow language conventions
- Write clear comments

## Best Practices
- Test before committing
- Document public APIs
- Review code changes
```

### MCP (Model Context Protocol) ✅

Most platforms support MCP for tool integration:
- **Claude Code**: Built-in MCP UI
- **Cursor**: Via VSCode settings (VSCode fork)
- **Cline**: Via VSCode settings (VSCode extension)
- **Roo-Code**: Via VSCode settings (VSCode extension)
- **Windsurf**: Unknown (needs verification)

### File-Based Configuration ✅

All platforms use file-based setup:
- Configuration stored in project folders
- Version control friendly
- Team sharing via git
- No cloud dependencies

## Platform-Specific Features

### Claude Code Exclusive

1. **Skills System**
   ```
   .claude/skills/skill-name/
   ├── SKILL.md           # Main skill
   ├── scripts/           # Python/Bash scripts
   ├── reference/         # Documentation
   ├── templates/         # File templates
   └── examples/          # Usage examples
   ```

2. **SubAgents**
   ```yaml
   ---
   name: agent-name
   description: Specialization description
   tools: Read, Edit, Write, Bash, Grep, Glob
   model: sonnet|opus|haiku
   ---
   ```

3. **YAML Triggers**
   ```yaml
   triggers: [keyword1, keyword2, keyword3]
   ```

### Cursor Exclusive

1. **.mdc File Extension**
   - Must use `.mdc` not `.md` for rules
   - Other files can be `.md`

2. **Composer Feature**
   - Multi-file editing in single view
   - Not available in other platforms

3. **@ Command Prefix**
   - Uses `@` not `/`

## Migration Guides

### Claude Code → Cursor

```bash
# 1. Convert Skills to Rules
mkdir -p .cursor/rules/
cp -r .claude/skills/* .cursor/rules/

# 2. Rename to .mdc
find .cursor/rules -name "SKILL.md" -exec sh -c '
  mv "$1" "$(dirname "$1")/rules.mdc"
' _ {} \;

# 3. Adapt YAML frontmatter
# Change:
---
name: skill-name
description: Description
triggers: [list]
---

# To:
---
description: Description
alwaysApply: true
---

# 4. Convert commands
cp -r .claude/commands .cursor/rules/commands
# Update invocation: / → @

# 5. SubAgents
# Merge into main rules (no direct equivalent)

# 6. Keep task system
# No changes needed for .fstrent_spec_tasks/
```

### Cursor → Claude Code

```bash
# 1. Convert Rules to Skills
mkdir -p .claude/skills/

# 2. Rename .mdc to SKILL.md
find .cursor/rules -name "*.mdc" -exec sh -c '
  mkdir -p ".claude/skills/$(basename $(dirname $1))"
  cp "$1" ".claude/skills/$(basename $(dirname $1))/SKILL.md"
' _ {} \;

# 3. Update YAML frontmatter
# Add name and triggers fields

# 4. Convert commands
cp -r .cursor/rules/*/commands .claude/commands
# Update invocation: @ → /

# 5. Keep project files
# Source code and docs unchanged
```

### To Windsurf/Cline/Roo-Code

```bash
# 1. Determine platform structure (needs research)
# Check platform documentation first

# 2. Convert from Claude Code
# - Skills → Platform rules format
# - SubAgents → Main AI instructions
# - Commands → Platform commands (if supported)
# - Keep project files unchanged

# 3. Test compatibility
# - Verify YAML frontmatter works
# - Test custom instructions
# - Check MCP integration
```

## Best Practices for Cross-Platform Templates

### 1. Use Universal Structures

```
✅ docs/                    # Standard documentation
✅ src/ or lib/             # Source code
✅ tests/                   # Test files
✅ README.md                # Project documentation
✅ .gitignore               # Version control
```

### 2. Platform-Specific Folders

```
.claude/              # Claude Code specific
.cursor/              # Cursor specific
.windsurf/            # Windsurf specific (if exists)
.vscode/              # VSCode extensions config
```

### 3. Dual-Format Rules (when possible)

```
.cursor/rules/feature.mdc         # For Cursor
.claude/skills/feature/SKILL.md   # For Claude Code

# Keep content synchronized
# Use scripts to sync if needed
```

### 4. Documentation

```
# Always document which platform features are used
## Platform Requirements
- ✅ Claude Code: Uses Skills, SubAgents
- ✅ Cursor: Uses .mdc rules
- ⚠️ Windsurf: Needs testing
- ⚠️ Cline: Needs testing
- ⚠️ Roo-Code: Needs testing
```

### 5. Testing Matrix

Test template on all platforms:

| Feature | Claude Code | Cursor | Windsurf | Cline | Roo-Code |
|---------|-------------|---------|-----------|-------|----------|
| Custom Instructions | ✅ | ✅ | ❓ | ❓ | ❓ |
| YAML Frontmatter | ✅ | ✅ | ❓ | ❓ | ❓ |
| MCP Integration | ✅ | ✅ | ❓ | ✅ | ✅ |
| Commands | ✅ | ✅ | ❓ | ❓ | ❓ |
| Skills/Agents | ✅ | ❌ | ❌ | ❌ | ❌ |

## Maintenance Checklist

### Quarterly Review

- [ ] Check Claude Code docs for new features
- [ ] Check Cursor docs for updates
- [ ] Research Windsurf capabilities
- [ ] Research Cline capabilities
- [ ] Research Roo-Code capabilities
- [ ] Update comparison table
- [ ] Test template on all platforms
- [ ] Update migration guides
- [ ] Document breaking changes

### When Adding New Features

- [ ] Document which platforms support it
- [ ] Create platform-specific versions if needed
- [ ] Update comparison table
- [ ] Test on primary platforms (Claude Code, Cursor)
- [ ] Document migration steps
- [ ] Update README with platform requirements

### Version Control

```bash
# Tag releases with platform compatibility
git tag -a v1.0.0-claude-cursor -m "Compatible with Claude Code & Cursor"

# Document in CHANGELOG.md
## v1.0.0 - 2025-10-26
### Platform Support
- ✅ Claude Code: Full support
- ✅ Cursor: Full support
- ⚠️ Windsurf: Experimental
- ⚠️ Cline: Untested
- ⚠️ Roo-Code: Untested
```

## Known Issues

### 1. Cursor .mdc Extension

**Issue**: Rules must be `.mdc` in Cursor, but `.md` everywhere else

**Workaround**:
- Maintain separate `.cursor/` folder
- Use scripts to sync content
- Document difference in README

### 2. Skills/SubAgents Platform Lock-in

**Issue**: Skills and SubAgents only work in Claude Code

**Workaround**:
- Keep core logic in fstrent_spec_tasks (universal)
- Use Skills/SubAgents as optional enhancement
- Provide fallback for other platforms

### 3. Command Prefix Differences

**Issue**: `/` vs `@` vs unknown

**Workaround**:
- Document both prefixes
- Update docs when testing new platforms
- Consider command alias system

## Future Research Needed

### Windsurf
- [ ] Exact directory structure
- [ ] Rule file format (.md vs .mdc vs other)
- [ ] Command support and syntax
- [ ] MCP integration details
- [ ] Task management compatibility

### Cline
- [ ] Configuration location
- [ ] Rule/instruction format
- [ ] MCP integration
- [ ] Custom command support
- [ ] VSCode settings integration

### Roo-Code
- [ ] Same questions as Cline
- [ ] Compare with Cline
- [ ] Identify unique features
- [ ] Document differences

## Contributing

Help complete this comparison:

1. **Test Platforms**: Try features on untested platforms
2. **Update Docs**: Add findings to platform-specific docs
3. **Report Issues**: Note incompatibilities
4. **Share Solutions**: Document workarounds
5. **Keep Current**: Update quarterly

## Resources

- **Claude Code**: https://docs.claude.com/en/docs/claude-code
- **Cursor**: https://cursor.com, https://docs.cursor.com
- **Windsurf**: https://codeium.com/windsurf
- **Cline**: [Research GitHub/docs]
- **Roo-Code**: [Research GitHub/docs]

---

**Last Updated**: 2025-10-26
**Next Review**: 2026-01-26 (quarterly)
**Status**: Active, needs community input for Windsurf/Cline/Roo-Code
