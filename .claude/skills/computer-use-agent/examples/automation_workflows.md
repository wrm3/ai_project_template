# Computer Use Agent - Example Automation Workflows

## Overview

This document provides practical examples of desktop automation workflows using the Computer Use Agent skill. Each example includes task description, workflow steps, safety considerations, and expected outcomes.

## Example 1: Form Filling - Customer Feedback

### Task
Fill out a customer feedback form with a 5-star rating and positive comment.

### Prerequisites
- Feedback form application is open
- Form is visible on screen
- No sensitive customer data visible

### Workflow Steps
```
1. Capture screenshot to locate form elements
2. Click on "Name" field
3. Type "John Smith"
4. Press Tab to move to next field
5. Type "john.smith@example.com"
6. Press Tab to move to rating
7. Click on 5-star rating
8. Click on "Comments" field
9. Type "Great service! Very satisfied with the product."
10. Click "Submit" button
11. Wait for confirmation dialog
12. Verify "Thank you" message appears
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 0.5
max_steps: 15
confirmation_mode: false  # Low risk task
screenshot_logging: true
```

### Expected Outcome
- Form successfully submitted
- Confirmation message displayed
- All fields contain correct values
- No errors occurred

### Common Issues
- **Form not visible**: Scroll to make form visible first
- **Field not accepting input**: Click field twice to ensure focus
- **Submit button disabled**: Verify all required fields filled

---

## Example 2: Menu Navigation - Export Settings

### Task
Navigate application menu to export settings as JSON file.

### Prerequisites
- Application is open and active
- User has permissions to export settings
- Export destination folder exists

### Workflow Steps
```
1. Capture screenshot to locate File menu
2. Click "File" menu
3. Wait 0.5s for menu to fully open
4. Capture screenshot of open menu
5. Move mouse to "Export" submenu
6. Wait for submenu to appear
7. Click "Export Settings..."
8. Wait for export dialog to open
9. Verify "Save As" dialog is displayed
10. Type "settings_backup.json" in filename field
11. Verify destination folder is correct
12. Click "Save" button
13. Wait for export to complete
14. Verify success message or file creation
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 1.0  # Slower for menu animations
max_steps: 20
confirmation_mode: false
screenshot_logging: true
```

### Expected Outcome
- Settings successfully exported
- JSON file created in destination folder
- File contains valid settings data
- Application returns to normal state

### Common Issues
- **Menu closes too quickly**: Increase action delay
- **Submenu doesn't appear**: Move mouse slower to trigger hover
- **Wrong export format selected**: Verify dropdown selection before save

---

## Example 3: File Organization - Downloads Cleanup

### Task
Move all PDF files from Downloads folder to Documents/PDFs folder.

### Prerequisites
- Windows File Explorer
- Downloads folder has PDF files
- Documents/PDFs folder exists
- User has permissions to move files

### Workflow Steps
```
1. Press Win key to open Start menu
2. Type "File Explorer"
3. Press Enter to open File Explorer
4. Click address bar
5. Type "%USERPROFILE%\Downloads"
6. Press Enter to navigate
7. Wait for folder to load
8. Click in empty space to focus window
9. Ctrl+F to open search
10. Type "*.pdf" to search for PDFs
11. Wait for search results
12. Ctrl+A to select all PDF files
13. Ctrl+X to cut files
14. Click address bar
15. Type "%USERPROFILE%\Documents\PDFs"
16. Press Enter to navigate
17. Ctrl+V to paste files
18. Wait for file transfer to complete
19. Verify files moved successfully
20. Close File Explorer
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 1.0
max_steps: 25
confirmation_mode: true  # First run - confirm before executing
screenshot_logging: true
```

### Expected Outcome
- All PDF files moved from Downloads to Documents/PDFs
- No files left in Downloads (except non-PDFs)
- All files intact in destination
- No errors during transfer

### Safety Considerations
- ⚠️ File operations are medium risk
- ✅ Backup Downloads folder before first run
- ✅ Test with small number of files first
- ✅ Verify destination exists before starting

### Common Issues
- **Files already exist**: Handle overwrite dialog
- **Insufficient permissions**: Run with appropriate permissions
- **Large files**: Increase max_steps and timeouts

---

## Example 4: Multi-Application - Data Export and Email

### Task
Export data from spreadsheet application and email it.

### Prerequisites
- Spreadsheet application open with data
- Email client configured
- Recipient email address known

### Workflow Steps
```
1. Focus spreadsheet application
2. Select data range (Ctrl+A or manual selection)
3. Click File > Export
4. Select "CSV" format
5. Enter filename "monthly_report.csv"
6. Click Save
7. Wait for export complete
8. Alt+Tab to switch to email client
9. Click "New Message" button
10. Type recipient email in To field
11. Tab to Subject field
12. Type "Monthly Report - [Current Date]"
13. Tab to body field
14. Type email message
15. Click "Attach" button
16. Navigate to exported CSV file
17. Select file and click "Open"
18. Verify file attached
19. Click "Send" button
20. Wait for sent confirmation
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 1.5  # Multiple applications
max_steps: 30
confirmation_mode: true  # Email sending requires confirmation
screenshot_logging: true
```

### Expected Outcome
- Data exported to CSV successfully
- Email created with correct recipient
- File attached to email
- Email sent successfully
- Sent confirmation received

### Safety Considerations
- 🛑 High risk - sending email
- ✅ Always require confirmation before sending
- ✅ Review recipient address
- ✅ Verify attachment is correct file
- ✅ Preview email before sending

### Common Issues
- **Wrong application focus**: Click title bar to ensure focus
- **Attachment dialog doesn't open**: Try keyboard shortcut (Ctrl+O)
- **Email sent prematurely**: Use confirmation mode

---

## Example 5: Testing - Automated UI Testing

### Task
Test login form with various input combinations to verify validation.

### Prerequisites
- Test application running
- Test credentials available
- Test environment (not production)

### Workflow Steps
```
Test Case 1: Valid Login
1. Navigate to login page
2. Enter valid username
3. Enter valid password
4. Click Login button
5. Verify dashboard loads
6. Logout

Test Case 2: Invalid Username
1. Navigate to login page
2. Enter invalid username
3. Enter valid password
4. Click Login button
5. Verify error message "Invalid username or password"
6. Verify still on login page

Test Case 3: Invalid Password
1. Navigate to login page
2. Enter valid username
3. Enter invalid password
4. Click Login button
5. Verify error message appears
6. Verify still on login page

Test Case 4: Empty Fields
1. Navigate to login page
2. Leave username empty
3. Leave password empty
4. Click Login button
5. Verify validation errors appear
6. Verify required field indicators
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 1.0
max_steps: 50  # Multiple test cases
confirmation_mode: false  # Test automation
screenshot_logging: true  # Capture test evidence
```

### Expected Outcome
- All test cases execute successfully
- Expected error messages appear
- Valid login succeeds
- Invalid logins fail appropriately
- Screenshots capture evidence

### Testing Best Practices
- ✅ Use test accounts only
- ✅ Test in isolated environment
- ✅ Document expected vs actual results
- ✅ Save screenshot logs as evidence
- ✅ Automate regression testing

---

## Example 6: Productivity - Meeting Notes Template

### Task
Open note-taking app and create new meeting notes from template.

### Prerequisites
- Note-taking application installed
- Meeting template exists
- Meeting details available

### Workflow Steps
```
1. Press Win key
2. Type note app name
3. Press Enter to open
4. Wait for app to load
5. Click "New Note" button
6. Type meeting title
7. Press Enter to confirm title
8. Type template structure:
   - "Date: [Auto-fill current date]"
   - "Attendees: "
   - "Agenda:"
   - "  1. "
   - "  2. "
   - "  3. "
   - "Discussion Notes:"
   - "Action Items:"
   - "  [ ] "
   - "  [ ] "
   - "Next Steps:"
9. Position cursor at Attendees field
10. Ready for user to fill in
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 0.3  # Fast for text entry
max_steps: 20
confirmation_mode: false  # Low risk
screenshot_logging: false  # Not needed for templates
```

### Expected Outcome
- New note created with title
- Template structure populated
- Cursor positioned for user input
- Ready to take meeting notes

### Use Cases
- Meeting notes
- Project planning templates
- Daily standup notes
- Task lists
- Documentation templates

---

## Example 7: Advanced - Database GUI Interaction

### Task
Open database client, execute query, export results to Excel.

### Prerequisites
- Database client installed
- Database connection configured
- Query prepared
- Excel installed

### Workflow Steps
```
1. Open database client application
2. Wait for connection establishment
3. Click "New Query" button
4. Type SQL query:
   "SELECT * FROM customers WHERE status = 'active' ORDER BY name"
5. Click "Execute" or press F5
6. Wait for query results to load
7. Verify results appear in grid
8. Right-click results grid
9. Select "Export to Excel"
10. Wait for Excel export dialog
11. Enter filename "active_customers.xlsx"
12. Select destination folder
13. Click "Export" button
14. Wait for export to complete
15. Verify success message
16. Close query window
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 2.0  # Database operations can be slow
max_steps: 25
confirmation_mode: true  # First run only
screenshot_logging: true
```

### Expected Outcome
- Query executed successfully
- Results displayed correctly
- Excel file created with data
- All rows exported completely
- File opens in Excel correctly

### Safety Considerations
- ⚠️ Verify query before execution
- ⚠️ Test with small result sets first
- ⚠️ Ensure read-only query (SELECT, not UPDATE/DELETE)
- ⚠️ Verify database connection is to test DB

---

## Example 8: System - Automated Software Update Check

### Task
Check for software updates in multiple applications.

### Prerequisites
- Applications support update checking
- Internet connection available
- User has permissions to check updates

### Workflow Steps
```
For each application:
1. Launch application
2. Wait for application to load fully
3. Click Help menu
4. Click "Check for Updates"
5. Wait for update check to complete
6. Capture screenshot of update status
7. If updates available:
   a. Note update availability
   b. Do NOT install automatically
8. Close update dialog
9. Close application
10. Move to next application

Applications to check:
- Web browser
- Office suite
- Development tools
- Communication apps
```

### Safety Settings
```yaml
failsafe_enabled: true
action_delay: 3.0  # Network operations
max_steps: 100  # Multiple applications
confirmation_mode: false
screenshot_logging: true  # Capture update status
```

### Expected Outcome
- All applications checked for updates
- Update status captured in screenshots
- No automatic installations
- Log of which apps need updates
- All applications closed cleanly

### Safety Considerations
- ✅ Check only, don't install
- ✅ Capture screenshots for review
- ✅ User reviews and decides on installations
- ❌ Never install updates automatically

---

## Workflow Templates

### Template: Form Filling
```
1. Capture screen to locate form
2. For each field:
   - Click field
   - Enter value
   - Verify entry
   - Move to next field
3. Review all entries
4. Submit form
5. Verify confirmation
```

### Template: Menu Navigation
```
1. Locate menu
2. Click menu
3. Wait for menu to open
4. Locate menu item
5. Click menu item
6. Verify expected action
```

### Template: File Operations
```
1. Open File Explorer
2. Navigate to source
3. Select file(s)
4. Copy/cut
5. Navigate to destination
6. Paste
7. Verify transfer
```

### Template: Multi-Application
```
1. Focus Application A
2. Execute actions in A
3. Extract/copy data
4. Switch to Application B
5. Focus Application B
6. Execute actions in B
7. Paste/use data
8. Verify result
```

## Best Practices Summary

1. **Always start simple** - Test basic workflows before complex ones
2. **Use appropriate delays** - Slower is more reliable
3. **Enable logging** - Screenshots help debugging
4. **Test in safe environments** - Never test in production
5. **Verify each step** - Confirm expected state after each action
6. **Handle errors gracefully** - Plan for unexpected dialogs
7. **Document workflows** - Save successful workflows for reuse
8. **Monitor closely** - Watch automation carefully
9. **Use FAILSAFE** - Keep hand ready to abort
10. **Build incrementally** - Add steps one at a time

## Next Steps

Start with Example 1 or 2 to build confidence, then progress to more complex workflows as you become comfortable with the tool.

Remember: Safety first, always!
