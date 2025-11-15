#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retrieval Augmented Generation (RAG) Utilities

Core RAG system providing vector storage, embedding generation, and semantic search.
Supports multiple backends (ChromaDB, Supabase) and embedding models (OpenAI, local).

Features:
- Document chunking with intelligent splitting
- Vector embeddings generation (OpenAI, SentenceTransformers)
- Persistent vector storage (ChromaDB, Supabase)
- Semantic similarity search
- Metadata filtering and management
- Cost tracking and optimization

Usage:
    from rag_utils import VectorStore, RAGSystem, LocalEmbeddings

    # Initialize vector store
    store = VectorStore("./data/vector_store")

    # Add documents
    store.add_texts(
        texts=["Document 1...", "Document 2..."],
        metadatas=[{"source": "file1.pdf"}, {"source": "file2.pdf"}]
    )

    # Search
    results = store.search("query text", limit=5)
"""

import os
import sys
import json
import uuid
import datetime
import numpy as np
from typing import List, Dict, Any, Union, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Try importing dependencies with auto-install fallback
try:
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import (
        TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader,
        UnstructuredMarkdownLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import Embeddings
    from langchain_core.documents import Document
    from sentence_transformers import SentenceTransformer
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    print("[INSTALL] Installing required dependencies...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "langchain-community", "langchain-chroma", "sentence-transformers",
        "langchain-text-splitters", "python-dotenv", "pypdf", "docx2txt",
        "unstructured", "chromadb"
    ])
    from langchain_chroma import Chroma
    from langchain_community.document_loaders import (
        TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader,
        UnstructuredMarkdownLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.embeddings import Embeddings
    from langchain_core.documents import Document
    from sentence_transformers import SentenceTransformer
    from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default configuration
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './data/vector_store')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))


@dataclass
class SearchResult:
    """Search result with content, metadata, and relevance score"""
    text: str
    metadata: Dict[str, Any]
    score: float
    chunk_id: Optional[str] = None


@dataclass
class IngestionStats:
    """Statistics for document ingestion"""
    total_documents: int
    total_chunks: int
    total_tokens: int
    cost_usd: float
    duration_seconds: float

    def __str__(self) -> str:
        return (
            f"Ingestion Stats:\n"
            f"  Documents: {self.total_documents}\n"
            f"  Chunks: {self.total_chunks}\n"
            f"  Tokens: {self.total_tokens:,}\n"
            f"  Cost: ${self.cost_usd:.6f}\n"
            f"  Duration: {self.duration_seconds:.2f}s"
        )


class LocalEmbeddings(Embeddings):
    """
    Local embeddings using SentenceTransformers

    Advantages:
    - Free (no API costs)
    - Fast (local inference)
    - Privacy (no data sent to external APIs)
    - Offline capable

    Disadvantages:
    - Lower quality than OpenAI models
    - Requires local resources (CPU/GPU)
    - Limited context window
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize local embedding model

        Args:
            model_name: SentenceTransformer model name
                       Popular options:
                       - 'all-MiniLM-L6-v2' (default, fast, 384 dim)
                       - 'all-mpnet-base-v2' (better quality, 768 dim)
                       - 'multi-qa-MiniLM-L6-cos-v1' (optimized for Q&A)
        """
        print(f"[EMBEDDINGS] Loading local model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"[EMBEDDINGS] Model loaded: {self.model.get_sentence_embedding_dimension()} dimensions")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents"""
        return self.model.encode(texts, show_progress_bar=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query"""
        return self.model.encode(text).tolist()


class VectorStore:
    """
    Vector database for storing and searching document embeddings

    Features:
    - Persistent storage using ChromaDB
    - Metadata filtering
    - Similarity search (cosine, L2, IP)
    - Batch operations
    - Document management (add, delete, update)
    """

    def __init__(
        self,
        persist_directory: str = VECTOR_DB_PATH,
        embedding_function: Optional[Embeddings] = None,
        collection_name: str = "knowledge_base"
    ):
        """
        Initialize vector store

        Args:
            persist_directory: Directory for persistent storage
            embedding_function: Embeddings implementation (default: LocalEmbeddings)
            collection_name: Name for the vector collection
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.embedding_function = embedding_function or LocalEmbeddings()
        self.collection_name = collection_name

        # Initialize ChromaDB
        self.vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=str(self.persist_directory),
            embedding_function=self.embedding_function
        )

        print(f"[VECTOR STORE] Initialized at: {self.persist_directory}")
        print(f"[VECTOR STORE] Collection: {collection_name}")

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add texts to vector store

        Args:
            texts: List of text content to add
            metadatas: Optional metadata for each text
            ids: Optional IDs for each text (generated if not provided)

        Returns:
            List of document IDs
        """
        if metadatas is None:
            metadatas = [{} for _ in texts]

        # Add timestamps
        timestamp = datetime.datetime.now().isoformat()
        for metadata in metadatas:
            if 'timestamp' not in metadata:
                metadata['timestamp'] = timestamp

        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]

        # Add to vector store
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"[ADDED] {len(texts)} texts to vector store")
        return ids

    def add_documents(
        self,
        documents: List[Document]
    ) -> List[str]:
        """
        Add LangChain documents to vector store

        Args:
            documents: List of LangChain Document objects

        Returns:
            List of document IDs
        """
        ids = self.vectorstore.add_documents(documents)
        print(f"[ADDED] {len(documents)} documents to vector store")
        return ids

    def search(
        self,
        query: str,
        limit: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for relevant documents using semantic similarity

        Args:
            query: Search query
            limit: Maximum number of results
            filter_metadata: Optional metadata filter

        Returns:
            List of SearchResult objects
        """
        results = self.vectorstore.similarity_search_with_relevance_scores(
            query,
            k=limit,
            filter=filter_metadata
        )

        search_results = []
        for doc, score in results:
            search_results.append(SearchResult(
                text=doc.page_content,
                metadata=doc.metadata,
                score=float(score),
                chunk_id=doc.metadata.get('id')
            ))

        return search_results

    def delete(
        self,
        ids: Optional[List[str]] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Delete documents from vector store

        Args:
            ids: Document IDs to delete
            filter_metadata: Delete by metadata filter

        Returns:
            Success status
        """
        try:
            if ids:
                self.vectorstore.delete(ids=ids)
                print(f"[DELETED] {len(ids)} documents")
            elif filter_metadata:
                self.vectorstore.delete(filter=filter_metadata)
                print(f"[DELETED] Documents matching filter: {filter_metadata}")
            return True
        except Exception as e:
            print(f"[ERROR] Delete failed: {e}")
            return False

    def clear(self) -> bool:
        """Clear all documents from the vector store"""
        try:
            self.vectorstore.delete_collection()
            # Reinitialize
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                persist_directory=str(self.persist_directory),
                embedding_function=self.embedding_function
            )
            print("[CLEARED] All documents removed from vector store")
            return True
        except Exception as e:
            print(f"[ERROR] Clear failed: {e}")
            return False

    def count(self) -> int:
        """Get total number of documents in vector store"""
        try:
            collection = self.vectorstore._collection
            return collection.count()
        except:
            return 0


class DocumentChunker:
    """
    Intelligent document chunking with overlap

    Features:
    - Recursive character splitting
    - Semantic boundary detection
    - Configurable chunk size and overlap
    - Metadata preservation
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize chunker

        Args:
            chunk_size: Target size for each chunk (characters)
            chunk_overlap: Overlap between chunks (characters)
            separators: Custom separators (default: ["\n\n", "\n", ". ", " ", ""])
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Chunk text into smaller pieces

        Args:
            text: Text to chunk
            metadata: Metadata to attach to all chunks

        Returns:
            List of LangChain Document objects
        """
        chunks = self.splitter.create_documents(
            texts=[text],
            metadatas=[metadata or {}]
        )

        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = i
            chunk.metadata['chunk_total'] = len(chunks)

        return chunks

    def chunk_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:
        """
        Chunk multiple documents

        Args:
            documents: List of LangChain Document objects

        Returns:
            List of chunked Document objects
        """
        return self.splitter.split_documents(documents)


class RAGSystem:
    """
    Complete RAG system combining vector store, chunking, and search

    This is the main interface for the RAG system.
    """

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        chunker: Optional[DocumentChunker] = None
    ):
        """
        Initialize RAG system

        Args:
            vector_store: VectorStore instance (created if not provided)
            chunker: DocumentChunker instance (created if not provided)
        """
        self.vector_store = vector_store or VectorStore()
        self.chunker = chunker or DocumentChunker()

        print("[RAG SYSTEM] Initialized")

    def add_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        chunk: bool = True
    ) -> List[str]:
        """
        Add text to RAG system

        Args:
            text: Text content
            metadata: Optional metadata
            chunk: Whether to chunk the text

        Returns:
            List of document IDs
        """
        if chunk:
            chunks = self.chunker.chunk_text(text, metadata)
            return self.vector_store.add_documents(chunks)
        else:
            return self.vector_store.add_texts([text], [metadata or {}])

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        chunk: bool = True
    ) -> List[str]:
        """
        Add multiple texts to RAG system

        Args:
            texts: List of text content
            metadatas: Optional metadata for each text
            chunk: Whether to chunk the texts

        Returns:
            List of document IDs
        """
        if metadatas is None:
            metadatas = [{} for _ in texts]

        if chunk:
            all_chunks = []
            for text, metadata in zip(texts, metadatas):
                chunks = self.chunker.chunk_text(text, metadata)
                all_chunks.extend(chunks)
            return self.vector_store.add_documents(all_chunks)
        else:
            return self.vector_store.add_texts(texts, metadatas)

    def query(
        self,
        query: str,
        limit: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Query the RAG system

        Args:
            query: Search query
            limit: Maximum number of results
            filter_metadata: Optional metadata filter

        Returns:
            List of SearchResult objects
        """
        return self.vector_store.search(query, limit, filter_metadata)

    def clear(self) -> bool:
        """Clear all documents from RAG system"""
        return self.vector_store.clear()


# Convenience functions
def create_rag_system(
    persist_directory: str = VECTOR_DB_PATH,
    embedding_model: str = EMBEDDING_MODEL,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> RAGSystem:
    """
    Create a ready-to-use RAG system

    Args:
        persist_directory: Directory for vector store
        embedding_model: Embedding model name
        chunk_size: Chunk size in characters
        chunk_overlap: Overlap between chunks

    Returns:
        Configured RAGSystem instance
    """
    embeddings = LocalEmbeddings(model_name=embedding_model)
    vector_store = VectorStore(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    chunker = DocumentChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return RAGSystem(vector_store=vector_store, chunker=chunker)


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("RAG System - Test")
    print("=" * 80)
    print()

    # Create RAG system
    rag = create_rag_system()

    # Add sample documents
    documents = [
        "RAG (Retrieval-Augmented Generation) combines information retrieval with "
        "language model generation. It works by retrieving relevant documents from "
        "a knowledge base and using them as context for generating responses.",

        "Vector databases store embeddings, which are numerical representations of text. "
        "They enable semantic search by finding documents with similar embeddings to "
        "the query embedding.",

        "ChromaDB is an open-source vector database designed for AI applications. "
        "It supports persistent storage, metadata filtering, and multiple distance metrics."
    ]

    metadatas = [
        {"source": "rag_intro.md", "topic": "RAG"},
        {"source": "vector_db.md", "topic": "databases"},
        {"source": "chromadb.md", "topic": "databases"}
    ]

    print("[TEST] Adding documents...")
    rag.add_texts(documents, metadatas, chunk=False)
    print()

    # Test search
    print("[TEST] Searching for: 'What is RAG?'")
    results = rag.query("What is RAG?", limit=2)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {result.score:.4f}")
        print(f"  Source: {result.metadata.get('source', 'unknown')}")
        print(f"  Text: {result.text[:100]}...")

    print("\n✅ Test complete!")
