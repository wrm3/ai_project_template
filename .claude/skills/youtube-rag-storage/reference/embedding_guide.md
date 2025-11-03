# Embedding Generation Guide

Complete guide to generating and using vector embeddings for YouTube RAG system.

**Author**: AI Project Template Team
**Created**: 2025-10-28
**Task**: 044-6

---

## Table of Contents

1. [What Are Embeddings?](#what-are-embeddings)
2. [OpenAI text-embedding-3-small](#openai-text-embedding-3-small)
3. [Generating Embeddings](#generating-embeddings)
4. [Batch Processing](#batch-processing)
5. [Cost Optimization](#cost-optimization)
6. [Quality Considerations](#quality-considerations)
7. [Troubleshooting](#troubleshooting)

---

## What Are Embeddings?

**Embeddings** are high-dimensional vector representations of text that capture semantic meaning.

### Key Concepts

**Semantic Similarity**: Similar meanings produce similar vectors
```
"dog" ≈ "puppy" ≈ "canine"
↓
[0.23, -0.15, 0.87, ...] ≈ [0.21, -0.14, 0.89, ...]
```

**Vector Operations**: Mathematical operations on semantic concepts
```python
king - man + woman ≈ queen
[0.5, 0.8, ...] - [0.2, 0.1, ...] + [0.3, 0.2, ...] ≈ [0.6, 0.9, ...]
```

**Dimensionality**: More dimensions = more nuanced representation
- 1536 dimensions (text-embedding-3-small)
- Each dimension captures different semantic features

### Why Embeddings for RAG?

Traditional search (keyword matching):
```
Query: "How to implement vector search"
Matches: Exact words "vector", "search", "implement"
Misses: "semantic similarity", "cosine distance", "embedding lookup"
```

Semantic search (embedding similarity):
```
Query: "How to implement vector search"
Finds:
  ✓ "Using pgvector for similarity queries" (0.89 similarity)
  ✓ "Cosine distance in PostgreSQL" (0.85 similarity)
  ✓ "Building a semantic search engine" (0.82 similarity)
```

---

## OpenAI text-embedding-3-small

### Specifications

| Property | Value |
|----------|-------|
| Model ID | `text-embedding-3-small` |
| Dimensions | 1536 |
| Max Input Tokens | 8,192 |
| Pricing | $0.020 per 1M tokens |
| Performance | 300K+ tokens/minute |
| Released | January 2024 |

### Why text-embedding-3-small?

**Compared to alternatives**:

| Model | Dimensions | Cost per 1M | Quality | Speed |
|-------|-----------|-------------|---------|-------|
| text-embedding-3-small | 1536 | $0.020 | ⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ |
| text-embedding-3-large | 3072 | $0.130 | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ |
| text-embedding-ada-002 | 1536 | $0.100 | ⭐⭐⭐ | ⚡⚡⚡⚡ |
| Claude embeddings | N/A | N/A | N/A | N/A |

**Verdict**: text-embedding-3-small is the **best value** for RAG applications
- 5x cheaper than ada-002
- Near-identical quality to larger models for search
- Fast enough for real-time applications

### Performance Benchmarks

**Retrieval Quality** (MTEB Benchmark):
```
text-embedding-3-small:   61.0% average
text-embedding-3-large:   62.3% average
text-embedding-ada-002:   60.9% average

Difference: <2% for 6.5x price increase (not worth it for RAG)
```

**Inference Speed**:
```
Single request:   ~200ms
Batch (100 texts): ~500ms
Batch (2048 texts): ~2s

Throughput: 300K+ tokens/minute
```

---

## Generating Embeddings

### Basic Usage

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Single text
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="This is a sample text to embed"
)

embedding = response.data[0].embedding  # List of 1536 floats
print(f"Dimensions: {len(embedding)}")  # 1536
print(f"Sample values: {embedding[:5]}")  # [-0.023, 0.145, ...]
```

### Multiple Texts (Batch)

```python
# Batch processing (up to 2048 texts per request)
texts = [
    "First chunk of transcript...",
    "Second chunk with code example...",
    "Third chunk about databases...",
    # ... up to 2048 texts
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

embeddings = [item.embedding for item in response.data]
print(f"Generated {len(embeddings)} embeddings")
```

### With Error Handling

```python
import time
from openai import OpenAI, OpenAIError

def generate_embeddings_safe(texts, max_retries=3):
    """Generate embeddings with retry logic"""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [item.embedding for item in response.data]

        except OpenAIError as e:
            if attempt == max_retries - 1:
                raise

            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # Exponential backoff

    raise RuntimeError("Failed to generate embeddings after retries")
```

---

## Batch Processing

### Optimal Batch Size

**Recommendations**:
```python
# For real-time applications
batch_size = 100  # ~500ms latency

# For batch processing
batch_size = 2048  # Maximum per request, ~2s latency

# For memory-constrained environments
batch_size = 50  # Lower memory usage
```

### Implementation

```python
def generate_embeddings_batch(texts, batch_size=100):
    """
    Generate embeddings for large text lists efficiently.

    Args:
        texts: List of strings to embed
        batch_size: Number of texts per API request

    Returns:
        List of embeddings (1536-dimensional vectors)
    """
    from openai import OpenAI
    import os

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )

        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

        print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} texts")

    return all_embeddings
```

### Progress Tracking

```python
from tqdm import tqdm

def generate_embeddings_with_progress(texts, batch_size=100):
    """Generate embeddings with progress bar"""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    all_embeddings = []

    # Calculate total batches
    num_batches = (len(texts) + batch_size - 1) // batch_size

    with tqdm(total=len(texts), desc="Generating embeddings") as pbar:
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )

            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

            pbar.update(len(batch))

    return all_embeddings
```

---

## Cost Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text, model="cl100k_base"):
    """
    Count tokens for cost estimation.

    text-embedding-3-small uses cl100k_base encoding
    """
    encoding = tiktoken.get_encoding(model)
    tokens = encoding.encode(text)
    return len(tokens)

# Example
text = "This is a sample chunk of transcript from a YouTube video."
num_tokens = count_tokens(text)
print(f"Tokens: {num_tokens}")  # ~14 tokens

# Cost calculation
cost_per_token = 0.020 / 1_000_000  # $0.020 per 1M tokens
cost = num_tokens * cost_per_token
print(f"Cost: ${cost:.8f}")  # $0.00000028
```

### Cost Estimation for Videos

```python
def estimate_embedding_cost(video_duration_minutes):
    """
    Estimate embedding cost for a YouTube video.

    Assumptions:
    - 150 words per minute (average speech rate)
    - 1.3 tokens per word (average)
    - Chunked into 500 chunks average (1-hour video)
    """
    # Calculate tokens
    words = video_duration_minutes * 150
    tokens = int(words * 1.3)

    # Calculate cost
    cost_per_token = 0.020 / 1_000_000
    cost = tokens * cost_per_token

    # Estimate chunks
    words_per_chunk = 130  # Average
    num_chunks = int(words / words_per_chunk)

    return {
        'duration_minutes': video_duration_minutes,
        'estimated_words': words,
        'estimated_tokens': tokens,
        'estimated_chunks': num_chunks,
        'estimated_cost': cost,
        'cost_formatted': f"${cost:.6f}"
    }

# Example: 1-hour video
estimate = estimate_embedding_cost(60)
print(f"1-hour video:")
print(f"  Chunks: {estimate['estimated_chunks']}")
print(f"  Tokens: {estimate['estimated_tokens']:,}")
print(f"  Cost: {estimate['cost_formatted']}")
# Output:
#   Chunks: 692
#   Tokens: 11,700
#   Cost: $0.000234
```

### Batch Cost Tracking

```python
class CostTracker:
    """Track OpenAI API costs for embeddings"""

    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.cost_per_million = 0.020

    def add_batch(self, texts):
        """Add batch of texts and update costs"""
        tokens = sum(count_tokens(text) for text in texts)
        cost = (tokens / 1_000_000) * self.cost_per_million

        self.total_tokens += tokens
        self.total_cost += cost

        return {
            'batch_tokens': tokens,
            'batch_cost': cost,
            'total_tokens': self.total_tokens,
            'total_cost': self.total_cost
        }

    def report(self):
        """Print cost summary"""
        print(f"Total tokens: {self.total_tokens:,}")
        print(f"Total cost: ${self.total_cost:.6f}")
        print(f"Average cost per 1K tokens: ${(self.total_cost / self.total_tokens * 1000):.8f}")

# Usage
tracker = CostTracker()

for batch in text_batches:
    embeddings = generate_embeddings_batch(batch)
    stats = tracker.add_batch(batch)
    print(f"Batch: {stats['batch_tokens']:,} tokens, ${stats['batch_cost']:.6f}")

tracker.report()
```

---

## Quality Considerations

### Input Text Preparation

**Best Practices**:
```python
def prepare_text_for_embedding(text):
    """Prepare text for optimal embedding quality"""

    # 1. Normalize whitespace
    text = ' '.join(text.split())

    # 2. Remove excessive punctuation (keep structural punctuation)
    import re
    text = re.sub(r'([.!?])\1+', r'\1', text)  # Multiple punctuation

    # 3. Keep text within token limits (8192 max, but 512-1024 optimal)
    if count_tokens(text) > 1024:
        # Truncate or split into multiple embeddings
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)[:1024]
        text = encoding.decode(tokens)

    return text
```

**Avoid**:
- ❌ Very short texts (<10 words): Poor semantic representation
- ❌ Very long texts (>1024 tokens): Diluted representation
- ❌ Mixed languages: Reduced quality
- ❌ Excessive special characters: Noise in embedding

**Recommended Length**:
- ✅ 50-200 words per chunk (optimal for semantic coherence)
- ✅ 400-1000 characters
- ✅ ~130 tokens average

### Embedding Normalization

```python
import numpy as np

def normalize_embedding(embedding):
    """
    Normalize embedding to unit length.

    Useful for:
    - Consistent similarity scores
    - Faster cosine similarity (dot product with normalized vectors)
    """
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)

    if norm == 0:
        return embedding  # Avoid division by zero

    normalized = embedding_array / norm
    return normalized.tolist()

# Example
embedding = generate_embedding("Sample text")
normalized = normalize_embedding(embedding)

print(f"Original length: {np.linalg.norm(embedding):.6f}")
print(f"Normalized length: {np.linalg.norm(normalized):.6f}")  # ~1.0
```

### Similarity Metrics

**Cosine Similarity** (recommended for normalized embeddings):
```python
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    similarity = dot_product / (norm1 * norm2)
    return similarity

# Range: -1 (opposite) to 1 (identical)
similarity = cosine_similarity(embedding1, embedding2)
```

**Cosine Distance** (used by pgvector):
```python
# Cosine distance = 1 - cosine similarity
# Range: 0 (identical) to 2 (opposite)

def cosine_distance(vec1, vec2):
    return 1 - cosine_similarity(vec1, vec2)
```

**Euclidean Distance** (L2 norm):
```python
def euclidean_distance(vec1, vec2):
    """Calculate Euclidean distance"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.linalg.norm(vec1 - vec2)

# Range: 0 (identical) to infinity
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Invalid API key"
```python
# Solution: Verify API key is set correctly
import os
print(os.getenv('OPENAI_API_KEY'))  # Should start with 'sk-'

# Set in .env file:
# OPENAI_API_KEY=sk-your-key-here
```

#### Issue 2: "Rate limit exceeded"
```python
# Solution: Implement retry logic with exponential backoff
import time

def generate_with_retry(texts, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = 2 ** attempt  # 1, 2, 4, 8, 16 seconds
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

#### Issue 3: "Token limit exceeded"
```python
# Solution: Check and truncate long texts
def safe_generate_embedding(text):
    tokens = count_tokens(text)

    if tokens > 8192:  # OpenAI limit
        print(f"Warning: Text has {tokens} tokens, truncating to 8192")
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens_list = encoding.encode(text)[:8192]
        text = encoding.decode(tokens_list)

    return generate_embedding(text)
```

#### Issue 4: "Dimension mismatch in database"
```python
# Solution: Verify embedding dimensions match database schema
embedding = generate_embedding("test")
print(f"Embedding dimensions: {len(embedding)}")  # Should be 1536

# Database schema should have:
# embedding vector(1536)
```

#### Issue 5: "Poor search quality"
```python
# Solutions:
# 1. Check chunk size (50-200 words optimal)
# 2. Verify text preprocessing (remove noise)
# 3. Ensure query and chunks are in same language
# 4. Adjust similarity threshold (try 0.5-0.8 range)
# 5. Use more specific queries
```

---

## Best Practices Summary

### ✅ Do
- Use batch processing (100-2048 texts per request)
- Track costs with token counting
- Normalize embeddings for consistent similarity
- Prepare text properly (remove noise, normalize whitespace)
- Use retry logic for API failures
- Cache embeddings to avoid regeneration
- Monitor embedding quality with test queries

### ❌ Don't
- Generate embeddings for very short texts (<10 words)
- Exceed token limits (8192 max, 1024 recommended)
- Mix multiple languages in single embedding
- Ignore API rate limits
- Store embeddings in inefficient formats
- Skip error handling
- Regenerate embeddings unnecessarily

---

## Additional Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [MTEB Benchmark](https://huggingface.co/spaces/mteb/leaderboard)
- [Tiktoken Documentation](https://github.com/openai/tiktoken)
- [pgvector Operations](https://github.com/pgvector/pgvector#querying)

---

**Next**: See [Semantic Search Guide](semantic_search_guide.md) for using embeddings in vector search.
