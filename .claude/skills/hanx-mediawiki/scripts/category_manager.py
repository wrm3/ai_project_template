"""
MediaWiki Category Manager

Utilities for managing categories, category trees, and page categorization.
"""

from typing import List, Dict, Optional, Any, Set
from collections import defaultdict
from .mediawiki_api import MediaWikiAPI, get_mediawiki_client


class CategoryManager:
    """
    Category management for MediaWiki.

    Provides tools for:
    - Category tree navigation
    - Bulk categorization
    - Category analysis
    - Automatic category suggestions
    """

    def __init__(self, client: Optional[MediaWikiAPI] = None):
        """
        Initialize category manager.

        Args:
            client: Optional MediaWikiAPI instance
        """
        self.client = client or get_mediawiki_client()

    def create_category(
        self,
        category_name: str,
        description: str,
        parent_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new category page.

        Args:
            category_name: Category name (without "Category:" prefix)
            description: Category description
            parent_categories: List of parent categories

        Returns:
            Creation result
        """
        # Ensure proper category title
        if not category_name.startswith('Category:'):
            category_title = f'Category:{category_name}'
        else:
            category_title = category_name

        # Build category page content
        content_parts = [description]

        # Add parent categories
        if parent_categories:
            content_parts.append('')  # Blank line
            for parent in parent_categories:
                if not parent.startswith('Category:'):
                    parent = f'Category:{parent}'
                content_parts.append(f'[[{parent}]]')

        content = '\n'.join(content_parts)

        return self.client.create_page(
            category_title,
            content,
            summary=f"Created category {category_name}"
        )

    def get_category_tree(
        self,
        category: str,
        depth: int = 2,
        include_pages: bool = False
    ) -> Dict[str, Any]:
        """
        Get category tree (subcategories and optionally pages).

        Args:
            category: Root category name
            depth: How many levels deep to traverse
            include_pages: Whether to include pages (not just subcategories)

        Returns:
            Category tree structure
        """
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        def _traverse_category(cat: str, current_depth: int) -> Dict[str, Any]:
            if current_depth <= 0:
                return {'name': cat, 'subcategories': [], 'pages': []}

            # Get category members
            params = {
                'action': 'query',
                'list': 'categorymembers',
                'cmtitle': cat,
                'cmlimit': 500,
                'cmprop': 'title|type'
            }

            response = self.client._request(params)
            members = response['query']['categorymembers']

            subcategories = []
            pages = []

            for member in members:
                if member['type'] == 'subcat':
                    # Recursively get subcategory tree
                    subtree = _traverse_category(member['title'], current_depth - 1)
                    subcategories.append(subtree)
                elif include_pages and member['type'] == 'page':
                    pages.append(member['title'])

            return {
                'name': cat,
                'subcategories': subcategories,
                'pages': pages if include_pages else []
            }

        return _traverse_category(category, depth)

    def get_parent_categories(
        self,
        category: str,
        recursive: bool = False
    ) -> List[str]:
        """
        Get parent categories of a category.

        Args:
            category: Category name
            recursive: If True, get all ancestor categories

        Returns:
            List of parent category names
        """
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        parents = self.client.get_categories(category)

        if not recursive:
            return parents

        # Recursively get all ancestors
        all_ancestors = set(parents)
        for parent in parents:
            grandparents = self.get_parent_categories(parent, recursive=True)
            all_ancestors.update(grandparents)

        return list(all_ancestors)

    def bulk_categorize(
        self,
        pages: List[str],
        categories: List[str],
        summary: str = "Bulk categorization via API"
    ) -> List[Dict[str, Any]]:
        """
        Add categories to multiple pages.

        Args:
            pages: List of page titles
            categories: List of category names to add
            summary: Edit summary

        Returns:
            List of results for each page
        """
        results = []

        for page in pages:
            try:
                page_results = []
                for category in categories:
                    result = self.client.add_category(page, category, summary)
                    page_results.append(result)

                results.append({
                    'page': page,
                    'success': True,
                    'categories_added': categories,
                    'results': page_results
                })
            except Exception as e:
                results.append({
                    'page': page,
                    'success': False,
                    'error': str(e)
                })

        return results

    def remove_category(
        self,
        page_title: str,
        category: str,
        summary: str = "Category removed via API"
    ) -> Dict[str, Any]:
        """
        Remove a category from a page.

        Args:
            page_title: Page title
            category: Category name to remove
            summary: Edit summary

        Returns:
            Edit result
        """
        # Ensure category has proper prefix
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        # Get current page content
        page = self.client.get_page(page_title)
        if not page:
            return {'success': False, 'error': 'Page not found'}

        content = page.get('content', '')

        # Remove category (handle various formats)
        category_patterns = [
            f'[[{category}]]',
            f'[[{category}|',  # Category with sort key
        ]

        modified = False
        for pattern in category_patterns:
            if pattern in content:
                # For sort keys, we need to find the complete category link
                if pattern.endswith('|'):
                    import re
                    # Find [[Category:Name|SortKey]]
                    regex = re.escape(pattern) + r'[^\]]*\]\]'
                    content = re.sub(regex, '', content)
                else:
                    content = content.replace(pattern, '')
                modified = True

        if not modified:
            return {'success': False, 'error': 'Category not found on page'}

        # Clean up extra newlines
        content = '\n'.join(line for line in content.split('\n') if line.strip() or not line)

        return self.client.edit_page(page_title, content, summary)

    def get_category_members_detailed(
        self,
        category: str,
        member_type: str = 'all',
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get detailed information about category members.

        Args:
            category: Category name
            member_type: Type of members ('page', 'subcat', 'file', 'all')
            limit: Maximum number of members

        Returns:
            List of detailed member information
        """
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': category,
            'cmlimit': limit,
            'cmprop': 'title|type|timestamp|ids'
        }

        if member_type != 'all':
            params['cmtype'] = member_type

        response = self.client._request(params)
        return response['query']['categorymembers']

    def find_uncategorized_pages(
        self,
        namespace: int = 0,
        limit: int = 100
    ) -> List[str]:
        """
        Find pages without categories.

        Args:
            namespace: Namespace to search
            limit: Maximum number of pages

        Returns:
            List of uncategorized page titles
        """
        params = {
            'action': 'query',
            'list': 'allpages',
            'aplimit': limit,
            'apnamespace': namespace
        }

        response = self.client._request(params)
        all_pages = response['query']['allpages']

        uncategorized = []

        for page in all_pages:
            categories = self.client.get_categories(page['title'])
            if not categories:
                uncategorized.append(page['title'])

        return uncategorized

    def suggest_categories(
        self,
        page_title: str,
        max_suggestions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Suggest categories for a page based on similar pages.

        Uses content similarity and existing categorizations.

        Args:
            page_title: Page to suggest categories for
            max_suggestions: Maximum number of suggestions

        Returns:
            List of category suggestions with confidence scores
        """
        # Get page content
        page = self.client.get_page(page_title)
        if not page:
            return []

        # Search for similar pages
        search_results = self.client.search(page_title, limit=20)

        # Collect categories from similar pages
        category_counts = defaultdict(int)

        for result in search_results[:10]:  # Check top 10 results
            similar_title = result['title']
            if similar_title == page_title:
                continue

            categories = self.client.get_categories(similar_title)
            for category in categories:
                category_counts[category] += 1

        # Sort by frequency and create suggestions
        sorted_categories = sorted(
            category_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        suggestions = []
        for category, count in sorted_categories[:max_suggestions]:
            suggestions.append({
                'category': category,
                'confidence': count / 10.0,  # Normalize to 0-1 range
                'found_in_similar_pages': count
            })

        return suggestions

    def analyze_category(self, category: str) -> Dict[str, Any]:
        """
        Analyze a category to get statistics and insights.

        Args:
            category: Category name

        Returns:
            Analysis results
        """
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        # Get all members
        members = self.get_category_members_detailed(category, limit=500)

        # Count by type
        type_counts = defaultdict(int)
        for member in members:
            type_counts[member['type']] += 1

        # Get subcategories
        subcats = [m['title'] for m in members if m['type'] == 'subcat']

        # Get parent categories
        parents = self.client.get_categories(category)

        return {
            'category': category,
            'total_members': len(members),
            'pages': type_counts.get('page', 0),
            'subcategories': type_counts.get('subcat', 0),
            'files': type_counts.get('file', 0),
            'parent_categories': parents,
            'subcategory_list': subcats,
            'depth': len(parents)  # Approximate depth in category tree
        }

    def merge_categories(
        self,
        source_category: str,
        target_category: str,
        delete_source: bool = False
    ) -> Dict[str, Any]:
        """
        Merge one category into another.

        Args:
            source_category: Category to merge from
            target_category: Category to merge into
            delete_source: Whether to delete source category after merge

        Returns:
            Merge results
        """
        # Get all pages in source category
        source_pages = self.client.get_pages_in_category(source_category, limit=500)

        results = {
            'pages_moved': 0,
            'errors': [],
            'source_deleted': False
        }

        # Move all pages to target category
        for page in source_pages:
            page_title = page['title']

            # Skip if it's a subcategory
            if page_title.startswith('Category:'):
                continue

            try:
                # Remove from source, add to target
                self.remove_category(page_title, source_category)
                self.client.add_category(page_title, target_category)
                results['pages_moved'] += 1
            except Exception as e:
                results['errors'].append({
                    'page': page_title,
                    'error': str(e)
                })

        # Optionally delete source category
        if delete_source and not results['errors']:
            try:
                self.client.delete_page(
                    source_category,
                    reason=f"Merged into {target_category}"
                )
                results['source_deleted'] = True
            except Exception as e:
                results['errors'].append({
                    'action': 'delete_source',
                    'error': str(e)
                })

        return results

    def get_category_intersection(
        self,
        categories: List[str],
        limit: int = 100
    ) -> List[str]:
        """
        Find pages that belong to ALL specified categories.

        Args:
            categories: List of category names
            limit: Maximum number of results

        Returns:
            List of pages in all categories
        """
        if not categories:
            return []

        # Get pages from first category
        pages_sets = []

        for category in categories:
            pages = self.client.get_pages_in_category(category, limit=limit)
            page_titles = {p['title'] for p in pages}
            pages_sets.append(page_titles)

        # Find intersection
        common_pages = pages_sets[0]
        for page_set in pages_sets[1:]:
            common_pages &= page_set

        return list(common_pages)[:limit]
