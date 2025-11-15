---
name: hanx-knowledge-base
description: Document ingestion and semantic search with RAG capabilities. Supports PDF, DOCX, MD, TXT, CSV, HTML, and JSON. Combines intelligent chunking, vector embeddings, and persistent storage for building searchable knowledge bases.
triggers:
  - "ingest this document"
  - "add to knowledge base"
  - "search my documents"
  - "semantic search for"
  - "find information about"
  - "build knowledge base from"
dependencies:
  - sentence-transformers (local embeddings)
  - chromadb (vector storage)
  - langchain (document processing)
version: 1.0.0
---

# Hanx Knowledge Base & RAG Skill

Build searchable knowledge bases from diverse document types with advanced RAG (Retrieval-Augmented Generation) capabilities.

## Overview

This skill provides a complete document ingestion and search pipeline:

1. **Document Processing**: Extract text from PDF, DOCX, MD, TXT, CSV, HTML, JSON
2. **Intelligent Chunking**: Split documents with semantic awareness
3. **Vector Embeddings**: Generate embeddings using local or OpenAI models
4. **Persistent Storage**: Store in ChromaDB vector database
5. **Semantic Search**: Find relevant content using natural language queries
6. **Category Management**: Organize documents by topic

## When to Use This Skill

### Automatic Triggers
- User says "ingest this document" or "add to knowledge base"
- User requests "search my documents" or "find information about"
- User mentions "build knowledge base from" a directory
- User wants to "query the knowledge base"

### Manual Invocation
```bash
# Add single document
python scripts/knowledge_base.py add document.pdf --category technical

# Add directory of documents
python scripts/knowledge_base.py add-batch ./documents --category research

# Search knowledge base
python scripts/search_kb.py "What is RAG?" --limit 5

# List all documents
python scripts/knowledge_base.py list
```

## Core Capabilities

### 1. Document Ingestion

**Supported Formats:**
- **PDF** (.pdf): Full text extraction with page numbers
- **Word** (.docx, .doc): Text, tables, and document properties
- **Markdown** (.md): With YAML frontmatter support
- **Text** (.txt): Plain text files
- **CSV** (.csv): Structured data with headers
- **HTML** (.html, .htm): Web pages with metadata extraction
- **JSON** (.json): Structured JSON data

**Features:**
- Automatic format detection
- Metadata extraction (author, title, dates, etc.)
- Batch processing for directories
- Category-based organization
- Progress tracking

### 2. Intelligent Chunking

**Chunking Strategy:**
```
Document
    ↓
[Extract Text]
    ↓
[Split by Semantic Boundaries]
    ↓
[Chunks with Overlap]
    ↓
Vector Embeddings
```

**Features:**
- Recursive character splitting
- Semantic boundary detection (paragraphs, sentences)
- Configurable chunk size (default: 1000 characters)
- Overlap between chunks (default: 200 characters)
- Metadata preservation per chunk

### 3. Vector Embeddings

**Local Embeddings (Default - FREE):**
- **Model**: all-MiniLM-L6-v2 (SentenceTransformers)
- **Dimensions**: 384
- **Speed**: Fast (local inference)
- **Cost**: $0 (no API costs)
- **Privacy**: Data stays local

**Alternative Models:**
- `all-mpnet-base-v2`: Better quality, 768 dimensions
- `multi-qa-MiniLM-L6-cos-v1`: Optimized for Q&A
- OpenAI embeddings: Highest quality (requires API key)

### 4. Vector Storage (ChromaDB)

**Features:**
- **Persistent Storage**: Documents saved to disk
- **Metadata Filtering**: Filter by category, author, date
- **Multiple Distance Metrics**: Cosine, L2, Inner Product
- **Efficient Indexing**: Fast similarity search
- **CRUD Operations**: Add, search, update, delete

**Storage Structure:**
```
knowledge_base/
├── documents/           # Original documents (categorized)
│   ├── technical/
│   ├── business/
│   ├── reference/
│   └── ...
├── metadata/           # Document metadata (JSON)
├── vector_store/       # ChromaDB vector database
└── exports/           # Exported metadata
```

### 5. Semantic Search

**Search Capabilities:**
- **Natural Language Queries**: "How do I implement RAG?"
- **Similarity Scoring**: Relevance scores (0.0 to 1.0)
- **Metadata Filtering**: Filter by category, file type, date
- **Top-K Retrieval**: Get most relevant chunks
- **Contextual Results**: Full text + metadata + score

**Example Search:**
```bash
$ python search_kb.py "vector database implementation"

================================================================================
Result 1
================================================================================
Relevance: 0.8742 ████████████████████
Category: technical
Source: chromadb_guide.pdf

Content:
--------------------------------------------------------------------------------
Vector databases are specialized databases designed to store and search
vector embeddings efficiently. ChromaDB provides an open-source solution
with features like persistent storage, metadata filtering, and cosine
similarity search. Implementation involves three key steps: 1) Generate
embeddings using a model like SentenceTransformers, 2) Store embeddings
in the vector database, 3) Query using similarity search.
--------------------------------------------------------------------------------
```

## Workflow Examples

### Example 1: Build Knowledge Base from Directory

**User**: "Build a knowledge base from all PDF files in ./research"

**Skill Actions**:
1. Scan directory for PDF files
2. Process each PDF (extract text + metadata)
3. Chunk documents intelligently
4. Generate embeddings for all chunks
5. Store in ChromaDB vector database
6. Report statistics

**Output**:
```
================================================================================
Knowledge Base Batch Ingestion
================================================================================

Directory: ./research
Category: research
Recursive: True
File Filter: .pdf

[1/15] Processing: machine_learning_survey.pdf
[KB] Adding document: machine_learning_survey.pdf
[KB] Category: research
[KB] Processing document...
[KB] Metadata saved: machine_learning_survey.json
[KB] Adding to RAG system...
[KB] ✅ Document added successfully in 2.34s
[KB] Document ID: doc_1730123456789

[2/15] Processing: neural_networks_intro.pdf
...

[15/15] Processing: transformer_architecture.pdf

================================================================================
BATCH INGESTION COMPLETE
================================================================================

Total Files: 15
Successfully Added: 15
Failed: 0
Total Time: 45.2s
Average Time per Document: 3.0s

Knowledge base ready for search!
```

### Example 2: Semantic Search with Filters

**User**: "Search my technical documents for information about embeddings with minimum relevance 0.7"

**Command**:
```bash
python search_kb.py "embeddings" --category technical --min-score 0.7 --limit 10
```

**Output**:
```
================================================================================
Knowledge Base Search
================================================================================

Knowledge Base: ./data/knowledge_base
Query: "embeddings"
Category Filter: technical
Max Results: 10
Min Score: 0.7

[SEARCH] Searching knowledge base...
[SEARCH] Found 8 results

================================================================================
Result 1
================================================================================
Relevance: 0.8921 ██████████████████
Category: technical
Source: rag_implementation_guide.md

Content:
--------------------------------------------------------------------------------
Embeddings are dense vector representations of text that capture semantic
meaning. Modern embedding models like OpenAI's text-embedding-3-small or
SentenceTransformers produce vectors of 384 to 3072 dimensions. These
embeddings enable semantic search by measuring similarity through cosine
distance or dot product calculations.
--------------------------------------------------------------------------------

[... more results ...]
```

### Example 3: Document Management

**List all documents:**
```bash
python scripts/knowledge_base.py list --category technical
```

**Output**:
```
Knowledge Base Documents
Total: 23 documents in 'technical' category

1. rag_implementation_guide.md (45.2 KB)
   Modified: 2025-11-01T10:30:45
   Metadata: {"author": "John Doe", "topics": ["RAG", "embeddings"]}

2. chromadb_setup.pdf (1.2 MB)
   Modified: 2025-10-28T14:22:10
   Metadata: {"author": "Tech Team", "version": "2.0"}

[... 21 more documents ...]
```

**Remove document:**
```bash
python scripts/knowledge_base.py remove chromadb_setup.pdf --category technical
```

**Export metadata:**
```bash
python scripts/knowledge_base.py export --output kb_metadata.json
```

## Technical Specifications

### Embedding Models Comparison

| Model | Dimensions | Speed | Quality | Cost | Use Case |
|-------|-----------|-------|---------|------|----------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | Free | Default, general purpose |
| all-mpnet-base-v2 | 768 | Medium | Better | Free | Higher quality needed |
| text-embedding-3-small | 1536 | API | Best | $0.020/1M tokens | Production, highest quality |
| text-embedding-3-large | 3072 | API | Superior | $0.130/1M tokens | Critical applications |

### Performance Characteristics

**Document Ingestion** (1000-page PDF):
- Text extraction: ~5 seconds
- Chunking: <1 second
- Embedding generation: ~10 seconds (local), ~3 seconds (API)
- Database storage: ~2 seconds
- **Total**: ~18 seconds (local), ~11 seconds (API)

**Search Performance**:
- Query embedding: ~100ms (local), ~200ms (API)
- Vector search (10K chunks): ~50ms
- Result formatting: <10ms
- **Total**: ~160ms (local), ~260ms (API)

**Storage Requirements** (per 1000 documents):
- Original documents: ~500 MB (varies by type)
- ChromaDB vectors: ~100 MB
- Metadata: ~10 MB
- **Total**: ~610 MB

### Chunking Configuration

**Default Settings:**
```python
CHUNK_SIZE = 1000         # characters per chunk
CHUNK_OVERLAP = 200       # overlap between chunks
SEPARATORS = [
    "\n\n",              # Paragraphs
    "\n",                # Lines
    ". ",                # Sentences
    " ",                 # Words
    ""                   # Characters
]
```

**Customization:**
```python
from rag_utils import DocumentChunker

chunker = DocumentChunker(
    chunk_size=1500,       # Larger chunks for technical docs
    chunk_overlap=300,     # More overlap for context
    separators=["\n\n", "\n", ". "]  # Custom separators
)
```

## Usage Instructions

### Setup (One-time)

1. **Install Dependencies:**
```bash
cd .claude/skills/hanx-knowledge-base
pip install -r scripts/requirements.txt
```

2. **Verify Installation:**
```bash
python scripts/rag_utils.py  # Runs test
python scripts/document_processor.py  # Tests processors
```

3. **Optional: Configure OpenAI Embeddings:**
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Basic Usage

**Initialize Knowledge Base:**
```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase("./data/my_kb")
```

**Add Documents:**
```python
# Single document
kb.add_document("document.pdf", category="technical")

# Batch add from directory
kb.add_documents_batch(
    "./documents",
    category="research",
    recursive=True,
    file_extensions=['.pdf', '.docx', '.md']
)
```

**Search:**
```python
results = kb.search("What is RAG?", limit=5)

for result in results:
    print(f"Score: {result.score:.4f}")
    print(f"Text: {result.text[:200]}...")
    print(f"Source: {result.metadata['source']}")
```

### Advanced Usage

**Custom RAG System:**
```python
from rag_utils import VectorStore, LocalEmbeddings, DocumentChunker, RAGSystem

# Configure components
embeddings = LocalEmbeddings(model_name="all-mpnet-base-v2")
vector_store = VectorStore(
    persist_directory="./my_vector_db",
    embedding_function=embeddings
)
chunker = DocumentChunker(chunk_size=1500, chunk_overlap=300)

# Create RAG system
rag = RAGSystem(vector_store=vector_store, chunker=chunker)

# Use it
rag.add_text("Document content here...", metadata={"source": "custom.txt"})
results = rag.query("search query", limit=10)
```

**Metadata Filtering:**
```python
# Search only recent documents
results = kb.search(
    "machine learning",
    limit=5,
    metadata_filter={"category": "research", "year": 2025}
)
```

**Programmatic Document Processing:**
```python
from document_processor import process_document, process_directory

# Process single document
content, metadata = process_document("document.pdf")

# Process directory
results = process_directory(
    "./documents",
    recursive=True,
    file_extensions=['.pdf', '.md']
)

for content, metadata in results:
    print(f"Processed: {metadata['file_name']}")
    print(f"Length: {len(content)} characters")
```

## Best Practices

### Document Organization

**Categories:**
- ✅ Use meaningful categories (technical, business, reference)
- ✅ Keep category names lowercase and simple
- ✅ Create custom categories as needed
- ❌ Don't over-categorize (use metadata for fine-grained classification)

**Metadata:**
- ✅ Add relevant metadata (author, date, topic, version)
- ✅ Use consistent metadata keys across documents
- ✅ Include source URLs for web content
- ❌ Don't duplicate information already in content

### Chunking Strategy

**When to use larger chunks (1500-2000 chars):**
- Technical documentation with code examples
- Academic papers with complex concepts
- Documents requiring more context

**When to use smaller chunks (500-800 chars):**
- Q&A documents
- Short articles or blog posts
- Documents with discrete topics

**Overlap considerations:**
- More overlap (300-400 chars): Better context preservation
- Less overlap (100-200 chars): More efficient storage
- Default 200 chars works well for most content

### Embedding Selection

**Use Local Embeddings when:**
- Privacy is critical (data cannot leave your system)
- Cost is a concern (embeddings are free)
- You have many documents to process
- Embedding quality is "good enough"

**Use OpenAI Embeddings when:**
- Highest quality is required
- Processing time is critical (API is faster than some local models)
- You need consistency with other OpenAI tools
- Cost is acceptable (~$0.02 per 1M tokens)

### Search Optimization

**Query Formulation:**
- ✅ Use natural language questions
- ✅ Be specific rather than general
- ✅ Include key terms from your domain
- ❌ Don't use single keywords (use phrases)

**Relevance Thresholds:**
- **0.8+**: Highly relevant, near-exact matches
- **0.7-0.8**: Very relevant, strong semantic match
- **0.5-0.7**: Relevant, moderate semantic match
- **<0.5**: Marginal relevance, consider filtering out

**Result Limits:**
- Start with 5 results for most queries
- Increase to 10-20 for broad exploratory queries
- Use 1-3 for highly specific questions

## Limitations

### Current Limitations
- **Languages**: Best results with English (models are English-optimized)
- **Image Content**: Text-only extraction (no OCR or image analysis)
- **Tables**: Basic table extraction (formatting may be lost)
- **Code**: Extracted as text (no syntax highlighting or execution)
- **Updates**: Documents must be re-ingested after changes
- **Scale**: ChromaDB optimized for <1M documents (beyond that, consider alternatives)

### Performance Constraints
- Large PDFs (>1000 pages) may be slow to process
- First-time embedding model download (~100MB) required
- Local embeddings require CPU/GPU resources
- Memory usage scales with number of documents

## Troubleshooting

### Common Issues

**Issue**: "Module not found" errors
```bash
# Solution: Install dependencies
pip install -r scripts/requirements.txt
```

**Issue**: "No results found" for valid queries
```bash
# Solution 1: Check if documents are loaded
python scripts/knowledge_base.py list

# Solution 2: Lower minimum score threshold
python search_kb.py "query" --min-score 0.0

# Solution 3: Rebuild knowledge base
python scripts/knowledge_base.py rebuild
```

**Issue**: "Out of memory" during embedding generation
```python
# Solution: Use smaller embedding model
from rag_utils import LocalEmbeddings

embeddings = LocalEmbeddings(model_name="all-MiniLM-L6-v2")  # Smaller, 384 dim
```

**Issue**: "Slow search performance"
```python
# Solution: Reduce chunk size or document count
# Or: Switch to more efficient embedding model
# Or: Consider upgrading hardware
```

**Issue**: "PDF text extraction failed"
```bash
# Solution: Check if PDF is text-based (not scanned image)
# For scanned PDFs, use OCR preprocessing:
# tesseract input.pdf output -l eng pdf
```

## Integration Examples

### With LangChain
```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from knowledge_base import KnowledgeBase

kb = KnowledgeBase("./data/kb")
retriever = kb.rag_system.vector_store.vectorstore.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever
)

answer = qa.run("What is RAG?")
```

### With Claude API
```python
import anthropic
from knowledge_base import KnowledgeBase

kb = KnowledgeBase("./data/kb")
results = kb.search("RAG implementation", limit=3)

# Build context from search results
context = "\n\n".join([r.text for r in results])

# Query Claude with context
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"Based on this context:\n\n{context}\n\nQuestion: How do I implement RAG?"
    }]
)

print(message.content[0].text)
```

## Reference Documentation

- **[RAG Utils Reference](reference/rag_utils_reference.md)**: Complete API documentation
- **[Document Processors](reference/document_processors_reference.md)**: Supported formats and extraction details
- **[Chunking Strategies](reference/chunking_guide.md)**: Best practices for document chunking
- **[Embedding Models](reference/embedding_models.md)**: Comparison and selection guide

## Examples

- **[Basic Workflow](examples/basic_workflow.md)**: Step-by-step basic usage
- **[Batch Ingestion](examples/batch_ingestion.md)**: Process multiple documents
- **[Advanced Search](examples/advanced_search.md)**: Complex queries and filtering
- **[Integration Examples](examples/integrations.md)**: Use with LangChain, Claude, etc.

---

**Version**: 1.0.0
**Created**: 2025-11-01
**Status**: Production Ready
**Task**: 022
**Dependencies**: sentence-transformers, chromadb, langchain
