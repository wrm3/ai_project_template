# Cline & Roo-Code Architecture

**Last Updated**: 2025-10-26
**Status**: ⚠️ Limited information - needs verification

## Overview

### Cline
- **Type**: VSCode Extension
- **Official**: https://github.com/cline/cline (verify URL)
- **Description**: AI coding assistant as VSCode extension

### Roo-Code
- **Type**: VSCode Extension
- **Official**: https://github.com/RooCode (verify URL)
- **Description**: AI coding assistant as VSCode extension

**Note**: These are VSCode extensions, so they inherit VSCode's architecture and limitations.

## Expected Directory Structure

Since both are VSCode extensions, they likely follow VSCode extension patterns:

```
.vscode/
├── settings.json          # Extension settings
└── extensions/            # Extension-specific files

[Platform-Specific Folder]/
├── rules/ or instructions/
│   └── *.md
└── [configuration files]
```

**⚠️ Note**: Exact structure needs verification. Each extension may use different folder names.

## Rules/Instructions

### Expected Format
- **File Type**: Likely `.md` (standard markdown)
- **Location**: TBD - needs investigation
- **Configuration**: Possibly in VSCode settings.json

### Questions to Answer
- [ ] Do they support custom rules/instructions?
- [ ] What file format do they use?
- [ ] Where are rules/instructions stored?
- [ ] How are they activated?

## MCP (Model Context Protocol)

### VSCode-Based Extensions
Since these are VSCode extensions, MCP support would typically be:
- Configured via VSCode settings
- Shared across Claude Code (if both installed)
- Standard MCP server protocol

### Questions
- [ ] Do Cline/Roo-Code support MCP?
- [ ] How is it configured?
- [ ] Is it compatible with Claude Code's MCP setup?

## Project Organization

### Custom Instructions
**Unknown** - needs testing

Since these are VSCode extensions:
- Likely support markdown-based instructions
- YAML frontmatter parsing uncertain
- May share VSCode settings format
- Configuration method needs verification

## Commands

### Slash Commands
- [ ] Do they support custom commands?
- [ ] What's the invocation syntax?
- [ ] How are commands defined?

## Skills/Knowledge Modules

**Likely NO** - Skills appear to be Claude Code-specific

## Agents/SubAgents

**Likely NO** - SubAgents appear to be Claude Code-specific

## Best Practices (Tentative)

Until more information is available:

1. **Use Standard Formats**
   - Stick to markdown (.md)
   - Use clear, descriptive file names
   - Follow VSCode conventions

2. **Test Compatibility**
   - Test if fstrent_spec_tasks works
   - Check if custom instructions work
   - Verify MCP integration

3. **Document Findings**
   - Update this doc with discoveries
   - Share knowledge with community
   - Report bugs/limitations

## Investigation Priorities

### For Cline
1. [ ] Determine if custom instructions/rules are supported
2. [ ] Test MCP integration
3. [ ] Check task management compatibility
4. [ ] Verify command support
5. [ ] Document exact directory structure

### For Roo-Code
1. [ ] Same investigation priorities as Cline
2. [ ] Compare with Cline to identify differences
3. [ ] Document unique features
4. [ ] Test cross-compatibility

## Cross-Platform Compatibility

### Migrating TO Cline/Roo-Code

**From Claude Code**:
- Skills → May not be supported
- SubAgents → Likely not supported
- Commands → Verify support
- MCP → Should work (VSCode-based)
- Custom instructions → Test format

**From Cursor**:
- .mdc rules → Convert to .md format
- Commands → Adapt if supported
- Project files → No changes needed

## Known Limitations (Tentative)

As VSCode extensions (not full IDEs):
- May have less customization than Cursor
- May lack Skills/SubAgents features
- May have simpler configuration
- May rely more on VSCode settings

## Official Resources

### Cline
- GitHub: [Verify URL]
- Docs: [Locate documentation]
- Community: [Find Discord/forum]

### Roo-Code
- GitHub: [Verify URL]
- Docs: [Locate documentation]
- Community: [Find Discord/forum]

## How to Complete This Documentation

1. **Install Extensions**
   - Install Cline in VSCode
   - Install Roo-Code in VSCode
   - Test features side-by-side

2. **Test Features**
   - Create test instructions/rules
   - Try custom commands
   - Test MCP integration
   - Verify custom instruction loading

3. **Document Results**
   - Update this file with findings
   - Add examples and code samples
   - Include screenshots if helpful
   - Note any bugs or limitations

4. **Compare Platforms**
   - How does Cline differ from Roo-Code?
   - What's unique about each?
   - Which features are shared?
   - Cross-compatibility notes

## Temporary Assumptions

**Based on VSCode Extension Architecture**:
- Likely use VSCode settings.json for configuration
- Probably support markdown instructions
- May share MCP configuration with Claude Code
- Might have simpler feature set than full IDEs

**These assumptions need verification**

## Version History

- **2025-10-26**: Initial placeholder documentation
  - Created investigation framework
  - Listed priority questions
  - Set up structure for community contributions

---

**⚠️ This Document is Incomplete**

This documentation needs community input:
1. Test Cline and Roo-Code
2. Document actual behavior
3. Update this file
4. Remove warning when complete

Last verified: Never (placeholder document)
