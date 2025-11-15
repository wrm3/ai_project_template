"""
MediaWiki Integration Scripts

This package provides comprehensive MediaWiki API integration
for Claude Code, enabling AI-powered wiki management.
"""

from .mediawiki_api import MediaWikiAPI, MediaWikiAPIError, get_mediawiki_client
from .page_manager import PageManager
from .search_manager import SearchManager
from .category_manager import CategoryManager
from .file_uploader import FileUploader

__all__ = [
    'MediaWikiAPI',
    'MediaWikiAPIError',
    'get_mediawiki_client',
    'PageManager',
    'SearchManager',
    'CategoryManager',
    'FileUploader'
]

__version__ = '1.0.0'
