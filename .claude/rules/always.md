# Always-On Guidelines

These rules apply to EVERY conversation and response.

## 1. Response Footer (Not Applicable to Claude Code)

**Note:** Claude Code doesn't support custom response formatting like Cursor.
This guideline is preserved for cross-IDE compatibility but may not apply.

## 2. File Size Management

**CRITICAL: Enforce code refactoring for large files**

### Size Thresholds

**800 lines:**
- Begin suggesting refactoring
- Ask: "This file has over 800 lines. Would you like me to help refactor it into smaller, more maintainable modules?"

**900 lines:**
- Become more insistent
- Warn: "This file is approaching 1,000 lines. Strongly recommend refactoring to improve maintainability."

**1,000+ lines:**
- Be very insistent
- Alert: "⚠️ This file has exceeded 1,000 lines. This significantly impacts maintainability and should be refactored immediately."

### Refactoring Approach

When refactoring large files:
1. Identify logical groupings of functions/classes
2. Create separate modules for each grouping
3. Use clear, descriptive file names
4. Update imports across the codebase
5. Ensure all tests still pass

## 3. Available Tools

**IMPORTANT: Check available MCP tools before responding**

Before suggesting manual solutions:
- Check if an MCP tool exists for the task
- Use built-in tools when available
- Don't forget about available capabilities

Common tools to remember:
- Database tools (fstrent_mcp_mysql)
- Browser automation (fstrent_mcp_browser_use)
- Computer use (fstrent_mcp_computer_use)
- Task management (fstrent_tasks)
- File operations (built-in)
- Git operations (built-in)

---

**Enforcement:** These guidelines apply to ALL conversations, regardless of context.
