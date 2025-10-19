# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Plugin marketplace distribution
- Additional IDE support (Windsurf, Roo-Code)
- Enhanced task templates
- Time tracking integration
- Gantt chart visualization

## [0.1.0] - 2025-10-19

### Added
- **Core Task Management System**
  - Task creation, update, and tracking
  - Task status management (Pending, In Progress, Completed, Cancelled)
  - Priority levels (Critical, High, Medium, Low)
  - Task dependencies and sub-tasks
  - Automatic task complexity assessment

- **Project Planning**
  - Product Requirements Document (PRD) templates
  - Feature specification system
  - User stories and acceptance criteria
  - Project context and scope management
  - 27-question planning framework

- **Bug Tracking**
  - Centralized bug tracking in BUGS.md
  - Severity classification (Critical, High, Medium, Low)
  - Bug-to-task relationships
  - Resolution tracking
  - Quality metrics

- **Cross-IDE Compatibility**
  - Full support for Claude Code
    - 3 comprehensive Skills (task-management, planning, qa)
    - 7 custom commands
    - 1 intelligent agent (task-expander)
  - Full support for Cursor
    - 4 rule files (.mdc format)
    - 4 custom commands
    - Progressive rule disclosure
  - Shared data layer (.fstrent_spec_tasks/)
  - Zero duplication between IDEs

- **Documentation**
  - Claude Code Setup Guide (4,200 words)
  - Cursor Compatibility Guide (8,200 words)
  - Troubleshooting Guide (11,500 words)
  - Main README (7,800 words)
  - Contributing guidelines
  - Code of Conduct

- **Example Project**
  - Complete TaskFlow web application
  - Flask backend (200 lines)
  - Sample PRD (4,800 words)
  - 16 sample tasks
  - 4 sample bugs
  - 3 feature specifications
  - Working demonstration of all features

- **GitHub Integration**
  - MIT License
  - Contributing guidelines
  - Code of Conduct
  - Issue templates
  - Pull request template
  - Changelog

### Technical Details
- **Languages**: Markdown, YAML, Python (example)
- **IDEs Supported**: Claude Code, Cursor
- **File Format**: Markdown with YAML frontmatter
- **Version Control**: Git-friendly
- **License**: MIT

### Statistics
- **Documentation**: 55,300+ words
- **Files**: 50+ files
- **Example Code**: 200+ lines
- **Skills**: 3 Claude Code Skills
- **Commands**: 11 total commands
- **Agents**: 1 intelligent agent

## [0.0.1] - 2025-10-01

### Added
- Initial project structure
- Basic task management concept
- Cursor rules prototype

---

## Version History

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards-compatible)
- **PATCH** version for backwards-compatible bug fixes

### Release Types

- **Major Release** (1.0.0, 2.0.0): Significant new features, breaking changes
- **Minor Release** (0.1.0, 0.2.0): New features, no breaking changes
- **Patch Release** (0.1.1, 0.1.2): Bug fixes, minor improvements

### Changelog Categories

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

---

## Upgrade Guide

### From 0.0.1 to 0.1.0

**Breaking Changes**: None (initial release)

**New Features**:
- Complete task management system
- Project planning framework
- Bug tracking
- Cross-IDE compatibility
- Comprehensive documentation
- Example project

**Migration Steps**:
1. No migration needed (initial release)
2. Follow installation instructions in README.md

---

## Future Roadmap

### v0.2.0 (Next Release)
- Plugin marketplace distribution
- Additional IDE support (Windsurf, Roo-Code)
- Enhanced task templates
- Time tracking integration
- Gantt chart visualization

### v1.0.0 (Stable Release)
- Web dashboard (optional)
- API for external integrations
- Advanced reporting
- Team analytics
- Mobile app (view-only)

### v2.0.0 (Major Update)
- Real-time collaboration
- Cloud synchronization
- Advanced AI features
- Enterprise features

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-username/fstrent-spec-tasks-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/fstrent-spec-tasks-toolkit/discussions)

---

**Note**: This changelog is maintained manually. For detailed commit history, see [GitHub commits](https://github.com/your-username/fstrent-spec-tasks-toolkit/commits/main).

