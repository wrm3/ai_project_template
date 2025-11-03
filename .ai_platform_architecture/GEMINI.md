# Gemini Architecture

**Last Updated**: 2025-10-28
**Official Website**: https://ai.google.dev/gemini-api
**Gemini CLI**: https://google-gemini.github.io/gemini-cli/
**Version Documented**: Gemini CLI + Gemini Code Assist (VSCode Extension)
**Status**: ✅ Documented (Multiple Systems)

## Overview

Google's Gemini has **multiple AI coding systems**, not just one:

1. **Gemini CLI** - Command-line interface for terminal-based development
2. **Gemini Code Assist** - VSCode extension for IDE integration
3. **Gemini in Google Cloud** - GitHub integration for code reviews

Each system has different configuration approaches and file structures.

### Critical Insight: Hierarchical Context System

**Unique Feature**: Gemini uses `GEMINI.md` files in a **hierarchical cascade** - unlike other platforms that load a single rule file, Gemini loads context files sequentially from root → subdirectories, allowing progressive instruction refinement.

## System 1: Gemini CLI (Command-Line Interface)

### Directory Structure

```
project-root/
├── .gemini/                     # Project configuration root
│   ├── GEMINI.md               # Project-level instructions
│   ├── settings.json           # CLI configuration
│   ├── config.yaml             # Feature toggles, ignore patterns
│   └── styleguide.md           # Custom style guides
├── src/
│   ├── GEMINI.md               # Source-specific instructions
│   ├── models/
│   │   └── GEMINI.md           # Models-specific instructions
│   └── views/
│       └── GEMINI.md           # Views-specific instructions
├── tests/
│   └── GEMINI.md               # Test-specific instructions
└── docs/
    └── GEMINI.md               # Documentation-specific instructions

# Global configuration
~/.gemini/
└── GEMINI.md                   # Global default instructions
```

### GEMINI.md Hierarchical Loading

**Loading Order** (Sequential Cascade):
1. **Global**: `~/.gemini/GEMINI.md` (user home directory)
2. **Project Root**: `project-root/GEMINI.md` (or nearest `.git` ancestor)
3. **Current Directory**: Working directory's `GEMINI.md`
4. **Subdirectories**: Alphabetically by subdirectory name

**Key Principle**: Instructions cascade from general → specific
- Higher-level files: General guidelines
- Lower-level files: Specific directives that can override

**Example Cascade**:
```
~/.gemini/GEMINI.md:
  "Always use TypeScript for type safety"

project-root/GEMINI.md:
  "This project uses React with functional components"

src/GEMINI.md:
  "Follow company coding standards for all source files"

src/components/GEMINI.md:
  "Components must have prop types and JSDoc comments"
```

When working in `src/components/`, ALL four files are loaded in order, building cumulative context.

### GEMINI.md File Format

**Standard Format**:
```markdown
# Project Instructions

## Overview
[Project context and goals]

## Coding Standards
- [Standard 1]
- [Standard 2]

## File Organization
[How files are organized]

## Common Commands
[Frequently used commands]

## Best Practices
[Project-specific best practices]
```

**Advanced Format** (with personas):
```markdown
# Development Instructions

## Persona
You are a senior TypeScript developer specializing in React applications.

## Context
This project is a React TypeScript application using:
- React 18
- TypeScript 5
- Vite for bundling
- Vitest for testing

## Coding Style
- Use functional components with hooks
- Prefer const over let
- Use explicit types, avoid 'any'
- Write comprehensive JSDoc comments

## Testing Requirements
- Unit tests for all business logic
- Integration tests for API calls
- Component tests using React Testing Library

## File Naming
- Components: PascalCase (Button.tsx)
- Utilities: camelCase (formatDate.ts)
- Tests: *.test.ts or *.spec.ts
```

### Configuration Files

#### settings.json

**Location**: `.gemini/settings.json`

**Format**:
```json
{
  "contextFiles": ["GEMINI.md"],
  "overrideDefaultUrl": {
    "/custom": "https://custom.endpoint.com"
  },
  "respectGitIgnore": true,
  "recursiveFileSearch": true,
  "maxContextFiles": 50,
  "filePatterns": {
    "include": ["src/**/*.ts", "src/**/*.tsx"],
    "exclude": ["**/*.test.ts", "**/node_modules/**"]
  }
}
```

**Key Settings**:
- `contextFiles`: Array of context file names (default: ["GEMINI.md"])
- `respectGitIgnore`: Honor .gitignore patterns (default: true)
- `recursiveFileSearch`: Search subdirectories (default: true)
- `maxContextFiles`: Maximum GEMINI.md files to load

#### config.yaml

**Location**: `.gemini/config.yaml`

**Format**:
```yaml
# Feature toggles
features:
  autoComplete: true
  codeReview: true
  refactoring: true
  testing: true

# File patterns to ignore
ignore:
  - "**/*.log"
  - "**/.git/**"
  - "**/node_modules/**"
  - "**/dist/**"
  - "**/build/**"

# Custom settings
settings:
  language: "typescript"
  framework: "react"
  testFramework: "vitest"
```

#### styleguide.md

**Location**: `.gemini/styleguide.md`

**Purpose**: Custom style guides for code reviews

**Format**:
```markdown
# Project Style Guide

## TypeScript Standards
- Use explicit return types for functions
- Prefer interfaces over type aliases for objects
- Use enums for string constants

## React Standards
- Use functional components only
- Use hooks for state management
- Avoid inline styles, use CSS modules

## Testing Standards
- Write tests before implementation (TDD)
- Aim for 80%+ code coverage
- Test behavior, not implementation

## Documentation Standards
- JSDoc for all public functions
- README.md in each major directory
- Inline comments for complex logic
```

### Monorepo Structure

**Gemini CLI Internal Structure** (for reference):
```
gemini-cli/
├── packages/
│   ├── cli/                   # Command-line interface
│   │   ├── src/
│   │   └── package.json
│   ├── core/                  # Core functionality
│   │   ├── src/
│   │   └── package.json
│   ├── tools/                 # Built-in tools
│   │   ├── src/
│   │   └── package.json
│   └── extensions/            # Extension system
│       ├── src/
│       └── package.json
├── lerna.json
└── package.json
```

**Key Packages**:
1. **CLI Package**: Command parsing, user interaction
2. **Core Package**: API client, state management
3. **Tools Package**: File system operations, shell commands
4. **Extensions Package**: Plugin loading, lifecycle management

### File System Tools

#### search_file_content Tool

**Purpose**: Search for patterns in files using regex

**Usage**:
```bash
# In Gemini CLI
/search "pattern" --directory src/ --glob "*.ts"

# Result format
src/utils/helper.ts:45: matching line content
src/models/user.ts:12: matching line content
```

**Features**:
- Regular expression support
- Glob pattern filtering
- Line number reporting
- File path context

#### replace Tool

**Purpose**: Precise text replacement with context awareness

**Usage**:
```bash
# In Gemini CLI
/replace --file src/app.ts --old "oldText" --new "newText" --context 3
```

**Features**:
- Multi-occurrence support
- Context-aware (requires surrounding lines for accuracy)
- Dry-run mode
- Multi-stage edit corrections

### Multi-Directory Workspace Support

**Command-Line Argument**:
```bash
gemini-cli --include-directories /path/to/dir1,/path/to/dir2
```

**Slash Commands**:
```bash
# Add directory to workspace
/directory add /path/to/additional/code

# Show all directories
/directory show

# Remove directory
/directory remove /path/to/code
```

**Use Case**: Projects with files spread across multiple locations
- Microservices in different repos
- Shared libraries in separate directories
- Related projects needing joint context

## System 2: Gemini Code Assist (VSCode Extension)

### Directory Structure

```
project-root/
├── .gemini/                     # Gemini configuration
│   ├── config.yaml             # Extension settings
│   └── styleguide.md           # Code review guidelines
├── .vscode/
│   └── settings.json           # VSCode settings (may include Gemini)
├── src/                        # Source code
└── tests/                      # Test files
```

### VSCode Extension Configuration

**Location**: `.vscode/settings.json` or `.gemini/config.yaml`

**Example**:
```json
{
  "gemini.enabled": true,
  "gemini.model": "gemini-1.5-pro",
  "gemini.codeReview": {
    "enabled": true,
    "autoTrigger": true,
    "styleguide": ".gemini/styleguide.md"
  },
  "gemini.autoComplete": {
    "enabled": true,
    "maxSuggestions": 3
  },
  "gemini.contextFiles": [
    ".gemini/styleguide.md",
    "GEMINI.md"
  ]
}
```

### Features

1. **Code Completion**: AI-powered suggestions
2. **Code Review**: Automated review based on styleguide.md
3. **Refactoring**: Intelligent code refactoring
4. **Documentation**: Auto-generate JSDoc comments
5. **Testing**: Generate test cases

### Integration with GEMINI.md

Gemini Code Assist **can** read `GEMINI.md` files (similar to CLI), but configuration is primarily through:
- `.gemini/config.yaml`
- `.gemini/styleguide.md`
- VSCode settings.json

## System 3: Gemini in Google Cloud (GitHub Integration)

### Directory Structure

```
github-repo/
├── .gemini/                     # Gemini Cloud configuration
│   ├── config.yaml             # Feature toggles
│   └── styleguide.md           # Code review guidelines
├── .github/
│   └── workflows/              # GitHub Actions (optional)
└── [project files]
```

### GitHub Integration Configuration

**Location**: `.gemini/config.yaml`

**Format**:
```yaml
# Code review settings
codeReview:
  enabled: true
  autoApprove: false
  requiredApprovals: 2
  checkStyleGuide: true

# Features
features:
  securityScanning: true
  performanceAnalysis: true
  testCoverage: true

# Ignore patterns
ignore:
  - "**/vendor/**"
  - "**/third_party/**"
  - "**/*.min.js"
```

### Code Review with styleguide.md

**Purpose**: Custom rules for automated code reviews in GitHub PRs

**Example**:
```markdown
# Code Review Guidelines

## Security
- No hardcoded credentials
- Use parameterized SQL queries
- Validate all user input

## Performance
- Avoid N+1 queries
- Use caching for expensive operations
- Lazy load large datasets

## Code Quality
- Functions should be < 50 lines
- Cyclomatic complexity < 10
- Test coverage > 80%

## Documentation
- Public APIs must have JSDoc
- README.md for new features
- Changelog entry for breaking changes
```

**GitHub Integration**:
- Gemini scans PRs automatically
- Comments on violations of styleguide.md
- Provides suggestions for improvements
- Can block merges if critical issues found

## File Naming Conventions

### GEMINI.md Files
- **File Name**: `GEMINI.md` (uppercase, exact)
- **Location**: Any directory in project hierarchy
- **Format**: Standard markdown
- **YAML Frontmatter**: Optional (not required like other platforms)

### Configuration Files
- **settings.json**: `.gemini/settings.json`
- **config.yaml**: `.gemini/config.yaml`
- **styleguide.md**: `.gemini/styleguide.md`

## Best Practices

### 1. Hierarchical Context Design

```
✅ Global Instructions (General)
~/.gemini/GEMINI.md:
  - Language preferences
  - Personal coding style
  - Common libraries

✅ Project Instructions (Project-Specific)
project-root/GEMINI.md:
  - Project overview
  - Tech stack
  - Team conventions

✅ Directory Instructions (Domain-Specific)
src/components/GEMINI.md:
  - Component patterns
  - Props conventions
  - Testing requirements

✅ Feature Instructions (Highly Specific)
src/components/auth/GEMINI.md:
  - Authentication patterns
  - Security requirements
  - Error handling
```

### 2. Context File Organization

```
✅ Keep GEMINI.md files focused
✅ Use clear, actionable language
✅ Provide examples where helpful
✅ Update regularly as project evolves
✅ Version control all GEMINI.md files
```

### 3. Multi-System Strategy

**For Teams Using Multiple Gemini Systems**:

```
.gemini/
├── GEMINI.md           # For CLI (hierarchical loading)
├── config.yaml         # For Code Assist + GitHub
├── styleguide.md       # For Code Review (all systems)
└── settings.json       # For CLI (advanced config)
```

**Share common content**:
- `styleguide.md` → Used by all systems
- `GEMINI.md` → Read by CLI and optionally by Code Assist
- `config.yaml` → Shared between Code Assist and GitHub

## Unique Gemini Features

### 1. Hierarchical Context Cascade

**Only Gemini has this**:
- Multiple GEMINI.md files loaded sequentially
- Context builds from general → specific
- Lower-level files override higher-level

**Other platforms**: Single rule file or multiple independent files (no cascade)

### 2. Multiple Systems Integration

**Gemini ecosystem**:
- CLI for terminal development
- VSCode extension for IDE work
- GitHub integration for code review
- Shared configuration across all three

**Other platforms**: Usually single system (IDE or extension)

### 3. Smart File System Tools

**Advanced tools**:
- `search_file_content`: Regex search with glob filtering
- `replace`: Context-aware text replacement with multi-stage corrections
- Multi-directory workspace support

**Other platforms**: Basic file operations

### 4. Styleguide-Driven Code Review

**Automated code review** based on `styleguide.md`:
- Scans PRs automatically
- Enforces custom rules
- Provides inline suggestions
- Can block merges

**Other platforms**: Manual or basic automated review

## Cross-Platform Compatibility

### From Other Platforms to Gemini

#### From Claude Code/Cursor
```bash
# 1. Convert Skills/Rules to GEMINI.md hierarchy

# Claude Code Skills → GEMINI.md
cp .claude/skills/my-skill/SKILL.md project-root/GEMINI.md

# Cursor Rules → GEMINI.md
# Convert .mdc content to GEMINI.md format

# 2. Organize by hierarchy
mkdir -p src/GEMINI.md
# Move specific instructions down

# 3. Create .gemini/ folder
mkdir -p .gemini
# Add config.yaml and styleguide.md

# 4. Test hierarchical loading
gemini-cli # Verify context cascade works
```

#### From agents.md Standard
```bash
# agents.md → GEMINI.md
cp agents.md GEMINI.md

# Add to .gemini/ for Code Assist
mkdir -p .gemini
cp agents.md .gemini/GEMINI.md

# Split into hierarchy if needed
# - General content → project-root/GEMINI.md
# - Specific content → subdirectories
```

### From Gemini to Other Platforms

#### To Claude Code/Cursor
```bash
# 1. Merge hierarchical GEMINI.md files
cat ~/.gemini/GEMINI.md project-root/GEMINI.md src/GEMINI.md > merged_context.md

# 2. Convert to platform format
# For Claude Code:
mkdir -p .claude/skills/project-context
mv merged_context.md .claude/skills/project-context/SKILL.md
# Add YAML frontmatter

# For Cursor:
mv merged_context.md .cursor/rules/project-context.mdc
# Add YAML frontmatter

# 3. Convert styleguide.md
cp .gemini/styleguide.md .claude/skills/styleguide/SKILL.md
# or
cp .gemini/styleguide.md .cursor/rules/styleguide.mdc
```

## Troubleshooting

### GEMINI.md Not Loading

1. ✅ Check file name: Must be exactly `GEMINI.md` (uppercase)
2. ✅ Verify file location: Should be in directory hierarchy
3. ✅ Check settings.json: `contextFiles` array includes "GEMINI.md"
4. ✅ Test hierarchy: Start with root, add subdirectory files incrementally
5. ✅ Restart CLI: `gemini-cli` to reload context

### Context Not Cascading Correctly

1. ✅ Verify loading order: Root → subdirectories alphabetically
2. ✅ Check for conflicts: Lower-level files should override
3. ✅ Test with verbose mode: See what's being loaded
4. ✅ Simplify hierarchy: Start with fewer files, add gradually

### Config.yaml Not Working

1. ✅ Check YAML syntax: Use validator
2. ✅ Verify location: Must be `.gemini/config.yaml`
3. ✅ Restart VSCode: Extension needs to reload config
4. ✅ Check GitHub integration: May need repo admin access

### Multi-Directory Workspace Issues

1. ✅ Verify paths: Use absolute paths
2. ✅ Check permissions: Ensure read access to all directories
3. ✅ Test incrementally: Add one directory at a time
4. ✅ Use `/directory show`: Verify directories are loaded

## Official Resources

- **Gemini API**: https://ai.google.dev/gemini-api
- **Gemini CLI**: https://google-gemini.github.io/gemini-cli/
- **Gemini Code Assist**: https://developers.google.com/gemini-code-assist
- **GitHub**: https://github.com/google-gemini/gemini-cli
- **Documentation**: https://geminicli.cloud/docs/

## Version History

- **2025-10-28**: Initial comprehensive documentation
  - Documented three Gemini systems (CLI, Code Assist, GitHub)
  - Explained hierarchical GEMINI.md cascade
  - Covered configuration files (settings.json, config.yaml, styleguide.md)
  - Documented monorepo structure and file system tools
  - Added multi-directory workspace support
  - Cross-platform migration guides
  - Troubleshooting section

---

**Critical Notes**:
1. **GEMINI.md must be uppercase** - Case-sensitive on Unix systems
2. **Hierarchical loading** - Multiple GEMINI.md files cascade from root → subdirectories
3. **Three systems** - CLI, VSCode extension, GitHub integration
4. **Shared configuration** - styleguide.md and config.yaml used across systems
5. Check Gemini docs quarterly for platform updates

**Unique to Gemini**:
- ✅ Hierarchical context cascade (GEMINI.md files)
- ✅ Multiple integrated systems (CLI + VSCode + GitHub)
- ✅ Advanced file system tools (search, replace)
- ✅ Multi-directory workspace support
- ✅ Styleguide-driven automated code review

