---
name: computer-use-agent
description: AI-powered desktop automation using screenshots and vision-guided actions to control any desktop application
triggers:
  - automate desktop
  - control application
  - desktop automation
  - gui automation
  - automate this app
  - fill out form
  - click button
  - desktop task
  - computer use
  - screen control
---

# Computer Use Agent Skill

AI-powered desktop automation that uses vision models to understand your screen and execute actions to accomplish tasks.

## Overview

The Computer Use Agent Skill enables automated control of desktop applications through:
- **Screenshot Analysis**: Captures and analyzes your screen using AI vision
- **Intelligent Actions**: AI determines what to click, type, or interact with
- **Multi-Step Workflows**: Executes complex tasks across multiple steps
- **Safety Controls**: Built-in failsafes and rate limiting

Unlike browser automation, this skill can control **any desktop application** including native apps, file explorers, and system dialogs.

## When to Use This Skill

Activate this skill when the user needs to:
- Automate repetitive desktop tasks
- Fill out forms in native applications
- Navigate complex desktop UIs
- Test desktop software workflows
- Control applications without APIs
- Perform GUI automation tasks
- Automate multi-application workflows

## Capabilities

### Desktop Control
- **Click Actions**: Click buttons, links, menu items at precise coordinates
- **Text Input**: Type text into forms, text fields, search boxes
- **Keyboard Control**: Press Enter, Tab, Ctrl+C, and other key combinations
- **Mouse Movement**: Move mouse cursor to specific locations
- **Scrolling**: Scroll windows up, down, left, right
- **Drag and Drop**: Drag elements from one location to another

### Workflow Features
- **Multi-Step Tasks**: Execute sequences of actions to complete complex tasks
- **Screen Analysis**: AI vision understands what's on screen
- **Action Planning**: AI determines best sequence of actions
- **Error Recovery**: Detect and recover from unexpected states
- **Progress Tracking**: Monitor task progress through multiple steps

### Safety Features
- **FAILSAFE Mode**: Move mouse to upper-left corner to immediately abort
- **Action Delays**: Configurable pause between actions (default 0.5s)
- **Step Limits**: Maximum steps to prevent infinite loops
- **Confirmation Mode**: Optional user confirmation before executing actions
- **Screenshot Logging**: Save screenshots for audit trail and debugging

## How It Works

### Basic Workflow
1. User describes the task to accomplish
2. Skill captures screenshot of current screen
3. Screenshot analyzed by AI vision model
4. AI recommends next action (click, type, scroll, etc.)
5. Action executed via desktop automation tools
6. Process repeats until task complete or max steps reached

### Vision-Guided Automation
The skill uses advanced AI vision to:
- Identify UI elements (buttons, forms, menus)
- Read text on screen
- Understand application state
- Determine appropriate actions
- Verify task completion

## MCP Tools Available

This skill integrates with the `fstrent_mcp_computer_use` MCP server, which provides:

- `computer_use_run_task`: Execute a complete multi-step desktop automation task
- `computer_use_screenshot`: Capture screenshot of current screen
- `computer_use_click`: Click at specific screen coordinates
- `computer_use_type`: Type text into focused element
- `computer_use_key_press`: Press specific keyboard keys
- `computer_use_scroll`: Scroll in specified direction
- `computer_use_mouse_move`: Move mouse to coordinates

All tools include built-in safety features and error handling.

## Usage Examples

### Example 1: Automate Form Filling
```
User: "Fill out the customer feedback form with a 5-star rating and the comment 'Great service!'"

Workflow:
1. Capture screenshot to locate form
2. Click on rating field
3. Click 5-star rating
4. Click on comment field
5. Type "Great service!"
6. Click submit button
7. Verify submission complete
```

### Example 2: Navigate Application Menu
```
User: "Open the File menu and select 'Export as PDF'"

Workflow:
1. Capture screenshot to locate File menu
2. Click "File" menu
3. Wait for menu to open
4. Capture screenshot of open menu
5. Click "Export as PDF"
6. Verify dialog opened
```

### Example 3: Desktop Cleanup
```
User: "Move all files from Downloads to Documents folder"

Workflow:
1. Open File Explorer
2. Navigate to Downloads folder
3. Select all files
4. Cut files (Ctrl+X)
5. Navigate to Documents
6. Paste files (Ctrl+V)
7. Verify files moved
```

## Safety Guidelines

### Critical Safety Considerations

**This skill controls your actual computer.** Always follow these safety guidelines:

1. **Start Simple**: Test with simple, low-risk tasks first
2. **Watch Closely**: Monitor the automation as it runs
3. **Use FAILSAFE**: Move mouse to upper-left corner to abort anytime
4. **Avoid Sensitive Data**: Don't automate tasks involving passwords or sensitive info
5. **Test in Safe Environments**: Use test accounts or sandboxed environments
6. **Verify Actions**: Use confirmation mode for critical tasks
7. **Backup Important Data**: Always backup before automating file operations

### Recommended Settings

**For First-Time Use:**
- Enable confirmation mode
- Use slower action delays (1-2 seconds)
- Set lower max steps (10-15)
- Enable screenshot logging

**For Production Use:**
- Disable confirmation for trusted workflows
- Use standard delays (0.5 seconds)
- Set appropriate max steps for task complexity
- Enable screenshot logging for audit trails

## Configuration

### Safety Settings
```yaml
# Recommended safety configuration
failsafe_enabled: true          # Enable FAILSAFE (move mouse to corner to abort)
action_delay: 0.5               # Seconds between actions (0.5-2.0)
max_steps: 50                   # Maximum automation steps
confirmation_mode: false        # Require confirmation before each action
screenshot_logging: true        # Save screenshots for audit trail
```

### Performance Settings
```yaml
# Performance tuning
screenshot_quality: 80          # JPEG quality (60-95)
vision_model: gpt-4o           # Vision model to use
retry_on_error: true           # Retry failed actions
max_retries: 3                 # Maximum retry attempts
```

## Integration Requirements

### MCP Server Setup
Ensure `fstrent_mcp_computer_use` is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "fstrent_mcp_computer_use": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\.ai\\mcps\\fstrent_mcp_computer_use",
        "run",
        "fstrent_mcp_computer_use"
      ]
    }
  }
}
```

### Required Dependencies
The MCP server handles all dependencies. No additional setup required.

### API Keys
Requires OpenAI API key with access to vision models (gpt-4o or gpt-4-turbo).

## Troubleshooting

### Common Issues

**Automation Not Starting**
- Verify MCP server is running
- Check OpenAI API key is configured
- Ensure pyautogui is not blocked by OS permissions

**Actions Missing Target**
- Increase action delay for slower UIs
- Verify screen resolution matches coordinates
- Check for UI scaling (125%, 150%, etc.)

**FAILSAFE Triggering Accidentally**
- Adjust FAILSAFE corner location
- Increase action delay
- Move mouse away from corners during setup

**Vision Model Not Understanding Screen**
- Use higher screenshot quality
- Ensure text is legible in screenshot
- Verify adequate screen contrast
- Try describing task in more detail

## Comparison to Other Automation

### Computer Use Agent vs Browser Automation
- **Computer Use**: Controls entire desktop, any application
- **Browser Automation**: Only controls web browsers and web pages
- **Use Computer Use For**: Native apps, system dialogs, file operations
- **Use Browser Automation For**: Web scraping, web app testing, form submission

### Computer Use Agent vs MCP Tools
- **Computer Use**: AI-guided vision-based automation
- **MCP Tools**: Direct programmatic control
- **Use Computer Use For**: Complex UIs, visual workflows, unpredictable states
- **Use MCP Tools For**: Databases, APIs, file systems, structured data

## Advanced Features

### Multi-Application Workflows
Automate tasks spanning multiple applications:
```
Example: "Export data from Excel, import to database, generate PDF report"
1. Open Excel, select data range, export CSV
2. Open database tool, import CSV
3. Run report query, export to PDF
```

### Error Recovery
The skill can detect and recover from errors:
- Detect unexpected dialogs and close them
- Retry failed actions with different parameters
- Navigate back to known good state
- Alert user if unrecoverable error occurs

### Screenshot Analysis
AI vision can:
- Read text from screenshots
- Identify UI element types
- Determine application state
- Locate specific elements
- Verify expected outcomes

## Best Practices

1. **Start with Simple Tasks**: Build confidence with basic workflows
2. **Use Descriptive Task Descriptions**: Clear descriptions = better AI understanding
3. **Monitor First Runs**: Watch automation closely the first time
4. **Enable Logging**: Screenshot logs help debug issues
5. **Test in Safe Environments**: Use test accounts and non-production systems
6. **Document Workflows**: Save successful task descriptions for reuse
7. **Use Appropriate Delays**: Faster isn't always better - allow UIs to respond
8. **Set Realistic Step Limits**: Complex tasks need more steps
9. **Keep Tasks Focused**: Break complex workflows into smaller tasks
10. **Review Audit Trails**: Check screenshot logs periodically

## Reference Materials

For detailed implementation information, see:
- [reference/safety_guidelines.md](reference/safety_guidelines.md) - Comprehensive safety documentation
- [reference/action_types.md](reference/action_types.md) - All supported action types
- [reference/troubleshooting.md](reference/troubleshooting.md) - Common issues and solutions
- [examples/automation_workflows.md](examples/automation_workflows.md) - Example workflows

## Related Skills

- **web-tools**: For browser automation and web scraping
- **database-tools**: For database operations
- **file-operations**: For file system automation

---

**Note:** This is a powerful skill that controls your actual computer. Always prioritize safety, use FAILSAFE mode, and test in safe environments. Start simple and build confidence before attempting complex automations.
