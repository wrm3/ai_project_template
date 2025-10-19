#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG Librarian Agent

This module provides a comprehensive command-line interface for managing and querying
the RAG (Retrieval Augmented Generation) system. It combines functionality from
multiple previous agents into a single, unified interface.

Features:
- Add text and documents to the knowledge base
- Ingest files, directories, YouTube transcripts, and web pages
- Search for relevant information
- Query the system with natural language questions
- Manage the knowledge base (list, delete, clear)

Example:
    # Add text to the knowledge base
    python agent_rag_librarian.py add "This is important information" --source "manual" --tags "example,test"
    
    # Ingest a file
    python agent_rag_librarian.py ingest-file path/to/document.txt --source "documentation" --tags "rag,docs"
    
    # Ingest a YouTube video transcript
    python agent_rag_librarian.py ingest-youtube dQw4w9WgXcQ --source "youtube" --tags "music,example"
    
    # Search the knowledge base
    python agent_rag_librarian.py search "important information" --limit 5
    
    # Query the system
    python agent_rag_librarian.py query "What information do we have about AI safety?" --provider openai
    
    # List all documents
    python agent_rag_librarian.py list --limit 10
"""

import os
import sys
import argparse
import json
import logging
from typing import Dict, Any, List, Optional, Union, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import from hanx_tools and hanx_apis
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import core RAG utilities
try:
    from hanx_tools.tool_rag_utils import (
        add_text, add_document, search, get_all_documents,
        delete_document, clear_database
    )
except ImportError:
    logger.error("Failed to import RAG utilities. Make sure tool_rag_utils.py exists in hanx_tools directory.")
    sys.exit(1)

# Import ingestion utilities if available
try:
    from hanx_tools.tool_rag_ingest import (
        ingest_text, ingest_file, ingest_directory,
        ingest_youtube, ingest_web, extract_youtube_id
    )
    HAS_INGEST = True
except ImportError:
    logger.warning("RAG ingestion utilities not available. Some features will be disabled.")
    HAS_INGEST = False

# Import LLM API for querying
try:
    from hanx_apis.api_llm import query_llm
    HAS_LLM = True
except ImportError:
    logger.warning("LLM API not available. Query functionality will be disabled.")
    HAS_LLM = False

def query_rag(query: str, limit: int = 5, provider: str = "openai") -> Dict[str, Any]:
    """Query the RAG system.
    
    Args:
        query: The query string
        limit: Maximum number of documents to retrieve
        provider: LLM provider to use
        
    Returns:
        Dictionary with response and relevant documents
    """
    if not HAS_LLM:
        return {
            "response": "LLM API not available. Cannot generate response.",
            "relevant_documents": []
        }
    
    # Retrieve relevant documents
    results = search(query, limit=limit)
    
    if not results:
        return {
            "response": "I don't have any relevant information to answer your question.",
            "relevant_documents": []
        }
    
    # Format context for the LLM
    context = "\n\n".join([f"Document {i+1}:\n{result['content']}" 
                          for i, result in enumerate(results)])
    
    # Create prompt for the LLM
    prompt = f"""You are a helpful assistant that answers questions based on the provided context.
If the context doesn't contain relevant information, say so instead of making up an answer.

Context:
{context}

Question: {query}

Answer:"""
    
    # Use LLM API for response generation
    response = query_llm(prompt, provider=provider)
    
    return {
        "response": response,
        "relevant_documents": results
    }

def process_metadata_args(args) -> Dict[str, Any]:
    """Process metadata arguments from command line args."""
    metadata = {}
    if hasattr(args, 'source') and args.source:
        metadata["source"] = args.source
    if hasattr(args, 'tags') and args.tags:
        metadata["tags"] = args.tags.split(",")
    return metadata

def main():
    """Command-line interface for the RAG Librarian."""
    parser = argparse.ArgumentParser(description="RAG Librarian - Knowledge Management System")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add text command
    add_parser = subparsers.add_parser("add", help="Add text to the knowledge base")
    add_parser.add_argument("text", help="Text to add")
    add_parser.add_argument("--source", help="Source of the text")
    add_parser.add_argument("--tags", help="Comma-separated tags")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=5, help="Maximum number of results")
    search_parser.add_argument("--source", help="Filter by source")
    search_parser.add_argument("--tags", help="Filter by comma-separated tags")
    search_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query the knowledge base with natural language")
    query_parser.add_argument("query", help="The query to search for")
    query_parser.add_argument("--limit", type=int, default=5, help="Maximum number of documents to retrieve")
    query_parser.add_argument("--provider", default="openai", 
                             choices=["openai", "anthropic", "gemini", "deepseek", "local"], 
                             help="LLM provider to use")
    query_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    # List documents command
    list_parser = subparsers.add_parser("list", help="List all documents in the knowledge base")
    list_parser.add_argument("--limit", type=int, default=100, help="Maximum number of documents")
    list_parser.add_argument("--source", help="Filter by source")
    list_parser.add_argument("--tags", help="Filter by comma-separated tags")
    list_parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    
    # Delete document command
    delete_parser = subparsers.add_parser("delete", help="Delete a document from the knowledge base")
    delete_parser.add_argument("doc_id", help="Document ID to delete")
    
    # Clear database command
    clear_parser = subparsers.add_parser("clear", help="Clear the knowledge base")
    clear_parser.add_argument("--confirm", action="store_true", help="Confirm clearing the database")
    
    # Add ingestion commands if available
    if HAS_INGEST:
        # Ingest file command
        ingest_file_parser = subparsers.add_parser("ingest-file", help="Ingest a file into the knowledge base")
        ingest_file_parser.add_argument("file_path", help="Path to the file")
        ingest_file_parser.add_argument("--source", help="Source of the file")
        ingest_file_parser.add_argument("--tags", help="Comma-separated tags")
        ingest_file_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
        ingest_file_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
        
        # Ingest directory command
        ingest_dir_parser = subparsers.add_parser("ingest-directory", help="Ingest a directory of files")
        ingest_dir_parser.add_argument("directory_path", help="Path to the directory")
        ingest_dir_parser.add_argument("--recursive", action="store_true", help="Recursively process subdirectories")
        ingest_dir_parser.add_argument("--file-pattern", default="*.*", help="File pattern to match (e.g., '*.txt')")
        ingest_dir_parser.add_argument("--source", help="Source of the files")
        ingest_dir_parser.add_argument("--tags", help="Comma-separated tags")
        ingest_dir_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
        ingest_dir_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
        
        # Ingest YouTube command
        ingest_yt_parser = subparsers.add_parser("ingest-youtube", help="Ingest a YouTube video transcript")
        ingest_yt_parser.add_argument("video_id", help="YouTube video ID or URL")
        ingest_yt_parser.add_argument("--source", default="youtube", help="Source label (default: 'youtube')")
        ingest_yt_parser.add_argument("--tags", help="Comma-separated tags")
        ingest_yt_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
        ingest_yt_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
        
        # Ingest web page command
        ingest_web_parser = subparsers.add_parser("ingest-web", help="Ingest a web page")
        ingest_web_parser.add_argument("url", help="URL of the web page")
        ingest_web_parser.add_argument("--source", default="web", help="Source label (default: 'web')")
        ingest_web_parser.add_argument("--tags", help="Comma-separated tags")
        ingest_web_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
        ingest_web_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
        
        # Ingest text command
        ingest_text_parser = subparsers.add_parser("ingest-text", help="Ingest text with chunking")
        ingest_text_parser.add_argument("text", help="Text to ingest")
        ingest_text_parser.add_argument("--source", help="Source of the text")
        ingest_text_parser.add_argument("--tags", help="Comma-separated tags")
        ingest_text_parser.add_argument("--chunk-size", type=int, default=2000, help="Size of each chunk")
        ingest_text_parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "add":
        metadata = process_metadata_args(args)
        doc_id = add_text(args.text, metadata)
        print(f"Added text with ID: {doc_id}")
    
    elif args.command == "search":
        metadata_filter = {}
        if args.source:
            metadata_filter["source"] = args.source
        if args.tags:
            metadata_filter["tags"] = {"$in": args.tags.split(",")}
        
        results = search(args.query, args.limit, metadata_filter)
        
        if not results:
            print("No results found.")
        else:
            if args.format == "json":
                print(json.dumps(results, indent=2))
            else:
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results):
                    print(f"\n--- Result {i+1} (Score: {result['score']:.4f}) ---")
                    print(f"Content: {result['content']}")
                    print(f"Metadata: {result['metadata']}")
    
    elif args.command == "query":
        if not HAS_LLM:
            print("Error: LLM API not available. Cannot execute query command.")
            sys.exit(1)
        
        result = query_rag(args.query, args.limit, args.provider)
        
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print("\n=== RAG Response ===")
            print(result["response"])
            
            print("\n=== Relevant Documents ===")
            if not result["relevant_documents"]:
                print("No relevant documents found.")
            else:
                for i, doc in enumerate(result["relevant_documents"]):
                    print(f"\n--- Document {i+1} (Score: {doc['score']:.4f}) ---")
                    print(f"Content: {doc['content'][:200]}...")
                    print(f"Metadata: {doc['metadata']}")
    
    elif args.command == "list":
        metadata_filter = {}
        if args.source:
            metadata_filter["source"] = args.source
        if args.tags:
            metadata_filter["tags"] = {"$in": args.tags.split(",")}
        
        documents = get_all_documents(args.limit, metadata_filter)
        
        if not documents:
            print("No documents found.")
        else:
            if args.format == "json":
                print(json.dumps(documents, indent=2))
            else:
                print(f"Found {len(documents)} documents:")
                for i, doc in enumerate(documents):
                    print(f"\n--- Document {i+1} ---")
                    print(f"ID: {doc['id']}")
                    print(f"Content: {doc['content'][:200]}...")
                    print(f"Metadata: {doc['metadata']}")
    
    elif args.command == "delete":
        success = delete_document(args.doc_id)
        if success:
            print(f"Deleted document with ID: {args.doc_id}")
        else:
            print(f"Failed to delete document with ID: {args.doc_id}")
    
    elif args.command == "clear":
        if not args.confirm:
            print("Warning: This will delete all documents in the knowledge base.")
            print("Use --confirm to proceed.")
            return
        
        success = clear_database()
        if success:
            print("Knowledge base cleared successfully.")
        else:
            print("Failed to clear knowledge base.")
    
    elif HAS_INGEST and args.command == "ingest-file":
        metadata = process_metadata_args(args)
        doc_ids = ingest_file(
            args.file_path, 
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print(f"Ingested file {args.file_path} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif HAS_INGEST and args.command == "ingest-directory":
        metadata = process_metadata_args(args)
        results = ingest_directory(
            args.directory_path,
            recursive=args.recursive,
            file_pattern=args.file_pattern,
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        total_files = len(results)
        total_chunks = sum(len(ids) for ids in results.values())
        print(f"Ingested {total_files} files into {total_chunks} chunks")
        for file_path, doc_ids in results.items():
            print(f"- {file_path}: {len(doc_ids)} chunks")
    
    elif HAS_INGEST and args.command == "ingest-youtube":
        metadata = process_metadata_args(args)
        # Check if input is a URL or video ID
        video_id = args.video_id
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = extract_youtube_id(video_id)
        
        doc_ids = ingest_youtube(
            video_id,
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print(f"Ingested YouTube video {video_id} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif HAS_INGEST and args.command == "ingest-web":
        metadata = process_metadata_args(args)
        doc_ids = ingest_web(
            args.url,
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print(f"Ingested web page {args.url} into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    elif HAS_INGEST and args.command == "ingest-text":
        metadata = process_metadata_args(args)
        doc_ids = ingest_text(
            args.text,
            metadata=metadata,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap
        )
        print(f"Ingested text into {len(doc_ids)} chunks with IDs: {', '.join(doc_ids)}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 