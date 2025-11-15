"""
MediaWiki File Uploader

Utilities for uploading and managing files (images, documents, media)
on MediaWiki.
"""

from typing import List, Dict, Optional, Any, Union
from pathlib import Path
import mimetypes
import hashlib
from .mediawiki_api import MediaWikiAPI, get_mediawiki_client


class FileUploader:
    """
    File upload and management for MediaWiki.

    Provides tools for:
    - Single and bulk file uploads
    - File metadata management
    - Duplicate detection
    - File usage tracking
    """

    # Supported file extensions (common MediaWiki defaults)
    ALLOWED_EXTENSIONS = {
        # Images
        'png', 'gif', 'jpg', 'jpeg', 'webp', 'svg',
        # Documents
        'pdf', 'odt', 'ods', 'odp', 'odg',
        # Media
        'mp3', 'mp4', 'webm', 'ogg', 'ogv',
        # Archives
        'zip', '7z',
        # Other
        'txt', 'csv', 'json', 'xml'
    }

    def __init__(self, client: Optional[MediaWikiAPI] = None):
        """
        Initialize file uploader.

        Args:
            client: Optional MediaWikiAPI instance
        """
        self.client = client or get_mediawiki_client()

    def upload_file(
        self,
        filepath: Union[str, Path],
        wiki_filename: Optional[str] = None,
        description: str = "",
        comment: str = "File uploaded via API",
        categories: Optional[List[str]] = None,
        ignore_warnings: bool = False,
        check_duplicate: bool = True
    ) -> Dict[str, Any]:
        """
        Upload a file to MediaWiki.

        Args:
            filepath: Path to file to upload
            wiki_filename: Filename on wiki (uses original name if not provided)
            description: File description for the file page
            comment: Upload comment
            categories: Categories to add to file page
            ignore_warnings: Ignore warnings (e.g., duplicates)
            check_duplicate: Check for duplicates before uploading

        Returns:
            Upload result with file information
        """
        filepath = Path(filepath)

        if not filepath.exists():
            return {
                'success': False,
                'error': f'File not found: {filepath}'
            }

        # Check file extension
        extension = filepath.suffix.lstrip('.').lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            return {
                'success': False,
                'error': f'File type .{extension} not allowed. Allowed: {", ".join(sorted(self.ALLOWED_EXTENSIONS))}'
            }

        # Use original filename if not specified
        if not wiki_filename:
            wiki_filename = filepath.name

        # Build file page description
        full_description = description

        # Add categories if specified
        if categories:
            category_links = '\n'.join([
                f'[[Category:{cat}]]' if not cat.startswith('Category:') else f'[[{cat}]]'
                for cat in categories
            ])
            full_description = f"{description}\n\n{category_links}"

        # Check for duplicates
        if check_duplicate and not ignore_warnings:
            duplicate = self._check_duplicate_file(filepath)
            if duplicate:
                return {
                    'success': False,
                    'error': f'Duplicate file exists: {duplicate["filename"]}',
                    'duplicate': duplicate
                }

        # Upload the file
        try:
            result = self.client.upload_file(
                wiki_filename,
                filepath,
                full_description,
                comment,
                ignore_warnings
            )

            return {
                'success': 'upload' in result,
                'result': result,
                'filename': wiki_filename,
                'filepath': str(filepath)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def bulk_upload(
        self,
        files: List[Dict[str, Any]],
        default_description: str = "",
        default_categories: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Upload multiple files.

        Args:
            files: List of file dictionaries with 'path' and optional 'filename', 'description', 'categories'
            default_description: Default description for files
            default_categories: Default categories for files

        Returns:
            List of upload results
        """
        results = []

        for file_data in files:
            filepath = file_data.get('path')
            if not filepath:
                results.append({
                    'success': False,
                    'error': 'No path specified'
                })
                continue

            wiki_filename = file_data.get('filename')
            description = file_data.get('description', default_description)
            categories = file_data.get('categories', default_categories or [])
            comment = file_data.get('comment', 'Bulk upload via API')

            result = self.upload_file(
                filepath,
                wiki_filename,
                description,
                comment,
                categories
            )

            results.append(result)

        return results

    def upload_directory(
        self,
        directory: Union[str, Path],
        pattern: str = '*',
        description_template: str = "Uploaded from {filename}",
        categories: Optional[List[str]] = None,
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Upload all files from a directory.

        Args:
            directory: Directory path
            pattern: File pattern (e.g., '*.png', '*.jpg')
            description_template: Template for file descriptions (can use {filename})
            categories: Categories to add to all files
            recursive: Whether to search subdirectories

        Returns:
            List of upload results
        """
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            return [{
                'success': False,
                'error': f'Directory not found: {directory}'
            }]

        # Find matching files
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))

        # Filter out directories
        files = [f for f in files if f.is_file()]

        results = []

        for filepath in files:
            description = description_template.format(filename=filepath.name)

            result = self.upload_file(
                filepath,
                wiki_filename=filepath.name,
                description=description,
                categories=categories or []
            )

            results.append(result)

        return results

    def get_file_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a file.

        Args:
            filename: File name (with or without "File:" prefix)

        Returns:
            File information or None if not found
        """
        if not filename.startswith('File:'):
            filename = f'File:{filename}'

        params = {
            'action': 'query',
            'titles': filename,
            'prop': 'imageinfo',
            'iiprop': 'url|size|mime|timestamp|user|sha1|metadata'
        }

        response = self.client._request(params)
        pages = response['query']['pages']
        page_id = list(pages.keys())[0]

        if page_id == '-1':
            return None

        page = pages[page_id]
        if 'imageinfo' not in page:
            return None

        return {
            'title': page['title'],
            'info': page['imageinfo'][0]
        }

    def get_file_usage(self, filename: str, limit: int = 100) -> List[str]:
        """
        Get pages that use a file.

        Args:
            filename: File name
            limit: Maximum number of pages

        Returns:
            List of page titles that use the file
        """
        if not filename.startswith('File:'):
            filename = f'File:{filename}'

        params = {
            'action': 'query',
            'list': 'imageusage',
            'iutitle': filename,
            'iulimit': limit
        }

        response = self.client._request(params)
        usage = response['query']['imageusage']

        return [page['title'] for page in usage]

    def delete_file(
        self,
        filename: str,
        reason: str = "File deleted via API"
    ) -> Dict[str, Any]:
        """
        Delete a file.

        Args:
            filename: File name to delete
            reason: Deletion reason

        Returns:
            Deletion result
        """
        if not filename.startswith('File:'):
            filename = f'File:{filename}'

        return self.client.delete_page(filename, reason)

    def _check_duplicate_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        Check if file is a duplicate based on SHA-1 hash.

        Args:
            filepath: Path to file to check

        Returns:
            Duplicate file info or None if no duplicate
        """
        # Calculate SHA-1 hash
        sha1 = hashlib.sha1()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        file_hash = sha1.hexdigest()

        # Search for duplicate by hash
        params = {
            'action': 'query',
            'list': 'allimages',
            'aisha1': file_hash,
            'ailimit': 1
        }

        response = self.client._request(params)
        images = response['query']['allimages']

        if images:
            return {
                'filename': images[0]['name'],
                'sha1': file_hash
            }

        return None

    def update_file_description(
        self,
        filename: str,
        description: str,
        summary: str = "Updated file description"
    ) -> Dict[str, Any]:
        """
        Update the description of a file page.

        Args:
            filename: File name
            description: New description
            summary: Edit summary

        Returns:
            Edit result
        """
        if not filename.startswith('File:'):
            filename = f'File:{filename}'

        return self.client.edit_page(filename, description, summary)

    def get_file_categories(self, filename: str) -> List[str]:
        """
        Get categories for a file.

        Args:
            filename: File name

        Returns:
            List of category names
        """
        if not filename.startswith('File:'):
            filename = f'File:{filename}'

        return self.client.get_categories(filename)

    def reupload_file(
        self,
        filepath: Union[str, Path],
        wiki_filename: str,
        comment: str = "File re-uploaded via API",
        ignore_warnings: bool = True
    ) -> Dict[str, Any]:
        """
        Re-upload a new version of an existing file.

        Args:
            filepath: Path to new file version
            wiki_filename: Existing filename on wiki
            comment: Upload comment
            ignore_warnings: Ignore warnings (usually needed for re-uploads)

        Returns:
            Upload result
        """
        filepath = Path(filepath)

        if not filepath.exists():
            return {
                'success': False,
                'error': f'File not found: {filepath}'
            }

        # Get existing description
        file_info = self.get_file_info(wiki_filename)
        if not file_info:
            return {
                'success': False,
                'error': f'File {wiki_filename} does not exist on wiki'
            }

        # Get current file page content for description
        if not wiki_filename.startswith('File:'):
            page_title = f'File:{wiki_filename}'
        else:
            page_title = wiki_filename

        page = self.client.get_page(page_title)
        description = page.get('content', '') if page else ''

        # Upload new version
        return self.upload_file(
            filepath,
            wiki_filename,
            description,
            comment,
            ignore_warnings=ignore_warnings
        )

    def get_mime_type(self, filepath: Union[str, Path]) -> str:
        """
        Get MIME type for a file.

        Args:
            filepath: Path to file

        Returns:
            MIME type string
        """
        mime_type, _ = mimetypes.guess_type(str(filepath))
        return mime_type or 'application/octet-stream'
