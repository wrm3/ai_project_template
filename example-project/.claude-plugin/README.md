# fstrent-spec-tasks Claude Code Plugin

This directory contains the plugin manifest for distributing `fstrent-spec-tasks` as a Claude Code plugin.

## Plugin Structure

```
.claude-plugin/
├── plugin.json          # Plugin metadata and manifest
└── README.md           # This file
```

## What Gets Installed

When users install this plugin, they get:

### Skills (3 comprehensive skills)
- **fstrent-task-management**: Complete task management system
- **fstrent-planning**: Project planning and PRD creation
- **fstrent-qa**: Bug tracking and quality assurance

### Commands (7 custom commands)
- `/project:new-task` - Create new task
- `/project:update-task` - Update task status
- `/project:report-bug` - Report bug
- `/project:start-planning` - Start project planning
- `/project:add-feature` - Add feature document
- `/project:quality-report` - Generate quality report
- `/project:status` - Project status overview

### Agents (to be added in Task 008)
- Task expander subagent (coming soon)

### File Structure
- `.fstrent_spec_tasks/` directory with all core files
- Complete reference materials
- Working examples
- Cross-IDE compatibility

## Installation

### For Users

```bash
# Add marketplace (once available)
/plugin marketplace add fstrent/claude-plugins

# Install plugin
/plugin install fstrent-spec-tasks@fstrent
```

### For Developers

```bash
# Clone repository
git clone https://github.com/fstrent/fstrent-spec-tasks.git

# Test locally
/plugin marketplace add ./fstrent-spec-tasks
/plugin install fstrent-spec-tasks@local
```

## Features

- ✅ 100% Cursor compatibility
- ✅ Cross-IDE file sharing
- ✅ Comprehensive task management
- ✅ Project planning with scope validation
- ✅ Bug tracking and quality metrics
- ✅ Progressive disclosure (Skills → Reference → Examples)
- ✅ ~68,500 words of documentation

## Version History

### 1.0.0 (2025-10-19)
- Initial release
- 3 core Skills
- 7 custom commands
- Complete reference materials
- Working examples
- 100% tested

## Support

- **Issues**: https://github.com/fstrent/fstrent-spec-tasks/issues
- **Documentation**: See README.md in repository root
- **Examples**: See `.claude/skills/*/examples/` folders

## License

MIT License - See LICENSE file in repository root

