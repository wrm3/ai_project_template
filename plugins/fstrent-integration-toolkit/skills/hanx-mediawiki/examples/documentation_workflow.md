# Documentation Workflow Examples

This guide demonstrates common documentation workflows using the MediaWiki Integration Skill.

## Example 1: Create Complete Documentation Structure

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager

# Initialize managers
page_manager = PageManager()
cat_manager = CategoryManager()

# Define documentation structure
doc_structure = {
    'Getting Started': {
        'content': '''
# Getting Started

Welcome to our project documentation!

## Quick Start

1. Install dependencies
2. Configure settings
3. Run the application

## Next Steps

- [[Installation Guide]]
- [[Configuration]]
- [[API Reference]]
''',
        'categories': ['Documentation', 'Getting Started']
    },
    'Installation Guide': {
        'content': '''
# Installation Guide

## Prerequisites

- Python 3.8+
- pip package manager
- Git

## Installation Steps

\`\`\`bash
# Clone repository
git clone https://github.com/example/project.git
cd project

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
\`\`\`

## Verification

Run tests to verify installation:

\`\`\`bash
pytest
\`\`\`
''',
        'categories': ['Documentation', 'Installation']
    },
    'API Reference': {
        'content': '''
# API Reference

## Authentication

All API requests require authentication using an API key.

### Example

\`\`\`python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY'
}

response = requests.get('https://api.example.com/users', headers=headers)
\`\`\`

## Endpoints

### Users

- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
''',
        'categories': ['Documentation', 'API', 'Reference']
    }
}

# Create all documentation pages
for title, data in doc_structure.items():
    # Create page
    result = page_manager.create_or_update_page(
        title=f'Docs:{title}',
        content=data['content'],
        summary=f'Created {title} documentation'
    )

    if result['success']:
        print(f"✓ Created: Docs:{title}")

        # Add categories
        for category in data['categories']:
            cat_manager.client.add_category(
                title=f'Docs:{title}',
                category=category,
                summary='Added category'
            )
    else:
        print(f"✗ Failed to create: Docs:{title}")

print("\nDocumentation structure created successfully!")
```

## Example 2: Update All Documentation with Template

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager

page_manager = PageManager()
cat_manager = CategoryManager()

# Get all pages in Documentation category
docs_pages = cat_manager.client.get_pages_in_category('Documentation')

# Template to add to all pages
doc_template = '''
{{Documentation Header
|version=2.0
|status=current
|last_reviewed={{CURRENTDATE}}
}}

'''

# Update each page
updated_count = 0
for page in docs_pages:
    page_title = page['title']

    # Get current content
    current_page = page_manager.client.get_page(page_title)
    if not current_page:
        continue

    current_content = current_page.get('content', '')

    # Skip if template already exists
    if '{{Documentation Header' in current_content:
        print(f"⊘ Skipped (already has template): {page_title}")
        continue

    # Add template at the top
    new_content = doc_template + current_content

    # Update page
    try:
        page_manager.client.edit_page(
            title=page_title,
            content=new_content,
            summary='Added documentation header template'
        )
        print(f"✓ Updated: {page_title}")
        updated_count += 1
    except Exception as e:
        print(f"✗ Failed to update {page_title}: {e}")

print(f"\nUpdated {updated_count} documentation pages")
```

## Example 3: Generate Documentation from Code

```python
from scripts.page_manager import PageManager
import ast
import inspect

page_manager = PageManager()

def generate_function_docs(module_path):
    """Generate documentation from Python module."""

    # Import module
    import importlib.util
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    docs = []

    # Get all functions
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            # Get function signature and docstring
            signature = str(inspect.signature(obj))
            docstring = inspect.getdoc(obj) or "No documentation available"

            docs.append({
                'name': name,
                'signature': signature,
                'doc': docstring
            })

    return docs

def create_api_docs(module_path, wiki_page_title):
    """Create API documentation page from Python module."""

    # Generate docs
    functions = generate_function_docs(module_path)

    # Build wiki content
    content_parts = [
        f"# {wiki_page_title}",
        "",
        "Auto-generated API documentation.",
        "",
        "== Functions ==",
        ""
    ]

    for func in functions:
        content_parts.extend([
            f"=== {func['name']}{func['signature']} ===",
            "",
            func['doc'],
            ""
        ])

    content = '\n'.join(content_parts)

    # Create wiki page
    result = page_manager.create_or_update_page(
        title=wiki_page_title,
        content=content,
        summary="Auto-generated API documentation from source code"
    )

    return result

# Usage
result = create_api_docs(
    module_path='src/api/users.py',
    wiki_page_title='API:Users'
)

if result['success']:
    print("✓ API documentation generated successfully")
```

## Example 4: Sync README to Wiki

```python
from scripts.page_manager import PageManager
from pathlib import Path
import re

page_manager = PageManager()

def convert_github_markdown_to_wikitext(md_content):
    """Convert GitHub Markdown to MediaWiki wikitext."""

    # Convert headers
    md_content = re.sub(r'^### (.+)$', r'=== \1 ===', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^## (.+)$', r'== \1 ==', md_content, flags=re.MULTILINE)
    md_content = re.sub(r'^# (.+)$', r'= \1 =', md_content, flags=re.MULTILINE)

    # Convert code blocks
    md_content = re.sub(r'```(\w+)\n(.*?)\n```',
                       r'<syntaxhighlight lang="\1">\n\2\n</syntaxhighlight>',
                       md_content, flags=re.DOTALL)

    # Convert inline code
    md_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', md_content)

    # Convert bold
    md_content = re.sub(r'\*\*(.+?)\*\*', r"'''\1'''", md_content)

    # Convert italic
    md_content = re.sub(r'\*(.+?)\*', r"''\1''", md_content)

    # Convert links
    md_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'[\2 \1]', md_content)

    return md_content

def sync_readme_to_wiki(readme_path='README.md', wiki_page='Project:README'):
    """Sync README.md to wiki page."""

    # Read README
    readme_content = Path(readme_path).read_text()

    # Convert to wikitext
    wiki_content = convert_github_markdown_to_wikitext(readme_content)

    # Add metadata
    wiki_content = f"""
{{{{Notice|This page is automatically synced from the project README.md}}}}

{wiki_content}

[[Category:Project Documentation]]
[[Category:Auto-Generated]]
"""

    # Update wiki page
    result = page_manager.create_or_update_page(
        title=wiki_page,
        content=wiki_content,
        summary="Synced from README.md"
    )

    return result

# Usage
result = sync_readme_to_wiki()
if result['success']:
    print("✓ README synced to wiki")
```

## Example 5: Create Documentation Index

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager
from scripts.search_manager import SearchManager

page_manager = PageManager()
cat_manager = CategoryManager()
search_manager = SearchManager()

def create_documentation_index():
    """Create an index page of all documentation."""

    # Get all documentation pages
    doc_pages = cat_manager.client.get_pages_in_category('Documentation')

    # Organize by subcategory
    by_category = {}
    for page in doc_pages:
        page_title = page['title']

        # Get categories for this page
        categories = cat_manager.client.get_categories(page_title)

        # Find subcategories (skip "Documentation" itself)
        subcats = [c for c in categories if c != 'Category:Documentation']

        if subcats:
            subcat = subcats[0].replace('Category:', '')
        else:
            subcat = 'General'

        if subcat not in by_category:
            by_category[subcat] = []

        by_category[subcat].append(page_title)

    # Build index content
    content_parts = [
        "= Documentation Index =",
        "",
        "Complete index of all project documentation.",
        "",
        "{{TOC}}",
        ""
    ]

    for category in sorted(by_category.keys()):
        content_parts.extend([
            f"== {category} ==",
            ""
        ])

        for page_title in sorted(by_category[category]):
            # Get page info
            page = page_manager.client.get_page(page_title, get_content=False)
            if page:
                content_parts.append(f"* [[{page_title}]]")

        content_parts.append("")

    # Add statistics
    content_parts.extend([
        "== Statistics ==",
        "",
        f"* Total pages: {len(doc_pages)}",
        f"* Categories: {len(by_category)}",
        "",
        "[[Category:Documentation]]",
        "[[Category:Index]]"
    ])

    content = '\n'.join(content_parts)

    # Create index page
    result = page_manager.create_or_update_page(
        title='Documentation:Index',
        content=content,
        summary="Updated documentation index"
    )

    return result

# Usage
result = create_documentation_index()
if result['success']:
    print("✓ Documentation index created")
```

## Example 6: Find and Fix Broken Links

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager
import re

page_manager = PageManager()
cat_manager = CategoryManager()

def find_broken_links_in_docs():
    """Find and report broken links in documentation."""

    # Get all documentation pages
    doc_pages = cat_manager.client.get_pages_in_category('Documentation')

    broken_links_report = []

    for page in doc_pages:
        page_title = page['title']

        # Get page content
        page_data = page_manager.client.get_page(page_title)
        if not page_data:
            continue

        content = page_data.get('content', '')

        # Find all wiki links
        links = re.findall(r'\[\[([^\]|]+)', content)

        # Check if each linked page exists
        for link in links:
            # Skip special pages and categories
            if link.startswith('Category:') or link.startswith('Special:'):
                continue

            linked_page = page_manager.client.get_page(link, get_content=False)

            if not linked_page:
                broken_links_report.append({
                    'page': page_title,
                    'broken_link': link
                })

    # Generate report
    if broken_links_report:
        print("Broken Links Found:\n")
        current_page = None
        for item in broken_links_report:
            if item['page'] != current_page:
                print(f"\n{item['page']}:")
                current_page = item['page']
            print(f"  - [[{item['broken_link']}]] (page does not exist)")
    else:
        print("✓ No broken links found!")

    return broken_links_report

# Usage
broken_links = find_broken_links_in_docs()
print(f"\nTotal broken links: {len(broken_links)}")
```

## Example 7: Versioned Documentation

```python
from scripts.page_manager import PageManager
from datetime import datetime

page_manager = PageManager()

def create_versioned_docs(content, page_base_name, version):
    """Create versioned documentation pages."""

    # Create current version page
    current_page = f"{page_base_name}"
    versioned_page = f"{page_base_name}/v{version}"

    # Add version notice to content
    versioned_content = f"""
{{{{Version Notice|version={version}|date={datetime.now().strftime('%Y-%m-%d')}}}}}

{content}

== Other Versions ==

* [[{page_base_name}|Latest]]
* [[{page_base_name}/Versions|All Versions]]

[[Category:Documentation]]
[[Category:Version {version}]]
"""

    # Create/update versioned page
    result1 = page_manager.create_or_update_page(
        title=versioned_page,
        content=versioned_content,
        summary=f"Created documentation for version {version}"
    )

    # Update current page to point to latest version
    current_content = f"""
#REDIRECT [[{versioned_page}]]

{{{{Current Version|{version}}}}}
"""

    result2 = page_manager.create_or_update_page(
        title=current_page,
        content=current_content,
        summary=f"Updated to version {version}"
    )

    return result1 and result2

# Usage
doc_content = """
# API Documentation

## Authentication

...
"""

result = create_versioned_docs(
    content=doc_content,
    page_base_name="API:Documentation",
    version="2.0"
)

if result:
    print("✓ Versioned documentation created")
```

## Best Practices

### 1. Use Consistent Naming

```python
# Good naming conventions:
# - Docs:Getting Started
# - API:Authentication
# - Tutorial:Python Basics
# - Reference:CLI Commands

# Avoid:
# - getting_started
# - auth_docs
# - python-tutorial
```

### 2. Add Navigation

```python
# Add navigation to all docs
navigation = """
{{Documentation Navigation
|prev=[[Previous Page]]
|next=[[Next Page]]
|up=[[Parent Page]]
}}
"""
```

### 3. Use Categories Effectively

```python
# Organize with hierarchical categories
categories = [
    'Documentation',  # Top level
    'API Documentation',  # Mid level
    'Authentication'  # Specific
]
```

### 4. Keep Content Updated

```python
# Add last updated timestamp
footer = f"""
---
''Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}''
"""
```

### 5. Version Your Documentation

```python
# Always maintain version history
# Use /vX.Y subpages for versions
# Use redirects for "latest" links
```

## Troubleshooting

### Issue: Formatting looks wrong

**Solution**: MediaWiki uses wikitext, not Markdown. Convert properly:

```python
# Use MediaWiki syntax:
# == Heading == (not ## Heading)
# '''bold''' (not **bold**)
# ''italic'' (not *italic*)
# [[Link]] (not [Link](url))
```

### Issue: Links to non-existent pages

**Solution**: Create placeholder pages:

```python
for link in missing_links:
    page_manager.create_page(
        title=link,
        content=f"# {link}\n\nPage under construction.",
        summary="Created placeholder"
    )
```

### Issue: Slow bulk operations

**Solution**: Add progress reporting and delays:

```python
import time
for i, page in enumerate(pages):
    update_page(page)
    if i % 10 == 0:
        print(f"Progress: {i}/{len(pages)}")
    time.sleep(0.5)
```
