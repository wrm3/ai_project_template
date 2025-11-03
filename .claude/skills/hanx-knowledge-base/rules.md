# Hanx Knowledge Base & RAG Skill - Rules

## Purpose

This skill enables Claude Code to build and search knowledge bases using RAG (Retrieval-Augmented Generation) technology. It processes various document formats, generates vector embeddings, and provides semantic search capabilities.

## When to Activate

Activate this skill when the user:

1. **Document Ingestion**:
   - Wants to "ingest" or "add" documents to a knowledge base
   - Says "process these documents"
   - Mentions "build knowledge base from" files or directories
   - Requests document extraction or processing

2. **Search and Retrieval**:
   - Asks to "search my documents" or "find information about"
   - Uses phrases like "semantic search" or "query knowledge base"
   - Wants to "retrieve relevant content" from documents
   - Needs to "find similar documents"

3. **Knowledge Base Management**:
   - Wants to organize documents by category
   - Asks to "list all documents" or view knowledge base contents
   - Needs to export metadata or statistics
   - Wants to remove or update documents

## Core Capabilities

### 1. Document Processing

**Supported Formats:**
- PDF, DOCX, MD, TXT, CSV, HTML, JSON

**Always:**
- Extract both text content AND metadata
- Preserve document structure (headings, lists, tables)
- Report processing progress for multiple documents
- Handle errors gracefully with informative messages

**Never:**
- Process unsupported file types without warning
- Skip metadata extraction
- Silently fail on processing errors

### 2. Vector Embeddings

**Default Configuration:**
- Use local embeddings (SentenceTransformers) unless user specifies OpenAI
- Model: all-MiniLM-L6-v2 (384 dimensions, free)
- Report embedding statistics (tokens, cost if using API)

**Always:**
- Show progress for batch embedding generation
- Provide cost estimates before using paid APIs
- Cache embeddings to avoid regeneration

**Never:**
- Use paid APIs without user confirmation
- Generate embeddings without clear progress indication
- Fail silently on embedding errors

### 3. Semantic Search

**Search Behavior:**
- Use natural language queries (not just keyword matching)
- Return results with relevance scores
- Include source metadata in results
- Show snippet of matching content

**Always:**
- Display relevance scores prominently
- Allow filtering by category or metadata
- Support minimum score thresholds
- Format results for readability

**Never:**
- Return results without scores
- Hide source information
- Present results in raw JSON without formatting

## Implementation Guidelines

### Document Ingestion

```python
# CORRECT: Full workflow with progress reporting
print(f"[KB] Processing: {filename}")
content, metadata = process_document(filepath)
print(f"[KB] Extracted {len(content)} characters")
kb.add_document(filepath, category="technical", metadata=metadata)
print(f"[KB] ✅ Added successfully")

# WRONG: Silent processing
kb.add_document(filepath)  # No user feedback
```

### Search Implementation

```python
# CORRECT: Formatted results with context
results = kb.search(query, limit=5)
for i, result in enumerate(results, 1):
    print(f"\nResult {i}: (Score: {result.score:.4f})")
    print(f"Source: {result.metadata['source']}")
    print(f"Preview: {result.text[:200]}...")

# WRONG: Raw output
print(results)  # Unhelpful
```

### Error Handling

```python
# CORRECT: Informative error handling
try:
    kb.add_document(filepath)
except FileNotFoundError:
    print(f"[ERROR] File not found: {filepath}")
    print("[HELP] Check the path and try again")
except Exception as e:
    print(f"[ERROR] Failed to process document: {e}")
    print("[HELP] Ensure file is not corrupted and is a supported format")

# WRONG: Silent failures
try:
    kb.add_document(filepath)
except:
    pass  # User has no idea what happened
```

## User Interaction Patterns

### Pattern 1: Single Document Ingestion

**User**: "Add this PDF to my knowledge base: research_paper.pdf"

**Claude Code Actions**:
1. Verify file exists
2. Process document (extract text + metadata)
3. Show extracted metadata (title, author, pages)
4. Ask for category if not specified
5. Generate embeddings and store
6. Report success with statistics

### Pattern 2: Batch Ingestion

**User**: "Build a knowledge base from all PDFs in ./research"

**Claude Code Actions**:
1. Scan directory and count files
2. Confirm with user (show file count)
3. Process files with progress indicators
4. Report statistics (success/failures, time, storage)
5. Suggest next steps (search examples)

### Pattern 3: Semantic Search

**User**: "Search my knowledge base for information about RAG systems"

**Claude Code Actions**:
1. Generate query embedding
2. Perform similarity search
3. Format results with scores and sources
4. Show content snippets
5. Offer to export results or refine search

### Pattern 4: Knowledge Base Management

**User**: "Show me all documents in the technical category"

**Claude Code Actions**:
1. List documents with metadata
2. Show statistics (count, total size)
3. Offer management options (remove, export, search)

## Best Practices

### Do's ✅

1. **Progress Reporting**
   - Always show progress for long operations
   - Use clear status messages ([PROCESSING], [COMPLETE], [ERROR])
   - Report statistics (time, documents processed, storage used)

2. **User Confirmation**
   - Confirm before batch operations
   - Warn about paid API usage
   - Show cost estimates

3. **Error Recovery**
   - Provide helpful error messages
   - Suggest solutions
   - Continue processing on partial failures

4. **Result Formatting**
   - Use clear visual separators
   - Show relevance scores prominently
   - Include source metadata
   - Provide content previews

5. **Performance Optimization**
   - Use batch processing when possible
   - Cache embeddings
   - Show performance metrics

### Don'ts ❌

1. **Silent Operations**
   - Never process without user feedback
   - Don't hide errors
   - Avoid unexplained delays

2. **Unclear Failures**
   - Don't fail without explaining why
   - Avoid technical jargon in error messages
   - Never silently skip documents

3. **Poor Result Presentation**
   - Don't dump raw JSON
   - Avoid results without context
   - Never omit relevance scores

4. **Resource Waste**
   - Don't regenerate embeddings unnecessarily
   - Avoid processing duplicate documents
   - Don't use paid APIs by default

## Performance Guidelines

### Embedding Generation

**For < 100 documents:**
- Use local embeddings (free, fast enough)
- Show progress bar
- Report completion time

**For 100-1000 documents:**
- Use local embeddings with batch processing
- Show detailed progress (batches completed)
- Provide time estimates

**For > 1000 documents:**
- Warn about processing time
- Suggest chunking into smaller batches
- Consider OpenAI API for faster processing (with cost estimate)

### Search Performance

**For < 10,000 chunks:**
- Instant search (<200ms)
- No special handling needed

**For 10,000-100,000 chunks:**
- May take 500ms-1s
- Show "Searching..." indicator

**For > 100,000 chunks:**
- Consider optimizations (IVF indexing)
- Warn about potential slowdowns
- Suggest metadata pre-filtering

## Output Formatting Standards

### Success Messages
```
[KB] ✅ Document added successfully
[KB] ✅ Batch ingestion complete: 15/15 documents
[SEARCH] ✅ Found 8 relevant results
```

### Error Messages
```
[ERROR] File not found: document.pdf
[HELP] Check the file path and ensure the file exists

[ERROR] Unsupported file type: .xlsx
[HELP] Supported formats: PDF, DOCX, MD, TXT, CSV, HTML, JSON
```

### Progress Indicators
```
[1/15] Processing: research_paper_1.pdf
[2/15] Processing: research_paper_2.pdf
...
[PROGRESS] 8/15 documents processed (53%)
```

### Result Formatting
```
================================================================================
Result 1
================================================================================
Relevance: 0.8742 ████████████████████
Category: technical
Source: rag_implementation.md

Content:
--------------------------------------------------------------------------------
RAG (Retrieval-Augmented Generation) combines information retrieval with
language model generation...
--------------------------------------------------------------------------------
```

## Integration with Other Skills

### youtube-video-analysis
```python
# Extract transcript, then add to knowledge base
from youtube_video_analysis import download_and_transcribe
from knowledge_base import KnowledgeBase

transcript = download_and_transcribe(video_url)
kb = KnowledgeBase("./data/kb")
kb.rag_system.add_text(
    transcript,
    metadata={"source": "youtube", "video_id": video_id}
)
```

### web-tools
```python
# Scrape web page, then ingest
from web_scraper import scrape_url
from knowledge_base import KnowledgeBase

content = scrape_url(url)
kb = KnowledgeBase("./data/kb")
kb.rag_system.add_text(
    content['text'],
    metadata={"source": url, "title": content['title']}
)
```

## Security and Privacy

### Always Consider:
1. **Data Privacy**: Local embeddings keep data on user's machine
2. **API Keys**: Never log or expose API keys
3. **File Access**: Validate file paths to prevent directory traversal
4. **Resource Limits**: Set reasonable limits on file sizes and batch operations

### Never:
1. Process files outside user's specified directories
2. Send sensitive data to external APIs without consent
3. Store API keys in code or logs
4. Allow unbounded resource consumption

## Skill Deactivation

Deactivate this skill when:
- User switches to a different task unrelated to document processing or search
- User explicitly requests a different skill
- Task is complete and no follow-up questions asked

Always offer to:
- Save current work
- Export metadata
- Provide next steps or suggestions

---

**Remember**: This skill is about making document knowledge accessible through semantic search. Always prioritize user experience with clear progress reporting, helpful error messages, and well-formatted results.
