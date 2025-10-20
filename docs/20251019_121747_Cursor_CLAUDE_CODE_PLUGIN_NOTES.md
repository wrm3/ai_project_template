# Claude Code Plugin Development Notes

## Overview

This document contains notes and resources for converting `fstrent-spec-tasks` into a distributable Claude Code plugin.

**Status**: Plugin structure created, full implementation deferred to end of project (Task 017)

---

## Resources Provided

### Document 1: Claude Code Starter Template
- Minimal, reusable starter template structure
- Separation of personal (`~/.claude/`) vs project-level (`.claude/`) configs
- Best practices for CLAUDE.md, .mcp.json, Skills, Agents, Commands
- Setup instructions and troubleshooting

**Key Insights**:
- Keep universal tools in `~/.claude/` (personal)
- Keep project-specific items in `.claude/` (project)
- Use environment variables for credentials (never hardcode)
- Commit `.claude/` to git, not personal configs

### Document 2: Creating Claude Code Plugins
- Complete guide to bundling MCPs, Skills, Agents, Commands
- Plugin structure and manifest format
- Publishing options (Git repo, marketplace)
- Team auto-install setup
- Security best practices

**Key Insights**:
- Plugins bundle Skills + MCPs + Agents + Commands
- Store in Git repository, install with one command
- Use `.claude-plugin/plugin.json` for metadata
- Environment variables for sensitive credentials
- Repository-level config for team auto-install

---

## Current Plugin Structure

```
.claude-plugin/
├── plugin.json          # Plugin metadata ✅ Created
└── README.md           # Plugin documentation ✅ Created
```

---

## What We Have Ready

### Skills (Complete)
- `.claude/skills/fstrent-task-management/` ✅
- `.claude/skills/fstrent-planning/` ✅
- `.claude/skills/fstrent-qa/` ✅

### Commands (Complete)
- `.claude/commands/new-task.md` ✅
- `.claude/commands/update-task.md` ✅
- `.claude/commands/report-bug.md` ✅
- `.claude/commands/start-planning.md` ✅
- `.claude/commands/add-feature.md` ✅
- `.claude/commands/quality-report.md` ✅
- `.claude/commands/status.md` ✅

### Agents (Pending)
- Task expander subagent (Task 008)

### Documentation (Complete)
- Reference materials ✅
- Examples ✅
- Command reference ✅
- Testing logs ✅

---

## What Needs to Be Done (Task 017)

### 1. MCP Configuration
Create `.mcp.json` for any external integrations:
- Database connections (if needed)
- API integrations (if needed)
- External tools (if needed)

**Note**: Currently no MCPs needed for core functionality

### 2. Plugin Manifest Updates
Update `.claude-plugin/plugin.json`:
- Finalize version number
- Add complete feature list
- Update repository URLs
- Add changelog

### 3. Marketplace Setup
Create marketplace repository:
- `my-plugin-marketplace/` structure
- `marketplace.json` configuration
- Plugin listing

### 4. Team Auto-Install
Create `.claude/settings.json`:
- Configure extra marketplaces
- Enable auto-install for teams
- Set plugin preferences

### 5. Testing
- Test local installation
- Test marketplace installation
- Test team auto-install
- Verify all features work

### 6. Documentation
- Update main README.md
- Create INSTALLATION.md
- Create CONTRIBUTING.md
- Add examples for plugin usage

### 7. Publishing
- Push to GitHub
- Create release
- Publish to marketplace (if available)
- Announce to community

---

## Plugin Distribution Options

### Option 1: Direct Git Installation (Simplest)
```bash
/plugin marketplace add fstrent/fstrent-spec-tasks
/plugin install fstrent-spec-tasks@fstrent
```

**Pros**:
- Simple setup
- Direct from repository
- Easy updates

**Cons**:
- Requires Git access
- Manual version management

### Option 2: Custom Marketplace (Recommended)
```bash
/plugin marketplace add fstrent/claude-plugins
/plugin install fstrent-spec-tasks@fstrent
```

**Pros**:
- Professional distribution
- Version management
- Multiple plugins support
- Team control

**Cons**:
- Requires marketplace repo
- More setup

### Option 3: Official Marketplace (Future)
```bash
/plugin install fstrent-spec-tasks
```

**Pros**:
- Widest distribution
- Official support
- Automatic updates

**Cons**:
- May not exist yet
- Submission process
- Review requirements

---

## Security Considerations

### Environment Variables
If we add MCPs in the future:
```json
{
  "mcpServers": {
    "example": {
      "env": {
        "API_KEY": "${EXAMPLE_API_KEY}"  // ✅ Use env vars
        // "API_KEY": "hardcoded-key"    // ❌ Never hardcode
      }
    }
  }
}
```

### .gitignore
Already configured to exclude:
- `.env` files
- Sensitive credentials
- Personal configs

### Documentation
Must include:
- Environment variable setup instructions
- Security best practices
- Credential management guide

---

## Team Auto-Install Configuration

For organizations wanting automatic plugin installation:

**`.claude/settings.json`** (to be created):
```json
{
  "extraKnownMarketplaces": {
    "fstrent-tools": {
      "source": {
        "type": "github",
        "repo": "fstrent/claude-plugins"
      }
    }
  },
  "plugins": {
    "fstrent-spec-tasks@fstrent-tools": "enabled"
  }
}
```

**Workflow**:
1. Team member clones project
2. Opens in Claude Code
3. Prompted to trust repository
4. Plugins auto-install
5. Ready to work!

---

## Version Management

### Semantic Versioning
- **1.0.0**: Initial release (current)
- **1.1.0**: Minor features (Task 008 subagent)
- **1.2.0**: Additional features (Phase 3)
- **2.0.0**: Breaking changes (if needed)

### Changelog Format
```markdown
# Changelog

## [1.0.0] - 2025-10-19
### Added
- 3 core Skills (task management, planning, QA)
- 7 custom commands
- Complete reference materials
- Working examples
- 100% Cursor compatibility

## [1.1.0] - TBD
### Added
- Task expander subagent
- Integration testing
- Enhanced documentation
```

---

## Testing Checklist

Before publishing:
- [ ] Local installation works
- [ ] All Skills activate correctly
- [ ] All Commands work
- [ ] All Agents function (when added)
- [ ] Reference materials accessible
- [ ] Examples work as templates
- [ ] Cross-IDE compatibility verified
- [ ] Documentation complete
- [ ] Security review passed
- [ ] Version numbers correct

---

## Next Steps (Deferred to Task 017)

1. Complete Phase 2 (Task 008-009)
2. Complete Phase 3 (Task 010-013)
3. Complete Phase 4 (Task 014-016)
4. **Then**: Implement full plugin distribution (Task 017)

---

## References

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/quickstart)
- [Agent Skills Guide](https://docs.claude.com/en/docs/claude-code/skills)
- [Subagents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

---

**Created**: 2025-10-19  
**Last Updated**: 2025-10-19  
**Status**: Planning phase, implementation deferred to Task 017

