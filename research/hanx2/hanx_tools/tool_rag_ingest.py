#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG Ingestion Tool

This tool provides utilities for ingesting various file types into the RAG system.
It handles chunking of large text bodies and supports multiple file formats.

Example:
    # Ingest a text file
    python tool_rag_ingest.py ingest-file path/to/document.txt --source "documentation" --tags "rag,documentation"
    
    # Ingest a directory of files
    python tool_rag_ingest.py ingest-directory path/to/docs --recursive --source "project-docs"
    
    # Ingest a YouTube video transcript
    python tool_rag_ingest.py ingest-youtube https://www.youtube.com/watch?v=VIDEO_ID --source "youtube-tutorial"
    
    # Ingest a web page
    python tool_rag_ingest.py ingest-web https://example.com/article --source "web-article"
"""

import os
import sys
import argparse
import json
import glob
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import logging

# Add the parent directory to the path so we can import from hanx_tools and hanx_agents
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import RAG utilities with fallbacks
try:
    from hanx.hanx_tools.tool_rag_utils import add_text, add_document
except ImportError:
    try:
        from tool_rag_utils import add_text, add_document
    except ImportError:
        logger.error("Failed to import RAG utilities. Make sure tool_rag_utils.py exists in hanx_tools directory.")
        
        # Define dummy functions as fallbacks
        def add_text(text, metadata=None):
            logger.warning("Using dummy add_text function")
            return str(uuid.uuid4())
            
        def add_document(file_path, metadata=None):
            logger.warning("Using dummy add_document function")
            return str(uuid.uuid4())

# Try to import optional dependencies
try:
    from hanx.hanx_tools.tool_web_scraper import scrape_url
except ImportError:
    try:
        from tool_web_scraper import scrape_url
        web_scraper_available = True
    except ImportError:
        web_scraper_available = False
        logger.warning("Web scraper not available. Web ingestion will be disabled.")
        
        def scrape_url(url):
            logger.warning("Using dummy scrape_url function")
            return f"Dummy content for {url}"

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    youtube_api_available = True
except ImportError:
    youtube_api_available = False
    logger.warning("YouTube transcript API not available. YouTube ingestion will be disabled.")

# File type handlers
def read_text_file(file_path: str) -> str:
    """Read a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        The text content of the file
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def read_pdf_file(file_path: str) -> str:
    """Read a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        The text content of the PDF
    """
    try:
        import pypdf
    except ImportError:
        logger.error("pypdf not installed. Install it with: pip install pypdf")
        sys.exit(1)
    
    text = ""
    with open(file_path, 'rb') as f:
        pdf = pypdf.PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"
    return text

def read_docx_file(file_path: str) -> str:
    """Read a DOCX file.
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        The text content of the DOCX
    """
    try:
        import docx2txt
    except ImportError:
        logger.error("docx2txt not installed. Install it with: pip install docx2txt")
        sys.exit(1)
    
    return docx2txt.process(file_path)

def read_excel_file(file_path: str) -> str:
    """Read an Excel file.
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        The text content of the Excel file
    """
    try:
        import pandas as pd
    except ImportError:
        logger.error("pandas not installed. Install it with: pip install pandas")
        sys.exit(1)
    
    dfs = pd.read_excel(file_path, sheet_name=None)
    text = ""
    for sheet_name, df in dfs.items():
        text += f"Sheet: {sheet_name}\n"
        text += df.to_string() + "\n\n"
    return text

def read_csv_file(file_path: str) -> str:
    """Read a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        The text content of the CSV file
    """
    try:
        import pandas as pd
    except ImportError:
        logger.error("pandas not installed. Install it with: pip install pandas")
        sys.exit(1)
    
    df = pd.read_csv(file_path)
    return df.to_string()

def get_youtube_transcript(video_id: str) -> str:
    """Get the transcript of a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        The transcript of the video
    """
    if not youtube_api_available:
        logger.error("YouTube transcript API not available. Install it with: pip install youtube-transcript-api")
        sys.exit(1)
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
        return transcript
    except Exception as e:
        logger.error(f"Failed to get YouTube transcript: {e}")
        sys.exit(1)

def get_web_content(url: str) -> str:
    """Get the content of a web page.
    
    Args:
        url: URL of the web page
        
    Returns:
        The text content of the web page
    """
    if not web_scraper_available:
        logger.error("Web scraper not available. Make sure tool_web_scraper.py exists in hanx_tools directory.")
        sys.exit(1)
    
    try:
        content = scrape_url(url)
        return content
    except Exception as e:
        logger.error(f"Failed to scrape web page: {e}")
        sys.exit(1)

# RAG ingestion functions
def ingest_text(text: str, metadata: Optional[Dict[str, Any]] = None, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
    """Ingest text into the RAG system.
    
    Args:
        text: The text to ingest
        metadata: Optional metadata for the text
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document IDs
    """
    if metadata is None:
        metadata = {}
    
    # Generate a document ID if not provided
    if 'id' not in metadata:
        metadata['id'] = str(uuid.uuid4())
    
    # Split text into chunks
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunk = text[i:i + chunk_size]
        if chunk:  # Skip empty chunks
            chunks.append(chunk)
    
    # If text is smaller than chunk size, just use it as is
    if not chunks:
        chunks = [text]
    
    # Add each chunk to the RAG system
    doc_ids = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = metadata.copy()
        chunk_metadata['chunk_index'] = i
        chunk_metadata['total_chunks'] = len(chunks)
        
        try:
            doc_id = add_text(chunk, chunk_metadata)
            doc_ids.append(doc_id)
            logger.info(f"Added chunk {i+1}/{len(chunks)} with ID: {doc_id}")
        except Exception as e:
            logger.error(f"Failed to add chunk {i+1}/{len(chunks)}: {e}")
    
    return doc_ids

def ingest_file(file_path: str, metadata: Optional[Dict[str, Any]] = None, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
    """Ingest a file into the RAG system.
    
    Args:
        file_path: Path to the file
        metadata: Optional metadata for the file
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document IDs
    """
    if metadata is None:
        metadata = {}
    
    # Add file info to metadata
    file_path_obj = Path(file_path)
    metadata['source_file'] = str(file_path_obj)
    metadata['filename'] = file_path_obj.name
    
    # Determine file type and read content
    ext = file_path_obj.suffix.lower()
    
    try:
        if ext in ('.txt', '.md', '.log', '.json', '.xml', '.html', '.htm', '.css', '.js', '.py', '.java', '.c', '.cpp', '.h', '.cs', '.php', '.rb', '.go', '.rs', '.ts', '.sh', '.bat', '.ps1'):
            text = read_text_file(file_path)
        elif ext == '.pdf':
            text = read_pdf_file(file_path)
        elif ext in ('.docx', '.doc'):
            text = read_docx_file(file_path)
        elif ext in ('.xlsx', '.xls'):
            text = read_excel_file(file_path)
        elif ext == '.csv':
            text = read_csv_file(file_path)
        else:
            # Try to read as text file
            logger.warning(f"Unknown file type: {ext}. Trying to read as text file.")
            text = read_text_file(file_path)
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        return []
    
    # Ingest the text
    return ingest_text(text, metadata, chunk_size, chunk_overlap)

def ingest_directory(directory_path: str, recursive: bool = False, file_pattern: str = "*.*", metadata: Optional[Dict[str, Any]] = None, chunk_size: int = 2000, chunk_overlap: int = 200) -> Dict[str, List[str]]:
    """Ingest all files in a directory into the RAG system.
    
    Args:
        directory_path: Path to the directory
        recursive: Whether to recursively process subdirectories
        file_pattern: Pattern to match files
        metadata: Optional metadata for the files
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        Dictionary mapping file paths to document IDs
    """
    if metadata is None:
        metadata = {}
    
    # Add directory info to metadata
    dir_path_obj = Path(directory_path)
    metadata['source_directory'] = str(dir_path_obj)
    
    # Find all files matching the pattern
    if recursive:
        file_paths = glob.glob(os.path.join(directory_path, "**", file_pattern), recursive=True)
    else:
        file_paths = glob.glob(os.path.join(directory_path, file_pattern))
    
    # Filter out directories
    file_paths = [fp for fp in file_paths if os.path.isfile(fp)]
    
    if not file_paths:
        logger.warning(f"No files found in {directory_path} matching pattern {file_pattern}")
        return {}
    
    # Ingest each file
    results = {}
    for file_path in file_paths:
        logger.info(f"Ingesting file: {file_path}")
        file_metadata = metadata.copy()
        file_metadata['relative_path'] = os.path.relpath(file_path, directory_path)
        
        doc_ids = ingest_file(file_path, file_metadata, chunk_size, chunk_overlap)
        results[file_path] = doc_ids
    
    return results

def ingest_youtube(video_id: str, metadata: Optional[Dict[str, Any]] = None, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
    """Ingest a YouTube video transcript into the RAG system.
    
    Args:
        video_id: YouTube video ID
        metadata: Optional metadata for the video
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document IDs
    """
    if metadata is None:
        metadata = {}
    
    # Add video info to metadata
    metadata['source'] = 'youtube'
    metadata['video_id'] = video_id
    metadata['video_url'] = f"https://www.youtube.com/watch?v={video_id}"
    
    # Get the transcript
    transcript = get_youtube_transcript(video_id)
    
    # Ingest the transcript
    return ingest_text(transcript, metadata, chunk_size, chunk_overlap)

def ingest_web(url: str, metadata: Optional[Dict[str, Any]] = None, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
    """Ingest a web page into the RAG system.
    
    Args:
        url: URL of the web page
        metadata: Optional metadata for the web page
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document IDs
    """
    if metadata is None:
        metadata = {}
    
    # Add web page info to metadata
    metadata['source'] = 'web'
    metadata['url'] = url
    
    # Get the web page content
    content = get_web_content(url)
    
    # Ingest the content
    return ingest_text(content, metadata, chunk_size, chunk_overlap)

def extract_youtube_id(url: str) -> str:
    """Extract the YouTube video ID from a URL.
    
    Args:
        url: YouTube URL
        
    Returns:
        YouTube video ID
    """
    import re
    
    # Try to extract the video ID using regex
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?]+)',
        r'(?:youtube\.com/embed/)([^&\n?]+)',
        r'(?:youtube\.com/v/)([^&\n?]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no match found, assume the input is already a video ID
    return url

def main():
    """Command-line interface for RAG ingestion."""
    parser = argparse.ArgumentParser(description="RAG Ingestion Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Ingest text command
    text_parser = subparsers.add_parser("ingest-text", help="Ingest text into the RAG system")
    text_parser.add_argument("text", help="Text to ingest")
    text_parser.add_argument("--source", help="Source of the text")
    text_parser.add_argument("--tags", help="Comma-separated tags")
    text_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
    text_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Ingest file command
    file_parser = subparsers.add_parser("ingest-file", help="Ingest a file into the RAG system")
    file_parser.add_argument("file_path", help="Path to the file")
    file_parser.add_argument("--source", help="Source of the file")
    file_parser.add_argument("--tags", help="Comma-separated tags")
    file_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
    file_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Ingest directory command
    dir_parser = subparsers.add_parser("ingest-directory", help="Ingest all files in a directory into the RAG system")
    dir_parser.add_argument("directory_path", help="Path to the directory")
    dir_parser.add_argument("--recursive", action="store_true", help="Recursively process subdirectories")
    dir_parser.add_argument("--file-pattern", default="*.*", help="Pattern to match files")
    dir_parser.add_argument("--source", help="Source of the files")
    dir_parser.add_argument("--tags", help="Comma-separated tags")
    dir_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
    dir_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Ingest YouTube video command
    youtube_parser = subparsers.add_parser("ingest-youtube", help="Ingest a YouTube video transcript into the RAG system")
    youtube_parser.add_argument("video_url", help="YouTube video URL or ID")
    youtube_parser.add_argument("--source", help="Source of the video")
    youtube_parser.add_argument("--tags", help="Comma-separated tags")
    youtube_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
    youtube_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Ingest web page command
    web_parser = subparsers.add_parser("ingest-web", help="Ingest a web page into the RAG system")
    web_parser.add_argument("url", help="URL of the web page")
    web_parser.add_argument("--source", help="Source of the web page")
    web_parser.add_argument("--tags", help="Comma-separated tags")
    web_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
    web_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Prepare metadata
    metadata = {}
    if hasattr(args, 'source') and args.source:
        metadata['source'] = args.source
    if hasattr(args, 'tags') and args.tags:
        metadata['tags'] = args.tags
    
    # Execute command
    if args.command == "ingest-text":
        doc_ids = ingest_text(args.text, metadata, args.chunk_size, args.chunk_overlap)
        print(f"Ingested text into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif args.command == "ingest-file":
        doc_ids = ingest_file(args.file_path, metadata, args.chunk_size, args.chunk_overlap)
        print(f"Ingested file {args.file_path} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif args.command == "ingest-directory":
        results = ingest_directory(args.directory_path, args.recursive, args.file_pattern, metadata, args.chunk_size, args.chunk_overlap)
        total_files = len(results)
        total_chunks = sum(len(doc_ids) for doc_ids in results.values())
        print(f"Ingested {total_files} files into {total_chunks} chunks")
        for file_path, doc_ids in results.items():
            print(f"  {file_path}: {len(doc_ids)} chunks")
    
    elif args.command == "ingest-youtube":
        video_id = extract_youtube_id(args.video_url)
        doc_ids = ingest_youtube(video_id, metadata, args.chunk_size, args.chunk_overlap)
        print(f"Ingested YouTube video {video_id} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif args.command == "ingest-web":
        doc_ids = ingest_web(args.url, metadata, args.chunk_size, args.chunk_overlap)
        print(f"Ingested web page {args.url} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 