# Knowledge Base Management Examples

Examples for building and maintaining knowledge bases using MediaWiki.

## Example 1: FAQ Management System

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager
from scripts.search_manager import SearchManager

page_manager = PageManager()
cat_manager = CategoryManager()
search_manager = SearchManager()

class FAQManager:
    """Manage FAQ pages in MediaWiki."""

    def __init__(self):
        self.page_manager = PageManager()
        self.cat_manager = CategoryManager()

    def create_faq(self, question, answer, category='General'):
        """Create a new FAQ page."""

        # Sanitize question for page title
        page_title = f"FAQ:{question[:100]}"  # Limit length

        # Build content
        content = f"""
= {question} =

== Answer ==

{answer}

== Related Questions ==

{{{{FAQ Navigation|category={category}}}}}

[[Category:FAQ]]
[[Category:FAQ - {category}]]
"""

        # Create page
        result = self.page_manager.create_or_update_page(
            title=page_title,
            content=content,
            summary=f"Created FAQ: {question}"
        )

        return result

    def update_faq(self, page_title, new_answer):
        """Update an existing FAQ answer."""

        # Get current page
        page = self.page_manager.client.get_page(page_title)
        if not page:
            return {'success': False, 'error': 'FAQ not found'}

        content = page.get('content', '')

        # Replace answer section
        import re
        pattern = r'== Answer ==\n\n(.+?)\n\n=='
        replacement = f'== Answer ==\n\n{new_answer}\n\n=='

        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        # Update page
        return self.page_manager.client.edit_page(
            title=page_title,
            content=new_content,
            summary="Updated FAQ answer"
        )

    def search_faq(self, query):
        """Search FAQ pages."""

        results = search_manager.search_by_category(
            category='FAQ',
            search_query=query,
            limit=20
        )

        return results

    def create_faq_index(self, category=None):
        """Create an index of all FAQs."""

        # Get all FAQ pages
        if category:
            faqs = self.cat_manager.client.get_pages_in_category(f'FAQ - {category}')
        else:
            faqs = self.cat_manager.client.get_pages_in_category('FAQ')

        # Build index
        content_parts = [
            "= Frequently Asked Questions =",
            "",
            "Browse our FAQ database below or use the search box.",
            "",
            "{{FAQ Search Box}}",
            ""
        ]

        # Group by category
        by_category = {}
        for faq in faqs:
            # Get categories
            categories = self.cat_manager.client.get_categories(faq['title'])
            faq_cats = [c.replace('Category:FAQ - ', '')
                       for c in categories
                       if c.startswith('Category:FAQ - ')]

            cat = faq_cats[0] if faq_cats else 'General'

            if cat not in by_category:
                by_category[cat] = []

            by_category[cat].append(faq['title'])

        # Add FAQs by category
        for cat in sorted(by_category.keys()):
            content_parts.extend([
                f"== {cat} ==",
                ""
            ])

            for faq_title in sorted(by_category[cat]):
                # Extract question from title
                question = faq_title.replace('FAQ:', '')
                content_parts.append(f"* [[{faq_title}|{question}]]")

            content_parts.append("")

        content_parts.extend([
            "[[Category:FAQ]]",
            "[[Category:Index]]"
        ])

        content = '\n'.join(content_parts)

        # Create index page
        return self.page_manager.create_or_update_page(
            title='FAQ:Index',
            content=content,
            summary="Updated FAQ index"
        )

# Usage
faq_manager = FAQManager()

# Create FAQs
faq_manager.create_faq(
    question="How do I reset my password?",
    answer="Click 'Forgot Password' on the login page and follow the instructions.",
    category="Account"
)

faq_manager.create_faq(
    question="What are the system requirements?",
    answer="- Python 3.8+\n- 4GB RAM\n- 10GB disk space",
    category="Technical"
)

# Create FAQ index
faq_manager.create_faq_index()

print("✓ FAQ system initialized")
```

## Example 2: Knowledge Article Lifecycle

```python
from scripts.page_manager import PageManager
from datetime import datetime, timedelta

class KnowledgeArticle:
    """Manage knowledge article lifecycle."""

    STATUS_DRAFT = 'draft'
    STATUS_REVIEW = 'review'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'

    def __init__(self, title, content, author):
        self.page_manager = PageManager()
        self.title = f"KB:{title}"
        self.content = content
        self.author = author
        self.status = self.STATUS_DRAFT

    def _build_metadata_template(self):
        """Build metadata template for article."""

        return f"""
{{{{Knowledge Article
|status={self.status}
|author={self.author}
|created={datetime.now().strftime('%Y-%m-%d')}
|last_updated={datetime.now().strftime('%Y-%m-%d')}
}}}}

"""

    def create_draft(self):
        """Create article as draft."""

        full_content = self._build_metadata_template() + self.content
        full_content += "\n\n[[Category:Knowledge Base]]\n[[Category:Draft Articles]]"

        return self.page_manager.create_or_update_page(
            title=self.title,
            content=full_content,
            summary=f"Created draft article by {self.author}"
        )

    def submit_for_review(self):
        """Submit article for review."""

        self.status = self.STATUS_REVIEW

        # Get current content
        page = self.page_manager.client.get_page(self.title)
        if not page:
            return {'success': False, 'error': 'Article not found'}

        content = page.get('content', '')

        # Update status in metadata
        import re
        content = re.sub(
            r'\|status=\w+',
            f'|status={self.status}',
            content
        )

        # Update categories
        content = content.replace(
            '[[Category:Draft Articles]]',
            '[[Category:Articles Under Review]]'
        )

        return self.page_manager.client.edit_page(
            title=self.title,
            content=content,
            summary="Submitted for review"
        )

    def publish(self, reviewer):
        """Publish article."""

        self.status = self.STATUS_PUBLISHED

        page = self.page_manager.client.get_page(self.title)
        if not page:
            return {'success': False, 'error': 'Article not found'}

        content = page.get('content', '')

        # Update status
        import re
        content = re.sub(
            r'\|status=\w+',
            f'|status={self.status}',
            content
        )

        # Add reviewer info
        content = re.sub(
            r'({{Knowledge Article[^}]+)}}',
            f'\\1|reviewer={reviewer}|published={datetime.now().strftime("%Y-%m-%d")}}}',
            content
        )

        # Update categories
        content = content.replace(
            '[[Category:Articles Under Review]]',
            '[[Category:Published Articles]]'
        )

        return self.page_manager.client.edit_page(
            title=self.title,
            content=content,
            summary=f"Published by {reviewer}"
        )

    def archive(self, reason):
        """Archive article."""

        self.status = self.STATUS_ARCHIVED

        page = self.page_manager.client.get_page(self.title)
        if not page:
            return {'success': False, 'error': 'Article not found'}

        content = page.get('content', '')

        # Add archival notice
        archival_notice = f"""
{{{{Archived|date={datetime.now().strftime('%Y-%m-%d')}|reason={reason}}}}}

"""

        content = archival_notice + content

        # Update categories
        content = content.replace(
            '[[Category:Published Articles]]',
            '[[Category:Archived Articles]]'
        )

        return self.page_manager.client.edit_page(
            title=self.title,
            content=content,
            summary=f"Archived: {reason}"
        )

# Usage
article = KnowledgeArticle(
    title="Database Backup Procedures",
    content="""
= Database Backup Procedures =

== Overview ==

This guide explains how to perform database backups.

== Daily Backups ==

...
""",
    author="John Doe"
)

# Lifecycle
article.create_draft()
print("✓ Draft created")

article.submit_for_review()
print("✓ Submitted for review")

article.publish(reviewer="Jane Smith")
print("✓ Published")
```

## Example 3: Internal Wiki Search Portal

```python
from scripts.search_manager import SearchManager
from scripts.page_manager import PageManager

search_manager = SearchManager()
page_manager = PageManager()

def create_search_portal():
    """Create a comprehensive search portal page."""

    content = """
= Knowledge Base Search =

Search our complete knowledge base below.

== Quick Search ==

{{Search Box}}

== Popular Categories ==

* [[Category:FAQ|Frequently Asked Questions]]
* [[Category:How-To Guides]]
* [[Category:Troubleshooting]]
* [[Category:Best Practices]]
* [[Category:API Documentation]]

== Recent Articles ==

{{Recent Articles|limit=10}}

== Most Viewed ==

{{Most Viewed Articles|limit=10|period=30 days}}

== Browse by Topic ==

=== Development ===

* [[KB:Git Workflow]]
* [[KB:Code Review Process]]
* [[KB:Testing Guidelines]]

=== Operations ===

* [[KB:Deployment Process]]
* [[KB:Monitoring Setup]]
* [[KB:Incident Response]]

=== Security ===

* [[KB:Security Best Practices]]
* [[KB:Access Control]]
* [[KB:Vulnerability Management]]

== Contribute ==

Help improve our knowledge base:

* [[KB:Contribution Guidelines]]
* [[Special:CreatePage|Create New Article]]
* [[Special:WantedPages|Most Wanted Pages]]

[[Category:Knowledge Base]]
[[Category:Portal]]
"""

    return page_manager.create_or_update_page(
        title='Portal:Knowledge Base',
        content=content,
        summary="Created knowledge base search portal"
    )

# Usage
result = create_search_portal()
if result['success']:
    print("✓ Search portal created")
```

## Example 4: Automated Article Recommendations

```python
from scripts.search_manager import SearchManager
from scripts.page_manager import PageManager

class ArticleRecommender:
    """Recommend related articles based on content similarity."""

    def __init__(self):
        self.search_manager = SearchManager()
        self.page_manager = PageManager()

    def get_recommendations(self, page_title, num_recommendations=5):
        """Get article recommendations based on similarity."""

        # Get the page content
        page = self.page_manager.client.get_page(page_title)
        if not page:
            return []

        # Use similar pages feature
        similar = self.search_manager.find_similar_pages(
            page_title,
            limit=num_recommendations
        )

        return similar

    def add_recommendations_to_page(self, page_title):
        """Add recommendations section to an article."""

        # Get recommendations
        recommendations = self.get_recommendations(page_title)

        if not recommendations:
            return {'success': False, 'error': 'No recommendations found'}

        # Build recommendations section
        rec_section = "\n\n== Related Articles ==\n\n"

        for rec in recommendations:
            rec_section += f"* [[{rec['title']}]]\n"

        # Append to page
        return self.page_manager.append_to_page(
            title=page_title,
            text=rec_section,
            summary="Added related articles section"
        )

# Usage
recommender = ArticleRecommender()

# Get recommendations
recs = recommender.get_recommendations('KB:Python Best Practices')
print("Recommendations:")
for rec in recs:
    print(f"  - {rec['title']} (similarity: {rec['similarity_score']})")

# Add to page
recommender.add_recommendations_to_page('KB:Python Best Practices')
```

## Example 5: Knowledge Gap Analysis

```python
from scripts.search_manager import SearchManager
from scripts.category_manager import CategoryManager
from collections import Counter
import re

search_manager = SearchManager()
cat_manager = CategoryManager()

def analyze_knowledge_gaps():
    """Identify gaps in knowledge base."""

    # Get all KB pages
    kb_pages = cat_manager.client.get_pages_in_category('Knowledge Base')

    # Track broken links and wanted pages
    broken_links = []
    link_frequency = Counter()

    for page in kb_pages:
        page_data = search_manager.client.get_page(page['title'])
        if not page_data:
            continue

        content = page_data.get('content', '')

        # Find all internal links
        links = re.findall(r'\[\[([^\]|]+)', content)

        for link in links:
            # Skip special pages and categories
            if link.startswith(('Category:', 'Special:', 'File:', 'Template:')):
                continue

            link_frequency[link] += 1

            # Check if page exists
            linked_page = search_manager.client.get_page(link, get_content=False)
            if not linked_page:
                broken_links.append({
                    'from': page['title'],
                    'to': link,
                    'frequency': link_frequency[link]
                })

    # Find most wanted pages (broken links with high frequency)
    wanted_pages = {}
    for item in broken_links:
        link = item['to']
        if link not in wanted_pages:
            wanted_pages[link] = {
                'link': link,
                'count': 0,
                'referenced_by': []
            }
        wanted_pages[link]['count'] += 1
        wanted_pages[link]['referenced_by'].append(item['from'])

    # Sort by frequency
    sorted_wanted = sorted(
        wanted_pages.values(),
        key=lambda x: x['count'],
        reverse=True
    )

    # Create report
    print("=== Knowledge Gap Analysis ===\n")
    print(f"Total KB articles: {len(kb_pages)}")
    print(f"Total unique links: {len(link_frequency)}")
    print(f"Broken links: {len(set(item['to'] for item in broken_links))}\n")

    print("=== Most Wanted Pages (Top 10) ===\n")
    for i, page in enumerate(sorted_wanted[:10], 1):
        print(f"{i}. {page['link']}")
        print(f"   Referenced {page['count']} times by:")
        for ref in page['referenced_by'][:3]:  # Show first 3
            print(f"   - {ref}")
        if len(page['referenced_by']) > 3:
            print(f"   ... and {len(page['referenced_by']) - 3} more")
        print()

    return sorted_wanted

# Usage
wanted_pages = analyze_knowledge_gaps()
```

## Example 6: Article Quality Scoring

```python
from scripts.page_manager import PageManager
from scripts.category_manager import CategoryManager
from datetime import datetime, timedelta

class ArticleQualityAnalyzer:
    """Analyze and score article quality."""

    def __init__(self):
        self.page_manager = PageManager()
        self.cat_manager = CategoryManager()

    def score_article(self, page_title):
        """Score article quality (0-100)."""

        page = self.page_manager.client.get_page(page_title)
        if not page:
            return None

        content = page.get('content', '')
        score = 0

        # Length check (0-20 points)
        word_count = len(content.split())
        if word_count > 500:
            score += 20
        elif word_count > 200:
            score += 10
        elif word_count > 50:
            score += 5

        # Structure check (0-20 points)
        if '==' in content:  # Has sections
            score += 10
        if '===' in content:  # Has subsections
            score += 10

        # Links check (0-15 points)
        import re
        internal_links = len(re.findall(r'\[\[[^\]]+\]\]', content))
        if internal_links > 5:
            score += 15
        elif internal_links > 2:
            score += 10
        elif internal_links > 0:
            score += 5

        # Categories check (0-15 points)
        categories = self.cat_manager.client.get_categories(page_title)
        if len(categories) >= 3:
            score += 15
        elif len(categories) >= 2:
            score += 10
        elif len(categories) >= 1:
            score += 5

        # Metadata check (0-15 points)
        if '{{Knowledge Article' in content or '{{Infobox' in content:
            score += 15

        # Recency check (0-15 points)
        history = self.page_manager.get_page_history(page_title, limit=1)
        if history:
            last_edit = datetime.strptime(
                history[0]['timestamp'],
                '%Y-%m-%dT%H:%M:%SZ'
            )
            days_old = (datetime.now() - last_edit).days

            if days_old < 30:
                score += 15
            elif days_old < 90:
                score += 10
            elif days_old < 180:
                score += 5

        return {
            'score': score,
            'title': page_title,
            'word_count': word_count,
            'internal_links': internal_links,
            'categories': len(categories),
            'rating': self._get_rating(score)
        }

    def _get_rating(self, score):
        """Get quality rating from score."""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Needs Improvement'
        else:
            return 'Poor'

    def analyze_all_articles(self):
        """Analyze all KB articles."""

        kb_pages = self.cat_manager.client.get_pages_in_category('Knowledge Base')

        results = []
        for page in kb_pages:
            score_data = self.score_article(page['title'])
            if score_data:
                results.append(score_data)

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results

# Usage
analyzer = ArticleQualityAnalyzer()

# Analyze single article
score = analyzer.score_article('KB:Python Best Practices')
print(f"Score: {score['score']}/100 ({score['rating']})")
print(f"Word count: {score['word_count']}")
print(f"Internal links: {score['internal_links']}")

# Analyze all articles
all_scores = analyzer.analyze_all_articles()

print("\n=== Article Quality Report ===\n")
print("Top 10 highest quality articles:")
for i, article in enumerate(all_scores[:10], 1):
    print(f"{i}. {article['title']}: {article['score']}/100 ({article['rating']})")

print("\nArticles needing improvement (score < 40):")
poor_articles = [a for a in all_scores if a['score'] < 40]
for article in poor_articles:
    print(f"- {article['title']}: {article['score']}/100")
```

## Best Practices for Knowledge Bases

### 1. Consistent Structure

Use templates for consistency:

```python
KB_TEMPLATE = """
{{{{Knowledge Article
|author={author}
|created={created}
|category={category}
}}}}

= {title} =

== Overview ==

Brief overview of the topic.

== Details ==

Detailed information.

== Examples ==

Practical examples.

== Related Topics ==

* [[Related Article 1]]
* [[Related Article 2]]

[[Category:Knowledge Base]]
[[Category:{category}]]
"""
```

### 2. Regular Maintenance

Schedule regular reviews:

```python
# Find articles not updated in 6 months
old_articles = []
for page in kb_pages:
    history = page_manager.get_page_history(page['title'], limit=1)
    # Check last edit date and flag if > 6 months
```

### 3. Track Metrics

Monitor usage and effectiveness:

```python
# Track:
# - Page views
# - Search queries
# - Broken links
# - Article age
# - Quality scores
```
