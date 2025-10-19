#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retrieval Augmented Generation (RAG) Access Tool

This tool provides a command-line interface for managing the RAG database.
It allows adding text and documents, searching for information, and managing stored data.

Usage:
    python tools/rag_access.py --add-text "Your text here" [--metadata '{"key": "value"}']
    python tools/rag_access.py --add-file "path/to/file.pdf" [--metadata '{"topic": "AI"}']
    python tools/rag_access.py --search "Your search query" [--limit 5]
    python tools/rag_access.py --list [--limit 10]
    python tools/rag_access.py --delete "document_id"
    python tools/rag_access.py --clear-all
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to the path so we can import from the tools
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Try to import our RAG utilities
try:
    from tools.rag_utils import (
        add_text, add_document, search, get_all_documents, delete_document, clear_database
    )
except ImportError:
    print("Error: RAG utilities not found. Make sure tools/rag_utils.py exists.")
    sys.exit(1)

def parse_metadata(metadata_str: Optional[str]) -> Dict[str, Any]:
    """Parse a JSON metadata string into a dictionary.
    
    Args:
        metadata_str: JSON string containing metadata
        
    Returns:
        Dictionary of metadata or empty dict if invalid
    """
    if not metadata_str:
        return {}
    
    try:
        return json.loads(metadata_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing metadata: {e}")
        print("Metadata should be valid JSON, e.g., '{\"key\": \"value\"}'")
        return {}

def format_document(doc: Dict[str, Any], show_full_text: bool = False) -> str:
    """Format a document for display.
    
    Args:
        doc: Document dictionary
        show_full_text: Whether to show the full text or a preview
        
    Returns:
        Formatted string representation
    """
    text = doc['text']
    if not show_full_text and len(text) > 100:
        text = text[:97] + "..."
    
    metadata = doc.get('metadata', {})
    
    # Format metadata for display
    metadata_str = "\n  ".join([f"{k}: {v}" for k, v in metadata.items() 
                              if k not in ('chunk', 'chunk_total')])
    
    result = f"ID: {metadata.get('id', 'unknown')}\n"
    result += f"Text: {text}\n"
    if 'score' in doc:
        result += f"Relevance: {doc['score']:.4f}\n"
    result += f"Metadata:\n  {metadata_str}"
    
    return result

def main():
    parser = argparse.ArgumentParser(description='RAG Database Management Tool')
    
    # Action group
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--add-text', help='Add text to the database')
    action_group.add_argument('--add-file', help='Add a document file to the database')
    action_group.add_argument('--search', help='Search for text in the database')
    action_group.add_argument('--list', action='store_true', help='List documents in the database')
    action_group.add_argument('--delete', help='Delete a document by ID')
    action_group.add_argument('--clear-all', action='store_true', help='Clear all documents from the database')
    
    # Options
    parser.add_argument('--metadata', help='JSON metadata to attach to the document')
    parser.add_argument('--limit', type=int, default=5, help='Maximum number of results to return')
    parser.add_argument('--full-text', action='store_true', help='Show full document text instead of preview')
    
    args = parser.parse_args()
    
    try:
        if args.add_text:
            metadata = parse_metadata(args.metadata)
            doc_id = add_text(args.add_text, metadata)
            print(f"Text added successfully with ID: {doc_id}")
        
        elif args.add_file:
            file_path = args.add_file
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                sys.exit(1)
                
            metadata = parse_metadata(args.metadata)
            doc_id = add_document(file_path, metadata)
            print(f"Document added successfully with ID: {doc_id}")
        
        elif args.search:
            results = search(args.search, limit=args.limit)
            if not results:
                print("No matching documents found.")
            else:
                print(f"Found {len(results)} matching documents:")
                for i, result in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(format_document(result, args.full_text))
        
        elif args.list:
            documents = get_all_documents(limit=args.limit)
            if not documents:
                print("No documents in the database.")
            else:
                print(f"Retrieved {len(documents)} documents:")
                for i, doc in enumerate(documents, 1):
                    print(f"\n--- Document {i} ---")
                    print(format_document(doc, args.full_text))
        
        elif args.delete:
            success = delete_document(args.delete)
            if success:
                print(f"Document {args.delete} deleted successfully.")
            else:
                print(f"Failed to delete document {args.delete}.")
        
        elif args.clear_all:
            confirm = input("Are you sure you want to clear ALL documents? (y/N): ")
            if confirm.lower() == 'y':
                success = clear_database()
                if success:
                    print("Database cleared successfully.")
                else:
                    print("Failed to clear database.")
            else:
                print("Operation cancelled.")
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 