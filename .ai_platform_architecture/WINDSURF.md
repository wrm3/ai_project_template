# Windsurf Architecture

**Last Updated**: 2025-10-26
**Official Website**: https://codeium.com/windsurf
**Version Documented**: Windsurf IDE
**Status**: ⚠️ Limited information - needs verification

## Overview
Windsurf is an AI-powered IDE from Codeium. Information about its architecture is limited compared to Cursor and Claude Code. This document contains preliminary information that should be verified and updated.

## Expected Directory Structure

```
.windsurf/
├── rules/                     # Expected: Custom rules/instructions
│   └── *.md                  # Markdown files (assumed)
└── [Other configuration]      # To be documented
```

**⚠️ Note**: Directory structure is speculative. Verify with official Windsurf documentation.

## Rules/Instructions System

### Expected Format
Based on similar AI IDEs, likely uses:
- **File Type**: `.md` (standard markdown)
- **Location**: `.windsurf/rules/` or similar
- **Format**: Markdown with possible YAML frontmatter

### Needs Investigation
- [ ] Exact file extension (.md vs .mdc vs other)
- [ ] YAML frontmatter requirements
- [ ] Glob pattern support
- [ ] Rule activation mechanism
- [ ] Subfolder support

## Project Organization

### Expected Compatibility
- **Custom Instructions**: Likely supports markdown-based rules
- **YAML Frontmatter**: Probably supported (common pattern)
- **MCP Integration**: Unknown - needs verification
- **Investigation Needed**: Test custom instruction format

## MCP Integration

**Status**: Unknown

### Questions to Answer
- [ ] Does Windsurf support MCP?
- [ ] If yes, how are MCP servers configured?
- [ ] What's the configuration file format?
- [ ] Are MCP tools accessible from AI?

## Commands/Slash Commands

**Status**: Unknown

### Questions to Answer
- [ ] Does Windsurf support custom commands?
- [ ] What's the invocation syntax?
- [ ] How are commands defined?
- [ ] Where are command files located?

## Agents/SubAgents

**Status**: Unknown

### Questions to Answer
- [ ] Does Windsurf have agent/subagent concept?
- [ ] If yes, how are they configured?
- [ ] What's the file format?
- [ ] Where are agent definitions stored?

## Skills/Knowledge Modules

**Status**: Unknown - likely NO

Based on research, Skills appear to be Claude Code-specific feature.

## File Naming Conventions

**Status**: Needs verification

Expected (based on IDE conventions):
- Rules: `kebab-case.md` or `snake_case.md`
- Commands: `command-name.md`
- Other files: Follow standard markdown naming

## Best Practices

### Until More Information Available
1. ✅ Use standard markdown (.md) for custom instructions
2. ✅ Include YAML frontmatter for metadata
3. ✅ Follow general IDE best practices
4. ✅ Document discoveries as you learn
5. ✅ Check Windsurf docs regularly for updates

## Cross-Platform Compatibility

### Migrating TO Windsurf

**From Claude Code**:
- Skills → May need to convert to rules/instructions
- SubAgents → May not be supported
- Commands → Check if supported
- MCP → Verify MCP support

**From Cursor**:
- .mdc rules → Convert to .md (if Windsurf uses .md)
- Commands → Adapt invocation syntax
- Task system → Test compatibility

## Investigation Checklist

### Priority 1: Core Features
- [ ] Document exact directory structure
- [ ] Test rule/instruction file format
- [ ] Verify YAML frontmatter requirements
- [ ] Check command support
- [ ] Test MCP integration

### Priority 2: Advanced Features
- [ ] Agent/SubAgent support?
- [ ] Custom tool integration?
- [ ] Plugin system?
- [ ] Extension marketplace?

### Priority 3: Project Setup
- [ ] Test project structure compatibility
- [ ] Check custom instruction loading
- [ ] Verify markdown file support
- [ ] Test YAML frontmatter parsing

## Official Resources

- **Website**: https://codeium.com/windsurf
- **Docs**: [Need to locate official documentation]
- **Community**: [Check for Discord/forum]

## How to Help Complete This Doc

1. **Test in Windsurf**: Create test files and verify behavior
2. **Check Official Docs**: Review Windsurf documentation when available
3. **Report Findings**: Update this document with discoveries
4. **Compare Behavior**: Test same features across platforms
5. **Document Edge Cases**: Note any unusual behavior

## Temporary Notes

**What We Know**:
- Windsurf is AI-powered IDE from Codeium
- Likely supports custom instructions/rules
- May have different architecture than Cursor/Claude Code

**What We Need to Know**:
- Exact file formats and locations
- MCP support and configuration
- Custom command support
- Task management system compatibility
- Agent/SubAgent concepts

## Version History

- **2025-10-26**: Initial placeholder documentation
  - Created structure for future documentation
  - Listed investigation priorities
  - Set up framework for community contributions

---

**⚠️ This Document is Incomplete**

Please help complete this documentation by:
1. Testing features in Windsurf
2. Consulting official documentation
3. Updating this file with findings
4. Removing this warning when documentation is complete

Last verified: Never (placeholder document)
