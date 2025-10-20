---
name: atlassian-integration
description: Complete integration with Atlassian products (Jira, Confluence, Bitbucket, Trello) for project management and documentation
triggers:
  - jira
  - confluence
  - bitbucket
  - trello
  - create jira issue
  - update confluence
  - pull request
  - atlassian
  - create ticket
  - update documentation
---

# Atlassian Integration Skill

Complete integration with Atlassian ecosystem products enabling AI-powered project management, documentation, code repository operations, and workflow automation.

## Overview

The Atlassian Integration Skill provides seamless interaction with:
- **Jira**: Issue tracking, project management, agile workflows
- **Confluence**: Documentation, knowledge base, collaboration
- **Bitbucket**: Code repositories, pull requests, code review
- **Trello**: Board management, task tracking, automation

## When to Use This Skill

Activate this skill when the user needs to:
- Create, update, or query Jira issues
- Manage Confluence pages and documentation
- Handle Bitbucket repositories and pull requests
- Manage Trello boards, lists, and cards
- Automate Atlassian workflows
- Generate reports from Atlassian data
- Synchronize data between Atlassian products

## Capabilities

### Jira Integration
- **Issue Management**: Create, update, search, transition issues
- **Project Operations**: List projects, get project details
- **Workflow**: Transition issues through workflows
- **Agile**: Sprint management, board operations
- **Bulk Operations**: Bulk create, update issues
- **Custom Fields**: Handle custom field values
- **Comments**: Add, update, delete comments
- **Attachments**: Upload, download attachments
- **JQL Queries**: Advanced issue search with JQL

### Confluence Integration
- **Page Management**: Create, update, delete pages
- **Space Operations**: List, create spaces
- **Content Search**: Full-text search across pages
- **Attachments**: Upload, manage attachments
- **Templates**: Use page templates
- **Permissions**: Manage page/space permissions
- **Labels**: Tag and categorize content
- **Export**: Export pages to PDF/Word
- **Version History**: View and restore versions

### Bitbucket Integration
- **Repository Management**: Create, list, delete repositories
- **Branch Operations**: Create, delete, list branches
- **Pull Requests**: Create, review, merge PRs
- **Code Review**: Comment on code, approve changes
- **Commit History**: View commits, diffs
- **Webhooks**: Configure repository webhooks
- **Pipelines**: Trigger and monitor CI/CD pipelines
- **Access Control**: Manage repository permissions

### Trello Integration
- **Board Management**: Create, update, list boards
- **List Operations**: Create, move, archive lists
- **Card Management**: Create, update, move, archive cards
- **Labels**: Create and assign labels
- **Checklists**: Add and manage checklists
- **Attachments**: Upload files to cards
- **Automation**: Butler automation rules
- **Power-Ups**: Enable and configure power-ups

## MCP Tools Available

This skill can integrate with multiple MCP servers:

### Confluence MCP (`fstrent_mcp_confluence`)
- `confluence_create_page`: Create new page
- `confluence_update_page`: Update existing page
- `confluence_get_page`: Retrieve page content
- `confluence_search`: Search pages
- `confluence_list_spaces`: List all spaces
- `confluence_upload_attachment`: Upload files

### Jira Integration
Note: Jira integration available through REST API or future MCP server

## Usage Examples

### Example 1: Create Jira Issue
```
User: "Create a Jira bug ticket for login failure"

Workflow:
1. Gather issue details:
   - Project: Select or ask user
   - Type: Bug
   - Summary: "Login failure on mobile app"
   - Description: User-provided details
   - Priority: Ask user or default to Medium
2. Create issue via API
3. Return issue key (e.g., PROJ-123)
```

### Example 2: Update Confluence Documentation
```
User: "Update the API documentation page with new endpoint info"

Workflow:
1. Search for "API documentation" page
2. Get current page content
3. Add new endpoint documentation:
   - Endpoint: /api/v2/users
   - Method: GET
   - Parameters: id (required)
   - Response: User object
4. Update page with new content
5. Return page URL
```

### Example 3: Create Pull Request
```
User: "Create PR to merge feature branch to main"

Workflow:
1. Get source branch: feature/new-login
2. Get target branch: main
3. Generate PR description from commits
4. Create pull request with:
   - Title: "Add new login feature"
   - Description: Commit summary
   - Reviewers: Auto-assign or ask user
5. Return PR URL
```

### Example 4: Trello Task Management
```
User: "Add task 'Review PRs' to my Trello TODO list"

Workflow:
1. Find user's board
2. Find "TODO" list
3. Create card:
   - Name: "Review PRs"
   - Description: Optional details
   - Due date: Optional
4. Add to list
5. Return card URL
```

### Example 5: Jira Report Generation
```
User: "Generate report of all open bugs in current sprint"

Workflow:
1. Query Jira with JQL:
   "project = PROJ AND type = Bug AND status != Done AND sprint in openSprints()"
2. Get all matching issues
3. Format report:
   - Total count
   - By priority
   - By assignee
   - By component
4. Return formatted report
```

### Example 6: Confluence Space Setup
```
User: "Create a new Confluence space for the mobile team"

Workflow:
1. Create space:
   - Key: MOBILE
   - Name: "Mobile Team"
   - Type: Documentation
2. Create initial pages:
   - Home page with team info
   - Architecture page
   - Meeting notes page
3. Set permissions (team access)
4. Return space URL
```

### Example 7: Bitbucket Code Review
```
User: "Review the latest PR in our repo"

Workflow:
1. Get latest pull request
2. Get changed files
3. Review code changes:
   - Check for issues
   - Verify tests added
   - Check documentation updated
4. Add review comments
5. Approve or request changes
```

### Example 8: Cross-Product Workflow
```
User: "When Jira issue is closed, update related Confluence page"

Workflow:
1. Get Jira issue details
2. Extract related Confluence page link
3. Update Confluence page:
   - Add status: Completed
   - Add link to resolved issue
   - Update last modified date
4. Comment on Jira issue with page link
```

## Configuration

### Authentication Setup

**Jira:**
```yaml
jira_url: https://yourcompany.atlassian.net
jira_email: your.email@company.com
jira_api_token: <API_TOKEN>
```

**Confluence:**
```yaml
confluence_url: https://yourcompany.atlassian.net/wiki
confluence_email: your.email@company.com
confluence_api_token: <API_TOKEN>
```

**Bitbucket:**
```yaml
bitbucket_url: https://bitbucket.org/yourteam
bitbucket_username: your-username
bitbucket_app_password: <APP_PASSWORD>
```

**Trello:**
```yaml
trello_api_key: <API_KEY>
trello_token: <TOKEN>
```

### API Rate Limits

**Jira Cloud:**
- Standard: ~150 requests/minute
- Premium: ~300 requests/minute

**Confluence Cloud:**
- Standard: ~150 requests/minute

**Bitbucket Cloud:**
- Standard: 60 requests/hour per IP
- Authenticated: 1000 requests/hour

**Trello:**
- 300 requests per 10 seconds per token
- 100 requests per 10-second interval per API key

## Integration Requirements

### Environment Variables
Create `.env.atlassian`:
```bash
# Jira
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_api_token

# Confluence
CONFLUENCE_URL=https://yourcompany.atlassian.net/wiki
CONFLUENCE_EMAIL=your.email@company.com
CONFLUENCE_API_TOKEN=your_api_token

# Bitbucket
BITBUCKET_URL=https://bitbucket.org/yourteam
BITBUCKET_USERNAME=your-username
BITBUCKET_APP_PASSWORD=your_app_password

# Trello
TRELLO_API_KEY=your_api_key
TRELLO_TOKEN=your_token
```

### Required Dependencies
If using scripts directly (not via MCP):
- `requests` - HTTP client
- `python-dotenv` - Environment variable management
- `atlassian-python-api` - Atlassian API wrapper (optional)

## Best Practices

### Jira Best Practices
1. **Use JQL Wisely**: Learn JQL for powerful queries
2. **Batch Operations**: Use bulk APIs for multiple issues
3. **Custom Fields**: Map custom fields correctly
4. **Transitions**: Check valid transitions before attempting
5. **Issue Links**: Use issue links for relationships

### Confluence Best Practices
1. **Page Hierarchy**: Organize pages in logical structure
2. **Templates**: Create reusable page templates
3. **Labels**: Use consistent labeling scheme
4. **Search**: Leverage CQL (Confluence Query Language)
5. **Permissions**: Set appropriate page/space permissions

### Bitbucket Best Practices
1. **Branch Strategy**: Follow gitflow or trunk-based development
2. **PR Templates**: Use PR templates for consistency
3. **Code Review**: Ensure PRs are reviewed before merging
4. **CI/CD**: Configure pipelines for automated testing
5. **Branch Permissions**: Protect important branches

### Trello Best Practices
1. **Board Structure**: Consistent list naming
2. **Labels**: Color-code by priority or type
3. **Checklists**: Break cards into subtasks
4. **Automation**: Use Butler for repetitive tasks
5. **Power-Ups**: Enable useful integrations

## Troubleshooting

### Authentication Issues

**Problem: 401 Unauthorized**
- Check API token is valid
- Verify email/username is correct
- Ensure token has required permissions
- Check if token has expired

**Problem: 403 Forbidden**
- User lacks permissions for operation
- Check project/space permissions
- Verify user role in workspace

### API Rate Limiting

**Problem: 429 Too Many Requests**
- Implement exponential backoff
- Reduce request frequency
- Use bulk operations where possible
- Cache responses when appropriate

### Data Issues

**Problem: Custom field not found**
- List all custom fields first
- Use field ID not field name
- Check field is available for issue type

**Problem: Page/Issue not found**
- Verify ID/key is correct
- Check if deleted or moved
- Ensure user has view permissions

## Security Considerations

### API Token Storage
- ✅ Store tokens in environment variables
- ✅ Never commit tokens to repository
- ✅ Use `.env` files (add to `.gitignore`)
- ✅ Rotate tokens regularly
- ❌ Don't hardcode in scripts

### Permission Management
- ✅ Grant minimum required permissions
- ✅ Use service accounts for automation
- ✅ Audit API token usage regularly
- ✅ Revoke unused tokens

### Data Privacy
- ✅ Respect data classification
- ✅ Don't expose sensitive information
- ✅ Follow company data policies
- ✅ Log API operations for audit trail

## Advanced Features

### JQL (Jira Query Language)
```jql
# Open bugs in current sprint
project = PROJ AND type = Bug AND sprint in openSprints() AND status != Done

# High priority issues assigned to me
assignee = currentUser() AND priority = High

# Recently updated issues
updated >= -7d ORDER BY updated DESC
```

### CQL (Confluence Query Language)
```cql
# Search pages by title
title ~ "API Documentation"

# Pages modified this week
lastModified >= now("-7d")

# Pages in specific space
space = "TEAM" AND type = "page"
```

### Automation Examples

**Auto-create Confluence page from Jira issue:**
```
1. When Jira issue created
2. Create Confluence page in project space
3. Link page to issue
4. Add issue details to page
```

**Auto-update Trello from Jira:**
```
1. When Jira issue status changes
2. Find related Trello card
3. Move card to corresponding list
4. Update card description
```

## Reference Materials

For detailed implementation information, see:
- [reference/jira_guide.md](reference/jira_guide.md) - Jira API and workflows
- [reference/confluence_guide.md](reference/confluence_guide.md) - Confluence operations
- [reference/bitbucket_guide.md](reference/bitbucket_guide.md) - Bitbucket integration
- [reference/trello_guide.md](reference/trello_guide.md) - Trello automation
- [examples/workflow_examples.md](examples/workflow_examples.md) - Common workflows

## Related Skills

- **web-tools**: For scraping Atlassian pages
- **database-tools**: For reporting on Atlassian data
- **fstrent-task-management**: Sync with local task management

---

**Note:** Ensure you have proper authorization and permissions before automating Atlassian operations. Always follow your organization's policies for API access and automation.
