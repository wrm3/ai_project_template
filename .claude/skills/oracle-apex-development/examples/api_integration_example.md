# Third-Party API Integration Example

## Overview
Integrate GitHub API to display user repositories and activity within APEX application.

## REST Data Source Configuration

### GitHub User API
```yaml
REST Data Source: GitHub User
Base URL: https://api.github.com
Service URL: /users/:username

Method: GET
Request Headers:
  - Accept: application/vnd.github.v3+json
  - User-Agent: APEX-Integration

Parameters:
  - username (URL Pattern Parameter)

Response Column Mappings:
  - LOGIN: $.login
  - NAME: $.name
  - BIO: $.bio
  - FOLLOWERS: $.followers
  - PUBLIC_REPOS: $.public_repos
  - AVATAR_URL: $.avatar_url
  - CREATED_AT: $.created_at
```

### GitHub Repositories API
```yaml
REST Data Source: GitHub Repos
Service URL: /users/:username/repos

Method: GET
Response Column Mappings:
  - REPO_NAME: $.name
  - DESCRIPTION: $.description
  - STARS: $.stargazers_count
  - FORKS: $.forks_count
  - LANGUAGE: $.language
  - UPDATED_AT: $.updated_at
```

## Application Pages

### Page 10: GitHub User Search
```yaml
Page Items:
  - P10_USERNAME (Text Field, placeholder: "Enter GitHub username")

Button: Search
  Action: Submit Page

Dynamic Action: On Page Load
  - Set Focus to P10_USERNAME
```

### Page 20: User Profile Display
```sql
-- Region: User Information
-- Source Type: REST Data Source
-- REST Source: GitHub User

SELECT login,
       name,
       bio,
       followers,
       public_repos,
       avatar_url
FROM   #APEX$SOURCE_DATA#
WHERE  :P10_USERNAME IS NOT NULL

-- Parameters: username = :P10_USERNAME
```

```html
<!-- HTML Expression for Avatar -->
<img src="&AVATAR_URL." alt="&NAME." 
     style="width:100px; border-radius:50%;">
<h2>&NAME.</h2>
<p>&BIO.</p>
<p>Followers: &FOLLOWERS. | Repos: &PUBLIC_REPOS.</p>
```

### Page 20: Repositories List
```sql
-- Region: Repositories
-- Source Type: REST Data Source
-- REST Source: GitHub Repos

SELECT repo_name,
       description,
       stars,
       forks,
       language,
       updated_at
FROM   #APEX$SOURCE_DATA#
ORDER BY stars DESC

-- Interactive Report with columns:
-- - Repository Name (link to GitHub)
-- - Description
-- - Stars
-- - Forks
-- - Language
-- - Last Updated
```

## Error Handling

### PL/SQL Error Handler
```plsql
-- Application Process: Handle API Errors
DECLARE
    l_response CLOB;
BEGIN
    IF apex_web_service.g_status_code != 200 THEN
        apex_error.add_error(
            p_message => 'GitHub API Error: ' || 
                         apex_web_service.g_status_code,
            p_display_location => apex_error.c_inline_in_notification
        );
    END IF;
END;
```

## OAuth 2.0 Integration (Optional)

### For Private Repositories
```yaml
Web Credentials:
  Name: GitHub OAuth
  Type: OAuth2 Client Credentials
  Client ID: your_github_client_id
  Client Secret: your_github_client_secret
  Authorization URL: https://github.com/login/oauth/authorize
  Token URL: https://github.com/login/oauth/access_token
  Scope: repo, user

REST Data Source:
  Authentication: Web Credentials
  Credentials: GitHub OAuth
```

## Features
- Search GitHub users
- Display user profile information
- List user repositories with statistics
- OAuth authentication for private repos
- Error handling for API failures
- Rate limit monitoring
- Cache API responses (5 minutes)
- Export repository list to CSV

## Testing
1. Enter valid GitHub username (e.g., "torvalds")
2. Verify user profile displays correctly
3. Check repositories list loads
4. Test error handling with invalid username
5. Test rate limit handling
6. Verify OAuth flow (if implemented)

## Production Considerations
- Implement caching to reduce API calls
- Handle rate limits (GitHub: 60 req/hour unauthenticated)
- Use OAuth for higher rate limits (5000 req/hour)
- Error messages for failed requests
- Retry logic with exponential backoff
- Monitor API usage
