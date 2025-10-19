#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retrieval Augmented Generation (RAG) Utilities

This module provides utilities for creating, managing, and querying a vector database
to store and retrieve information for retrieval augmented generation.

Example:
    from tools.rag_utils import add_text, add_document, search
    
    # Add some text with metadata
    add_text("This is important information about X.", {"source": "user conversation", "date": "2024-01-01"})
    
    # Add a document file
    add_document("path/to/document.pdf", {"source": "uploaded file", "topic": "finance"})
    
    # Search for relevant information
    results = search("Tell me about X", limit=5)
    for result in results:
        print(f"Content: {result.text}")
        print(f"Metadata: {result.metadata}")
        print(f"Relevance: {result.score}")
"""

import os
import sys
import json
import uuid
import datetime
from typing import List, Dict, Any, Union, Optional, Tuple
from pathlib import Path

# Add the parent directory to the path so we can import from libs
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import dependencies
try:
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import (
        TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader, UnstructuredMarkdownLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import Embeddings
    from langchain_core.documents import Document
    from sentence_transformers import SentenceTransformer
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "langchain-community", "langchain-chroma", "sentence-transformers", "langchain-text-splitters",
                          "python-dotenv", "pypdf", "docx2txt", "unstructured"])
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import (
        TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader, UnstructuredMarkdownLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import Embeddings
    from langchain_core.documents import Document
    from sentence_transformers import SentenceTransformer
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default settings from environment variables or use defaults
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', os.path.join(parent_dir, 'vector_db'))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))

# Create directory for vector database if it doesn't exist
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

class LocalEmbeddings(Embeddings):
    """Wrapper for sentence_transformers embeddings for use with LangChain."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence_transformers model to use
        """
        self.model = SentenceTransformer(model_name)
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents.
        
        Args:
            texts: List of document texts to embed
            
        Returns:
            List of embedding vectors
        """
        return self.model.encode(texts).tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embeddings for a query string.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector
        """
        return self.model.encode(text).tolist()

# Initialize embeddings and vector store
_embeddings = LocalEmbeddings()
_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

def _get_vector_store():
    """Get or create the vector store."""
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=_embeddings
    )

def add_text(text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Add text to the vector database.
    
    Args:
        text: The text content to add
        metadata: Optional metadata for the text
        
    Returns:
        ID of the added document
    """
    if metadata is None:
        metadata = {}
    
    # Add timestamp and ID if not provided
    if 'timestamp' not in metadata:
        metadata['timestamp'] = datetime.datetime.now().isoformat()
    if 'id' not in metadata:
        metadata['id'] = str(uuid.uuid4())
    
    # Split text into chunks
    chunks = _text_splitter.split_text(text)
    
    # Create documents with metadata
    documents = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = metadata.copy()
        chunk_metadata['chunk'] = i
        chunk_metadata['chunk_total'] = len(chunks)
        documents.append(Document(page_content=chunk, metadata=chunk_metadata))
    
    # Add to vector store
    vector_store = _get_vector_store()
    vector_store.add_documents(documents)
    
    return metadata['id']

def add_document(file_path: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Add a document file to the vector database.
    
    Args:
        file_path: Path to the document file
        metadata: Optional metadata for the document
        
    Returns:
        ID of the added document
    """
    if metadata is None:
        metadata = {}
    
    # Add file info to metadata
    file_path = Path(file_path)
    metadata['source'] = str(file_path)
    metadata['filename'] = file_path.name
    
    # Select appropriate loader based on file extension
    ext = file_path.suffix.lower()
    if ext == '.pdf':
        loader = PyPDFLoader(str(file_path))
    elif ext in ('.docx', '.doc'):
        loader = Docx2txtLoader(str(file_path))
    elif ext == '.txt':
        loader = TextLoader(str(file_path))
    elif ext == '.csv':
        loader = CSVLoader(str(file_path))
    elif ext in ('.md', '.markdown'):
        loader = UnstructuredMarkdownLoader(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Load and split the document
    documents = loader.load()
    split_docs = _text_splitter.split_documents(documents)
    
    # Update metadata for each chunk
    doc_id = str(uuid.uuid4())
    for i, doc in enumerate(split_docs):
        doc.metadata.update(metadata)
        doc.metadata['id'] = doc_id
        doc.metadata['chunk'] = i
        doc.metadata['chunk_total'] = len(split_docs)
    
    # Add to vector store
    vector_store = _get_vector_store()
    vector_store.add_documents(split_docs)
    
    return doc_id

def search(query: str, limit: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Search for relevant documents based on a query.
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        metadata_filter: Optional filter for metadata fields
        
    Returns:
        List of relevant documents with content, metadata, and relevance score
    """
    vector_store = _get_vector_store()
    
    # Perform the search
    results = vector_store.similarity_search_with_relevance_scores(
        query, k=limit, filter=metadata_filter
    )
    
    # Format the results
    formatted_results = []
    for doc, score in results:
        # Normalize scores to be between 0 and 1
        # Some embedding models may return scores outside of this range
        normalized_score = max(0, min(1, score))
        formatted_results.append({
            'text': doc.page_content,
            'metadata': doc.metadata,
            'score': normalized_score
        })
    
    return formatted_results

def get_all_documents(limit: int = 100, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Get all documents in the database, optionally filtered by metadata.
    
    Args:
        limit: Maximum number of documents to return
        metadata_filter: Optional filter for metadata fields
        
    Returns:
        List of documents with content and metadata
    """
    vector_store = _get_vector_store()
    
    # Get all documents
    try:
        # For newer versions of Chroma
        where = metadata_filter if metadata_filter else None
        collection = vector_store._collection
        results = collection.get(limit=limit, where=where)
        documents = []
        for i in range(len(results['ids'])):
            metadata = results['metadatas'][i] if results['metadatas'] and i < len(results['metadatas']) else {}
            # Ensure ID is available in the metadata for compatibility with test script
            if 'id' not in metadata and results['ids'] and i < len(results['ids']):
                metadata['id'] = results['ids'][i]
            
            documents.append({
                'id': results['ids'][i],
                'text': results['documents'][i],
                'metadata': metadata
            })
        return documents
    except Exception as e:
        print(f"Error getting documents: {e}")
        return []

def delete_document(doc_id: str) -> bool:
    """Delete a document and all its chunks from the database.
    
    Args:
        doc_id: The document ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        vector_store = _get_vector_store()
        vector_store.delete(filter={"id": doc_id})
        return True
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False

def clear_database() -> bool:
    """Clear all documents from the database.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        vector_store = _get_vector_store()
        collection = vector_store._collection
        # Get all document IDs
        results = collection.get()
        if results and 'ids' in results and results['ids']:
            # Delete all documents by their IDs
            collection.delete(ids=results['ids'])
        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False

# Example usage
if __name__ == "__main__":
    print("This module is intended to be imported, not run directly.")
    print("Example usage:")
    print("  from tools.rag_utils import add_text, add_document, search")
    print("  doc_id = add_text('This is a test document', {'source': 'test'})")
    print("  results = search('test document')") 