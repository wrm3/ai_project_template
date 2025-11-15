# Semantic Search Guide

Complete guide to implementing and optimizing semantic search for YouTube RAG system.

**Author**: AI Project Template Team
**Created**: 2025-10-28
**Task**: 044-6

---

## Table of Contents

1. [What Is Semantic Search?](#what-is-semantic-search)
2. [Vector Similarity Basics](#vector-similarity-basics)
3. [PostgreSQL + pgvector](#postgresql--pgvector)
4. [Query Patterns](#query-patterns)
5. [Performance Optimization](#performance-optimization)
6. [Result Ranking](#result-ranking)
7. [Advanced Techniques](#advanced-techniques)

---

## What Is Semantic Search?

**Semantic search** finds content based on meaning, not just keywords.

### Traditional Keyword Search

```sql
-- Finds exact matches only
SELECT * FROM documents
WHERE content LIKE '%vector database%'
```

**Problems**:
- Misses synonyms ("embedding storage", "similarity search")
- Misses related concepts ("cosine distance", "pgvector")
- No ranking by relevance
- Order-dependent ("database vector" doesn't match "vector database")

### Semantic Search with Embeddings

```sql
-- Finds semantically similar content
SELECT * FROM documents
WHERE embedding <-> query_embedding < 0.3  -- Cosine distance threshold
ORDER BY embedding <-> query_embedding
LIMIT 10
```

**Advantages**:
- ✅ Matches similar meanings ("vector DB" = "embedding store")
- ✅ Finds related concepts automatically
- ✅ Ranked by semantic similarity
- ✅ Order-independent
- ✅ Works across languages (with translation)

### Example Comparison

**Query**: "How to store vectors in database"

**Keyword search finds**:
- "Tutorial on storing vectors in a database" ✓
- Misses: "Vector database implementation guide" (no exact words)
- Misses: "Using pgvector for similarity search" (different words)

**Semantic search finds**:
- "Tutorial on storing vectors in a database" (0.95 similarity) ✓
- "Vector database implementation guide" (0.89 similarity) ✓
- "Using pgvector for similarity search" (0.87 similarity) ✓
- "Embedding storage with PostgreSQL" (0.84 similarity) ✓

---

## Vector Similarity Basics

### Cosine Similarity

**What it measures**: Angle between vectors (orientation, not magnitude)

```
Vector A: [1, 0]
Vector B: [1, 1]  (45° angle)

Cosine similarity = cos(45°) = 0.707

Vector C: [-1, 0]  (180° angle)
Cosine similarity = cos(180°) = -1.0
```

**Range**: -1 (opposite) to 1 (identical)

**Formula**:
```
cos(θ) = (A · B) / (|A| × |B|)

Where:
  A · B = dot product
  |A| = magnitude of A
  |B| = magnitude of B
```

**In Python**:
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    magnitude_a = np.linalg.norm(vec1)
    magnitude_b = np.linalg.norm(vec2)

    return dot_product / (magnitude_a * magnitude_b)
```

### Cosine Distance

**What it is**: 1 - cosine similarity (used by pgvector)

**Range**: 0 (identical) to 2 (opposite)

```
Distance = 1 - Similarity

Examples:
  Identical vectors: 1 - 1.0 = 0.0
  Orthogonal vectors: 1 - 0.0 = 1.0
  Opposite vectors: 1 - (-1.0) = 2.0
```

**Why use distance instead of similarity?**
- Smaller values = better matches (intuitive for "distance")
- Compatible with index structures (IVFFlat, HNSW)
- Easier to set thresholds (< 0.3 = good match)

### Other Distance Metrics

**Euclidean Distance (L2)**:
```python
def euclidean_distance(vec1, vec2):
    return np.linalg.norm(np.array(vec1) - np.array(vec2))

# Range: 0 to infinity
# Good for: Magnitude-sensitive comparisons
```

**Manhattan Distance (L1)**:
```python
def manhattan_distance(vec1, vec2):
    return np.sum(np.abs(np.array(vec1) - np.array(vec2)))

# Range: 0 to infinity
# Good for: High-dimensional sparse vectors
```

**Dot Product** (inner product):
```python
def dot_product(vec1, vec2):
    return np.dot(vec1, vec2)

# Range: -infinity to infinity
# Good for: Normalized vectors (equivalent to cosine similarity)
```

**Recommendation**: Use **cosine distance** for text embeddings (standard in RAG)

---

## PostgreSQL + pgvector

### Vector Type

```sql
-- Create table with vector column
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- 1536 dimensions for text-embedding-3-small
);
```

### Distance Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `<->` | Cosine distance | `embedding <-> query_embedding` |
| `<#>` | Negative inner product | `embedding <#> query_embedding` |
| `<=>` | Euclidean distance (L2) | `embedding <=> query_embedding` |

**Most common**: Use `<->` for cosine distance

### Basic Query

```sql
-- Find 10 most similar documents
SELECT
    id,
    content,
    embedding <-> '[0.1, 0.2, ...]'::vector AS distance
FROM documents
ORDER BY embedding <-> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

### With Filters

```sql
-- Search within specific video
SELECT
    c.chunk_text,
    c.embedding <-> %s::vector AS distance,
    v.title
FROM transcript_chunks c
JOIN youtube_videos v ON c.video_id = v.id
WHERE v.video_id = 'dQw4w9WgXcQ'
ORDER BY c.embedding <-> %s::vector
LIMIT 10;
```

### Index Types

**IVFFlat** (Inverted File with Flat compression):
```sql
CREATE INDEX idx_embedding ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- lists = number of partitions
-- Rule of thumb: lists = sqrt(total_rows)
```

**Pros**:
- Faster than exact search for large datasets
- Good balance of speed and accuracy

**Cons**:
- Approximate results (not exact)
- Requires VACUUM ANALYZE after bulk inserts

**HNSW** (Hierarchical Navigable Small World):
```sql
CREATE INDEX idx_embedding ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- m = max connections per layer
-- ef_construction = size of dynamic candidate list during construction
```

**Pros**:
- Faster query time than IVFFlat
- Better recall (accuracy)

**Cons**:
- Slower to build
- More memory usage

**Recommendation**: Use **IVFFlat** for RAG (good balance)

---

## Query Patterns

### Pattern 1: Basic Semantic Search

```python
def semantic_search(query: str, limit: int = 10):
    """
    Find semantically similar content.

    Args:
        query: Natural language query
        limit: Maximum results to return

    Returns:
        List of matching chunks with similarity scores
    """
    from openai import OpenAI
    from db_client import SupabaseClient

    # 1. Generate query embedding
    openai_client = OpenAI()
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding

    # 2. Search database
    db_client = SupabaseClient()
    results = db_client.semantic_search(
        query_embedding=query_embedding,
        limit=limit
    )
    db_client.close()

    return results
```

### Pattern 2: Search with Filters

```python
def filtered_search(
    query: str,
    video_id: str = None,
    chunk_type: str = None,
    min_similarity: float = 0.7,
    limit: int = 10
):
    """
    Search with metadata filters.

    Args:
        query: Natural language query
        video_id: Filter by specific video
        chunk_type: Filter by chunk type (code, transcript, etc.)
        min_similarity: Minimum similarity threshold
        limit: Maximum results

    Returns:
        Filtered and ranked results
    """
    # Generate query embedding
    query_embedding = generate_embedding(query)

    # Build SQL with filters
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT
            c.chunk_text,
            c.chunk_type,
            c.timestamp_start,
            v.title,
            v.author,
            1 - (c.embedding <-> %s::vector) AS similarity
        FROM transcript_chunks c
        JOIN youtube_videos v ON c.video_id = v.id
        WHERE 1=1
    """

    params = [query_embedding]

    if video_id:
        sql += " AND v.video_id = %s"
        params.append(video_id)

    if chunk_type:
        sql += " AND c.chunk_type = %s"
        params.append(chunk_type)

    if min_similarity > 0:
        sql += " AND (1 - (c.embedding <-> %s::vector)) >= %s"
        params.extend([query_embedding, min_similarity])

    sql += """
        ORDER BY c.embedding <-> %s::vector
        LIMIT %s
    """
    params.extend([query_embedding, limit])

    cursor.execute(sql, params)
    return cursor.fetchall()
```

### Pattern 3: Multi-Query Search

```python
def multi_query_search(queries: List[str], limit: int = 10):
    """
    Search using multiple related queries and combine results.

    Args:
        queries: List of related queries
        limit: Total results to return

    Returns:
        Combined and deduplicated results
    """
    all_results = []

    for query in queries:
        results = semantic_search(query, limit=limit * 2)
        all_results.extend(results)

    # Deduplicate and re-rank
    seen_ids = set()
    unique_results = []

    for result in sorted(all_results, key=lambda x: x['similarity'], reverse=True):
        if result['id'] not in seen_ids:
            seen_ids.add(result['id'])
            unique_results.append(result)

            if len(unique_results) >= limit:
                break

    return unique_results
```

### Pattern 4: Hybrid Search (Semantic + Keyword)

```python
def hybrid_search(query: str, limit: int = 10):
    """
    Combine semantic search with traditional keyword search.

    Args:
        query: Natural language query
        limit: Maximum results

    Returns:
        Combined results from both methods
    """
    # Semantic search
    semantic_results = semantic_search(query, limit=limit)

    # Keyword search (full-text)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.chunk_text,
            ts_rank(to_tsvector('english', c.chunk_text), plainto_tsquery('english', %s)) AS rank
        FROM transcript_chunks c
        WHERE to_tsvector('english', c.chunk_text) @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT %s
    """, (query, query, limit))

    keyword_results = cursor.fetchall()

    # Combine results (weighted)
    combined_scores = {}

    for result in semantic_results:
        combined_scores[result['id']] = result['similarity'] * 0.7  # 70% weight

    for result in keyword_results:
        if result['id'] in combined_scores:
            combined_scores[result['id']] += result['rank'] * 0.3  # 30% weight
        else:
            combined_scores[result['id']] = result['rank'] * 0.3

    # Sort by combined score
    sorted_ids = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_ids[:limit]
```

---

## Performance Optimization

### 1. Index Optimization

**IVFFlat `lists` parameter**:
```sql
-- Rule of thumb: lists = sqrt(total_rows)

-- For 10K rows
CREATE INDEX idx_embedding ON transcript_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- sqrt(10000) = 100

-- For 100K rows
CREATE INDEX idx_embedding ON transcript_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 316);  -- sqrt(100000) ≈ 316

-- For 1M rows
CREATE INDEX idx_embedding ON transcript_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 1000);  -- sqrt(1000000) = 1000
```

**Rebuild index after bulk inserts**:
```sql
-- After inserting many rows
VACUUM ANALYZE transcript_chunks;

-- Rebuild index
REINDEX INDEX idx_embedding;
```

### 2. Query Optimization

**Use `EXPLAIN ANALYZE`**:
```sql
EXPLAIN ANALYZE
SELECT chunk_text, embedding <-> '[...]'::vector AS distance
FROM transcript_chunks
ORDER BY embedding <-> '[...]'::vector
LIMIT 10;

-- Check for:
-- - Index usage (should see "Index Scan using idx_embedding")
-- - Execution time
-- - Row estimation accuracy
```

**Optimize with `probes`** (IVFFlat):
```sql
-- Increase probes for better accuracy (slower)
SET ivfflat.probes = 10;  -- Default is 1

SELECT * FROM transcript_chunks
ORDER BY embedding <-> '[...]'::vector
LIMIT 10;

-- Probes trade-off:
-- probes = 1: Fastest, ~90% recall
-- probes = 10: Slower, ~95% recall
-- probes = lists: Exact search (no approximation)
```

### 3. Connection Pooling

```python
from psycopg2.pool import SimpleConnectionPool

class DatabaseClient:
    def __init__(self, min_conn=2, max_conn=10):
        self.pool = SimpleConnectionPool(
            minconn=min_conn,
            maxconn=max_conn,
            dsn=connection_string
        )

    def search(self, query_embedding, limit=10):
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM transcript_chunks
                ORDER BY embedding <-> %s::vector
                LIMIT %s
            """, (query_embedding, limit))
            return cursor.fetchall()
        finally:
            self.pool.putconn(conn)
```

### 4. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_query_embedding(query: str):
    """Cache query embeddings to avoid regeneration"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return tuple(response.data[0].embedding)  # Tuple for hashability
```

---

## Result Ranking

### Similarity Score Interpretation

| Similarity | Distance | Quality |
|-----------|----------|---------|
| 0.90-1.00 | 0.00-0.10 | Excellent match |
| 0.80-0.89 | 0.11-0.20 | Very good match |
| 0.70-0.79 | 0.21-0.30 | Good match |
| 0.60-0.69 | 0.31-0.40 | Moderate match |
| < 0.60 | > 0.40 | Poor match |

**Recommended threshold**: 0.70 similarity (0.30 distance)

### Reranking Strategies

**1. Metadata Boost**:
```python
def rerank_with_metadata(results):
    """Boost scores based on metadata"""
    for result in results:
        # Boost recent content
        days_old = (datetime.now() - result['created_at']).days
        recency_boost = max(0, 1 - days_old / 365)  # Decay over a year

        # Boost popular videos
        popularity_boost = min(result['views'] / 1_000_000, 1.0)  # Cap at 1M views

        # Boost code chunks if query mentions code
        code_boost = 1.2 if result['has_code'] and 'code' in query.lower() else 1.0

        # Combine boosts
        result['boosted_similarity'] = (
            result['similarity'] *
            (1 + recency_boost * 0.1) *
            (1 + popularity_boost * 0.1) *
            code_boost
        )

    return sorted(results, key=lambda x: x['boosted_similarity'], reverse=True)
```

**2. Cross-Encoder Reranking**:
```python
from sentence_transformers import CrossEncoder

def rerank_with_cross_encoder(query: str, results: List[dict]):
    """
    Rerank top results using cross-encoder model.

    Cross-encoders are more accurate but slower.
    Use for final reranking of top-K results.
    """
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    # Prepare pairs
    pairs = [[query, result['chunk_text']] for result in results]

    # Get cross-encoder scores
    scores = model.predict(pairs)

    # Update results
    for result, score in zip(results, scores):
        result['rerank_score'] = score

    return sorted(results, key=lambda x: x['rerank_score'], reverse=True)
```

---

## Advanced Techniques

### 1. Query Expansion

```python
def expand_query(query: str) -> List[str]:
    """
    Expand query with synonyms and related terms.

    Uses LLM to generate alternative phrasings.
    """
    from anthropic import Anthropic

    client = Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Generate 3 alternative phrasings of this search query:
            "{query}"

            Return only the alternatives, one per line."""
        }]
    )

    alternatives = [query]  # Original query
    alternatives.extend(response.content[0].text.strip().split('\n'))

    return alternatives

# Usage
query = "How to implement RAG"
queries = expand_query(query)
# ["How to implement RAG",
#  "RAG implementation tutorial",
#  "Building retrieval-augmented generation",
#  "Setting up vector search for LLMs"]

results = multi_query_search(queries, limit=10)
```

### 2. Contextual Retrieval

```python
def contextual_search(query: str, context: dict, limit: int = 10):
    """
    Search with user context for personalized results.

    Args:
        query: User query
        context: User context (preferences, history, etc.)
        limit: Maximum results

    Returns:
        Personalized results
    """
    # Enhance query with context
    enhanced_query = f"{query} {context.get('domain', '')}"

    # Search with enhanced query
    results = semantic_search(enhanced_query, limit=limit * 2)

    # Filter by user preferences
    if 'preferred_authors' in context:
        results = [r for r in results if r['author'] in context['preferred_authors']]

    # Boost based on user history
    if 'watched_videos' in context:
        for result in results:
            if result['video_id'] in context['watched_videos']:
                result['similarity'] *= 1.2  # Boost familiar content

    return sorted(results, key=lambda x: x['similarity'], reverse=True)[:limit]
```

### 3. Negative Sampling

```python
def search_with_negatives(query: str, negative_queries: List[str], limit: int = 10):
    """
    Search while excluding content similar to negative queries.

    Args:
        query: Positive query (what to find)
        negative_queries: What to avoid
        limit: Maximum results

    Returns:
        Filtered results
    """
    # Get positive results
    positive_results = semantic_search(query, limit=limit * 3)

    # Get negative embeddings
    negative_embeddings = [generate_embedding(nq) for nq in negative_queries]

    # Filter out results too similar to negatives
    filtered_results = []
    for result in positive_results:
        # Check similarity to negatives
        max_negative_sim = max(
            cosine_similarity(result['embedding'], neg_emb)
            for neg_emb in negative_embeddings
        )

        # Keep if not too similar to negatives
        if max_negative_sim < 0.7:
            filtered_results.append(result)

            if len(filtered_results) >= limit:
                break

    return filtered_results
```

---

## Best Practices Summary

### ✅ Do
- Use cosine distance for text embeddings
- Set appropriate similarity thresholds (0.7 recommended)
- Create indexes for large datasets (>1K rows)
- Use connection pooling for performance
- Cache query embeddings
- Rerank top results with metadata
- Monitor query performance with EXPLAIN
- Adjust IVFFlat `lists` based on dataset size

### ❌ Don't
- Use exact search for large datasets (>10K rows)
- Set similarity threshold too high (>0.9)
- Forget to rebuild indexes after bulk inserts
- Skip query optimization
- Ignore user context and preferences
- Return too many results (keep limit reasonable)
- Mix different embedding models

---

## Additional Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [Sentence Transformers](https://www.sbert.net/)
- [HNSW Paper](https://arxiv.org/abs/1603.09320)

---

**Next**: See [Database Schema](database_schema.md) for complete schema reference.
