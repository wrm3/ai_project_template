# Batch Ingestion Example

This example demonstrates how to ingest multiple documents from a directory into the knowledge base.

## Scenario

You have a directory structure with various document types that need to be processed and made searchable:

```
documents/
├── research/
│   ├── paper1.pdf
│   ├── paper2.pdf
│   └── paper3.pdf
├── guides/
│   ├── setup_guide.md
│   ├── api_reference.md
│   └── tutorial.docx
└── data/
    ├── metrics.csv
    └── config.json
```

## Method 1: Batch Add from Directory

```python
from knowledge_base import KnowledgeBase

# Initialize knowledge base
kb = KnowledgeBase("./data/my_kb")

# Add all PDFs from research directory
doc_ids = kb.add_documents_batch(
    directory_path="./documents/research",
    category="research",
    recursive=False,
    file_extensions=['.pdf']
)

print(f"Added {len(doc_ids)} research papers")
```

**Output:**
```
[KB] Batch ingestion from: ./documents/research
[KB] Category: research
[KB] Recursive: False
[KB] Found 3 files to process

[KB] Processing 1/3: paper1.pdf
[KB] Adding document: paper1.pdf
[KB] Category: research
[KB] Processing document...
[KB] Metadata saved: paper1.json
[KB] Adding to RAG system...
[ADDED] 156 texts to vector store
[KB] ✅ Document added successfully in 8.42s

[KB] Processing 2/3: paper2.pdf
[KB] Adding document: paper2.pdf
[KB] Category: research
[KB] Processing document...
[KB] Metadata saved: paper2.json
[KB] Adding to RAG system...
[ADDED] 203 texts to vector store
[KB] ✅ Document added successfully in 10.15s

[KB] Processing 3/3: paper3.pdf
[KB] Adding document: paper3.pdf
[KB] Category: research
[KB] Processing document...
[KB] Metadata saved: paper3.json
[KB] Adding to RAG system...
[ADDED] 178 texts to vector store
[KB] ✅ Document added successfully in 9.23s

[KB] ✅ Batch ingestion complete: 3/3 documents added
Added 3 research papers
```

## Method 2: Process Multiple Categories

```python
from knowledge_base import KnowledgeBase
import time

kb = KnowledgeBase("./data/my_kb")

# Define categories and their directories
categories = {
    "research": "./documents/research",
    "documentation": "./documents/guides",
    "data": "./documents/data"
}

# Process each category
total_docs = 0
start_time = time.time()

for category, directory in categories.items():
    print(f"\n{'='*80}")
    print(f"Processing category: {category}")
    print(f"{'='*80}\n")

    doc_ids = kb.add_documents_batch(
        directory_path=directory,
        category=category,
        recursive=True
    )

    total_docs += len(doc_ids)
    print(f"Added {len(doc_ids)} documents to '{category}' category")

duration = time.time() - start_time
print(f"\n{'='*80}")
print(f"BATCH INGESTION COMPLETE")
print(f"{'='*80}")
print(f"Total documents: {total_docs}")
print(f"Total time: {duration:.2f}s")
print(f"Average time per document: {duration/total_docs:.2f}s")
```

**Output:**
```
================================================================================
Processing category: research
================================================================================

[KB] Batch ingestion from: ./documents/research
[KB] Category: research
[KB] Recursive: True
[KB] Found 3 files to process
...
[KB] ✅ Batch ingestion complete: 3/3 documents added
Added 3 documents to 'research' category

================================================================================
Processing category: documentation
================================================================================

[KB] Batch ingestion from: ./documents/guides
[KB] Category: documentation
[KB] Recursive: True
[KB] Found 3 files to process
...
[KB] ✅ Batch ingestion complete: 3/3 documents added
Added 3 documents to 'documentation' category

================================================================================
Processing category: data
================================================================================

[KB] Batch ingestion from: ./documents/data
[KB] Category: data
[KB] Recursive: True
[KB] Found 2 files to process
...
[KB] ✅ Batch ingestion complete: 2/2 documents added
Added 2 documents to 'data' category

================================================================================
BATCH INGESTION COMPLETE
================================================================================
Total documents: 8
Total time: 67.34s
Average time per document: 8.42s
```

## Method 3: Filtered Batch Processing

```python
from knowledge_base import KnowledgeBase
from pathlib import Path

kb = KnowledgeBase("./data/my_kb")

# Only process specific file types
supported_extensions = ['.pdf', '.md', '.docx']

doc_ids = kb.add_documents_batch(
    directory_path="./documents",
    category="mixed",
    recursive=True,
    file_extensions=supported_extensions
)

print(f"\nProcessed {len(doc_ids)} documents")
print(f"Supported extensions: {supported_extensions}")
```

## Method 4: Custom Batch Processing with Metadata

```python
from knowledge_base import KnowledgeBase
from pathlib import Path
import json

kb = KnowledgeBase("./data/my_kb")

# Custom metadata from configuration file
with open("documents_config.json", "r") as f:
    config = json.load(f)

# Process documents with custom metadata
for doc_config in config["documents"]:
    file_path = doc_config["path"]
    category = doc_config["category"]
    custom_metadata = doc_config["metadata"]

    print(f"\nProcessing: {file_path}")
    print(f"  Metadata: {custom_metadata}")

    try:
        doc_id = kb.add_document(
            file_path,
            category=category,
            metadata=custom_metadata
        )
        print(f"  ✅ Added: {doc_id}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
```

**documents_config.json:**
```json
{
  "documents": [
    {
      "path": "./documents/research/paper1.pdf",
      "category": "research",
      "metadata": {
        "author": "John Doe",
        "year": 2024,
        "topic": "Machine Learning",
        "citation": "Doe et al., 2024"
      }
    },
    {
      "path": "./documents/guides/setup_guide.md",
      "category": "documentation",
      "metadata": {
        "version": "2.0",
        "audience": "developers",
        "last_updated": "2025-10-15"
      }
    }
  ]
}
```

## Method 5: Progress Tracking and Error Handling

```python
from knowledge_base import KnowledgeBase
from pathlib import Path
import time

def batch_ingest_with_tracking(kb, directory, category):
    """Batch ingest with detailed progress tracking"""

    directory = Path(directory)
    files = list(directory.rglob("*.*"))

    # Filter supported files
    supported_ext = ['.pdf', '.docx', '.md', '.txt', '.csv', '.html', '.json']
    files = [f for f in files if f.suffix.lower() in supported_ext]

    print(f"\n{'='*80}")
    print(f"Batch Ingestion: {directory}")
    print(f"{'='*80}")
    print(f"Total files found: {len(files)}")
    print(f"Category: {category}\n")

    # Track results
    successful = []
    failed = []
    start_time = time.time()

    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
        print(f"  Size: {file_path.stat().st_size / 1024:.1f} KB")

        try:
            doc_start = time.time()
            doc_id = kb.add_document(
                str(file_path),
                category=category
            )
            doc_time = time.time() - doc_start

            successful.append({
                'file': file_path.name,
                'doc_id': doc_id,
                'time': doc_time
            })

            # Progress estimate
            elapsed = time.time() - start_time
            avg_time = elapsed / i
            remaining = (len(files) - i) * avg_time

            print(f"  ✅ Success in {doc_time:.2f}s")
            print(f"  ⏱️  Estimated remaining: {remaining:.1f}s")

        except Exception as e:
            failed.append({
                'file': file_path.name,
                'error': str(e)
            })
            print(f"  ❌ Failed: {e}")

    # Summary
    total_time = time.time() - start_time

    print(f"\n{'='*80}")
    print(f"BATCH INGESTION COMPLETE")
    print(f"{'='*80}")
    print(f"Total files: {len(files)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average time per file: {total_time/len(files):.2f}s")

    if failed:
        print(f"\n⚠️  Failed files:")
        for failure in failed:
            print(f"  - {failure['file']}: {failure['error']}")

    return successful, failed

# Use the function
kb = KnowledgeBase("./data/my_kb")
successful, failed = batch_ingest_with_tracking(
    kb,
    "./documents/research",
    "research"
)
```

**Output:**
```
================================================================================
Batch Ingestion: ./documents/research
================================================================================
Total files found: 5
Category: research

[1/5] Processing: paper1.pdf
  Size: 1234.5 KB
[KB] Adding document: paper1.pdf
[KB] Category: research
...
  ✅ Success in 8.42s
  ⏱️  Estimated remaining: 33.7s

[2/5] Processing: paper2.pdf
  Size: 2341.2 KB
...
  ✅ Success in 12.15s
  ⏱️  Estimated remaining: 30.7s

[3/5] Processing: corrupted_file.pdf
  Size: 45.3 KB
  ❌ Failed: Invalid PDF file

[4/5] Processing: paper3.pdf
  Size: 1523.8 KB
...
  ✅ Success in 9.87s
  ⏱️  Estimated remaining: 9.9s

[5/5] Processing: paper4.pdf
  Size: 1845.1 KB
...
  ✅ Success in 10.23s
  ⏱️  Estimated remaining: 0.0s

================================================================================
BATCH INGESTION COMPLETE
================================================================================
Total files: 5
Successful: 4
Failed: 1
Total time: 40.67s
Average time per file: 8.13s

⚠️  Failed files:
  - corrupted_file.pdf: Invalid PDF file
```

## Performance Tips

### Tip 1: Use File Extensions Filter
```python
# Only process PDFs (faster than checking all files)
kb.add_documents_batch(
    "./documents",
    category="research",
    file_extensions=['.pdf']
)
```

### Tip 2: Process in Parallel (Advanced)
```python
from concurrent.futures import ThreadPoolExecutor
from knowledge_base import KnowledgeBase

def process_file(file_path, kb, category):
    """Process single file (for parallel execution)"""
    try:
        return kb.add_document(str(file_path), category=category)
    except Exception as e:
        return None

# Parallel processing
kb = KnowledgeBase("./data/my_kb")
files = list(Path("./documents").rglob("*.pdf"))

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(process_file, f, kb, "research")
        for f in files
    ]

    doc_ids = [f.result() for f in futures if f.result()]

print(f"Processed {len(doc_ids)} documents in parallel")
```

### Tip 3: Skip Already Processed Files
```python
def smart_batch_add(kb, directory, category):
    """Only process new files not already in KB"""

    # Get existing files in KB
    existing = kb.list_documents(category=category)
    existing_names = {doc['name'] for doc in existing}

    # Find new files
    new_files = []
    for file_path in Path(directory).rglob("*.*"):
        if file_path.name not in existing_names:
            new_files.append(file_path)

    print(f"Found {len(new_files)} new files to process")

    # Process only new files
    for file_path in new_files:
        kb.add_document(str(file_path), category=category)
```

## Next Steps

After batch ingestion:
1. Verify all documents loaded: `kb.list_documents()`
2. Check statistics: `kb.get_statistics()`
3. Test search: `kb.search("your query")`
4. Export metadata: `kb.export_metadata()`

See also:
- [Basic Workflow](basic_workflow.md)
- [Advanced Search](advanced_search.md)
