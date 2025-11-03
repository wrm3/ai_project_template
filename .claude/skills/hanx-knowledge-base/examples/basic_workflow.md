# Basic Workflow Example

This example demonstrates the complete workflow for building and searching a knowledge base.

## Scenario

You have a collection of technical documentation in PDF and Markdown format that you want to make searchable using semantic search.

## Step 1: Initialize Knowledge Base

```python
from knowledge_base import KnowledgeBase

# Create or load knowledge base
kb = KnowledgeBase("./data/my_knowledge_base")
```

**Output:**
```
[EMBEDDINGS] Loading local model: all-MiniLM-L6-v2
[EMBEDDINGS] Model loaded: 384 dimensions
[VECTOR STORE] Initialized at: ./data/my_knowledge_base/vector_store
[VECTOR STORE] Collection: knowledge_base
[RAG SYSTEM] Initialized
[KB] Knowledge Base initialized at: ./data/my_knowledge_base
```

## Step 2: Add Documents

### Add Single Document

```python
# Add a PDF document
doc_id = kb.add_document(
    "rag_implementation_guide.pdf",
    category="technical",
    metadata={
        "author": "John Doe",
        "version": "1.0",
        "topics": ["RAG", "embeddings", "vector databases"]
    }
)
```

**Output:**
```
[KB] Adding document: rag_implementation_guide.pdf
[KB] Category: technical
[KB] Processing document...
[KB] Metadata saved: rag_implementation_guide.json
[KB] Adding to RAG system...
[ADDED] 42 texts to vector store
[KB] ✅ Document added successfully in 3.42s
[KB] Document ID: doc_1730123456789
```

### Add Markdown Document

```python
# Add a markdown file
doc_id = kb.add_document(
    "vector_databases_intro.md",
    category="technical",
    metadata={
        "author": "Jane Smith",
        "date": "2025-10-15"
    }
)
```

**Output:**
```
[KB] Adding document: vector_databases_intro.md
[KB] Category: technical
[KB] Processing document...
[KB] Metadata saved: vector_databases_intro.json
[KB] Adding to RAG system...
[ADDED] 18 texts to vector store
[KB] ✅ Document added successfully in 1.23s
[KB] Document ID: doc_1730123456790
```

## Step 3: List Documents

```python
# View all documents in knowledge base
documents = kb.list_documents()

for doc in documents:
    print(f"\n{doc['name']}")
    print(f"  Category: {doc['category']}")
    print(f"  Size: {doc['size'] / 1024:.1f} KB")
    print(f"  Modified: {doc['modified']}")
```

**Output:**
```
rag_implementation_guide.pdf
  Category: technical
  Size: 1234.5 KB
  Modified: 2025-11-01T10:30:45

vector_databases_intro.md
  Category: technical
  Size: 45.2 KB
  Modified: 2025-10-15T14:22:10
```

## Step 4: Search Knowledge Base

### Basic Search

```python
# Search for information about RAG
results = kb.search("What is RAG and how does it work?", limit=3)

for i, result in enumerate(results, 1):
    print(f"\n{'='*80}")
    print(f"Result {i}")
    print(f"{'='*80}")
    print(f"Relevance: {result.score:.4f}")
    print(f"Source: {result.metadata['file_name']}")
    print(f"Category: {result.metadata['category']}")
    print(f"\nContent:")
    print(result.text[:300] + "...")
```

**Output:**
```
================================================================================
Result 1
================================================================================
Relevance: 0.8921
Source: rag_implementation_guide.pdf
Category: technical

Content:
RAG (Retrieval-Augmented Generation) is a technique that enhances large language
models by combining them with external knowledge retrieval. The system works in
three main steps: 1) When a query is received, it's converted into a vector
embedding. 2) The vector database is searched for similar embeddings...

================================================================================
Result 2
================================================================================
Relevance: 0.8534
Source: vector_databases_intro.md
Category: technical

Content:
Vector databases are specialized databases designed to store and query vector
embeddings efficiently. They enable semantic search by measuring the similarity
between query vectors and stored document vectors using metrics like cosine
similarity or dot product...

================================================================================
Result 3
================================================================================
Relevance: 0.7823
Source: rag_implementation_guide.pdf
Category: technical

Content:
The key components of a RAG system include: the vector database (like ChromaDB
or Pinecone), an embedding model (OpenAI or SentenceTransformers), a chunking
strategy for splitting documents, and the LLM for generating responses...
```

### Search with Category Filter

```python
# Search only in technical category
results = kb.search(
    "vector similarity search",
    limit=5,
    category="technical"
)

print(f"Found {len(results)} results in 'technical' category")
```

**Output:**
```
Found 5 results in 'technical' category
```

## Step 5: Get Statistics

```python
# View knowledge base statistics
stats = kb.get_statistics()

print("Knowledge Base Statistics:")
print(f"  Total Documents: {stats['total_documents']}")
print(f"  Total Size: {stats['total_size_mb']} MB")
print(f"  Categories: {stats['categories']}")
print(f"  File Types: {stats['file_types']}")
```

**Output:**
```
Knowledge Base Statistics:
  Total Documents: 2
  Total Size: 1.25 MB
  Categories: {'technical': 2}
  File Types: {'.pdf': 1, '.md': 1}
```

## Step 6: Export Metadata

```python
# Export all metadata to JSON
export_file = kb.export_metadata()
print(f"Metadata exported to: {export_file}")
```

**Output:**
```
[KB] Metadata exported to: ./data/my_knowledge_base/exports/metadata_export_20251101_103045.json
Metadata exported to: ./data/my_knowledge_base/exports/metadata_export_20251101_103045.json
```

## Complete Script

Here's the complete workflow in a single script:

```python
#!/usr/bin/env python3
"""
Basic Knowledge Base Workflow
"""
from knowledge_base import KnowledgeBase

def main():
    # 1. Initialize
    print("Step 1: Initializing knowledge base...")
    kb = KnowledgeBase("./data/my_knowledge_base")

    # 2. Add documents
    print("\nStep 2: Adding documents...")

    doc_id1 = kb.add_document(
        "rag_implementation_guide.pdf",
        category="technical",
        metadata={"author": "John Doe", "version": "1.0"}
    )

    doc_id2 = kb.add_document(
        "vector_databases_intro.md",
        category="technical",
        metadata={"author": "Jane Smith"}
    )

    # 3. List documents
    print("\nStep 3: Listing documents...")
    documents = kb.list_documents()
    print(f"Total documents: {len(documents)}")

    # 4. Search
    print("\nStep 4: Searching knowledge base...")
    results = kb.search("What is RAG?", limit=3)

    print(f"\nFound {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.metadata['file_name']} (Score: {result.score:.4f})")
        print(f"   {result.text[:150]}...")

    # 5. Statistics
    print("\nStep 5: Knowledge base statistics...")
    stats = kb.get_statistics()
    print(f"Documents: {stats['total_documents']}")
    print(f"Size: {stats['total_size_mb']} MB")

    # 6. Export
    print("\nStep 6: Exporting metadata...")
    export_file = kb.export_metadata()
    print(f"Exported to: {export_file}")

    print("\n✅ Workflow complete!")

if __name__ == "__main__":
    main()
```

## Next Steps

After completing this basic workflow, you can:

1. **Add more documents**: Use `add_documents_batch()` for multiple files
2. **Advanced search**: Try different queries and filters
3. **Customize chunking**: Adjust chunk size for your content type
4. **Use different embeddings**: Try OpenAI for higher quality
5. **Integrate with LLMs**: Use search results to build RAG pipelines

See other examples:
- [Batch Ingestion](batch_ingestion.md)
- [Advanced Search](advanced_search.md)
- [Integration Examples](integrations.md)
