"""
MediaWiki Page Manager

High-level page management utilities for common wiki operations.
Provides convenient wrappers around the MediaWiki API for page manipulation.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
from .mediawiki_api import MediaWikiAPI, get_mediawiki_client


class PageManager:
    """
    High-level page management for MediaWiki.

    Provides convenient methods for common page operations like
    bulk updates, template management, and page organization.
    """

    def __init__(self, client: Optional[MediaWikiAPI] = None):
        """
        Initialize page manager.

        Args:
            client: Optional MediaWikiAPI instance (creates new one if not provided)
        """
        self.client = client or get_mediawiki_client()

    def create_or_update_page(
        self,
        title: str,
        content: str,
        summary: str = "Page updated via API",
        force_create: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new page or update existing one.

        Args:
            title: Page title
            content: Page content (wikitext)
            summary: Edit summary
            force_create: If True, only create new pages (fail if exists)

        Returns:
            Operation result
        """
        existing_page = self.client.get_page(title, get_content=False)

        if existing_page and force_create:
            return {
                'success': False,
                'error': f"Page '{title}' already exists and force_create is True"
            }

        result = self.client.edit_page(title, content, summary)

        return {
            'success': 'edit' in result,
            'result': result,
            'created': not existing_page,
            'updated': existing_page is not None
        }

    def bulk_create_pages(
        self,
        pages: List[Dict[str, str]],
        default_summary: str = "Bulk page creation via API"
    ) -> List[Dict[str, Any]]:
        """
        Create multiple pages at once.

        Args:
            pages: List of page dictionaries with 'title', 'content', and optional 'summary'
            default_summary: Default summary if not specified per page

        Returns:
            List of results for each page
        """
        results = []

        for page_data in pages:
            title = page_data.get('title')
            content = page_data.get('content', '')
            summary = page_data.get('summary', default_summary)

            try:
                result = self.create_or_update_page(title, content, summary)
                results.append({
                    'title': title,
                    'success': result['success'],
                    'result': result
                })
            except Exception as e:
                results.append({
                    'title': title,
                    'success': False,
                    'error': str(e)
                })

        return results

    def get_page_with_metadata(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get page with all metadata including categories and links.

        Args:
            title: Page title

        Returns:
            Complete page data or None if page doesn't exist
        """
        page = self.client.get_page(title)

        if not page:
            return None

        # Enrich with categories
        categories = self.client.get_categories(title)

        return {
            **page,
            'categories': categories
        }

    def move_page(
        self,
        from_title: str,
        to_title: str,
        reason: str = "Page moved via API",
        move_talk: bool = False,
        no_redirect: bool = False
    ) -> Dict[str, Any]:
        """
        Move/rename a page.

        Note: This requires move permissions on the wiki.

        Args:
            from_title: Current page title
            to_title: New page title
            reason: Move reason
            move_talk: Also move the talk page
            no_redirect: Don't create a redirect

        Returns:
            Move result
        """
        if not self.client._logged_in:
            self.client.login()

        params = {
            'action': 'move',
            'from': from_title,
            'to': to_title,
            'reason': reason,
            'token': self.client._get_csrf_token()
        }

        if move_talk:
            params['movetalk'] = '1'
        if no_redirect:
            params['noredirect'] = '1'

        return self.client._request(params, method='POST')

    def protect_page(
        self,
        title: str,
        protections: Dict[str, str],
        expiry: str = 'infinite',
        reason: str = "Page protected via API"
    ) -> Dict[str, Any]:
        """
        Protect a page.

        Args:
            title: Page title
            protections: Protection levels (e.g., {'edit': 'sysop', 'move': 'sysop'})
            expiry: Protection expiry (e.g., 'infinite', '1 week', '2025-12-31T23:59:59Z')
            reason: Protection reason

        Returns:
            Protection result
        """
        if not self.client._logged_in:
            self.client.login()

        # Build protection string (e.g., "edit=sysop|move=sysop")
        protections_str = '|'.join([f"{action}={level}" for action, level in protections.items()])
        expiry_str = '|'.join([expiry] * len(protections))

        params = {
            'action': 'protect',
            'title': title,
            'protections': protections_str,
            'expiry': expiry_str,
            'reason': reason,
            'token': self.client._get_csrf_token()
        }

        return self.client._request(params, method='POST')

    def append_to_page(
        self,
        title: str,
        text: str,
        summary: str = "Content appended via API",
        section: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Append text to a page.

        Args:
            title: Page title
            text: Text to append
            summary: Edit summary
            section: Optional section to append to

        Returns:
            Edit result
        """
        if not self.client._logged_in:
            self.client.login()

        params = {
            'action': 'edit',
            'title': title,
            'appendtext': text,
            'summary': summary,
            'token': self.client._get_csrf_token()
        }

        if section is not None:
            params['section'] = section

        return self.client._request(params, method='POST')

    def prepend_to_page(
        self,
        title: str,
        text: str,
        summary: str = "Content prepended via API"
    ) -> Dict[str, Any]:
        """
        Prepend text to a page.

        Args:
            title: Page title
            text: Text to prepend
            summary: Edit summary

        Returns:
            Edit result
        """
        if not self.client._logged_in:
            self.client.login()

        params = {
            'action': 'edit',
            'title': title,
            'prependtext': text,
            'summary': summary,
            'token': self.client._get_csrf_token()
        }

        return self.client._request(params, method='POST')

    def get_page_history(
        self,
        title: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get page revision history.

        Args:
            title: Page title
            limit: Maximum number of revisions to retrieve

        Returns:
            List of revisions
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'ids|timestamp|user|comment|size|flags',
            'rvlimit': limit
        }

        response = self.client._request(params)
        pages = response['query']['pages']
        page_id = list(pages.keys())[0]

        if page_id == '-1':
            return []

        return pages[page_id].get('revisions', [])

    def purge_page(self, title: str) -> Dict[str, Any]:
        """
        Purge page cache.

        Args:
            title: Page title

        Returns:
            Purge result
        """
        params = {
            'action': 'purge',
            'titles': title
        }

        return self.client._request(params, method='POST')

    def get_page_links(
        self,
        title: str,
        namespace: Optional[int] = None,
        limit: int = 500
    ) -> List[str]:
        """
        Get all links from a page.

        Args:
            title: Page title
            namespace: Filter by namespace
            limit: Maximum number of links

        Returns:
            List of linked page titles
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'links',
            'pllimit': limit
        }

        if namespace is not None:
            params['plnamespace'] = namespace

        response = self.client._request(params)
        pages = response['query']['pages']
        page_id = list(pages.keys())[0]

        if page_id == '-1' or 'links' not in pages[page_id]:
            return []

        return [link['title'] for link in pages[page_id]['links']]

    def get_backlinks(
        self,
        title: str,
        limit: int = 100
    ) -> List[str]:
        """
        Get pages that link to this page.

        Args:
            title: Page title
            limit: Maximum number of backlinks

        Returns:
            List of page titles that link to this page
        """
        params = {
            'action': 'query',
            'list': 'backlinks',
            'bltitle': title,
            'bllimit': limit
        }

        response = self.client._request(params)
        backlinks = response['query']['backlinks']

        return [bl['title'] for bl in backlinks]

    def compare_revisions(
        self,
        from_rev: int,
        to_rev: int
    ) -> Dict[str, Any]:
        """
        Compare two revisions of a page.

        Args:
            from_rev: Starting revision ID
            to_rev: Ending revision ID

        Returns:
            Comparison result with diff
        """
        params = {
            'action': 'compare',
            'fromrev': from_rev,
            'torev': to_rev
        }

        return self.client._request(params)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if hasattr(self.client, '__exit__'):
            self.client.__exit__(exc_type, exc_val, exc_tb)
