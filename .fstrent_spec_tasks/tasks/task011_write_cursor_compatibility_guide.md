---
id: 011
title: 'Write Cursor compatibility guide'
type: documentation
status: completed
priority: high
feature: Documentation
subsystems: [documentation, cross_ide_compatibility]
project_context: 'Explain how fstrent_spec_tasks works seamlessly across both Claude Code and Cursor with shared files'
dependencies: [001, 002, 003, 009, 010]
---

# Task 011: Write Cursor Compatibility Guide

## Objective
Create a comprehensive guide explaining how `fstrent_spec_tasks` achieves 100% compatibility between Claude Code and Cursor, enabling seamless cross-IDE workflows and team collaboration.

## Background
Our integration testing (Task 009) confirmed 100% cross-IDE compatibility. Users need to understand:
- How the system works in both IDEs
- What's shared vs IDE-specific
- How to switch between IDEs
- Team collaboration workflows
- Best practices

## Guide Structure

### 1. Overview
- What cross-IDE compatibility means
- Benefits for individuals and teams
- Architecture overview

### 2. How It Works
- Shared directory (`.fstrent_spec_tasks/`)
- IDE-specific features
- File format compatibility
- No conflicts

### 3. Using Both IDEs
- Installing in both
- Switching between IDEs
- Concurrent usage
- File synchronization

### 4. Team Collaboration
- Git-based workflows
- Coordinating edits
- Best practices
- Common scenarios

### 5. Feature Comparison
- What works in both
- Claude Code specific
- Cursor specific
- Choosing the right IDE

## Acceptance Criteria

- [ ] Guide created in `docs/CURSOR_COMPATIBILITY_GUIDE.md`
- [ ] Architecture explanation clear
- [ ] Shared vs IDE-specific documented
- [ ] Installation for both IDEs covered
- [ ] Team workflows documented
- [ ] Feature comparison table included
- [ ] Best practices provided
- [ ] Examples for common scenarios
- [ ] Troubleshooting section
- [ ] Clear, accessible language

## Success Metrics

- Users understand cross-IDE compatibility
- Teams can collaborate effectively
- No confusion about what's shared
- Clear guidance on IDE choice
- Common scenarios addressed

## Notes

- Emphasize the benefits
- Show concrete examples
- Address team concerns
- Highlight flexibility
- Keep it practical

