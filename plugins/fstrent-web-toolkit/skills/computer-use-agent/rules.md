# Computer Use Agent Skill - Implementation Rules

## Skill Activation

Activate this skill when user requests involve:
- Desktop application automation
- GUI control or navigation
- Form filling in native apps
- Multi-application workflows
- Tasks requiring vision-based screen analysis
- Automation that can't be done via browser or API

**Do NOT activate for:**
- Web scraping or browser automation (use web-tools skill)
- Database operations (use database-tools skill)
- File operations only (use file-operations skill)
- API integrations (use appropriate integration skill)

## Core Workflow

### Step 1: Task Analysis
When user requests desktop automation:

1. **Understand the Goal**: Clarify what the user wants to accomplish
2. **Identify Applications**: Determine which desktop apps are involved
3. **Assess Complexity**: Estimate number of steps required
4. **Check Safety**: Identify any sensitive data or risky operations
5. **Confirm Approach**: Explain plan to user before executing

### Step 2: Safety Configuration
Before ANY automation:

1. **Verify FAILSAFE**: Confirm FAILSAFE mode is enabled
2. **Set Action Delay**: Use appropriate delay for task complexity
   - Simple tasks: 0.5 seconds
   - Complex UIs: 1.0 seconds
   - Slow applications: 2.0 seconds
3. **Set Max Steps**: Configure reasonable step limit
   - Simple tasks: 10-20 steps
   - Medium tasks: 20-50 steps
   - Complex tasks: 50-100 steps
4. **Enable Logging**: Always enable screenshot logging for audit trail
5. **Confirmation Mode**: Enable for first-time or high-risk tasks

### Step 3: Execute Automation
Use the `computer_use_run_task` MCP tool:

```python
# Example invocation
computer_use_run_task(
    task_description="Fill out customer feedback form with 5-star rating",
    max_steps=25,
    action_delay=0.5,
    save_screenshots=True
)
```

### Step 4: Monitor and Report
After execution:

1. **Check Results**: Verify task completed successfully
2. **Review Screenshots**: Check saved screenshots for issues
3. **Report to User**: Summarize what was done
4. **Provide Audit Trail**: Share screenshot paths if requested
5. **Note Any Issues**: Report errors or unexpected behavior

## Action Type Guidelines

### Click Actions
Use when user needs to:
- Click buttons, links, menu items
- Select checkboxes or radio buttons
- Activate UI controls

**Best Practices:**
- Verify element location via screenshot analysis first
- Use appropriate action delay after click
- Confirm expected state change occurred

### Type Actions
Use when user needs to:
- Fill out text fields
- Enter search queries
- Input data into forms

**Best Practices:**
- Click field first to ensure focus
- Type slowly for applications that process input character-by-character
- Press Tab or Enter after typing if needed
- Verify text was entered correctly

### Key Press Actions
Use when user needs to:
- Press Enter to submit forms
- Use Tab to navigate fields
- Trigger keyboard shortcuts (Ctrl+C, Ctrl+V, etc.)
- Press Escape to close dialogs

**Common Key Combinations:**
- `Enter`: Submit forms, confirm dialogs
- `Tab`: Navigate between fields
- `Escape`: Close dialogs, cancel operations
- `Ctrl+C`: Copy
- `Ctrl+V`: Paste
- `Ctrl+A`: Select all
- `Ctrl+S`: Save
- `Alt+F4`: Close window

### Scroll Actions
Use when user needs to:
- Scroll down to see more content
- Navigate long pages or lists
- Reveal hidden UI elements

**Scroll Directions:**
- `down`: Scroll down (most common)
- `up`: Scroll up
- `left`: Scroll left (horizontal scrolling)
- `right`: Scroll right (horizontal scrolling)

**Best Practices:**
- Capture screenshot after scrolling to analyze new content
- Use multiple small scrolls rather than one large scroll
- Verify target element is visible after scrolling

### Mouse Move Actions
Use when user needs to:
- Hover over elements to reveal tooltips
- Position mouse before drag operations
- Trigger hover-based UI changes

**Best Practices:**
- Move mouse slowly for smooth motion
- Pause after mouse move to allow UI to respond
- Verify hover state activated if expected

## Multi-Step Workflow Patterns

### Pattern 1: Form Filling
```
1. Capture screenshot to locate form
2. For each field:
   a. Click field to focus
   b. Type value
   c. Verify value entered
   d. Move to next field
3. Click submit button
4. Verify submission confirmation
```

### Pattern 2: Menu Navigation
```
1. Capture screenshot to locate menu
2. Click menu to open
3. Wait for menu animation
4. Capture screenshot of open menu
5. Click menu item
6. Verify expected result (dialog, page change, etc.)
```

### Pattern 3: File Operations
```
1. Open File Explorer
2. Navigate to source folder
3. Select file(s)
4. Copy/cut files (Ctrl+C or Ctrl+X)
5. Navigate to destination folder
6. Paste files (Ctrl+V)
7. Verify files copied/moved
```

### Pattern 4: Application Workflow
```
1. Launch application (if not running)
2. Wait for application to load
3. Navigate to required section
4. Execute series of actions
5. Save results (Ctrl+S or File > Save)
6. Close application or return to start state
```

### Pattern 5: Multi-Application Workflow
```
1. Execute task in Application A
2. Copy/export data
3. Switch to Application B (Alt+Tab or click)
4. Import/paste data
5. Process in Application B
6. Export results
7. Switch back to Application A
8. Import results
```

## Error Handling

### Common Errors and Recovery

**Element Not Found:**
```
1. Capture fresh screenshot
2. Verify application state
3. Scroll if element might be off-screen
4. Try alternate element identification
5. If still not found, report to user
```

**Unexpected Dialog:**
```
1. Capture screenshot of dialog
2. Analyze dialog type (error, warning, info)
3. Click appropriate button (OK, Cancel, Close)
4. Return to expected application state
5. Retry original action if appropriate
```

**Application Not Responding:**
```
1. Wait longer (increase action delay)
2. Check if application crashed
3. Try keyboard shortcut to activate window
4. If unrecoverable, report to user
5. Do NOT force close without user permission
```

**Wrong Application Focus:**
```
1. Click application title bar
2. Or use Alt+Tab to switch
3. Verify correct application has focus
4. Resume workflow
```

**Action Failed:**
```
1. Capture screenshot of failure state
2. Analyze what went wrong
3. Attempt recovery action
4. Retry original action (max 3 retries)
5. If still failing, report to user
```

## Safety Rules

### Mandatory Safety Checks

**BEFORE executing ANY automation:**
1. ✅ Verify FAILSAFE is enabled
2. ✅ Confirm appropriate action delay is set
3. ✅ Set reasonable max steps limit
4. ✅ Enable screenshot logging
5. ✅ Explain to user what will happen

**DURING automation:**
1. ✅ Pause between actions (respect action_delay)
2. ✅ Verify each action completed successfully
3. ✅ Check for unexpected states
4. ✅ Count steps to prevent infinite loops
5. ✅ Save screenshots for audit trail

**AFTER automation:**
1. ✅ Verify task completed as expected
2. ✅ Report results to user
3. ✅ Note any errors or issues
4. ✅ Provide screenshot paths for audit
5. ✅ Clean up any temporary files

### Prohibited Actions

**NEVER automate:**
- ❌ Password entry (security risk)
- ❌ Banking or financial transactions (too risky)
- ❌ System configuration changes (without explicit user permission)
- ❌ File deletion (without confirmation)
- ❌ Email sending (without user review)
- ❌ Social media posting (without user review)
- ❌ Anything involving PII or sensitive data

**ALWAYS require explicit permission for:**
- File modifications or deletions
- Application installations or updates
- System setting changes
- Actions that modify data permanently
- Actions involving external communications

### Risk Assessment

**Low Risk (OK to automate):**
- Reading/viewing content
- Navigating menus
- Filling out test forms
- Moving/copying test files
- Taking screenshots
- Opening applications

**Medium Risk (Require confirmation):**
- Filling out real forms
- Modifying files
- Sending data to applications
- Changing application settings
- Downloading files

**High Risk (Require explicit permission + confirmation):**
- Deleting files or data
- Sending emails or messages
- Financial operations
- System configuration changes
- Installing software

**Prohibited (Never automate):**
- Password entry
- Banking/financial transactions
- Anything with sensitive personal data

## Performance Optimization

### Screenshot Quality
- Use 80% JPEG quality for balance of speed and clarity
- Use higher quality (90-95%) if vision model struggles to read text
- Use lower quality (60-70%) for simple UIs to improve speed

### Action Delays
- Fast UIs: 0.3-0.5 seconds
- Standard UIs: 0.5-1.0 seconds
- Slow UIs: 1.0-2.0 seconds
- Network-dependent UIs: 2.0-5.0 seconds

### Vision Model Selection
- Use `gpt-4o` for best speed/accuracy balance
- Use `gpt-4-turbo` for complex visual understanding
- Use `gpt-4o-mini` for simple tasks (faster, cheaper)

### Step Optimization
- Minimize unnecessary screenshots (only after state changes)
- Combine multiple key presses into single action if possible
- Use keyboard shortcuts instead of menu navigation when possible
- Batch similar actions together

## Integration with MCP Tools

### Available MCP Tools

**computer_use_run_task(task_description, max_steps, action_delay, save_screenshots)**
- Primary tool for full automation workflows
- Handles screenshot capture, vision analysis, action execution
- Returns task results and screenshot paths

**computer_use_screenshot()**
- Capture current screen without executing actions
- Useful for analysis or verification
- Returns base64-encoded screenshot

**computer_use_click(x, y)**
- Click at specific screen coordinates
- For manual control when needed
- Returns success/failure status

**computer_use_type(text)**
- Type text into currently focused element
- Supports special characters and Unicode
- Returns success/failure status

**computer_use_key_press(key)**
- Press specific keyboard key
- Supports modifiers (Ctrl, Alt, Shift)
- Returns success/failure status

**computer_use_scroll(direction, amount)**
- Scroll in specified direction
- Amount controls scroll distance
- Returns success/failure status

**computer_use_mouse_move(x, y)**
- Move mouse to coordinates without clicking
- For hover effects or drag setup
- Returns success/failure status

### Tool Selection Guidelines

**Use `computer_use_run_task` when:**
- User describes goal in natural language
- Task requires multiple steps
- AI should determine action sequence
- Full automation desired

**Use individual action tools when:**
- You know exact action needed
- Testing or debugging
- Combining with other skills
- Fine-grained control required

## User Communication

### Initial Response Template
```
I'll help you automate [TASK]. Here's my plan:

1. [Step 1]
2. [Step 2]
3. [Step 3]
...

This will use AI vision to analyze your screen and execute actions to accomplish the task.

Safety settings:
- FAILSAFE enabled (move mouse to upper-left corner to abort)
- Action delay: [X] seconds
- Max steps: [Y]
- Screenshot logging: enabled

Ready to proceed? (I'll start when you confirm)
```

### Progress Updates
Provide updates during long-running tasks:
```
Progress update:
- Completed: [Completed steps]
- Current: [Current action]
- Remaining: [Estimated remaining steps]
- Status: [On track / Issue detected / Needs attention]
```

### Completion Report
```
Task completed successfully!

Summary:
- Task: [Task description]
- Steps executed: [X]
- Time elapsed: [Y] seconds
- Screenshots saved: [Z] files
- Issues encountered: [None / List issues]

Screenshot audit trail: [Path to screenshots]

Would you like me to:
1. Repeat this task
2. Modify and re-run
3. Save this workflow for future use
```

### Error Report
```
Task encountered an error:

Error: [Error description]
Step failed: [Which step]
Application state: [Current state]

Screenshot of error: [Path]

Attempted recovery: [What was tried]
Recovery successful: [Yes/No]

Next steps:
1. [Recommended action 1]
2. [Recommended action 2]
3. [Alternative approach if applicable]

Shall I retry, try a different approach, or would you like to handle this manually?
```

## Testing and Validation

### Before Production Use
Test the workflow with:
1. Simple single-step actions
2. Multi-step workflows
3. Error conditions
4. Different screen resolutions
5. Different application states
6. Different UI scaling (100%, 125%, 150%)

### Validation Checklist
- [ ] FAILSAFE works correctly
- [ ] Action delays are appropriate
- [ ] Screenshots are clear and readable
- [ ] Vision model understands UI elements
- [ ] Actions target correct elements
- [ ] Error recovery works as expected
- [ ] Max steps limit prevents runaway automation
- [ ] Screenshot logging works correctly
- [ ] User can abort via FAILSAFE
- [ ] Results are reported accurately

## Troubleshooting Guide

### Vision Model Issues
**Symptom:** AI doesn't understand what's on screen
**Solutions:**
- Increase screenshot quality
- Improve screen contrast
- Enlarge UI elements (accessibility settings)
- Provide more specific task description
- Try different vision model

### Timing Issues
**Symptom:** Actions execute before UI is ready
**Solutions:**
- Increase action delay
- Add explicit wait after UI changes
- Verify animation/transition completed
- Use slower step-by-step mode

### Coordinate Issues
**Symptom:** Clicks missing targets
**Solutions:**
- Check screen scaling settings
- Verify resolution matches expected
- Recalibrate coordinate system
- Use larger click targets if possible

### Application Focus Issues
**Symptom:** Actions go to wrong application
**Solutions:**
- Click application title bar first
- Use Alt+Tab to switch focus
- Verify window is in foreground
- Close unnecessary windows

## Best Practices Summary

1. **Always prioritize safety** - Use FAILSAFE, confirmations, logging
2. **Start simple** - Test with easy tasks before complex workflows
3. **Explain before executing** - Tell user what will happen
4. **Monitor closely** - Watch first runs carefully
5. **Use appropriate delays** - Don't rush, let UIs respond
6. **Set realistic step limits** - Prevent runaway automation
7. **Enable logging** - Always save screenshots for audit trail
8. **Verify results** - Check that task completed as expected
9. **Handle errors gracefully** - Detect, recover, or report
10. **Communicate clearly** - Keep user informed of progress

## Integration with Other Skills

### With web-tools Skill
- Use web-tools for browser automation
- Use computer-use-agent for native app parts
- Combine for workflows spanning web and desktop

### With database-tools Skill
- Use database-tools for data queries
- Use computer-use-agent for UI that lacks API
- Combine for data import/export workflows

### With file-operations Skill
- Use file-operations for batch file processing
- Use computer-use-agent for GUI file operations
- Combine for complex file management workflows

---

**Remember:** This skill controls the user's actual computer. Safety must always be the top priority. When in doubt, ask for user confirmation.
