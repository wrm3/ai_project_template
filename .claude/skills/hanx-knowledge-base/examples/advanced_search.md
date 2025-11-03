# Advanced Search Examples

This example demonstrates advanced search techniques and filtering capabilities.

## Basic Semantic Search

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase("./data/my_kb")

# Natural language query
results = kb.search("How do I implement RAG with vector databases?", limit=5)

for result in results:
    print(f"Score: {result.score:.4f} | {result.metadata['file_name']}")
```

## Category-Filtered Search

```python
# Search only in technical documentation
results = kb.search(
    "machine learning algorithms",
    limit=10,
    category="technical"
)

print(f"Found {len(results)} results in 'technical' category")
```

## Metadata-Filtered Search

```python
# Search documents from specific author
results = kb.search(
    "neural networks",
    limit=5,
    metadata_filter={"author": "John Doe"}
)

# Search recent documents (requires date in metadata)
results = kb.search(
    "latest research",
    limit=5,
    metadata_filter={"year": 2025}
)

# Complex filter: category AND author
results = kb.search(
    "deep learning",
    limit=5,
    category="research",
    metadata_filter={"author": "Jane Smith", "topic": "AI"}
)
```

## Relevance Threshold Filtering

```python
# Only return highly relevant results (score >= 0.8)
results = kb.search("vector embeddings", limit=20)

# Filter by minimum score
high_quality_results = [r for r in results if r.score >= 0.8]

print(f"Total results: {len(results)}")
print(f"High quality (>= 0.8): {len(high_quality_results)}")

for result in high_quality_results:
    print(f"  {result.score:.4f} | {result.metadata['file_name']}")
```

## Multi-Query Search

```python
def multi_query_search(kb, queries, limit=5):
    """Search with multiple queries and combine results"""

    all_results = {}  # Track by chunk_id to avoid duplicates

    for query in queries:
        results = kb.search(query, limit=limit)

        for result in results:
            chunk_id = result.metadata.get('id', id(result))

            # Keep highest score for each chunk
            if chunk_id not in all_results or result.score > all_results[chunk_id].score:
                all_results[chunk_id] = result

    # Sort by score
    combined = sorted(all_results.values(), key=lambda x: x.score, reverse=True)

    return combined[:limit]

# Example usage
queries = [
    "What is RAG?",
    "retrieval augmented generation",
    "combining retrieval with LLMs"
]

results = multi_query_search(kb, queries, limit=10)
print(f"Combined results from {len(queries)} queries: {len(results)}")
```

## Contextual Search with Re-ranking

```python
def search_with_context(kb, query, context_keywords, limit=10):
    """Search and re-rank based on context keywords"""

    # Get initial results
    results = kb.search(query, limit=limit * 2)

    # Re-rank based on keyword presence
    scored_results = []

    for result in results:
        # Base score from semantic search
        score = result.score

        # Boost score if context keywords present
        text_lower = result.text.lower()
        keyword_matches = sum(1 for kw in context_keywords if kw.lower() in text_lower)

        # Boost: 0.05 per keyword match
        boosted_score = min(1.0, score + (keyword_matches * 0.05))

        scored_results.append((boosted_score, result))

    # Sort by boosted score
    scored_results.sort(key=lambda x: x[0], reverse=True)

    # Return top results
    return [result for _, result in scored_results[:limit]]

# Example
results = search_with_context(
    kb,
    query="database optimization",
    context_keywords=["vector", "embeddings", "index", "performance"],
    limit=5
)
```

## Search with Pagination

```python
def paginated_search(kb, query, page=1, per_page=10):
    """Search with pagination support"""

    # Get more results than needed
    total_to_fetch = page * per_page

    results = kb.search(query, limit=total_to_fetch)

    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    page_results = results[start_idx:end_idx]

    return {
        'results': page_results,
        'page': page,
        'per_page': per_page,
        'total_results': len(results),
        'has_next': end_idx < len(results),
        'has_prev': page > 1
    }

# Get first page
page1 = paginated_search(kb, "machine learning", page=1, per_page=10)
print(f"Page {page1['page']}: {len(page1['results'])} results")
print(f"Has next page: {page1['has_next']}")

# Get next page
if page1['has_next']:
    page2 = paginated_search(kb, "machine learning", page=2, per_page=10)
    print(f"Page {page2['page']}: {len(page2['results'])} results")
```

## Similarity Grouping

```python
from collections import defaultdict

def group_by_similarity(results, threshold=0.1):
    """Group similar results together"""

    groups = []
    used = set()

    for i, result1 in enumerate(results):
        if i in used:
            continue

        group = [result1]
        used.add(i)

        # Find similar results
        for j, result2 in enumerate(results[i+1:], start=i+1):
            if j in used:
                continue

            # If scores are very close, group together
            if abs(result1.score - result2.score) <= threshold:
                group.append(result2)
                used.add(j)

        groups.append(group)

    return groups

# Example
results = kb.search("vector databases", limit=20)
groups = group_by_similarity(results, threshold=0.05)

print(f"Found {len(groups)} distinct groups:")
for i, group in enumerate(groups, 1):
    print(f"\nGroup {i} ({len(group)} results):")
    for result in group:
        print(f"  {result.score:.4f} | {result.metadata['file_name']}")
```

## Export Search Results

```python
import json
from datetime import datetime

def export_search_results(results, query, output_file):
    """Export search results to JSON"""

    export_data = {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'total_results': len(results),
        'results': []
    }

    for i, result in enumerate(results, 1):
        export_data['results'].append({
            'rank': i,
            'score': result.score,
            'text': result.text,
            'metadata': result.metadata
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)

    print(f"Exported {len(results)} results to {output_file}")

# Example
results = kb.search("RAG implementation", limit=10)
export_search_results(results, "RAG implementation", "search_results.json")
```

## Search Analytics

```python
def analyze_search_results(kb, queries):
    """Analyze search quality across multiple queries"""

    analytics = {
        'total_queries': len(queries),
        'avg_results': 0,
        'avg_top_score': 0,
        'queries': []
    }

    total_results = 0
    total_top_score = 0

    for query in queries:
        results = kb.search(query, limit=10)

        query_data = {
            'query': query,
            'result_count': len(results),
            'top_score': results[0].score if results else 0,
            'avg_score': sum(r.score for r in results) / len(results) if results else 0,
            'score_distribution': {
                '0.9+': len([r for r in results if r.score >= 0.9]),
                '0.8-0.9': len([r for r in results if 0.8 <= r.score < 0.9]),
                '0.7-0.8': len([r for r in results if 0.7 <= r.score < 0.8]),
                '<0.7': len([r for r in results if r.score < 0.7])
            }
        }

        analytics['queries'].append(query_data)
        total_results += len(results)
        total_top_score += query_data['top_score']

    analytics['avg_results'] = total_results / len(queries)
    analytics['avg_top_score'] = total_top_score / len(queries)

    return analytics

# Example
test_queries = [
    "What is RAG?",
    "vector database setup",
    "embedding generation",
    "semantic search implementation",
    "chunking strategies"
]

analytics = analyze_search_results(kb, test_queries)

print("Search Analytics:")
print(f"  Total queries: {analytics['total_queries']}")
print(f"  Avg results per query: {analytics['avg_results']:.1f}")
print(f"  Avg top score: {analytics['avg_top_score']:.4f}")

print("\nScore distribution across all queries:")
for query_data in analytics['queries']:
    print(f"\n  {query_data['query']}:")
    print(f"    Results: {query_data['result_count']}")
    print(f"    Top score: {query_data['top_score']:.4f}")
    dist = query_data['score_distribution']
    print(f"    Distribution: 0.9+ ({dist['0.9+']}), 0.8-0.9 ({dist['0.8-0.9']}), 0.7-0.8 ({dist['0.7-0.8']}), <0.7 ({dist['<0.7']})")
```

## Command-Line Advanced Search

Using the provided `search_kb.py` script:

```bash
# Basic search
python search_kb.py "vector databases"

# With category filter
python search_kb.py "machine learning" --category research

# With minimum score threshold
python search_kb.py "embeddings" --min-score 0.75

# More results
python search_kb.py "RAG systems" --limit 20

# Verbose output (show all metadata)
python search_kb.py "semantic search" --verbose

# Export to JSON
python search_kb.py "knowledge base" --output results.json

# Combined filters
python search_kb.py "neural networks" \
    --category research \
    --min-score 0.8 \
    --limit 15 \
    --verbose \
    --output nn_results.json
```

## Best Practices

### Query Formulation

**Good queries:**
- ✅ "How do I implement RAG with vector databases?"
- ✅ "What are the best practices for chunking documents?"
- ✅ "Explain the difference between cosine and euclidean distance"

**Poor queries:**
- ❌ "RAG" (too short, use full phrase)
- ❌ "database" (too generic)
- ❌ "help" (not specific)

### Result Interpretation

**Score ranges:**
- **0.9-1.0**: Excellent match, highly relevant
- **0.8-0.9**: Very good match, relevant
- **0.7-0.8**: Good match, likely relevant
- **0.6-0.7**: Fair match, may be relevant
- **<0.6**: Poor match, likely not relevant

### Performance Optimization

```python
# Cache frequently used queries
query_cache = {}

def cached_search(kb, query, limit=5):
    """Search with caching for frequently used queries"""
    cache_key = f"{query}:{limit}"

    if cache_key not in query_cache:
        query_cache[cache_key] = kb.search(query, limit)

    return query_cache[cache_key]

# Use cached search
results = cached_search(kb, "common query", limit=5)
```

## Next Steps

- Try different query formulations
- Experiment with relevance thresholds
- Combine with LLMs for RAG pipelines
- Build custom search interfaces

See also:
- [Basic Workflow](basic_workflow.md)
- [Batch Ingestion](batch_ingestion.md)
