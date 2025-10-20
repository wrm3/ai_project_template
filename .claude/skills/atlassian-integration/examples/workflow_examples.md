# Atlassian Integration - Workflow Examples

## Jira Examples

### Create Bug Issue
```
User: "Create a bug for login failure on mobile"

jira_create_issue(
  project="MOBILE",
  type="Bug",
  summary="Login fails on iOS app",
  description="Users report login button not responding",
  priority="High"
)
→ Returns: MOBILE-123 (https://company.atlassian.net/browse/MOBILE-123)
```

### Query Open Bugs
```
User: "Show all open bugs in current sprint"

JQL: project = MOBILE AND type = Bug AND sprint in openSprints() AND status != Done
→ Returns: List of 15 bugs with details
```

### Transition Issue
```
User: "Move MOBILE-123 to In Progress"

jira_transition_issue(
  issue_key="MOBILE-123",
  transition="In Progress",
  comment="Starting work on this"
)
→ Returns: Success, issue now In Progress
```

## Confluence Examples

### Create Documentation Page
```
User: "Create API docs page in TEAM space"

confluence_create_page(
  space="TEAM",
  title="API Documentation v2.0",
  content="<h1>API Endpoints</h1><p>...</p>",
  parent_id=null
)
→ Returns: Page ID 12345 (https://company.atlassian.net/wiki/spaces/TEAM/pages/12345)
```

### Update Page
```
User: "Update the architecture page with new diagram"

confluence_update_page(
  page_id=12345,
  content="<updated content>",
  version_increment=true
)
→ Returns: Success, page version now 4
```

### Search Documentation
```
User: "Find pages about authentication"

CQL: space = TEAM AND text ~ "authentication"
→ Returns: 8 pages matching search
```

## Bitbucket Examples

### Create Pull Request
```
User: "Create PR from feature/login to main"

bitbucket_create_pr(
  repository="mobile-app",
  source_branch="feature/login",
  target_branch="main",
  title="Add biometric login",
  reviewers=["john.doe", "jane.smith"]
)
→ Returns: PR #42 (https://bitbucket.org/company/mobile-app/pull-requests/42)
```

### Review Code
```
User: "Review PR #42"

1. Get PR changes
2. Check for issues
3. Add comments
4. Approve or request changes
→ Returns: Review submitted
```

## Trello Examples

### Create Task Card
```
User: "Add 'Review PRs' to my TODO list"

trello_create_card(
  board_id="abc123",
  list_name="TODO",
  name="Review PRs",
  due_date="2025-10-20"
)
→ Returns: Card ID xyz789 (https://trello.com/c/xyz789)
```

### Move Card
```
User: "Move card to Done"

trello_move_card(
  card_id="xyz789",
  target_list="Done"
)
→ Returns: Card moved successfully
```

## Cross-Product Workflows

### Jira → Confluence
```
When bug is created → Create documentation page

1. Jira bug MOBILE-123 created
2. Create Confluence page "Bug Analysis: MOBILE-123"
3. Add technical details to page
4. Link page in Jira issue
```

### Bitbucket → Jira
```
When PR merged → Update Jira issues

1. PR #42 merged
2. Extract MOBILE-123 from commits
3. Add comment to MOBILE-123: "Fixed in PR #42"
4. Transition to "Ready for QA"
```

### Trello → Jira
```
Convert Trello card to Jira issue

1. Trello card: "Fix login bug"
2. Create Jira issue with same details
3. Link Trello card to Jira issue
4. Archive Trello card (optional)
```

---

For detailed implementation, see [../rules.md](../rules.md) and [../SKILL.md](../SKILL.md).
