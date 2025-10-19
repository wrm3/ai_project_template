---
id: 018
title: 'Add rules.md files to Claude Code Skills'
type: enhancement
status: completed
priority: medium
feature: Claude Code Skills
subsystems: [claude_skills, cross_ide_compatibility]
project_context: 'Enhance Claude Code Skills with rules.md files for potential progressive disclosure, based on Anthropic Skills pattern observed in video'
dependencies: [001, 002, 003]
created_date: '2025-10-19'
estimated_effort: '2 hours'
---

# Task 018: Add rules.md Files to Claude Code Skills

## Objective
Add `rules.md` files to each Claude Code Skill folder, containing detailed implementation rules derived from Cursor rules, while keeping existing SKILL.md files unchanged.

## Background

### Discovery
User observed in Anthropic Skills video that Skills can have `rules.md` files in addition to `SKILL.md`. This pattern may provide:
- Progressive disclosure (load rules.md only when needed)
- Better separation of concerns (overview vs detailed rules)
- Consistency with potential Anthropic standard

### Current Structure
```
.claude/skills/fstrent-task-management/
├── SKILL.md (4,800 words - complete, standalone)
├── reference/ (4 files)
└── examples/ (5 files)
```

### Proposed Structure
```
.claude/skills/fstrent-task-management/
├── SKILL.md (4,800 words - unchanged)
├── rules.md (NEW - detailed implementation rules)
├── reference/ (4 files)
└── examples/ (5 files)
```

## Strategy: Additive Enhancement

**Key Principle**: Add rules.md WITHOUT modifying SKILL.md

### Benefits
1. **No Breaking Changes**: SKILL.md still complete and working
2. **Future-Proof**: Ready if rules.md becomes standard
3. **Cross-IDE Consistency**: Rules from Cursor preserved
4. **Progressive Disclosure**: Claude can load rules.md when needed
5. **Safe**: If rules.md not used, SKILL.md still works

### Content Source
Extract detailed rules from Cursor `.mdc` files:
- `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc` → fstrent-task-management/rules.md
- `.cursor/rules/fstrent_spec_tasks/rules/plans.mdc` → fstrent-planning/rules.md
- `.cursor/rules/fstrent_spec_tasks/rules/qa.mdc` → fstrent-qa/rules.md

## Implementation Plan

### Phase 1: Preparation
- [x] Create this task
- [x] Initialize Git repository
- [x] Make initial commit (before changes)
- [ ] Create comparison document (already done: docs/EXAMPLE_RULES_MD_COMPARISON.md)

### Phase 2: Create rules.md Files
- [ ] Create `.claude/skills/fstrent-task-management/rules.md`
  - Extract from Cursor rules.mdc
  - Format for Claude Code
  - Add cross-reference to SKILL.md
  
- [ ] Create `.claude/skills/fstrent-planning/rules.md`
  - Extract from Cursor plans.mdc
  - Format for Claude Code
  - Add cross-reference to SKILL.md
  
- [ ] Create `.claude/skills/fstrent-qa/rules.md`
  - Extract from Cursor qa.mdc
  - Format for Claude Code
  - Add cross-reference to SKILL.md

### Phase 3: Verification
- [ ] Verify SKILL.md files unchanged
- [ ] Test in Claude Code (if available)
- [ ] Test in Cursor (ensure no breakage)
- [ ] Update documentation

### Phase 4: Documentation
- [ ] Update CLAUDE_CODE_SETUP_GUIDE.md
- [ ] Update README.md (mention rules.md)
- [ ] Update CHANGELOG.md
- [ ] Commit changes

## rules.md File Structure

### Template
```markdown
# [Skill Name] Rules

> Detailed implementation rules for the [skill-name] Skill.
> These rules are derived from Cursor's fstrent_spec_tasks system
> and maintain 100% cross-IDE compatibility.

## Overview
[Brief description of what these rules cover]

## Core Rules
[Fundamental rules and principles]

## [Specific Topic] Rules
[Detailed rules for specific aspects]

## Integration with Cursor
These rules maintain compatibility with Cursor's rules system.
See `.cursor/rules/fstrent_spec_tasks/rules/[file].mdc` for source.

## Cross-References
- Main Skill: `SKILL.md`
- Reference Materials: `reference/`
- Examples: `examples/`
```

## Content for Each rules.md

### fstrent-task-management/rules.md
**Source**: `.cursor/rules/fstrent_spec_tasks/rules/rules.mdc`

**Sections**:
1. Task File Format Rules
2. YAML Frontmatter Validation
3. File Naming Conventions
4. Status Management Rules
5. Windows Emoji Requirements
6. Task ID Assignment
7. TASKS.md Update Procedures
8. Sub-Task Creation Rules
9. Dependency Management
10. Error Handling

### fstrent-planning/rules.md
**Source**: `.cursor/rules/fstrent_spec_tasks/rules/plans.mdc`

**Sections**:
1. PRD Structure Requirements
2. Planning Questionnaire Rules
3. Scope Validation Criteria
4. Feature Document Format
5. User Story Format
6. Acceptance Criteria Rules
7. Technical Considerations
8. Milestone Planning
9. Over-Engineering Prevention
10. Integration with Tasks

### fstrent-qa/rules.md
**Source**: `.cursor/rules/fstrent_spec_tasks/rules/qa.mdc`

**Sections**:
1. Bug Classification Rules
2. Severity Determination
3. Bug Tracking Workflow
4. Quality Metrics Calculations
5. Retroactive Documentation Rules
6. Bug-to-Task Relationships
7. Resolution Tracking
8. Quality Gates
9. Testing Standards
10. Integration with Tasks

## Acceptance Criteria

- [ ] Three rules.md files created (one per Skill)
- [ ] Content extracted from Cursor rules
- [ ] Formatted for Claude Code
- [ ] SKILL.md files unchanged
- [ ] Cross-references added
- [ ] Git commit made before changes
- [ ] Git commit made after changes
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Works in both IDEs

## Testing Plan

### Before Changes
1. Verify current Skills work in Claude Code
2. Verify current rules work in Cursor
3. Make Git commit

### After Changes
1. Verify Skills still work in Claude Code
2. Verify rules still work in Cursor
3. Check if rules.md are loaded (if possible)
4. Test task creation in both IDEs
5. Verify cross-IDE compatibility maintained

## Risks & Mitigation

### Risk 1: Breaking Changes
**Mitigation**: Keep SKILL.md unchanged, only add files

### Risk 2: Duplication Issues
**Mitigation**: Clearly document which file is authoritative (both are)

### Risk 3: rules.md Not Standard
**Mitigation**: Additive approach means no harm if not used

### Risk 4: Maintenance Burden
**Mitigation**: Rules are stable, unlikely to change frequently

## Success Metrics

- Skills continue working in both IDEs
- No user-facing changes (unless rules.md improves behavior)
- Documentation updated
- Git history clean
- Cross-IDE compatibility maintained

## Notes

### Research Questions
- Is rules.md an official Anthropic pattern?
- Does Claude Code use rules.md?
- What's the loading order (SKILL.md then rules.md)?

### Future Considerations
- If rules.md proves valuable, consider refactoring SKILL.md
- If rules.md not used, consider removing
- Monitor Anthropic documentation for official guidance

## Related Files

- Comparison: `docs/EXAMPLE_RULES_MD_COMPARISON.md`
- Cursor Rules: `.cursor/rules/fstrent_spec_tasks/rules/*.mdc`
- Skills: `.claude/skills/*/SKILL.md`

## Timeline

**Estimated**: 2 hours
- Preparation: 15 minutes (Git setup)
- Create rules.md: 1 hour (3 files)
- Testing: 30 minutes
- Documentation: 15 minutes

**Target Completion**: 2025-10-19

