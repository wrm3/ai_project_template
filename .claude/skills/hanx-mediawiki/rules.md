# MediaWiki Integration Skill - Rules

## When to Use This Skill

### Automatic Triggers

This skill should be automatically invoked when the user mentions:

- MediaWiki operations or wiki management
- Wikipedia-style wikis
- Wiki page creation, editing, or management
- Wiki documentation projects
- Knowledge base management using MediaWiki
- Wiki content migration
- Category management on wikis
- File uploads to wikis
- Wiki search operations

### Keywords and Phrases

**Primary Keywords:**
- MediaWiki
- wiki page
- wiki documentation
- knowledge base (if MediaWiki context)
- wiki category
- wiki upload
- wikitext
- wiki search

**Context Indicators:**
- "Create a wiki page for..."
- "Update the wiki documentation..."
- "Search our wiki for..."
- "Upload files to the wiki..."
- "Organize wiki categories..."
- "Migrate content to MediaWiki..."

## Core Principles

### 1. Authentication First

Always ensure proper authentication before performing write operations:

```python
# ✓ GOOD - Explicit login check
if not client._logged_in:
    client.login()

# ✓ GOOD - Use context manager
with get_mediawiki_client(auto_login=True) as wiki:
    wiki.create_page(...)

# ✗ BAD - No authentication check
client.create_page(...)  # May fail if not logged in
```

### 2. Descriptive Edit Summaries

Always provide meaningful edit summaries:

```python
# ✓ GOOD
wiki.edit_page(
    title="API Documentation",
    content=new_content,
    summary="Updated authentication section for v2.0 API"
)

# ✗ BAD
wiki.edit_page(
    title="API Documentation",
    content=new_content,
    summary="update"
)
```

### 3. Error Handling

Always handle errors gracefully:

```python
# ✓ GOOD
try:
    result = wiki.create_page(title, content, summary)
    return {'success': True, 'result': result}
except MediaWikiAPIError as e:
    return {'success': False, 'error': str(e)}

# ✗ BAD
result = wiki.create_page(title, content, summary)  # Unhandled exception
```

### 4. Respect Rate Limits

Add delays for bulk operations:

```python
# ✓ GOOD
import time
for page in pages:
    manager.update_page(page)
    time.sleep(0.5)  # 500ms delay

# ✗ BAD
for page in pages:
    manager.update_page(page)  # May hit rate limits
```

### 5. Validate Inputs

Always validate user inputs:

```python
# ✓ GOOD
if not title or not title.strip():
    raise ValueError("Page title cannot be empty")

# Check for invalid characters
if any(char in title for char in ['<', '>', '[', ']', '{', '}', '|']):
    raise ValueError("Page title contains invalid characters")

# ✗ BAD
wiki.create_page(title, content)  # No validation
```

## Workflow Patterns

### Pattern 1: Single Page Operations

For creating or editing individual pages:

```python
from scripts.mediawiki_api import get_mediawiki_client

# 1. Authenticate
wiki = get_mediawiki_client(auto_login=True)

# 2. Perform operation
result = wiki.create_page(
    title="New Page",
    content="Page content",
    summary="Page created via Claude Code"
)

# 3. Verify success
if 'edit' in result:
    print(f"✓ Page created successfully")
else:
    print(f"✗ Failed to create page")
```

### Pattern 2: Bulk Operations

For processing multiple pages:

```python
from scripts.page_manager import PageManager

manager = PageManager()

pages = [...]  # List of pages to process

# Process with error tracking
results = []
for page_data in pages:
    try:
        result = manager.create_or_update_page(
            title=page_data['title'],
            content=page_data['content']
        )
        results.append({'page': page_data['title'], 'success': True})
    except Exception as e:
        results.append({'page': page_data['title'], 'success': False, 'error': str(e)})

# Report results
successful = sum(1 for r in results if r['success'])
print(f"Processed {len(results)} pages: {successful} successful, {len(results) - successful} failed")
```

### Pattern 3: Search and Process

For finding and processing pages based on search:

```python
from scripts.search_manager import SearchManager
from scripts.page_manager import PageManager

search = SearchManager()
manager = PageManager()

# 1. Search for pages
results = search.search_full_text("outdated template", limit=50)

# 2. Process each result
for result in results:
    page = manager.client.get_page(result['title'])
    if page:
        # Update content
        updated_content = update_template(page['content'])
        manager.client.edit_page(
            title=result['title'],
            content=updated_content,
            summary="Updated template via automated process"
        )
```

### Pattern 4: Category Organization

For managing categories:

```python
from scripts.category_manager import CategoryManager

cat_manager = CategoryManager()

# 1. Find uncategorized pages
uncategorized = cat_manager.find_uncategorized_pages(limit=100)

# 2. Auto-categorize based on suggestions
for page_title in uncategorized:
    suggestions = cat_manager.suggest_categories(page_title, max_suggestions=1)

    if suggestions and suggestions[0]['confidence'] > 0.5:
        category = suggestions[0]['category']
        cat_manager.client.add_category(
            title=page_title,
            category=category,
            summary=f"Auto-categorized based on content similarity"
        )
```

## Best Practices

### Security

1. **Never hardcode credentials** - Use environment variables
2. **Use bot passwords** - Create dedicated bot accounts
3. **Validate all inputs** - Prevent injection attacks
4. **Use HTTPS** - Always use secure connections
5. **Minimal permissions** - Grant only necessary permissions

### Performance

1. **Batch operations** - Use bulk methods when available
2. **Add delays** - Respect rate limits (0.5-1s between requests)
3. **Cache results** - Store frequently accessed data
4. **Limit queries** - Use appropriate `limit` parameters
5. **Use namespaces** - Filter by namespace to reduce results

### Maintainability

1. **Descriptive summaries** - Always explain what changed
2. **Log operations** - Track all changes
3. **Handle errors** - Graceful error handling
4. **Test changes** - Verify operations succeed
5. **Document code** - Comment complex operations

## Common Pitfalls

### Pitfall 1: Missing Authentication

**Problem:**
```python
wiki = MediaWikiAPI(api_url="...")
wiki.create_page(...)  # Fails - not logged in
```

**Solution:**
```python
wiki = MediaWikiAPI(api_url="...")
wiki.login()
wiki.create_page(...)
```

### Pitfall 2: Not Handling Page Not Found

**Problem:**
```python
page = wiki.get_page("Nonexistent Page")
content = page['content']  # Fails - page is None
```

**Solution:**
```python
page = wiki.get_page("Nonexistent Page")
if page:
    content = page['content']
else:
    print("Page not found")
```

### Pitfall 3: Overwriting Content Accidentally

**Problem:**
```python
wiki.edit_page(title, new_content)  # Overwrites entire page
```

**Solution:**
```python
# If you want to append:
manager.append_to_page(title, new_content)

# If you want to update:
page = wiki.get_page(title)
if page:
    updated = page['content'] + "\n" + new_content
    wiki.edit_page(title, updated)
```

### Pitfall 4: Category Naming

**Problem:**
```python
wiki.add_category("Page", "Documentation")  # Works
wiki.add_category("Page", "Category:Documentation")  # Also works - redundant prefix
```

**Solution:**
```python
# The API handles both formats, but be consistent:
wiki.add_category("Page", "Documentation")  # Preferred - API adds prefix
```

### Pitfall 5: Not Checking File Extensions

**Problem:**
```python
uploader.upload_file("malware.exe")  # May fail or be blocked
```

**Solution:**
```python
allowed_extensions = {'.png', '.jpg', '.pdf', '.txt'}
if filepath.suffix.lower() in allowed_extensions:
    uploader.upload_file(filepath)
else:
    print(f"File type {filepath.suffix} not allowed")
```

## Integration Guidelines

### With Claude Code Workflows

When Claude Code uses this skill:

1. **Ask for confirmation** before bulk operations
2. **Show preview** of changes when possible
3. **Report progress** for long-running operations
4. **Provide summary** of what was done
5. **Handle errors gracefully** and report to user

Example:
```python
# Claude Code should do this:
print("About to update 50 pages in the Documentation category.")
print("Preview of changes:")
print("- Adding {{Infobox}} template")
print("- Adding to Category:Technical Documentation")

# Ask for confirmation
response = input("Proceed? (y/n): ")
if response.lower() == 'y':
    # Perform operation with progress reporting
    for i, page in enumerate(pages):
        update_page(page)
        if i % 10 == 0:
            print(f"Progress: {i}/{len(pages)} pages updated")
```

### With Other Skills

This skill can be combined with:

- **fstrent-planning**: Document project plans on wiki
- **fstrent-task-management**: Sync tasks to wiki pages
- **github-integration**: Link GitHub issues to wiki documentation
- **atlassian-integration**: Migrate Confluence to MediaWiki

## Cursor IDE Compatibility

This skill is fully compatible with Cursor IDE:

- Use the same file paths and imports
- Environment variables work identically
- All examples are IDE-agnostic
- Can be invoked via Cursor's AI features

## Troubleshooting

### Connection Issues

```python
# Test connection
try:
    response = requests.get(api_url)
    print(f"✓ API endpoint reachable: {response.status_code}")
except Exception as e:
    print(f"✗ Cannot reach API endpoint: {e}")
```

### Authentication Failures

```python
# Verify credentials
import os
from dotenv import load_dotenv

load_dotenv()

print(f"API URL: {os.getenv('MEDIAWIKI_API_URL')}")
print(f"Username: {os.getenv('MEDIAWIKI_USERNAME')}")
print(f"Password: {'*' * len(os.getenv('MEDIAWIKI_PASSWORD', ''))}")
```

### Permission Errors

Common permission requirements:
- `read` - Read pages (usually granted to all)
- `edit` - Edit pages
- `createpage` - Create new pages
- `move` - Move/rename pages
- `delete` - Delete pages
- `upload` - Upload files
- `protect` - Protect pages

## Claude Code AI Instructions

When Claude Code uses this skill, it should:

1. **Always validate environment variables** before operations
2. **Use context managers** when possible
3. **Provide clear feedback** on operations
4. **Handle errors gracefully** with user-friendly messages
5. **Suggest related operations** based on context
6. **Preview changes** before applying in bulk
7. **Log all operations** for audit trail
8. **Respect rate limits** automatically
9. **Offer to undo** if operation seems incorrect
10. **Learn from errors** and adjust approach

## Version Compatibility

- **MediaWiki API**: 1.19+
- **Python**: 3.7+
- **Dependencies**: requests, python-dotenv

## Updates and Maintenance

Check for updates:
- MediaWiki API changes
- New features and endpoints
- Security updates
- Bug fixes

Report issues:
- File in project issue tracker
- Include MediaWiki version
- Provide error messages
- Share minimal reproduction code
