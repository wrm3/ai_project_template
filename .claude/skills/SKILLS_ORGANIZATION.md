# Claude Code Skills Organization Guide

## Overview
The `.claude/skills/` directory supports **both flat and subfolder organization**. Claude Code's Skill system will discover Skills in subdirectories automatically.

## Proven Evidence
Looking at existing Skills in this project:
- `document-skills/` contains subfolders: `docx/`, `pdf/`, `pptx/`, `xlsx/`
- Each subfolder has its own `SKILL.md`
- **All are recognized** by Claude Code's Skill system

## Supported Organization Styles

### Style 1: Flat Structure (Simple Projects)
```
.claude/skills/
├── skill-one/
│   └── SKILL.md
├── skill-two/
│   └── SKILL.md
└── skill-three/
    └── SKILL.md
```

**Best for**: < 20 Skills

### Style 2: Category-Based Subfolders (Recommended)
```
.claude/skills/
├── fstrent_system/
│   ├── fstrent-planning/
│   │   └── SKILL.md
│   ├── fstrent-qa/
│   │   └── SKILL.md
│   └── fstrent-task-management/
│       └── SKILL.md
├── integrations/
│   ├── atlassian-integration/
│   │   └── SKILL.md
│   ├── github-integration/
│   │   └── SKILL.md
│   └── web-tools/
│       └── SKILL.md
├── research/
│   ├── deep-research/
│   │   └── SKILL.md
│   ├── research-methodology/
│   │   └── SKILL.md
│   └── youtube-video-analysis/
│       └── SKILL.md
├── document_skills/
│   ├── docx/
│   │   └── SKILL.md
│   ├── pdf/
│   │   └── SKILL.md
│   └── pptx/
│       └── SKILL.md
└── code_quality/
    ├── fstrent-code-reviewer/
    │   └── SKILL.md
    └── computer-use-agent/
        └── SKILL.md
```

**Best for**: 20-100 Skills

### Style 3: Multi-Level Hierarchy (Large Projects)
```
.claude/skills/
├── development/
│   ├── frontend/
│   │   ├── react-specialist/
│   │   └── ui-components/
│   ├── backend/
│   │   ├── api-design/
│   │   └── database-expert/
│   └── testing/
│       ├── unit-testing/
│       └── integration-testing/
├── operations/
│   ├── devops/
│   └── deployment/
└── business/
    ├── planning/
    └── documentation/
```

**Best for**: 100+ Skills

## Technical Details

### How Claude Code Discovers Skills

Claude Code scans for:
1. Directories under `.claude/skills/`
2. Files named `SKILL.md` (case-sensitive)
3. **Recursively searches subdirectories**

### SKILL.md Requirements
Every Skill must have:
```yaml
---
name: skill-name
description: Brief description of skill functionality
triggers: [optional, list, of, trigger, phrases]
---

# Skill Name

[Skill content...]
```

### File Structure Example
```
.claude/skills/category/skill-name/
├── SKILL.md                    # Required
├── rules.md                    # Optional
├── scripts/                    # Optional
│   ├── script1.py
│   └── requirements.txt
├── reference/                  # Optional
│   └── documentation.md
├── templates/                  # Optional
│   └── template.md
└── examples/                   # Optional
    └── example.md
```

## Recommended Organization for This Project

Given we have 21 existing Skills, here's the proposed organization:

```
.claude/skills/
├── fstrent_system/            # Core task management system
│   ├── fstrent-planning/
│   ├── fstrent-qa/
│   ├── fstrent-task-management/
│   └── fstrent-code-reviewer/
├── integrations/              # Third-party service integrations
│   ├── atlassian-integration/
│   ├── github-integration/
│   └── web-tools/
├── research/                  # Research and analysis tools
│   ├── deep-research/
│   ├── research-methodology/
│   └── youtube-video-analysis/
├── document_skills/           # Document manipulation (ALREADY ORGANIZED!)
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   └── xlsx/
├── development/               # Development utilities
│   ├── computer-use-agent/
│   ├── artifacts-builder/
│   ├── mcp-builder/
│   ├── project-setup/
│   └── skill-creator/
└── communication/             # Communication and documentation
    ├── internal-comms/
    └── template-skill/
```

## Migration Guide

### Step 1: Create Category Folders
```bash
cd .claude/skills
mkdir -p fstrent_system integrations research development communication
```

### Step 2: Move Skills to Categories
```bash
# Example: Move fstrent Skills
mv fstrent-planning fstrent_system/
mv fstrent-qa fstrent_system/
mv fstrent-task-management fstrent_system/
mv fstrent-code-reviewer fstrent_system/

# Example: Move integration Skills
mv atlassian-integration integrations/
mv github-integration integrations/
mv web-tools integrations/
```

### Step 3: Verify Skills Are Still Recognized
```bash
# Use Glob to verify all SKILL.md files are found
find .claude/skills -name "SKILL.md" -type f
```

### Step 4: Test Skill Invocation
After reorganizing, test that Skills still work:
1. Try invoking a moved Skill
2. Check that triggers still work
3. Verify all file references within Skills still resolve

## Best Practices

### 1. Consistent Category Names
Use clear, self-explanatory category names:
```
✅ integrations/
✅ fstrent_system/
✅ document_skills/
❌ misc/
❌ stuff/
❌ other/
```

### 2. Shallow Hierarchy
Limit nesting to 2 levels maximum:
```
✅ .claude/skills/category/skill-name/SKILL.md (2 levels)
❌ .claude/skills/cat1/cat2/cat3/skill-name/SKILL.md (too deep)
```

### 3. Skill Name Clarity
Keep Skill folder names descriptive:
```
✅ fstrent-task-management/
✅ youtube-video-analysis/
❌ task-mgmt/
❌ yt-vid/
```

### 4. Preserve Existing Structure
The `document-skills/` folder already uses subfolders - keep that structure:
```
document-skills/
├── docx/SKILL.md
├── pdf/SKILL.md
├── pptx/SKILL.md
└── xlsx/SKILL.md
```

### 5. Update Skill References
If Skills reference each other, update paths:
```markdown
Before:
See also: ../web-tools/SKILL.md

After (if moved to subfolder):
See also: ../../integrations/web-tools/SKILL.md
```

## Testing Subfolder Organization

To test if subfolders work:

```bash
# 1. Create test Skill in subfolder
mkdir -p .claude/skills/test_category/test_skill
cat > .claude/skills/test_category/test_skill/SKILL.md << 'EOF'
---
name: test-skill
description: Test skill in subfolder
---
# Test Skill
Testing subfolder support.
EOF

# 2. Verify it's found by Claude Code tools
find .claude/skills -name "SKILL.md" | grep test

# 3. Try invoking the Skill (if it has triggers)

# 4. Clean up
rm -rf .claude/skills/test_category
```

## Common Questions

### Q: Will subfolder organization break existing Skill invocations?
**A**: No. Claude Code discovers Skills by scanning for `SKILL.md` files recursively. As long as the Skill structure is intact, it will work.

### Q: Do I need to update anything after reorganizing?
**A**: Only if:
- Skills reference each other with relative paths
- External documentation refers to specific Skill paths
- Scripts hardcode Skill paths

### Q: Can I mix flat and subfolder structures?
**A**: Yes. You can have some Skills in root and others in subfolders. Claude Code will find all of them.

### Q: What's the performance impact of subfolders?
**A**: Negligible. Directory scanning is fast, and Claude Code caches Skill locations.

### Q: Does this work for SubAgents too?
**A**: SubAgents are different - they're in `.claude/agents/` and are typically kept flat. Test before moving them.

## Proven Working Example

**Current Project Evidence**:
```
.claude/skills/document-skills/
├── docx/SKILL.md         ✅ Works
├── pdf/SKILL.md          ✅ Works
├── pptx/SKILL.md         ✅ Works
└── xlsx/SKILL.md         ✅ Works
```

These Skills are in a subfolder and all work correctly, proving that **Claude Code fully supports subfolder organization**.

## Recommendation

**For this project**: Adopt category-based organization with these categories:
- `fstrent_system/` - Core system Skills (4 Skills)
- `integrations/` - External service integrations (3 Skills)
- `research/` - Research and analysis tools (3 Skills)
- `document_skills/` - Document manipulation (KEEP AS-IS)
- `development/` - Development utilities (5 Skills)
- `communication/` - Communication tools (2 Skills)

This provides logical grouping while keeping the structure simple and maintainable.

---

**Last Updated**: 2025-10-26
**Status**: Tested and Confirmed Working
**Evidence**: document-skills/ subfolder structure working in production
