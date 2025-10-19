# Project Context: fstrent_spec_tasks Claude Code Adaptation

## 🎯 Mission
Create a Claude Code adaptation of the fstrent_spec_tasks task management system that maintains 100% compatibility with Cursor's implementation, enabling seamless cross-IDE collaboration.

## 📍 Current Phase
**Phase 1: Core Skills Development**

Focus on creating the three primary Skills that form the foundation of the Claude Code adaptation:
1. Task management Skill
2. Planning Skill
3. Quality assurance Skill

## ✅ Success Criteria

### Primary Objectives
- [ ] Claude Code Skills can read/write `.fstrent_spec_tasks/` files
- [ ] 100% file format compatibility with Cursor
- [ ] Zero data loss or corruption
- [ ] Natural language interaction (no special syntax)
- [ ] Skills activate automatically based on user intent

### Quality Standards
- Skills follow Anthropic's official specification
- SKILL.md files are clear and concise (< 5k words)
- Progressive disclosure used effectively
- Comprehensive testing with both IDEs
- Documentation covers all use cases

### User Experience Goals
- Time to first task: < 2 minutes
- Skill activation accuracy: > 90%
- User satisfaction: > 4/5
- Zero learning curve for Cursor users

## 🔄 Current Status

### Completed
- [✅] Initial project setup
- [✅] PLAN.md created with full PRD
- [✅] Task list (TASKS.md) initialized
- [✅] skill-creator Skill installed
- [✅] Project structure created

### In Progress
- [🔄] Task 001: fstrent-task-management Skill
- [ ] Task 002: fstrent-planning Skill
- [ ] Task 003: fstrent-qa Skill

### Upcoming
- Phase 2: Commands & Agents
- Phase 3: Documentation & Examples
- Phase 4: Polish & Release

## 🛡️ Scope Boundaries

### In Scope
- Claude Code Skills for task management
- Claude Code Commands for quick operations
- Claude Code Subagents for complex workflows
- Shared `.fstrent_spec_tasks/` data files
- Documentation for both IDEs
- MCP tool compatibility

### Out of Scope
- Modifying Cursor's existing rules system
- Creating new task management features
- Supporting IDEs other than Cursor and Claude Code
- Cloud sync or collaboration features
- Real-time multi-user editing
- GUI or web interface

### Approved Complexity
- **File-based storage**: Simple, no database
- **Local-only**: No cloud services
- **Git-based collaboration**: Standard version control
- **Progressive disclosure**: Skills load content as needed
- **Natural language**: No special syntax required

## 🎨 Architecture Principles

### Cross-IDE Compatibility
- **Shared Data Layer**: `.fstrent_spec_tasks/` files work in both IDEs
- **IDE-Specific Interfaces**: Cursor uses rules, Claude Code uses Skills
- **Same Templates**: Identical YAML and markdown formats
- **Unified MCP**: Shared `.mcp.json` configuration

### Progressive Disclosure
1. **Metadata**: Skill name + description (always loaded)
2. **SKILL.md**: Full instructions (loaded when triggered)
3. **References**: Detailed docs (loaded as needed)
4. **Scripts**: Executable code (executed without loading)

### Design Philosophy
- **Simplicity First**: File-based, no complex infrastructure
- **Natural Interaction**: Conversational, not command-driven
- **Zero Friction**: Works with existing projects
- **Team Friendly**: Multiple IDE support

## 📊 Key Metrics

### Technical Metrics
- File format compatibility: Target 100%
- Skill activation accuracy: Target > 90%
- Data corruption incidents: Target 0
- MCP tool compatibility: Target 100%

### User Metrics
- Time to create first task: Target < 2 minutes
- Task creation success rate: Target > 95%
- User satisfaction: Target > 4/5
- Cross-IDE workflow rating: Target > 4/5

## 🔗 Integration Points

### Anthropic Systems
- Skills API and specification
- Claude Code IDE
- Official Skills repository: https://github.com/anthropics/skills

### Existing Systems
- Cursor IDE and rules system
- fstrent_mcp_tasks MCP server
- Git version control
- File system

### Shared Resources
- `.fstrent_spec_tasks/` folder structure
- `.mcp.json` configuration
- Task and plan templates
- Documentation standards

## 📚 Reference Links

### Official Documentation
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skill Creator](https://github.com/anthropics/skills/tree/main/skill-creator)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/quickstart)
- [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### Internal Documentation
- `.cursor/rules/fstrent_spec_tasks/` - Cursor rules reference
- `PLAN.md` - Full PRD
- `TASKS.md` - Task list
- `docs/SETUP_SUMMARY.md` - Initial setup documentation

## 🚀 Next Steps

### Immediate (This Week)
1. Complete Task 001: fstrent-task-management Skill
2. Complete Task 002: fstrent-planning Skill
3. Complete Task 003: fstrent-qa Skill
4. Test Skills with sample project

### Short Term (Next Week)
1. Create custom commands
2. Create task-expander subagent
3. Integration testing
4. Begin documentation

### Long Term (Weeks 3-4)
1. Complete all documentation
2. Create example projects
3. Video tutorials (optional)
4. Community release

---

**Last Updated**: 2025-10-19
**Project Status**: Active Development
**Current Phase**: Phase 1 - Core Skills Development

