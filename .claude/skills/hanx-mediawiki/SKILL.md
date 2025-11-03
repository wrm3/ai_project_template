# MediaWiki Integration Skill

> **Comprehensive MediaWiki API integration for wiki management and documentation**

## Overview

This skill provides complete MediaWiki integration for Claude Code, enabling AI-powered management of wiki content, documentation, and knowledge bases. MediaWiki powers Wikipedia and thousands of enterprise wikis worldwide.

## Quick Start

### Prerequisites

```bash
# Install required Python packages
pip install requests python-dotenv
```

### Environment Setup

Create a `.env` file in your project root:

```bash
MEDIAWIKI_API_URL=https://your-wiki.com/api.php
MEDIAWIKI_USERNAME=your_username
MEDIAWIKI_PASSWORD=your_password_or_bot_token
```

### Basic Usage

```python
from scripts.mediawiki_api import get_mediawiki_client

# Create authenticated client
wiki = get_mediawiki_client(auto_login=True)

# Create a page
wiki.create_page(
    title="My New Page",
    content="This is the page content in **wikitext** format.",
    summary="Created via API"
)

# Search wiki
results = wiki.search("python programming", limit=10)

# Get page content
page = wiki.get_page("Main Page")
print(page['content'])
```

## Core Modules

### 1. MediaWiki API Client (`mediawiki_api.py`)

Low-level API client with full MediaWiki API support.

**Key Features:**
- Authentication (login/logout, bot passwords)
- Page CRUD operations
- Search functionality
- Category management
- File uploads
- Recent changes tracking

**Example:**
```python
from scripts.mediawiki_api import MediaWikiAPI

# Initialize client
client = MediaWikiAPI(
    api_url="https://wiki.example.com/api.php",
    username="bot_user",
    password="bot_password"
)

# Login
client.login()

# Create/edit page
result = client.edit_page(
    title="Tutorial:Python",
    content="# Python Tutorial\n\nLearn Python basics...",
    summary="Initial tutorial creation"
)

# Search
results = client.search("machine learning", limit=20)
for result in results:
    print(f"{result['title']}: {result['snippet']}")

# Logout
client.logout()
```

### 2. Page Manager (`page_manager.py`)

High-level page management utilities.

**Key Features:**
- Bulk page operations
- Page history and revisions
- Move/rename pages
- Page protection
- Content appending/prepending
- Backlink tracking

**Example:**
```python
from scripts.page_manager import PageManager

manager = PageManager()

# Create or update multiple pages
pages = [
    {
        'title': 'Project:Overview',
        'content': '# Project Overview\n\nThis project...',
        'summary': 'Initial overview'
    },
    {
        'title': 'Project:Setup',
        'content': '# Setup Guide\n\nFollow these steps...',
        'summary': 'Setup instructions'
    }
]

results = manager.bulk_create_pages(pages)

# Append to existing page
manager.append_to_page(
    title="Project:Changelog",
    text="\n## Version 2.0\n- New features...",
    summary="Added v2.0 changelog"
)

# Get page history
history = manager.get_page_history("Main Page", limit=10)
for revision in history:
    print(f"{revision['timestamp']}: {revision['comment']}")
```

### 3. Search Manager (`search_manager.py`)

Advanced search capabilities.

**Key Features:**
- Full-text search with ranking
- Title search and prefix matching
- Category-based filtering
- Regex search support
- Similar page discovery
- Search statistics

**Example:**
```python
from scripts.search_manager import SearchManager

search = SearchManager()

# Advanced search with filters
results = search.advanced_search(
    query="API documentation",
    filters={
        'namespace': 0,  # Main namespace
        'min_size': 1000,  # At least 1KB
        'category': 'Documentation'
    },
    limit=10
)

# Find similar pages
similar = search.find_similar_pages("Python Tutorial", limit=5)
for page in similar:
    print(f"{page['title']}: similarity={page['similarity_score']}")

# Search with prefix
prefixed_pages = search.search_prefix("User:", limit=50)
```

### 4. Category Manager (`category_manager.py`)

Category organization and management.

**Key Features:**
- Category tree navigation
- Bulk categorization
- Category merging
- Category analysis
- Automatic category suggestions
- Uncategorized page detection

**Example:**
```python
from scripts.category_manager import CategoryManager

cat_manager = CategoryManager()

# Create category
cat_manager.create_category(
    category_name="API Documentation",
    description="Documentation for our APIs",
    parent_categories=["Documentation", "Technical"]
)

# Bulk categorize pages
cat_manager.bulk_categorize(
    pages=["API:Auth", "API:Users", "API:Data"],
    categories=["API Documentation", "Developer Resources"]
)

# Analyze category
analysis = cat_manager.analyze_category("Documentation")
print(f"Total pages: {analysis['pages']}")
print(f"Subcategories: {analysis['subcategories']}")

# Suggest categories for a page
suggestions = cat_manager.suggest_categories("New API Page")
for suggestion in suggestions:
    print(f"{suggestion['category']}: confidence={suggestion['confidence']}")
```

### 5. File Uploader (`file_uploader.py`)

File upload and media management.

**Key Features:**
- Single and bulk uploads
- Directory uploads
- Duplicate detection
- File metadata management
- Usage tracking
- File re-uploads

**Example:**
```python
from scripts.file_uploader import FileUploader

uploader = FileUploader()

# Upload single file
result = uploader.upload_file(
    filepath="docs/architecture.png",
    wiki_filename="Architecture_Diagram.png",
    description="System architecture overview",
    categories=["Diagrams", "Architecture"]
)

# Bulk upload from directory
results = uploader.upload_directory(
    directory="docs/images/",
    pattern="*.png",
    description_template="Documentation image: {filename}",
    categories=["Documentation", "Images"]
)

# Get file usage
usage = uploader.get_file_usage("Logo.png")
print(f"Logo used in {len(usage)} pages")

# Re-upload new version
uploader.reupload_file(
    filepath="docs/logo_v2.png",
    wiki_filename="Logo.png",
    comment="Updated logo design"
)
```

## Use Cases

### 1. Documentation Project Management

```python
# Automated documentation updates
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager

manager = PageManager()
cat_manager = CategoryManager()

# Create documentation structure
docs = [
    {'title': 'Docs:Getting Started', 'content': '...'},
    {'title': 'Docs:API Reference', 'content': '...'},
    {'title': 'Docs:Examples', 'content': '...'}
]

results = manager.bulk_create_pages(docs)

# Categorize all docs
doc_pages = [d['title'] for d in docs]
cat_manager.bulk_categorize(
    pages=doc_pages,
    categories=["Documentation", "User Guide"]
)
```

### 2. Knowledge Base Maintenance

```python
# Find and fix uncategorized pages
from scripts.category_manager import CategoryManager

cat_manager = CategoryManager()

# Find uncategorized pages
uncategorized = cat_manager.find_uncategorized_pages(limit=100)

# Auto-suggest and apply categories
for page_title in uncategorized:
    suggestions = cat_manager.suggest_categories(page_title, max_suggestions=3)

    if suggestions:
        # Apply top suggestion
        top_category = suggestions[0]['category']
        cat_manager.client.add_category(page_title, top_category)
        print(f"Added {page_title} to {top_category}")
```

### 3. Content Migration

```python
# Migrate content from external source
from scripts.page_manager import PageManager
import json

manager = PageManager()

# Load external content
with open('migration_data.json', 'r') as f:
    data = json.load(f)

# Migrate pages
for item in data:
    manager.create_or_update_page(
        title=item['title'],
        content=item['content'],
        summary=f"Migrated from {item['source']}"
    )
```

### 4. Team Wiki Automation

```python
# Weekly status report automation
from scripts.page_manager import PageManager
from datetime import datetime

manager = PageManager()

# Generate weekly report
week = datetime.now().strftime("%Y-W%W")
report_title = f"Status Reports/{week}"

report_content = f"""
# Weekly Status Report - {week}

## Completed Tasks
* Task 1
* Task 2

## In Progress
* Task 3

## Blockers
* None
"""

manager.create_page(
    title=report_title,
    content=report_content,
    summary=f"Weekly status report for {week}"
)

# Add to archive category
from scripts.category_manager import CategoryManager
cat_manager = CategoryManager()
cat_manager.client.add_category(report_title, "Status Reports")
```

## Advanced Features

### Context Manager Support

All managers support Python context managers:

```python
from scripts.mediawiki_api import get_mediawiki_client
from scripts.page_manager import PageManager

# Automatic login/logout
with get_mediawiki_client() as wiki:
    page = wiki.get_page("Main Page")
    print(page['content'])

# Automatic resource cleanup
with PageManager() as manager:
    manager.create_or_update_page(
        title="Test Page",
        content="Test content"
    )
```

### Error Handling

```python
from scripts.mediawiki_api import MediaWikiAPI, MediaWikiAPIError

try:
    wiki = MediaWikiAPI(api_url="https://wiki.example.com/api.php")
    wiki.login("username", "password")

    result = wiki.create_page(
        title="Test",
        content="Content",
        summary="Test"
    )
except MediaWikiAPIError as e:
    print(f"MediaWiki error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Batch Processing

```python
from scripts.page_manager import PageManager

manager = PageManager()

# Process pages in batches
def update_template(page_title):
    page = manager.client.get_page(page_title)
    if page:
        # Add template to page
        new_content = "{{Infobox}}\n" + page.get('content', '')
        manager.client.edit_page(
            title=page_title,
            content=new_content,
            summary="Added infobox template"
        )

# Get all pages in category
from scripts.category_manager import CategoryManager
cat_manager = CategoryManager()

pages = cat_manager.client.get_pages_in_category("Articles", limit=500)
for page in pages:
    update_template(page['title'])
```

## Best Practices

### 1. Use Bot Passwords

For automated operations, always use bot passwords instead of account passwords:

1. Go to Special:BotPasswords on your wiki
2. Create a new bot password with appropriate permissions
3. Use bot username and password in your `.env` file

### 2. Respect Rate Limits

```python
import time

# Add delays between bulk operations
for page in pages:
    manager.update_page(page)
    time.sleep(0.5)  # 500ms delay
```

### 3. Use Descriptive Edit Summaries

```python
# Good
wiki.edit_page(
    title="API Docs",
    content=new_content,
    summary="Updated API endpoints for v2.0 release"
)

# Bad
wiki.edit_page(
    title="API Docs",
    content=new_content,
    summary="update"
)
```

### 4. Handle Errors Gracefully

```python
from scripts.page_manager import PageManager

manager = PageManager()

pages = ["Page1", "Page2", "Page3"]
results = []

for page_title in pages:
    try:
        result = manager.update_page(page_title, content)
        results.append({'page': page_title, 'success': True})
    except Exception as e:
        results.append({'page': page_title, 'success': False, 'error': str(e)})

# Log results
for r in results:
    if r['success']:
        print(f"✓ {r['page']}")
    else:
        print(f"✗ {r['page']}: {r['error']}")
```

## Security Considerations

1. **Never commit credentials**: Use `.env` files and add them to `.gitignore`
2. **Use bot passwords**: Create dedicated bot accounts with minimal permissions
3. **Validate inputs**: Sanitize user inputs before creating pages
4. **HTTPS only**: Always use HTTPS URLs for API endpoints
5. **Token management**: Tokens are automatically managed and refreshed

## Troubleshooting

### Authentication Issues

```python
# Test connection
from scripts.mediawiki_api import MediaWikiAPI

client = MediaWikiAPI(api_url="https://wiki.example.com/api.php")

try:
    client.login("username", "password")
    print("✓ Login successful")
except Exception as e:
    print(f"✗ Login failed: {e}")
```

### Permission Errors

Ensure your bot account has the necessary permissions:
- `edit` - Edit pages
- `move` - Move pages
- `delete` - Delete pages
- `upload` - Upload files
- `protect` - Protect pages

### API URL Format

Correct API URL format:
```
https://your-wiki.com/api.php
https://your-wiki.com/w/api.php
https://en.wikipedia.org/w/api.php
```

## Integration with Claude Code

This skill is designed for seamless integration with Claude Code workflows:

```python
# Example: Claude Code usage
# User: "Update all pages in the API Documentation category with the new template"

from scripts.category_manager import CategoryManager
from scripts.page_manager import PageManager

cat_manager = CategoryManager()
page_manager = PageManager()

# Get pages in category
pages = cat_manager.client.get_pages_in_category("API Documentation")

# Update each page
for page in pages:
    current = page_manager.client.get_page(page['title'])
    if current:
        new_content = "{{API Template}}\n" + current.get('content', '')
        page_manager.client.edit_page(
            title=page['title'],
            content=new_content,
            summary="Added API template via Claude Code"
        )

print(f"Updated {len(pages)} pages")
```

## API Reference

### MediaWikiAPI

- `login(username, password)` - Authenticate with MediaWiki
- `logout()` - End session
- `get_page(title, get_content=True)` - Retrieve page
- `create_page(title, content, summary)` - Create page
- `edit_page(title, content, summary, ...)` - Edit page
- `delete_page(title, reason)` - Delete page
- `search(query, limit, namespace)` - Search content
- `get_categories(title)` - Get page categories
- `add_category(title, category, summary)` - Add category
- `get_pages_in_category(category, limit)` - List category members
- `upload_file(filename, filepath, description, ...)` - Upload file
- `get_recent_changes(limit, namespace, show_bot)` - Get recent changes

### PageManager

- `create_or_update_page(title, content, summary, force_create)` - Create/update page
- `bulk_create_pages(pages, default_summary)` - Bulk create
- `move_page(from_title, to_title, reason, ...)` - Move/rename
- `protect_page(title, protections, expiry, reason)` - Protect page
- `append_to_page(title, text, summary, section)` - Append content
- `prepend_to_page(title, text, summary)` - Prepend content
- `get_page_history(title, limit)` - Get revision history
- `get_page_links(title, namespace, limit)` - Get outgoing links
- `get_backlinks(title, limit)` - Get incoming links

### SearchManager

- `search_full_text(query, limit, namespace, sort_by)` - Full-text search
- `search_titles(query, limit, namespace)` - Title search
- `search_prefix(prefix, limit, namespace)` - Prefix search
- `search_by_category(category, search_query, limit)` - Category search
- `advanced_search(query, filters, limit)` - Advanced search
- `find_similar_pages(title, limit)` - Find similar pages
- `search_statistics(query)` - Get search stats

### CategoryManager

- `create_category(category_name, description, parent_categories)` - Create category
- `get_category_tree(category, depth, include_pages)` - Get tree
- `get_parent_categories(category, recursive)` - Get parents
- `bulk_categorize(pages, categories, summary)` - Bulk categorize
- `remove_category(page_title, category, summary)` - Remove category
- `find_uncategorized_pages(namespace, limit)` - Find uncategorized
- `suggest_categories(page_title, max_suggestions)` - Suggest categories
- `analyze_category(category)` - Analyze category
- `merge_categories(source, target, delete_source)` - Merge categories

### FileUploader

- `upload_file(filepath, wiki_filename, description, ...)` - Upload file
- `bulk_upload(files, default_description, default_categories)` - Bulk upload
- `upload_directory(directory, pattern, ...)` - Upload directory
- `get_file_info(filename)` - Get file info
- `get_file_usage(filename, limit)` - Get file usage
- `delete_file(filename, reason)` - Delete file
- `reupload_file(filepath, wiki_filename, comment)` - Re-upload file

## Version

**Current Version:** 1.0.0

## License

Part of the AI Project Template - MediaWiki Integration Skill

## Support

For issues, questions, or contributions:
- File issues in the project repository
- Check MediaWiki API documentation: https://www.mediawiki.org/wiki/API:Main_page
- Review skill examples in the `examples/` directory
