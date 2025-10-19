---
id: 004
title: 'Add reference materials to Skills'
type: feature
status: completed
priority: high
feature: Claude Code Skills
subsystems: [skills_system, documentation]
project_context: 'Enhance Skills with reference documentation similar to mcp-builder pattern, providing comprehensive guidance and templates'
dependencies: [001, 002, 003]
---

# Task 004: Add Reference Materials to Skills

## Objective
Add `reference/` folders to each of the three core Skills, containing comprehensive documentation, templates, and cross-IDE compatibility information. This follows the pattern established by Anthropic's mcp-builder Skill.

## Background
Analysis of Anthropic's Skills reveals that complex Skills include `reference/` folders with detailed documentation that supports the main SKILL.md. Our Skills are comprehensive (15,500 words total) but could benefit from structured reference materials.

## Acceptance Criteria
- [ ] Create `reference/` folder in each Skill directory
- [ ] Add Cursor rules reference for comparison
- [ ] Add YAML schema documentation
- [ ] Add template examples
- [ ] Add cross-IDE compatibility matrix
- [ ] Reference materials are properly linked from SKILL.md
- [ ] Documentation is clear and comprehensive

## Implementation Plan

### For fstrent-task-management/reference/
1. **cursor_rules_comparison.md**
   - Side-by-side comparison of Cursor rules vs Claude Skill
   - Migration guide from Cursor to Claude Code
   - Feature parity matrix

2. **yaml_schema.md**
   - Complete YAML frontmatter specification
   - Field descriptions and constraints
   - Validation rules
   - Examples for each task type

3. **task_templates.md**
   - Template for feature tasks
   - Template for bug_fix tasks
   - Template for retroactive_fix tasks
   - Template for sub-tasks

4. **windows_emoji_guide.md**
   - Windows-safe emoji reference
   - Status indicators
   - Why certain emojis are used

### For fstrent-planning/reference/
1. **cursor_rules_comparison.md**
   - Planning rules comparison
   - PRD structure alignment
   - Feature management differences

2. **prd_template.md**
   - Complete 10-section PRD template
   - Detailed field descriptions
   - Best practices for each section

3. **planning_questionnaire.md**
   - Full 27-question framework
   - Question categorization
   - How to use responses

4. **scope_validation.md**
   - 5 essential questions detailed
   - Over-engineering prevention strategies
   - Decision trees for complexity

### For fstrent-qa/reference/
1. **cursor_rules_comparison.md**
   - QA rules comparison
   - Bug tracking differences
   - Quality workflow alignment

2. **bug_classification.md**
   - Severity level definitions
   - Source attribution guidelines
   - Status lifecycle detailed

3. **retroactive_documentation.md**
   - When to document fixes
   - Scope assessment criteria
   - Template usage guide

4. **quality_metrics.md**
   - Metric definitions
   - How to calculate
   - Interpretation guidelines

## File Structure
```
.claude/skills/
├── fstrent-task-management/
│   ├── SKILL.md
│   └── reference/
│       ├── cursor_rules_comparison.md
│       ├── yaml_schema.md
│       ├── task_templates.md
│       └── windows_emoji_guide.md
├── fstrent-planning/
│   ├── SKILL.md
│   └── reference/
│       ├── cursor_rules_comparison.md
│       ├── prd_template.md
│       ├── planning_questionnaire.md
│       └── scope_validation.md
└── fstrent-qa/
    ├── SKILL.md
    └── reference/
        ├── cursor_rules_comparison.md
        ├── bug_classification.md
        ├── retroactive_documentation.md
        └── quality_metrics.md
```

## Testing Plan
1. Verify all reference files are created
2. Check links from SKILL.md to reference files
3. Validate markdown formatting
4. Ensure examples are accurate
5. Test that Claude can access and use reference materials

## Resource Requirements
- Access to `.cursor/rules/fstrent_spec_tasks/` for comparison
- Cursor rules documentation
- YAML specification knowledge

## Success Metrics
- All reference folders created with complete documentation
- Skills can reference detailed information when needed
- Users can find comprehensive guidance
- Cross-IDE compatibility is clearly documented

## Notes
- Reference materials should be concise but comprehensive
- Focus on practical guidance, not theory
- Include examples for every concept
- Maintain consistency across all three Skills

