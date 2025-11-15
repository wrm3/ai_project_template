#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Knowledge Base Manager

Organizes and manages document collections with RAG capabilities.
Provides categorization, batch processing, and search interfaces.

Features:
- Category-based organization
- Automatic document processing
- Metadata tracking
- Batch ingestion
- Search and retrieval
- Export/import capabilities

Usage:
    from knowledge_base import KnowledgeBase

    # Initialize knowledge base
    kb = KnowledgeBase("./data/knowledge_base")

    # Add documents
    kb.add_document("document.pdf", category="technical")

    # Search
    results = kb.search("query text", limit=5)

    # List all documents
    documents = kb.list_documents()
"""

import os
import sys
import json
import shutil
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import time

# Add script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from rag_utils import RAGSystem, create_rag_system, SearchResult
from document_processor import process_document, process_directory


class KnowledgeBase:
    """
    Knowledge base manager with RAG capabilities

    Manages document collections organized by categories, with full RAG support
    for semantic search and retrieval.
    """

    DEFAULT_CATEGORIES = [
        "technical",      # Technical documentation, specs
        "business",       # Business documents, reports
        "reference",      # Reference materials, guides
        "documentation",  # User documentation, manuals
        "research",       # Research papers, articles
        "code",          # Code examples, snippets
        "other"          # Miscellaneous
    ]

    def __init__(
        self,
        base_path: str,
        auto_load: bool = True,
        create_categories: bool = True
    ):
        """
        Initialize knowledge base

        Args:
            base_path: Base directory for knowledge base
            auto_load: Automatically load existing documents on init
            create_categories: Create default category directories
        """
        self.base_path = Path(base_path)

        # Directory structure
        self.docs_path = self.base_path / "documents"
        self.metadata_path = self.base_path / "metadata"
        self.vector_store_path = self.base_path / "vector_store"
        self.exports_path = self.base_path / "exports"

        # Create directory structure
        self._create_directory_structure(create_categories)

        # Initialize RAG system
        self.rag_system = create_rag_system(
            persist_directory=str(self.vector_store_path)
        )

        # Load existing documents if requested
        if auto_load:
            print("[KB] Loading existing documents...")
            self.load_all_documents()

        print(f"[KB] Knowledge Base initialized at: {self.base_path}")

    def _create_directory_structure(self, create_categories: bool = True) -> None:
        """Create knowledge base directory structure"""
        # Create main directories
        self.docs_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        self.exports_path.mkdir(parents=True, exist_ok=True)

        # Create category subdirectories
        if create_categories:
            for category in self.DEFAULT_CATEGORIES:
                (self.docs_path / category).mkdir(exist_ok=True)

    def add_document(
        self,
        source_path: str,
        category: str = "other",
        metadata: Optional[Dict[str, Any]] = None,
        copy_file: bool = True
    ) -> str:
        """
        Add a document to the knowledge base

        Args:
            source_path: Path to source document
            category: Category for organization
            metadata: Additional metadata
            copy_file: Whether to copy file to knowledge base

        Returns:
            Document ID

        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        print(f"\n[KB] Adding document: {source_path.name}")
        print(f"[KB] Category: {category}")

        # Determine target path
        target_dir = self.docs_path / category
        target_dir.mkdir(exist_ok=True)
        target_path = target_dir / source_path.name

        # Copy or link file
        if copy_file:
            shutil.copy2(source_path, target_path)
            print(f"[KB] Copied to: {target_path}")
        else:
            # Just track the original path
            target_path = source_path

        # Process document
        print("[KB] Processing document...")
        start_time = time.time()

        base_metadata = metadata or {}
        base_metadata["category"] = category
        base_metadata["ingestion_date"] = datetime.now().isoformat()

        content, doc_metadata = process_document(str(source_path), base_metadata)

        # Generate document ID
        doc_id = f"doc_{int(time.time() * 1000)}"
        doc_metadata["doc_id"] = doc_id

        # Save metadata
        metadata_file = self.metadata_path / f"{target_path.stem}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(doc_metadata, f, indent=2)

        print(f"[KB] Metadata saved: {metadata_file.name}")

        # Add to RAG system
        print("[KB] Adding to RAG system...")
        self.rag_system.add_text(content, doc_metadata)

        duration = time.time() - start_time
        print(f"[KB] ✅ Document added successfully in {duration:.2f}s")
        print(f"[KB] Document ID: {doc_id}")

        return doc_id

    def add_documents_batch(
        self,
        directory_path: str,
        category: str = "other",
        recursive: bool = True,
        file_extensions: List[str] = None
    ) -> List[str]:
        """
        Add multiple documents from a directory

        Args:
            directory_path: Path to directory containing documents
            category: Category for all documents
            recursive: Process subdirectories
            file_extensions: Filter by extensions (e.g., ['.pdf', '.docx'])

        Returns:
            List of document IDs
        """
        print(f"\n[KB] Batch ingestion from: {directory_path}")
        print(f"[KB] Category: {category}")
        print(f"[KB] Recursive: {recursive}")

        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Invalid directory: {directory_path}")

        doc_ids = []
        pattern = "**/*" if recursive else "*"

        # Collect files
        files = [
            f for f in directory.glob(pattern)
            if f.is_file() and (
                not file_extensions or f.suffix.lower() in file_extensions
            )
        ]

        print(f"[KB] Found {len(files)} files to process\n")

        # Process each file
        for i, file_path in enumerate(files, 1):
            try:
                print(f"[KB] Processing {i}/{len(files)}: {file_path.name}")
                doc_id = self.add_document(
                    str(file_path),
                    category=category,
                    copy_file=True
                )
                doc_ids.append(doc_id)
            except Exception as e:
                print(f"[KB] ❌ Error processing {file_path.name}: {e}")

        print(f"\n[KB] ✅ Batch ingestion complete: {len(doc_ids)}/{len(files)} documents added")
        return doc_ids

    def load_all_documents(self) -> int:
        """
        Load all documents from the knowledge base into RAG system

        Returns:
            Number of documents loaded
        """
        count = 0

        if not self.docs_path.exists():
            return count

        for category_dir in self.docs_path.iterdir():
            if not category_dir.is_dir():
                continue

            category = category_dir.name

            for doc_path in category_dir.iterdir():
                if not doc_path.is_file():
                    continue

                # Load metadata if available
                metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                metadata = {}

                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                else:
                    metadata = {"category": category}

                # Process and add to RAG system
                try:
                    content, doc_metadata = process_document(str(doc_path), metadata)
                    self.rag_system.add_text(content, doc_metadata, chunk=True)
                    count += 1
                except Exception as e:
                    print(f"[KB] Error loading {doc_path.name}: {e}")

        if count > 0:
            print(f"[KB] Loaded {count} documents")

        return count

    def search(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search the knowledge base

        Args:
            query: Search query
            limit: Maximum number of results
            category: Filter by category
            metadata_filter: Additional metadata filters

        Returns:
            List of SearchResult objects
        """
        # Build metadata filter
        filter_dict = metadata_filter or {}

        if category:
            filter_dict["category"] = category

        return self.rag_system.query(query, limit, filter_dict if filter_dict else None)

    def list_documents(
        self,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all documents in the knowledge base

        Args:
            category: Filter by category (optional)

        Returns:
            List of document info dictionaries
        """
        documents = []

        if not self.docs_path.exists():
            return documents

        # Determine which categories to list
        if category:
            categories = [category] if (self.docs_path / category).exists() else []
        else:
            categories = [d.name for d in self.docs_path.iterdir() if d.is_dir()]

        # Collect document info
        for cat in categories:
            cat_dir = self.docs_path / cat

            for doc_path in cat_dir.iterdir():
                if not doc_path.is_file():
                    continue

                # Load metadata
                metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                metadata = {}

                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                documents.append({
                    "name": doc_path.name,
                    "category": cat,
                    "path": str(doc_path),
                    "size": doc_path.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        doc_path.stat().st_mtime
                    ).isoformat(),
                    "metadata": metadata
                })

        return documents

    def remove_document(
        self,
        document_name: str,
        category: Optional[str] = None
    ) -> bool:
        """
        Remove a document from the knowledge base

        Args:
            document_name: Name of document to remove
            category: Category (searches all if not specified)

        Returns:
            Success status
        """
        # Search for document
        if category:
            doc_path = self.docs_path / category / document_name
            if doc_path.exists():
                doc_path.unlink()

                # Remove metadata
                metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                if metadata_file.exists():
                    metadata_file.unlink()

                print(f"[KB] Removed: {document_name} (category: {category})")
                return True
        else:
            # Search all categories
            for cat_dir in self.docs_path.iterdir():
                if not cat_dir.is_dir():
                    continue

                doc_path = cat_dir / document_name
                if doc_path.exists():
                    doc_path.unlink()

                    # Remove metadata
                    metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                    if metadata_file.exists():
                        metadata_file.unlink()

                    print(f"[KB] Removed: {document_name} (category: {cat_dir.name})")
                    return True

        print(f"[KB] Document not found: {document_name}")
        return False

    def export_metadata(self, output_file: str = None) -> str:
        """
        Export all metadata to JSON file

        Args:
            output_file: Output file path (auto-generated if not specified)

        Returns:
            Path to exported file
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.exports_path / f"metadata_export_{timestamp}.json"
        else:
            output_file = Path(output_file)

        documents = self.list_documents()

        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_documents": len(documents),
            "knowledge_base_path": str(self.base_path),
            "documents": documents
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        print(f"[KB] Metadata exported to: {output_file}")
        return str(output_file)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics

        Returns:
            Dictionary with statistics
        """
        documents = self.list_documents()

        # Count by category
        category_counts = {}
        total_size = 0

        for doc in documents:
            cat = doc['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
            total_size += doc.get('size', 0)

        # Get file type counts
        file_type_counts = {}
        for doc in documents:
            ext = Path(doc['name']).suffix.lower()
            file_type_counts[ext] = file_type_counts.get(ext, 0) + 1

        return {
            "total_documents": len(documents),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "categories": category_counts,
            "file_types": file_type_counts,
            "vector_store_path": str(self.vector_store_path),
        }


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("Knowledge Base Manager - Test")
    print("=" * 80)
    print()

    # Create test knowledge base
    kb = KnowledgeBase("./test_kb", auto_load=False)

    # Create a test document
    test_file = "test_doc.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test document about RAG systems.\n\n")
        f.write("RAG combines retrieval with generation for better AI responses.")

    try:
        # Add document
        print("[TEST] Adding document...")
        doc_id = kb.add_document(test_file, category="technical")

        # List documents
        print("\n[TEST] Listing documents...")
        docs = kb.list_documents()
        print(f"Found {len(docs)} documents")

        # Search
        print("\n[TEST] Searching for 'RAG systems'...")
        results = kb.search("RAG systems", limit=2)

        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"  Score: {result.score:.4f}")
            print(f"  Category: {result.metadata.get('category')}")
            print(f"  Text: {result.text[:100]}...")

        # Statistics
        print("\n[TEST] Knowledge base statistics:")
        stats = kb.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\n✅ Test complete!")

    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if Path("./test_kb").exists():
            shutil.rmtree("./test_kb")
