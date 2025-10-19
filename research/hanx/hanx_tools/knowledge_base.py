"""
Knowledge base manager for organizing and loading documents.
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import shutil
from datetime import datetime

from document_processors import process_document
from rag_utils import VectorStore, RAGSystem

class KnowledgeBase:
    """Manages a collection of documents and their metadata."""
    def __init__(
        self,
        base_path: str,
        rag_system: RAGSystem,
        auto_load: bool = True
    ):
        self.base_path = Path(base_path)
        self.rag_system = rag_system
        
        # Create directory structure
        self.docs_path = self.base_path / "documents"
        self.metadata_path = self.base_path / "metadata"
        self.vector_store_path = self.base_path / "vector_store"
        
        self._create_directory_structure()
        
        if auto_load:
            self.load_all_documents()

    def _create_directory_structure(self) -> None:
        """Create the knowledge base directory structure."""
        # Create main directories
        self.docs_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Create category subdirectories
        categories = [
            "technical",
            "business",
            "reference",
            "documentation",
            "articles",
            "other"
        ]
        
        for category in categories:
            (self.docs_path / category).mkdir(exist_ok=True)

    def add_document(
        self,
        source_path: str,
        category: str = "other",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a document to the knowledge base."""
        source_path = Path(source_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Determine target path
        target_dir = self.docs_path / category
        target_path = target_dir / source_path.name
        
        # Copy file to knowledge base
        shutil.copy2(source_path, target_path)
        
        # Process document
        base_metadata = metadata or {}
        base_metadata["category"] = category
        content, doc_metadata = process_document(str(target_path), base_metadata)
        
        # Save metadata
        metadata_file = self.metadata_path / f"{target_path.stem}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(doc_metadata, f, indent=2)
        
        # Add to RAG system
        self.rag_system.add_documents([content], [doc_metadata])
        
        print(f"Added document: {target_path.name}")
        print(f"Category: {category}")
        print(f"Metadata saved to: {metadata_file.name}")

    def load_all_documents(self) -> None:
        """Load all documents from the knowledge base into the RAG system."""
        print("Loading knowledge base documents...")
        
        for category_dir in self.docs_path.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                print(f"\nProcessing category: {category}")
                
                for doc_path in category_dir.iterdir():
                    if doc_path.is_file():
                        # Load existing metadata if available
                        metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                        metadata = {}
                        if metadata_file.exists():
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                        
                        # Process document
                        try:
                            content, doc_metadata = process_document(str(doc_path), metadata)
                            self.rag_system.add_documents([content], [doc_metadata])
                            print(f"Loaded: {doc_path.name}")
                        except Exception as e:
                            print(f"Error loading {doc_path.name}: {str(e)}")

    def list_documents(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all documents in the knowledge base."""
        documents = []
        
        categories = [category] if category else [d.name for d in self.docs_path.iterdir() if d.is_dir()]
        
        for cat in categories:
            cat_dir = self.docs_path / cat
            if cat_dir.exists() and cat_dir.is_dir():
                for doc_path in cat_dir.iterdir():
                    if doc_path.is_file():
                        metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                        metadata = {}
                        if metadata_file.exists():
                            with open(metadata_file, 'r', encoding='utf-8') as f:
                                metadata = json.load(f)
                        
                        documents.append({
                            "name": doc_path.name,
                            "category": cat,
                            "path": str(doc_path),
                            "metadata": metadata
                        })
        
        return documents

    def remove_document(self, document_name: str, category: Optional[str] = None) -> None:
        """Remove a document from the knowledge base."""
        # Find the document
        if category:
            doc_path = self.docs_path / category / document_name
            if doc_path.exists():
                doc_path.unlink()
                
                # Remove metadata
                metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                if metadata_file.exists():
                    metadata_file.unlink()
                
                print(f"Removed document: {document_name}")
                print(f"Category: {category}")
                return
        else:
            # Search in all categories
            for cat_dir in self.docs_path.iterdir():
                if cat_dir.is_dir():
                    doc_path = cat_dir / document_name
                    if doc_path.exists():
                        doc_path.unlink()
                        
                        # Remove metadata
                        metadata_file = self.metadata_path / f"{doc_path.stem}.json"
                        if metadata_file.exists():
                            metadata_file.unlink()
                        
                        print(f"Removed document: {document_name}")
                        print(f"Category: {cat_dir.name}")
                        return
        
        raise FileNotFoundError(f"Document not found: {document_name}")

def main():
    """Example usage of the knowledge base."""
    from rag_utils import VectorStore, OpenAIRAGSystem
    
    # Initialize RAG system
    vector_store = VectorStore("./data/kb_vector_store")
    rag_system = OpenAIRAGSystem(
        vector_store=vector_store,
        embedding_model=None,
        llm=None
    )
    
    # Initialize knowledge base
    kb = KnowledgeBase(
        base_path="./data/knowledge_base",
        rag_system=rag_system
    )
    
    # Example: Add a document
    # kb.add_document("path/to/document.pdf", category="technical")
    
    # List documents
    documents = kb.list_documents()
    print("\nKnowledge Base Contents:")
    for doc in documents:
        print(f"\nDocument: {doc['name']}")
        print(f"Category: {doc['category']}")
        print(f"Metadata: {json.dumps(doc['metadata'], indent=2)}")

if __name__ == "__main__":
    main() 