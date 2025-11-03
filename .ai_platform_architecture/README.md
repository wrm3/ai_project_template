# AI Platform Architecture Documentation

**Purpose**: Source of truth for AI coding platform setup, features, and cross-platform compatibility.

## Overview

This folder documents the architecture, features, and setup requirements for major AI coding platforms, enabling developers to:
- **Understand platform differences** - File formats, directory structures, unique features
- **Switch platforms mid-project** - Migration guides and compatibility notes
- **Set up new projects** - Platform-specific configuration templates
- **Stay current** - Track new features as platforms evolve

### The Simple Truth About Platform Architectures

**Three unique architectures, not six:**

1. **Claude Code** - Unique architecture with Skills & SubAgents
2. **Gemini** - Unique hierarchical GEMINI.md cascade + 3 integrated systems (CLI, VSCode, GitHub)
3. **Everyone Else** - Nearly identical rules-based architecture

**Key Insights**: 
- Cursor, Windsurf, Cline, and Roo-Code all follow the same pattern
- The ONLY significant difference is Cursor uses `.mdc` while others use `.md`
- Migration between non-unique platforms is trivial!

### Platforms Documented
- **Claude Code** (Anthropic's VSCode extension) - Unique architecture with Skills/SubAgents
- **Gemini** (Google's multi-system) - Unique hierarchical context cascade (CLI + VSCode + GitHub)
- **Cursor** (AI-first IDE) - Rules-based, uses `.mdc`
- **Windsurf** (Codeium's IDE) - Rules-based, uses `.md`
- **Cline** (VSCode extension) - Rules-based, uses `.md`
- **Roo-Code** (VSCode extension) - Rules-based, uses `.md`

## Documentation Files

| File/Folder | Description | Status |
|-------------|-------------|--------|
| [Claude_Code/](Claude_Code/) | **Comprehensive Claude Code documentation** | ✅ Complete |
| ├─ [ARCHITECTURE.md](Claude_Code/ARCHITECTURE.md) | Deep dive: Skills, SubAgents, plugins, workflows | ✅ Complete |
| ├─ [RESEARCH_TOPICS.md](Claude_Code/RESEARCH_TOPICS.md) | 23 research topics (CLI, web, mobile, etc.) | 🔍 Active |
| ├─ [PLATFORM_OVERVIEW.md](Claude_Code/PLATFORM_OVERVIEW.md) | Quick reference guide | ✅ Complete |
| [GEMINI.md](GEMINI.md) | Complete Gemini architecture (3 systems) | ✅ Complete |
| [CURSOR.md](CURSOR.md) | Complete Cursor architecture | ✅ Complete |
| [WINDSURF.md](WINDSURF.md) | Windsurf architecture (preliminary) | ⚠️ Needs verification |
| [CLINE_AND_ROO_CODE.md](CLINE_AND_ROO_CODE.md) | Cline & Roo-Code architecture | ⚠️ Needs research |
| [PLATFORM_COMPARISON.md](PLATFORM_COMPARISON.md) | Cross-platform comparison | ✅ Active |

**Note**: Additional platform-specific folders (Gemini/, Cursor/, Windsurf/, Cline/, Roo_Code/) created for future detailed research.

## Quick Start

### For Template Maintainers

1. **Read PLATFORM_COMPARISON.md first** - Understand key differences
2. **Check platform-specific docs** before making changes
3. **Test on multiple platforms** when adding features
4. **Update docs** when discovering new information

### For Platform-Specific Users

If you're only using one platform, read your platform's doc:
- Using Claude Code? → [Claude_Code/](Claude_Code/) folder (comprehensive docs)
  - Quick start: [PLATFORM_OVERVIEW.md](Claude_Code/PLATFORM_OVERVIEW.md)
  - Deep dive: [ARCHITECTURE.md](Claude_Code/ARCHITECTURE.md)
  - Research: [RESEARCH_TOPICS.md](Claude_Code/RESEARCH_TOPICS.md)
- Using Gemini? → [GEMINI.md](GEMINI.md)
- Using Cursor? → [CURSOR.md](CURSOR.md)
- Using Windsurf? → [WINDSURF.md](WINDSURF.md)
- Using Cline/Roo-Code? → [CLINE_AND_ROO_CODE.md](CLINE_AND_ROO_CODE.md)

## Critical Differences

### Architecture Patterns

**Pattern 1: Claude Code (Unique)**
```
✅ Skills system - Reusable knowledge modules
✅ SubAgents - Specialized AI assistants  
✅ Complex structure - agents/, skills/, commands/
✅ File format: .md with YAML frontmatter
✅ Commands: /command prefix
```

**Pattern 2: Non-Claude Platforms (Nearly Identical)**
```
✅ Rules-based - Custom instructions
✅ Simple structure - rules/ folder
✅ File format: .md (or .mdc for Cursor only)
✅ YAML frontmatter - Same format across all
✅ Commands: Platform-specific (@command for Cursor)
```

### The ONLY Real Difference Between Non-Claude Platforms

**File Extension:**
```
Cursor:       .mdc ← ONLY difference from others
Windsurf:     .md
Cline:        .md
Roo-Code:     .md
```

**Everything else is the same:**
- Same YAML frontmatter format
- Same rule structure
- Same markdown syntax
- Same directory pattern (`.{platform}/rules/`)
- Migration = rename folder + change extension!

## Maintenance Schedule

### Quarterly Review (Every 3 Months)
- [ ] Check all platform official docs for updates
- [ ] Test template on each platform
- [ ] Update architecture docs
- [ ] Update comparison table
- [ ] Document breaking changes

### When Adding Features
- [ ] Document platform compatibility
- [ ] Test on Claude Code and Cursor (primary)
- [ ] Update platform-specific folders
- [ ] Update comparison doc
- [ ] Tag release with compatibility notes

### When Discovering Issues
- [ ] Document in platform-specific file
- [ ] Add to "Known Issues" in comparison
- [ ] Provide workaround if available
- [ ] Update affected migration guides

## How to Contribute

### Researching Unknown Platforms

For Windsurf, Cline, Roo-Code (incomplete docs):

1. **Install the Platform**
   - Download and install
   - Set up a test project
   - Try basic features

2. **Test Structure**
   ```bash
   # Create test files
   mkdir -p .platform/rules
   echo "test" > .platform/rules/test.md

   # Test if recognized
   # Check AI behavior
   # Document findings
   ```

3. **Document Findings**
   - Update platform-specific .md file
   - Add to comparison table
   - Share examples
   - Note limitations

4. **Submit Update**
   - Edit relevant docs
   - Add examples
   - Update README
   - Note verification status

### Improving Existing Docs

- Clarify confusing sections
- Add examples
- Fix errors
- Update outdated information
- Add troubleshooting tips

## Key Concepts

### Universal Features
Work on all platforms:
- **Markdown files** - All platforms support `.md` files
- **YAML frontmatter** - Widely supported for metadata
- **MCP (Model Context Protocol)** - Standard tool integration
- **Custom instructions** - All platforms support AI behavior customization
- **File-based configuration** - All use file-based setup

### Platform-Specific Features
Only work on specific platforms:
- **Skills/SubAgents**: Claude Code only
- **.mdc files**: Cursor only (must use `.mdc` not `.md`)
- **Command prefixes**: `/` (Claude Code), `@` (Cursor), varies for others
- **MCP UI**: Built-in (Claude Code), VSCode settings (others)
- **Directory names**: `.claude/`, `.cursor/`, `.windsurf/`, etc.

### Cross-Platform Strategy
1. **Start with universal features** - Markdown, YAML, MCP
2. **Add platform-specific configs** - Create platform folders as needed
3. **Document requirements** - Note which features need which platform
4. **Test on target platforms** - Verify before committing
5. **Keep docs updated** - Track platform changes quarterly

## Common Tasks

### Adding New Rule/Instruction

```bash
# 1. Create for Claude Code
echo "---
name: my-rule
description: What it does
---
# My Rule
Content..." > .claude/skills/my-rule/SKILL.md

# 2. Create for Cursor
echo "---
description: What it does
alwaysApply: true
---
# My Rule
Content..." > .cursor/rules/my-rule.mdc

# 3. Document
# Add to PLATFORM_COMPARISON.md
```

### Testing Cross-Platform

```bash
# 1. Test in Claude Code
code . # Open in VSCode with Claude Code

# 2. Test in Cursor
cursor . # Open in Cursor

# 3. Document results
# Update platform-specific docs
```

### Migrating Between Platforms

See migration guides in [PLATFORM_COMPARISON.md](PLATFORM_COMPARISON.md):
- Claude Code → Cursor
- Cursor → Claude Code
- To Windsurf/Cline/Roo-Code

## Verification Status

| Platform | Directory Structure | File Format | Commands | MCP | Skills/Agents |
|----------|-------------------|-------------|-----------|-----|---------------|
| Claude Code | ✅ Verified | ✅ `.md` | ✅ `/command` | ✅ Built-in | ✅ Yes |
| Cursor | ✅ Verified | ✅ `.mdc` | ✅ `@command` | ✅ VSCode | ❌ No |
| Windsurf | ❓ Unknown | ❓ Unknown | ❓ Unknown | ❓ Unknown | ❓ Unknown |
| Cline | ❓ Unknown | ❓ Unknown | ❓ Unknown | ✅ Likely VSCode | ❌ Likely No |
| Roo-Code | ❓ Unknown | ❓ Unknown | ❓ Unknown | ✅ Likely VSCode | ❌ Likely No |

Legend:
- ✅ Confirmed working
- ❌ Confirmed not supported
- ❓ Needs verification
- ⚠️ Partial support

## Official Resources

- **Claude Code**: https://docs.claude.com/en/docs/claude-code
- **Cursor**: https://docs.cursor.com
- **Windsurf**: https://codeium.com/windsurf
- **Cline**: [Add link when found]
- **Roo-Code**: [Add link when found]
- **MCP Protocol**: https://modelcontextprotocol.io/

## Questions?

1. Check platform-specific documentation
2. Check PLATFORM_COMPARISON.md
3. Search official platform docs
4. Ask in platform community (Discord/forum)
5. Update this documentation with answer

## Version History

- **2025-10-26**: Initial documentation
  - Complete docs for Claude Code and Cursor
  - Placeholder docs for Windsurf, Cline, Roo-Code
  - Comprehensive comparison table
  - Migration guides
  - Maintenance schedule

---

**Maintained by**: Template maintainers
**Last Review**: 2025-10-26
**Next Review**: 2026-01-26
**Status**: Active documentation, community contributions welcome
