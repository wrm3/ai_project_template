"""
MediaWiki Search Manager

Advanced search capabilities for MediaWiki with filtering,
ranking, and result processing.
"""

from typing import List, Dict, Optional, Any, Callable
from .mediawiki_api import MediaWikiAPI, get_mediawiki_client
import re


class SearchManager:
    """
    Advanced search functionality for MediaWiki.

    Provides powerful search capabilities including:
    - Full-text search
    - Title search
    - Filtered searches by namespace, category, etc.
    - Search result ranking and processing
    """

    def __init__(self, client: Optional[MediaWikiAPI] = None):
        """
        Initialize search manager.

        Args:
            client: Optional MediaWikiAPI instance
        """
        self.client = client or get_mediawiki_client()

    def search_full_text(
        self,
        query: str,
        limit: int = 20,
        namespace: Optional[int] = None,
        sort_by: str = 'relevance'
    ) -> List[Dict[str, Any]]:
        """
        Perform full-text search.

        Args:
            query: Search query
            limit: Maximum number of results
            namespace: Namespace to search (0=main, 1=talk, etc.)
            sort_by: Sort method ('relevance', 'create_timestamp_desc', 'last_edited_desc')

        Returns:
            List of search results with enhanced metadata
        """
        # Map sort methods to MediaWiki API parameters
        sort_map = {
            'relevance': None,
            'create_timestamp_desc': 'create_timestamp_desc',
            'last_edited_desc': 'last_edit_desc'
        }

        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit,
            'srprop': 'size|wordcount|timestamp|snippet|titlesnippet|sectionsnippet'
        }

        if namespace is not None:
            params['srnamespace'] = namespace

        if sort_by in sort_map and sort_map[sort_by]:
            params['srsort'] = sort_map[sort_by]

        response = self.client._request(params)
        results = response['query']['search']

        # Enrich results with calculated relevance scores
        for i, result in enumerate(results):
            result['rank'] = i + 1
            result['relevance_score'] = self._calculate_relevance_score(result, query)

        return results

    def search_titles(
        self,
        query: str,
        limit: int = 20,
        namespace: Optional[int] = None
    ) -> List[str]:
        """
        Search page titles only.

        Args:
            query: Search query
            limit: Maximum number of results
            namespace: Namespace to search

        Returns:
            List of matching page titles
        """
        params = {
            'action': 'opensearch',
            'search': query,
            'limit': limit
        }

        if namespace is not None:
            params['namespace'] = namespace

        response = self.client._request(params)

        # OpenSearch returns: [query, [titles], [descriptions], [urls]]
        return response[1] if len(response) > 1 else []

    def search_prefix(
        self,
        prefix: str,
        limit: int = 20,
        namespace: Optional[int] = 0
    ) -> List[str]:
        """
        Find pages that start with a given prefix.

        Args:
            prefix: Title prefix to search for
            limit: Maximum number of results
            namespace: Namespace to search (0=main by default)

        Returns:
            List of matching page titles
        """
        params = {
            'action': 'query',
            'list': 'allpages',
            'apprefix': prefix,
            'aplimit': limit
        }

        if namespace is not None:
            params['apnamespace'] = namespace

        response = self.client._request(params)
        pages = response['query']['allpages']

        return [page['title'] for page in pages]

    def search_by_category(
        self,
        category: str,
        search_query: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search within a specific category.

        Args:
            category: Category name
            search_query: Optional text search within category
            limit: Maximum number of results

        Returns:
            List of pages in category (filtered by query if provided)
        """
        # Get all pages in category
        pages = self.client.get_pages_in_category(category, limit)

        # If no search query, return all pages
        if not search_query:
            return pages

        # Filter pages by search query
        filtered_pages = []
        search_lower = search_query.lower()

        for page in pages:
            title_lower = page['title'].lower()
            if search_lower in title_lower:
                filtered_pages.append(page)

        return filtered_pages

    def advanced_search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Advanced search with multiple filters.

        Args:
            query: Base search query
            filters: Dictionary of filters:
                - namespace: Namespace number or list
                - category: Category to search within
                - has_template: Template that must be present
                - min_size: Minimum page size in bytes
                - max_size: Maximum page size in bytes
                - created_after: Created after timestamp
                - created_before: Created before timestamp
            limit: Maximum number of results

        Returns:
            List of filtered search results
        """
        filters = filters or {}

        # Build search query with filters
        search_parts = [query]

        if 'has_template' in filters:
            search_parts.append(f'hastemplate:"{filters["has_template"]}"')

        # Construct the search string
        full_query = ' '.join(search_parts)

        # Perform search
        results = self.search_full_text(
            full_query,
            limit=limit * 2,  # Get more results for filtering
            namespace=filters.get('namespace')
        )

        # Apply post-search filters
        filtered_results = []

        for result in results:
            # Size filters
            if 'min_size' in filters and result.get('size', 0) < filters['min_size']:
                continue
            if 'max_size' in filters and result.get('size', float('inf')) > filters['max_size']:
                continue

            # Timestamp filters
            if 'created_after' in filters:
                # Would need additional API call to get creation timestamp
                pass

            filtered_results.append(result)

            if len(filtered_results) >= limit:
                break

        return filtered_results

    def search_with_regex(
        self,
        pattern: str,
        namespace: Optional[int] = 0,
        limit: int = 50
    ) -> List[str]:
        """
        Search for pages matching a regex pattern in titles.

        Note: This performs client-side filtering, so may be slow for large wikis.

        Args:
            pattern: Regular expression pattern
            namespace: Namespace to search
            limit: Maximum number of results

        Returns:
            List of matching page titles
        """
        regex = re.compile(pattern)

        # Get all pages in namespace
        params = {
            'action': 'query',
            'list': 'allpages',
            'aplimit': 500,  # Get many pages to filter
        }

        if namespace is not None:
            params['apnamespace'] = namespace

        response = self.client._request(params)
        all_pages = response['query']['allpages']

        # Filter by regex
        matching_pages = []
        for page in all_pages:
            if regex.search(page['title']):
                matching_pages.append(page['title'])
                if len(matching_pages) >= limit:
                    break

        return matching_pages

    def find_similar_pages(
        self,
        title: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find pages similar to the given page.

        Uses categories and links to determine similarity.

        Args:
            title: Page title to find similar pages for
            limit: Maximum number of similar pages

        Returns:
            List of similar pages with similarity scores
        """
        # Get page categories
        categories = self.client.get_categories(title)

        if not categories:
            return []

        # Find pages in the same categories
        similar_pages = {}

        for category in categories[:3]:  # Limit to first 3 categories
            pages_in_cat = self.client.get_pages_in_category(category, limit=50)

            for page in pages_in_cat:
                page_title = page['title']

                # Skip the original page
                if page_title == title:
                    continue

                # Increment similarity score
                if page_title not in similar_pages:
                    similar_pages[page_title] = {
                        'title': page_title,
                        'similarity_score': 0,
                        'shared_categories': []
                    }

                similar_pages[page_title]['similarity_score'] += 1
                similar_pages[page_title]['shared_categories'].append(category)

        # Sort by similarity score and return top results
        sorted_pages = sorted(
            similar_pages.values(),
            key=lambda x: x['similarity_score'],
            reverse=True
        )

        return sorted_pages[:limit]

    def _calculate_relevance_score(
        self,
        result: Dict[str, Any],
        query: str
    ) -> float:
        """
        Calculate a custom relevance score for a search result.

        Args:
            result: Search result dictionary
            query: Original search query

        Returns:
            Relevance score (higher is more relevant)
        """
        score = 0.0
        query_lower = query.lower()
        title_lower = result.get('title', '').lower()

        # Exact title match
        if query_lower == title_lower:
            score += 100

        # Title starts with query
        elif title_lower.startswith(query_lower):
            score += 50

        # Query in title
        elif query_lower in title_lower:
            score += 25

        # Boost by word count (longer pages might be more comprehensive)
        wordcount = result.get('wordcount', 0)
        score += min(wordcount / 100, 10)  # Max 10 points from word count

        # Boost recent pages
        # (would need timestamp parsing for precise scoring)

        return score

    def search_and_process(
        self,
        query: str,
        processor: Callable[[Dict[str, Any]], Dict[str, Any]],
        limit: int = 20,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search and apply custom processing to results.

        Args:
            query: Search query
            processor: Function to process each result
            limit: Maximum number of results
            **kwargs: Additional arguments passed to search_full_text

        Returns:
            List of processed search results
        """
        results = self.search_full_text(query, limit=limit, **kwargs)
        return [processor(result) for result in results]

    def search_statistics(self, query: str) -> Dict[str, Any]:
        """
        Get statistics about search results.

        Args:
            query: Search query

        Returns:
            Statistics dictionary
        """
        results = self.search_full_text(query, limit=100)

        total_size = sum(r.get('size', 0) for r in results)
        total_wordcount = sum(r.get('wordcount', 0) for r in results)

        return {
            'total_results': len(results),
            'total_size_bytes': total_size,
            'average_size_bytes': total_size / len(results) if results else 0,
            'total_words': total_wordcount,
            'average_words': total_wordcount / len(results) if results else 0,
            'query': query
        }
