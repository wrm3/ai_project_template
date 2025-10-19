# PostgreSQL-based RAG Storage System Design

## Overview

This document outlines the design for a robust RAG (Retrieval Augmented Generation) storage system using PostgreSQL with vector search capabilities. This system will replace the current Chroma-based implementation to provide better scalability, reliability, and performance for large text bodies and diverse data sources.

## Motivation

The current Chroma-based RAG system has several limitations:
1. Limited text size in command-line operations
2. Inefficient handling of large document collections
3. Limited metadata filtering capabilities
4. Lack of robust transaction support and data integrity guarantees

PostgreSQL with the pgvector extension provides a mature, scalable solution that addresses these limitations while maintaining compatibility with our existing RAG architecture.

## Architecture

### Database Schema

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Document chunks table
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(384), -- Dimension depends on embedding model
    metadata JSONB NOT NULL DEFAULT '{}',
    chunk_index INTEGER NOT NULL,
    total_chunks INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_documents_metadata ON documents USING GIN (metadata);
CREATE INDEX idx_chunks_document_id ON chunks(document_id);
CREATE INDEX idx_chunks_metadata ON chunks USING GIN (metadata);
CREATE INDEX idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops);
```

### Component Design

1. **Database Connection Manager**
   - Handles connection pooling
   - Manages transactions
   - Provides retry logic for resilience

2. **Document Manager**
   - Adds, updates, and deletes documents
   - Handles document metadata
   - Manages document-level operations

3. **Chunk Manager**
   - Splits documents into chunks
   - Generates embeddings for chunks
   - Manages chunk-level operations

4. **Vector Search Engine**
   - Performs similarity searches
   - Handles hybrid search (vector + metadata)
   - Optimizes search performance

5. **RAG Interface**
   - Provides a high-level API for RAG operations
   - Maintains compatibility with existing code
   - Abstracts database details from clients

## Implementation Plan

### Phase 1: Core Infrastructure

1. Set up PostgreSQL with pgvector extension
2. Implement database schema
3. Create database connection manager
4. Implement basic document and chunk managers

### Phase 2: Migration and Compatibility

1. Create migration utilities to transfer data from Chroma
2. Implement compatibility layer for existing RAG code
3. Update tool_rag_utils.py to use the new PostgreSQL backend

### Phase 3: Advanced Features

1. Implement hybrid search capabilities
2. Add support for document versioning
3. Implement bulk operations for better performance
4. Add monitoring and analytics

## API Design

### PostgreSQL RAG Client

```python
class PostgresRAGClient:
    """Client for the PostgreSQL-based RAG system."""
    
    def __init__(self, connection_string: str):
        """Initialize the client with a PostgreSQL connection string."""
        pass
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add a document to the RAG system."""
        pass
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get a document by ID."""
        pass
    
    def update_document(self, document_id: str, content: str = None, metadata: Dict[str, Any] = None) -> bool:
        """Update a document."""
        pass
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document."""
        pass
    
    def search(self, query: str, limit: int = 5, metadata_filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for documents similar to the query."""
        pass
    
    def list_documents(self, limit: int = 100, offset: int = 0, metadata_filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """List documents with optional filtering."""
        pass
```

### Compatibility Layer

```python
class PostgresVectorStore:
    """Vector store implementation using PostgreSQL for compatibility with existing code."""
    
    def __init__(self, persist_directory: str = None, embedding_function = None):
        """Initialize the vector store with PostgreSQL connection."""
        pass
    
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None) -> List[str]:
        """Add texts to the vector store."""
        pass
    
    def similarity_search_with_score(self, query: str, k: int = 5, filter: Dict[str, Any] = None) -> List[Tuple[Document, float]]:
        """Search for similar documents with scores."""
        pass
    
    # Other methods for compatibility with LangChain
```

## Dependencies

- PostgreSQL 14+ with pgvector extension
- SQLAlchemy for database ORM
- psycopg2 or asyncpg for PostgreSQL connection
- sentence-transformers for embeddings (same as current implementation)

## Performance Considerations

- Use connection pooling for efficient database connections
- Implement batch operations for adding multiple documents
- Use appropriate indexing strategies for vector search
- Consider partitioning for very large document collections
- Implement caching for frequently accessed documents

## Security Considerations

- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Encrypt sensitive data in transit and at rest
- Regularly backup the database
- Implement proper error handling and logging

## Migration Strategy

1. Deploy PostgreSQL with pgvector extension
2. Create the new schema
3. Implement the new RAG client
4. Create a migration script to transfer data from Chroma
5. Update the tool_rag_utils.py to use the new backend
6. Test thoroughly with existing data
7. Switch over to the new system

## Future Enhancements

1. **Multi-model Embeddings**: Support for different embedding models
2. **Versioning**: Track changes to documents over time
3. **Access Control**: Fine-grained permissions for documents
4. **Analytics**: Track usage patterns and optimize accordingly
5. **Distributed Deployment**: Scale horizontally for very large collections
6. **Real-time Updates**: Streaming updates for real-time applications

## Installation Strategy

To simplify deployment and ensure consistency across environments, the PostgreSQL-based RAG system should be installed using standard methods:

### Benefits of Standard Installation
- **Flexibility**: Allows for customization based on specific environment needs
- **Direct Control**: Provides direct access to PostgreSQL configuration
- **Integration**: Easier integration with existing database infrastructure
- **Performance Tuning**: Direct access to performance optimization settings
- **Maintenance**: Simplified maintenance and updates

### PostgreSQL with pgvector Installation

1. **Install PostgreSQL**:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   
   # On macOS with Homebrew
   brew install postgresql
   
   # On Windows
   # Download and install from https://www.postgresql.org/download/windows/
   ```

2. **Install pgvector Extension**:
   ```bash
   # Install build dependencies
   sudo apt-get install build-essential git postgresql-server-dev-15
   
   # Clone and build pgvector
   git clone https://github.com/pgvector/pgvector.git
   cd pgvector
   make
   sudo make install
   ```

3. **Configure Database**:
   ```bash
   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE ragdb;
   CREATE USER raguser WITH PASSWORD 'ragpassword';
   GRANT ALL PRIVILEGES ON DATABASE ragdb TO raguser;
   
   # Connect to the database and enable the extension
   \c ragdb
   CREATE EXTENSION vector;
   ```

## Implementation Roadmap

// ... existing code ... 