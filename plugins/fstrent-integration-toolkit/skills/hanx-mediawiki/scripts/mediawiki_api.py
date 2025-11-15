"""
MediaWiki API Client

Provides a comprehensive interface to interact with MediaWiki installations
using the MediaWiki API. Supports authentication, page management, search,
categories, and file uploads.

Dependencies:
    pip install requests python-dotenv
"""

import os
import requests
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()


class MediaWikiAPIError(Exception):
    """Custom exception for MediaWiki API errors."""
    pass


class MediaWikiAPI:
    """
    MediaWiki API client for managing wiki content.

    This client provides methods for:
    - Authentication (login/logout)
    - Page management (create, read, update, delete)
    - Search functionality
    - Category management
    - File uploads
    - Template handling
    """

    def __init__(
        self,
        api_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize MediaWiki API client.

        Args:
            api_url: MediaWiki API endpoint (e.g., https://wiki.example.com/api.php)
                    Falls back to MEDIAWIKI_API_URL environment variable
            username: MediaWiki username (falls back to MEDIAWIKI_USERNAME)
            password: MediaWiki password (falls back to MEDIAWIKI_PASSWORD)
        """
        self.api_url = api_url or os.getenv('MEDIAWIKI_API_URL')
        self.username = username or os.getenv('MEDIAWIKI_USERNAME')
        self.password = password or os.getenv('MEDIAWIKI_PASSWORD')

        if not self.api_url:
            raise MediaWikiAPIError("API URL is required. Set MEDIAWIKI_API_URL or pass api_url parameter.")

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MediaWiki-Python-Client/1.0'
        })

        self._logged_in = False
        self._tokens = {}

    def _request(
        self,
        params: Dict[str, Any],
        method: str = 'GET',
        files: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the MediaWiki API.

        Args:
            params: API parameters
            method: HTTP method (GET or POST)
            files: Optional files to upload

        Returns:
            API response as dictionary

        Raises:
            MediaWikiAPIError: If the request fails
        """
        params['format'] = 'json'

        try:
            if method.upper() == 'GET':
                response = self.session.get(self.api_url, params=params)
            else:
                response = self.session.post(self.api_url, data=params, files=files)

            response.raise_for_status()
            data = response.json()

            # Check for API errors
            if 'error' in data:
                raise MediaWikiAPIError(f"API Error: {data['error'].get('info', 'Unknown error')}")

            return data

        except requests.exceptions.RequestException as e:
            raise MediaWikiAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise MediaWikiAPIError(f"Invalid JSON response: {str(e)}")

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """
        Login to MediaWiki.

        Args:
            username: Optional username (uses instance username if not provided)
            password: Optional password (uses instance password if not provided)

        Returns:
            True if login successful

        Raises:
            MediaWikiAPIError: If login fails
        """
        username = username or self.username
        password = password or self.password

        if not username or not password:
            raise MediaWikiAPIError("Username and password are required for login")

        # Get login token
        token_response = self._request({
            'action': 'query',
            'meta': 'tokens',
            'type': 'login'
        })

        login_token = token_response['query']['tokens']['logintoken']

        # Perform login
        login_response = self._request({
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': login_token
        }, method='POST')

        if login_response['login']['result'] == 'Success':
            self._logged_in = True
            return True
        else:
            raise MediaWikiAPIError(f"Login failed: {login_response['login']['result']}")

    def logout(self) -> None:
        """Logout from MediaWiki."""
        if self._logged_in:
            self._request({'action': 'logout'}, method='POST')
            self._logged_in = False
            self._tokens = {}

    def _get_csrf_token(self) -> str:
        """
        Get CSRF token for write operations.

        Returns:
            CSRF token
        """
        if 'csrf' not in self._tokens:
            response = self._request({
                'action': 'query',
                'meta': 'tokens'
            })
            self._tokens['csrf'] = response['query']['tokens']['csrftoken']

        return self._tokens['csrf']

    def get_page(self, title: str, get_content: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get page information and content.

        Args:
            title: Page title
            get_content: Whether to retrieve page content

        Returns:
            Page data dictionary or None if page doesn't exist
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'info'
        }

        if get_content:
            params['prop'] += '|revisions'
            params['rvprop'] = 'content|timestamp|user|comment'
            params['rvslots'] = 'main'

        response = self._request(params)
        pages = response['query']['pages']

        # Get the first (and only) page
        page_id = list(pages.keys())[0]

        if page_id == '-1':
            return None  # Page doesn't exist

        page_data = pages[page_id]

        if get_content and 'revisions' in page_data:
            page_data['content'] = page_data['revisions'][0]['slots']['main']['*']

        return page_data

    def create_page(
        self,
        title: str,
        content: str,
        summary: str = "Page created via API",
        minor: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new page or update existing page.

        Args:
            title: Page title
            content: Page content (wikitext)
            summary: Edit summary
            minor: Whether this is a minor edit

        Returns:
            Edit result dictionary
        """
        return self.edit_page(title, content, summary, minor, create_only=False)

    def edit_page(
        self,
        title: str,
        content: str,
        summary: str = "Page updated via API",
        minor: bool = False,
        create_only: bool = False,
        no_create: bool = False
    ) -> Dict[str, Any]:
        """
        Edit a page.

        Args:
            title: Page title
            content: New page content (wikitext)
            summary: Edit summary
            minor: Whether this is a minor edit
            create_only: Only create page, fail if it exists
            no_create: Only edit existing page, fail if it doesn't exist

        Returns:
            Edit result dictionary
        """
        if not self._logged_in:
            self.login()

        params = {
            'action': 'edit',
            'title': title,
            'text': content,
            'summary': summary,
            'token': self._get_csrf_token()
        }

        if minor:
            params['minor'] = '1'
        if create_only:
            params['createonly'] = '1'
        if no_create:
            params['nocreate'] = '1'

        return self._request(params, method='POST')

    def delete_page(self, title: str, reason: str = "Deleted via API") -> Dict[str, Any]:
        """
        Delete a page.

        Args:
            title: Page title to delete
            reason: Deletion reason

        Returns:
            Deletion result dictionary
        """
        if not self._logged_in:
            self.login()

        params = {
            'action': 'delete',
            'title': title,
            'reason': reason,
            'token': self._get_csrf_token()
        }

        return self._request(params, method='POST')

    def search(
        self,
        query: str,
        limit: int = 10,
        namespace: Optional[Union[int, List[int]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search wiki content.

        Args:
            query: Search query
            limit: Maximum number of results
            namespace: Namespace(s) to search (0=main, 1=talk, etc.)

        Returns:
            List of search results
        """
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit
        }

        if namespace is not None:
            if isinstance(namespace, list):
                params['srnamespace'] = '|'.join(map(str, namespace))
            else:
                params['srnamespace'] = str(namespace)

        response = self._request(params)
        return response['query']['search']

    def get_categories(self, title: str) -> List[str]:
        """
        Get categories for a page.

        Args:
            title: Page title

        Returns:
            List of category names
        """
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'categories',
            'cllimit': 'max'
        }

        response = self._request(params)
        pages = response['query']['pages']
        page_id = list(pages.keys())[0]

        if page_id == '-1' or 'categories' not in pages[page_id]:
            return []

        return [cat['title'] for cat in pages[page_id]['categories']]

    def add_category(
        self,
        title: str,
        category: str,
        summary: str = "Category added via API"
    ) -> Dict[str, Any]:
        """
        Add a category to a page.

        Args:
            title: Page title
            category: Category name (with or without "Category:" prefix)
            summary: Edit summary

        Returns:
            Edit result dictionary
        """
        # Ensure category has proper prefix
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        # Get current page content
        page = self.get_page(title)
        if not page:
            raise MediaWikiAPIError(f"Page '{title}' does not exist")

        content = page.get('content', '')

        # Check if category already exists
        if f'[[{category}]]' in content:
            return {'result': 'category_already_exists'}

        # Add category at the end
        new_content = content.rstrip() + f'\n[[{category}]]'

        return self.edit_page(title, new_content, summary)

    def get_pages_in_category(
        self,
        category: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all pages in a category.

        Args:
            category: Category name (with or without "Category:" prefix)
            limit: Maximum number of pages to retrieve

        Returns:
            List of pages in the category
        """
        # Ensure category has proper prefix
        if not category.startswith('Category:'):
            category = f'Category:{category}'

        params = {
            'action': 'query',
            'list': 'categorymembers',
            'cmtitle': category,
            'cmlimit': limit
        }

        response = self._request(params)
        return response['query']['categorymembers']

    def upload_file(
        self,
        filename: str,
        filepath: Union[str, Path],
        description: str = "",
        comment: str = "File uploaded via API",
        ignore_warnings: bool = False
    ) -> Dict[str, Any]:
        """
        Upload a file to the wiki.

        Args:
            filename: Name for the file on the wiki
            filepath: Path to the file to upload
            description: File description (wikitext for file page)
            comment: Upload comment
            ignore_warnings: Whether to ignore warnings (e.g., duplicate files)

        Returns:
            Upload result dictionary
        """
        if not self._logged_in:
            self.login()

        filepath = Path(filepath)
        if not filepath.exists():
            raise MediaWikiAPIError(f"File not found: {filepath}")

        params = {
            'action': 'upload',
            'filename': filename,
            'comment': comment,
            'text': description,
            'token': self._get_csrf_token()
        }

        if ignore_warnings:
            params['ignorewarnings'] = '1'

        with open(filepath, 'rb') as f:
            files = {'file': f}
            return self._request(params, method='POST', files=files)

    def get_recent_changes(
        self,
        limit: int = 10,
        namespace: Optional[Union[int, List[int]]] = None,
        show_bot: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get recent changes to the wiki.

        Args:
            limit: Maximum number of changes to retrieve
            namespace: Namespace(s) to filter (0=main, 1=talk, etc.)
            show_bot: Whether to include bot edits

        Returns:
            List of recent changes
        """
        params = {
            'action': 'query',
            'list': 'recentchanges',
            'rclimit': limit,
            'rcprop': 'title|timestamp|user|comment|sizes|flags'
        }

        if namespace is not None:
            if isinstance(namespace, list):
                params['rcnamespace'] = '|'.join(map(str, namespace))
            else:
                params['rcnamespace'] = str(namespace)

        if not show_bot:
            params['rcshow'] = '!bot'

        response = self._request(params)
        return response['query']['recentchanges']

    def __enter__(self):
        """Context manager entry."""
        if self.username and self.password:
            self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.logout()


# Convenience function for quick initialization
def get_mediawiki_client(
    api_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    auto_login: bool = True
) -> MediaWikiAPI:
    """
    Get a MediaWiki API client instance.

    Args:
        api_url: MediaWiki API endpoint
        username: MediaWiki username
        password: MediaWiki password
        auto_login: Whether to automatically login

    Returns:
        MediaWikiAPI instance
    """
    client = MediaWikiAPI(api_url, username, password)

    if auto_login and client.username and client.password:
        client.login()

    return client
