# Atlassian Integration Skill - Implementation Rules

## Skill Activation

Activate this skill when user requests involve:
- Jira issue operations (create, update, query)
- Confluence page management (create, update, search)
- Bitbucket repository operations (PR, branches, commits)
- Trello board/card management
- Cross-product Atlassian workflows
- Atlassian reporting and automation

**Do NOT activate for:**
- Generic project management (without Atlassian context)
- Local file documentation (use file-operations)
- GitHub operations (different platform)
- Non-Atlassian task tracking

## Core Workflow

### Step 1: Identify Product and Operation
Determine which Atlassian product and what operation:

**Jira** - Keywords: issue, ticket, bug, story, epic, sprint, project
**Confluence** - Keywords: page, documentation, wiki, knowledge base, space
**Bitbucket** - Keywords: repository, pull request, PR, branch, commit, code review
**Trello** - Keywords: board, card, list, task, checklist

### Step 2: Gather Required Information
Before executing, collect:
- **Authentication**: API tokens, credentials
- **Target**: Project key, space key, repository name, board ID
- **Operation details**: Issue type, page title, branch name, etc.
- **Permissions**: Verify user has required access

### Step 3: Execute Operation
Use appropriate API or MCP tool:
- Validate inputs
- Handle authentication
- Execute operation with error handling
- Return structured result

### Step 4: Confirm and Report
- Verify operation succeeded
- Return relevant IDs/URLs
- Provide next steps if applicable
- Log operation for audit

## Jira Workflows

### Create Issue
```
1. Determine issue type (Bug, Story, Task, etc.)
2. Gather required fields:
   - Project key (e.g., PROJ)
   - Summary (title)
   - Description (optional but recommended)
   - Priority (default: Medium)
   - Assignee (optional)
   - Labels (optional)
   - Custom fields (as needed)
3. Validate project exists
4. Create issue via API
5. Return issue key (PROJ-123) and URL
```

### Update Issue
```
1. Get issue key (PROJ-123)
2. Determine what to update:
   - Fields (summary, description, priority, etc.)
   - Status transition
   - Add comment
   - Add attachment
3. Validate issue exists and is editable
4. Update via API
5. Return confirmation
```

### Query Issues (JQL)
```
1. Build JQL query based on criteria:
   - Project filter
   - Status filter
   - Assignee filter
   - Date ranges
   - Custom conditions
2. Execute search via API
3. Get results (paginated if needed)
4. Format results for user
5. Return structured data
```

### Transition Issue
```
1. Get issue key
2. Get current status
3. Get available transitions
4. Validate target transition is valid
5. Execute transition
6. Add comment if provided
7. Return new status
```

### Common JQL Patterns
```jql
# My open issues
assignee = currentUser() AND status != Done

# Bugs in current sprint
type = Bug AND sprint in openSprints()

# High priority overdue
priority = High AND duedate < now()

# Recently created
created >= -7d ORDER BY created DESC

# Unassigned in project
project = PROJ AND assignee is EMPTY

# Blocked issues
status = Blocked OR labels = blocked
```

## Confluence Workflows

### Create Page
```
1. Gather page details:
   - Space key (TEAM)
   - Title
   - Content (markdown or HTML)
   - Parent page ID (optional)
2. Validate space exists
3. Check for duplicate titles in space
4. Convert content to Confluence storage format
5. Create page via API or MCP
6. Return page ID and URL
```

### Update Page
```
1. Get page ID or search by title
2. Get current page version
3. Prepare updated content
4. Increment version number
5. Update via API
6. Return updated page URL
```

### Search Pages
```
1. Build CQL (Confluence Query Language) query:
   - Space filter
   - Title search
   - Content search
   - Date filters
   - Label filters
2. Execute search
3. Get results (paginated)
4. Format and return results
```

### Upload Attachment
```
1. Get page ID
2. Prepare file for upload
3. Check file size limits
4. Upload via API
5. Return attachment URL
```

### Common CQL Patterns
```cql
# Pages by title
title ~ "API Documentation"

# Recent pages in space
space = TEAM AND lastModified >= now("-7d")

# Pages with label
label = "important" AND space = TEAM

# Pages by creator
creator = currentUser()

# Full-text search
text ~ "authentication"
```

## Bitbucket Workflows

### Create Pull Request
```
1. Get repository details
2. Identify source and target branches
3. Generate PR title from branch or commits
4. Generate description from commits
5. Add reviewers (auto-assign or user-specified)
6. Create PR via API
7. Return PR ID and URL
```

### Review Pull Request
```
1. Get PR ID
2. Get changed files and diffs
3. Review changes:
   - Check code quality
   - Verify tests added
   - Check documentation
4. Add comments on specific lines
5. Request changes or approve
6. Return review summary
```

### Merge Pull Request
```
1. Get PR ID
2. Verify PR is approved
3. Check CI/CD status
4. Resolve conflicts if any
5. Execute merge
6. Delete source branch (optional)
7. Return merge commit hash
```

### Branch Operations
```
Create branch:
1. Get source branch (usually main/master)
2. Create new branch with naming convention
3. Return branch name

Delete branch:
1. Verify branch is merged or confirm deletion
2. Delete branch via API
3. Return confirmation
```

## Trello Workflows

### Create Card
```
1. Get board ID and list ID
2. Prepare card details:
   - Name (title)
   - Description
   - Due date (optional)
   - Labels (optional)
   - Members (optional)
3. Create card via API
4. Return card ID and URL
```

### Move Card
```
1. Get card ID
2. Get target list ID
3. Optionally set position in list
4. Move card via API
5. Return confirmation
```

### Update Card
```
1. Get card ID
2. Update fields:
   - Name
   - Description
   - Due date
   - Labels
   - Checklist items
3. Update via API
4. Return updated card
```

### Board Management
```
Create board:
1. Set board name
2. Choose board type (Kanban, Scrum, etc.)
3. Set visibility (private, team, public)
4. Create default lists
5. Return board ID and URL

Add list:
1. Get board ID
2. Set list name
3. Set position
4. Create list via API
5. Return list ID
```

## Cross-Product Workflows

### Pattern 1: Jira to Confluence
```
When Jira issue is created → Create Confluence page

1. Detect Jira issue created
2. Extract issue details
3. Create Confluence page in project space:
   - Title: Issue key + summary
   - Content: Issue description + details
   - Add link back to Jira
4. Add Confluence page link to Jira issue
```

### Pattern 2: Bitbucket to Jira
```
When PR is merged → Update Jira issue

1. Detect PR merged event
2. Extract Jira issue keys from PR/commits
3. For each issue:
   - Add comment with PR link
   - Transition to "Ready for QA" (if applicable)
   - Update fix version
```

### Pattern 3: Trello to Jira
```
Sync Trello card to Jira issue

1. Create Jira issue from Trello card
2. Map Trello fields to Jira:
   - Card name → Issue summary
   - Description → Issue description
   - Due date → Due date
   - Labels → Labels
3. Add link between systems
4. Set up webhook for sync
```

### Pattern 4: Confluence to Jira
```
Generate Jira issues from Confluence page

1. Parse Confluence page for action items
2. For each action item:
   - Create Jira issue
   - Link back to Confluence page
   - Set due date from page
3. Update Confluence page with issue links
```

## Error Handling

### Authentication Errors

**401 Unauthorized:**
```
Recovery:
1. Check API token is valid
2. Verify credentials in .env file
3. Test authentication with simple API call
4. Regenerate token if expired
5. Report to user with setup instructions
```

**403 Forbidden:**
```
Recovery:
1. Check user has required permissions
2. Verify project/space access
3. Check if operation requires admin rights
4. Report specific permission needed
```

### Rate Limiting

**429 Too Many Requests:**
```
Recovery:
1. Implement exponential backoff:
   - Wait 1s, retry
   - Wait 2s, retry
   - Wait 4s, retry
   - Wait 8s, fail
2. Reduce request frequency
3. Use bulk operations where possible
4. Cache API responses
```

### Data Errors

**Issue/Page Not Found:**
```
Recovery:
1. Verify ID/key is correct
2. Check if deleted or archived
3. Search by alternative identifier
4. Report to user with details
```

**Invalid Field Value:**
```
Recovery:
1. Get valid values for field
2. Suggest valid options to user
3. Provide field schema/requirements
4. Retry with corrected value
```

### Network Errors

**Timeout:**
```
Recovery:
1. Retry with increased timeout
2. Check network connectivity
3. Verify API endpoint is accessible
4. Report to user if persistent
```

## API Best Practices

### Request Optimization

**Batch Operations:**
```
Instead of:
- Create 10 issues with 10 API calls

Use:
- Create 10 issues with 1 bulk API call
```

**Pagination:**
```
For large result sets:
1. Use pagination parameters (start, limit)
2. Fetch pages progressively
3. Cache results locally
4. Don't fetch all at once
```

**Field Filtering:**
```
Request only needed fields:
- fields=summary,status,assignee
Not all fields
```

### Caching Strategy

**Cache:**
- Project lists (1 hour)
- User lists (1 hour)
- Issue types (1 day)
- Workflow transitions (1 day)
- Space lists (1 hour)

**Invalidate:**
- On explicit update
- On error responses
- On user request

### Response Handling

**Success Response:**
```
1. Extract relevant data
2. Transform to user-friendly format
3. Return with context (URLs, IDs)
4. Log operation for audit
```

**Error Response:**
```
1. Parse error details
2. Determine if recoverable
3. Attempt recovery if possible
4. Report clear error message to user
5. Suggest corrective action
```

## Security Best Practices

### API Token Management

**Storage:**
```
✅ Store in .env file (gitignored)
✅ Use environment variables
✅ Encrypt at rest if possible
❌ Never commit to repository
❌ Don't log tokens
❌ Don't expose in URLs
```

**Rotation:**
```
1. Generate new token
2. Update in .env file
3. Test new token
4. Revoke old token
5. Document rotation date
```

### Permission Principle

**Minimum Required:**
```
Jira:
- Read: List projects, search issues
- Write: Create/update issues
- Admin: Only if managing projects

Confluence:
- Read: View pages
- Write: Create/update pages
- Admin: Only if managing spaces

Bitbucket:
- Read: View repositories
- Write: Create PRs, branches
- Admin: Only if managing repos
```

### Audit Logging

**Log All Operations:**
```
Record:
- Operation type
- User/API token used
- Target resource (issue, page, etc.)
- Timestamp
- Result (success/failure)
- Error details if failed
```

## User Communication

### Initial Response Template
```
I'll help you [create/update/query] [Jira issue/Confluence page/etc.].

Details:
- Target: [Project/Space/Repository]
- Operation: [Specific action]
- Required: [What info is needed]

Do you want me to proceed?
```

### Progress Updates
```
For long operations (bulk, migrations):

Progress: [X/Y items]
- Completed: [count]
- In progress: [current item]
- Failed: [count] (will retry)

Estimated time remaining: [X seconds/minutes]
```

### Completion Report
```
Operation completed successfully!

Created:
- [Resource type]: [ID/Key]
- URL: [Direct link]

Details:
- [Relevant information]
- [Next steps]

Would you like me to:
1. [Follow-up action 1]
2. [Follow-up action 2]
```

### Error Report
```
Operation failed: [Error summary]

Error: [Detailed error message]
Cause: [Root cause]

Attempted recovery:
- [What was tried]
- [Result]

To fix:
1. [Action 1]
2. [Action 2]

Would you like me to:
- Retry with different parameters
- Try alternative approach
- Help troubleshoot the issue
```

## Integration with Other Skills

### With fstrent-task-management
- Sync Jira issues to local task system
- Create Jira issues from local tasks
- Bi-directional updates

### With web-tools
- Scrape Atlassian pages for data
- Extract information from Confluence
- Monitor Jira dashboards

### With database-tools
- Export Atlassian data to database
- Generate reports from combined data
- Analytics and insights

## Best Practices Summary

**Authentication:**
1. ✅ Use API tokens, not passwords
2. ✅ Store securely in environment variables
3. ✅ Rotate tokens regularly
4. ✅ Use minimum required permissions

**Operations:**
1. ✅ Validate inputs before API calls
2. ✅ Use bulk operations for efficiency
3. ✅ Handle rate limiting gracefully
4. ✅ Cache responses appropriately
5. ✅ Log all operations for audit

**Error Handling:**
1. ✅ Implement retry logic with backoff
2. ✅ Provide clear error messages
3. ✅ Suggest corrective actions
4. ✅ Don't expose sensitive details

**User Experience:**
1. ✅ Explain what will happen
2. ✅ Ask for confirmation on destructive operations
3. ✅ Provide progress updates
4. ✅ Return actionable results with URLs

---

**Remember:** Always follow your organization's policies for API access, data handling, and automation. Ensure you have proper authorization before performing operations.
