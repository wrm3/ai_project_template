#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retrieval Augmented Generation (RAG) Utilities Tool

This module provides utilities for creating, managing, and querying a vector database
to store and retrieve information for retrieval augmented generation.

Example:
    from hanx_tools.tool_rag_utils import VectorStore, RAGSystem, OpenAIRAGSystem
    
    # Initialize vector store
    vector_store = VectorStore("../hanx_data/vector_store")
    
    # Initialize RAG system
    rag = OpenAIRAGSystem(vector_store=vector_store)
    
    # Add documents
    rag.add_documents(["Document content here"], [{"source": "example"}])
    
    # Query the system
    results = rag.query("Your question here?")
"""

import os
import sys
import json
import uuid
import datetime
import time
import numpy as np
from typing import List, Dict, Any, Union, Optional, Tuple
from pathlib import Path
from abc import ABC, abstractmethod

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
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', os.path.join(os.getcwd(), 'vector_db'))
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))

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

class VectorStore:
    """Vector store for document embeddings and similarity search."""
    
    def __init__(self, persist_directory: str = VECTOR_DB_PATH, embedding_function: Optional[Embeddings] = None):
        """Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the vector store
            embedding_function: Embedding function to use
        """
        self.persist_directory = persist_directory
        self.embedding_function = embedding_function or LocalEmbeddings()
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        # Initialize vector store
        self.store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_function
        )
    
    def _process_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process metadata to ensure compatibility with Chroma.
        
        Args:
            metadata: Metadata dictionary
            
        Returns:
            Processed metadata dictionary
        """
        processed = metadata.copy()
        
        # Convert list values to strings to avoid Chroma errors
        for key, value in list(processed.items()):
            if isinstance(value, list):
                processed[key] = ", ".join(str(item) for item in value)
        
        return processed
    
    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add text to the vector store.
        
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
        chunks = self.text_splitter.split_text(text)
        
        # Create documents with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = self._process_metadata(metadata.copy())
            chunk_metadata['chunk'] = i
            chunk_metadata['chunk_total'] = len(chunks)
            documents.append(Document(page_content=chunk, metadata=chunk_metadata))
        
        # Add to vector store
        self.store.add_documents(documents)
        
        return metadata['id']
    
    def add_document(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a document file to the vector store.
        
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
        split_docs = self.text_splitter.split_documents(documents)
        
        # Update metadata for each chunk
        doc_id = str(uuid.uuid4())
        for i, doc in enumerate(split_docs):
            processed_metadata = self._process_metadata(metadata.copy())
            doc.metadata.update(processed_metadata)
            doc.metadata['id'] = doc_id
            doc.metadata['chunk'] = i
            doc.metadata['chunk_total'] = len(split_docs)
        
        # Add to vector store
        self.store.add_documents(split_docs)
        
        return doc_id
    
    def search(self, query: str, limit: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents based on a query.
        
        Args:
            query: The search query
            limit: Maximum number of results to return
            metadata_filter: Optional filter for metadata fields
            
        Returns:
            List of relevant documents with content, metadata, and relevance score
        """
        # Perform the search
        try:
            # Handle empty metadata filter
            if not metadata_filter:
                results = self.store.similarity_search_with_score(query, k=limit)
                formatted_results = []
                for doc, score in results:
                    # Normalize scores to be between 0 and 1
                    normalized_score = max(0, min(1, score))
                    formatted_results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'score': normalized_score
                    })
                return formatted_results
            else:
                # Format the filter for Chroma
                where = {}
                for key, value in metadata_filter.items():
                    where[key] = value
                
                results = self.store.similarity_search_with_score(query, k=limit, filter=where)
                formatted_results = []
                for doc, score in results:
                    # Normalize scores to be between 0 and 1
                    normalized_score = max(0, min(1, score))
                    formatted_results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'score': normalized_score
                    })
                return formatted_results
        except Exception as e:
            print(f"Error during search: {e}")
            # Fallback to basic search without filters
            try:
                results = self.store.similarity_search_with_score(query, k=limit)
                formatted_results = []
                for doc, score in results:
                    # Normalize scores to be between 0 and 1
                    normalized_score = max(0, min(1, score))
                    formatted_results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata,
                        'score': normalized_score
                    })
                return formatted_results
            except Exception as e2:
                print(f"Fallback search also failed: {e2}")
                return []
    
    def get_all_documents(self, limit: int = 100, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all documents in the database, optionally filtered by metadata.
        
        Args:
            limit: Maximum number of documents to return
            metadata_filter: Optional filter for metadata fields
            
        Returns:
            List of documents with content and metadata
        """
        try:
            # For newer versions of Chroma
            where = metadata_filter if metadata_filter else None
            collection = self.store._collection
            results = collection.get(limit=limit, where=where)
            documents = []
            for i in range(len(results['ids'])):
                metadata = results['metadatas'][i] if results['metadatas'] and i < len(results['metadatas']) else {}
                # Ensure ID is available in the metadata
                if 'id' not in metadata and results['ids'] and i < len(results['ids']):
                    metadata['id'] = results['ids'][i]
                
                documents.append({
                    'id': results['ids'][i],
                    'content': results['documents'][i],
                    'metadata': metadata
                })
            return documents
        except Exception as e:
            print(f"Error getting documents: {e}")
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document and all its chunks from the database.
        
        Args:
            doc_id: The document ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.store.delete(filter={"id": doc_id})
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def clear_database(self) -> bool:
        """Clear all documents from the database.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            collection = self.store._collection
            # Get all document IDs
            results = collection.get()
            if results and 'ids' in results and results['ids']:
                # Delete all documents by their IDs
                collection.delete(ids=results['ids'])
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False
    
    def count(self) -> int:
        """Get the number of documents in the database.
        
        Returns:
            Number of documents
        """
        try:
            collection = self.store._collection
            results = collection.get()
            return len(results['ids']) if results and 'ids' in results else 0
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

class RAGSystem(ABC):
    """Abstract base class for RAG systems."""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize the RAG system.
        
        Args:
            vector_store: Vector store for document storage and retrieval
        """
        self.vector_store = vector_store
    
    @abstractmethod
    def add_documents(self, documents: List[str], metadata_list: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add documents to the RAG system.
        
        Args:
            documents: List of document texts
            metadata_list: Optional list of metadata dictionaries
            
        Returns:
            List of document IDs
        """
        pass
    
    @abstractmethod
    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Query the RAG system.
        
        Args:
            query: The query string
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with response and relevant documents
        """
        pass

class OpenAIRAGSystem(RAGSystem):
    """RAG system using OpenAI for embeddings and response generation."""
    
    def __init__(self, vector_store: VectorStore, embedding_model=None, llm=None):
        """Initialize the OpenAI RAG system.
        
        Args:
            vector_store: Vector store for document storage and retrieval
            embedding_model: Optional embedding model
            llm: Optional language model
        """
        super().__init__(vector_store)
        # These parameters are placeholders for future implementation
        # Currently using the vector_store's embedding function and external LLM API
        self.embedding_model = embedding_model
        self.llm = llm
    
    def add_documents(self, documents: List[str], metadata_list: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add documents to the RAG system.
        
        Args:
            documents: List of document texts
            metadata_list: Optional list of metadata dictionaries
            
        Returns:
            List of document IDs
        """
        if metadata_list is None:
            metadata_list = [{} for _ in documents]
        
        if len(documents) != len(metadata_list):
            raise ValueError("Number of documents and metadata entries must match")
        
        doc_ids = []
        for doc, meta in zip(documents, metadata_list):
            doc_id = self.vector_store.add_text(doc, meta)
            doc_ids.append(doc_id)
        
        return doc_ids
    
    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Query the RAG system.
        
        Args:
            query: The query string
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with response and relevant documents
        """
        # Retrieve relevant documents
        results = self.vector_store.search(query, limit=top_k)
        
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
        
        # Use external LLM API for response generation
        try:
            from hanx_apis.api_llm import query_llm
            response = query_llm(prompt)
        except ImportError:
            response = "Error: LLM API not available. Please install the required dependencies."
        
        return {
            "response": response,
            "relevant_documents": results
        }

# Standalone functions for backward compatibility
def add_text(text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Add text to the vector database (standalone function).
    
    Args:
        text: The text content to add
        metadata: Optional metadata for the text
        
    Returns:
        ID of the added document
    """
    vector_store = VectorStore()
    return vector_store.add_text(text, metadata)

def add_document(file_path: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Add a document file to the vector database (standalone function).
    
    Args:
        file_path: Path to the document file
        metadata: Optional metadata for the document
        
    Returns:
        ID of the added document
    """
    vector_store = VectorStore()
    return vector_store.add_document(file_path, metadata)

def search(query: str, limit: int = 5, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Search for relevant documents based on a query (standalone function).
    
    Args:
        query: The search query
        limit: Maximum number of results to return
        metadata_filter: Optional filter for metadata fields
        
    Returns:
        List of relevant documents with content, metadata, and relevance score
    """
    vector_store = VectorStore()
    return vector_store.search(query, limit, metadata_filter)

def get_all_documents(limit: int = 100, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Get all documents in the database (standalone function).
    
    Args:
        limit: Maximum number of documents to return
        metadata_filter: Optional filter for metadata fields
        
    Returns:
        List of documents with content and metadata
    """
    vector_store = VectorStore()
    return vector_store.get_all_documents(limit, metadata_filter)

def delete_document(doc_id: str) -> bool:
    """Delete a document and all its chunks from the database (standalone function).
    
    Args:
        doc_id: The document ID to delete
        
    Returns:
        True if successful, False otherwise
    """
    vector_store = VectorStore()
    return vector_store.delete_document(doc_id)

def clear_database() -> bool:
    """Clear all documents from the database (standalone function).
    
    Returns:
        True if successful, False otherwise
    """
    vector_store = VectorStore()
    return vector_store.clear_database()

# Example usage
if __name__ == "__main__":
    print("This module is intended to be imported, not run directly.")
    print("Example usage:")
    print("  from hanx_tools.tool_rag_utils import VectorStore, OpenAIRAGSystem")
    print("  vector_store = VectorStore('../hanx_data/vector_store')")
    print("  rag = OpenAIRAGSystem(vector_store)")
    print("  rag.add_documents(['This is a test document'], [{'source': 'test'}])")
    print("  results = rag.query('test document')") 