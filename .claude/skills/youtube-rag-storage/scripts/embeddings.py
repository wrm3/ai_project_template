"""
Embedding Generation Module for YouTube RAG Storage

Generates vector embeddings using OpenAI's text-embedding-3-small model.
Handles batch processing, cost estimation, and error recovery.

Usage:
    from embeddings import generate_embeddings_batch, generate_embedding_single

    # Batch processing
    embeddings = generate_embeddings_batch(["text 1", "text 2", ...])

    # Single embedding
    embedding = generate_embedding_single("query text")
"""

import os
import openai
import numpy as np
from typing import List, Optional, Dict
import time
from dataclasses import dataclass


@dataclass
class EmbeddingStats:
    """Statistics for embedding generation"""
    total_texts: int
    total_tokens: int
    cost_usd: float
    duration_seconds: float
    texts_per_second: float
    tokens_per_second: float


class EmbeddingGenerator:
    """
    Handles embedding generation with OpenAI API

    Features:
    - Batch processing (up to 2048 texts per request)
    - Automatic retries with exponential backoff
    - Token counting and cost estimation
    - Progress tracking
    - Error handling
    """

    # Pricing (as of Oct 2025)
    PRICING = {
        'text-embedding-3-small': 0.020,  # per 1M tokens
        'text-embedding-3-large': 0.130   # per 1M tokens
    }

    # Model dimensions
    DIMENSIONS = {
        'text-embedding-3-small': 1536,
        'text-embedding-3-large': 3072
    }

    # API limits
    MAX_BATCH_SIZE = 2048  # OpenAI limit per request
    MAX_TOKENS_PER_REQUEST = 8191  # Context window

    def __init__(self, model: str = 'text-embedding-3-small', api_key: Optional[str] = None):
        """
        Initialize embedding generator

        Args:
            model: OpenAI embedding model name
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
        """
        self.model = model
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))

        if model not in self.PRICING:
            raise ValueError(f"Unknown model: {model}. Supported: {list(self.PRICING.keys())}")

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text

        Simple heuristic: ~130 tokens per 100 words
        For precise counting, use tiktoken library

        Args:
            text: Input text

        Returns:
            Estimated token count
        """
        # Simple approximation: 1 token ≈ 0.75 words
        word_count = len(text.split())
        return int(word_count * 1.3)

    def estimate_cost(self, total_tokens: int) -> float:
        """
        Estimate embedding cost

        Args:
            total_tokens: Total tokens to embed

        Returns:
            Estimated cost in USD
        """
        price_per_million = self.PRICING[self.model]
        return (total_tokens / 1_000_000) * price_per_million

    def generate_embedding_single(
        self,
        text: str,
        max_retries: int = 3
    ) -> np.ndarray:
        """
        Generate embedding for single text

        Args:
            text: Input text
            max_retries: Maximum retry attempts on failure

        Returns:
            Embedding vector as numpy array

        Raises:
            Exception: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=[text]  # API expects list
                )

                embedding = np.array(response.data[0].embedding)
                return embedding

            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"[RETRY] Attempt {attempt + 1}/{max_retries} failed: {e}")
                    print(f"[WAIT] Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed after {max_retries} attempts: {e}")

    def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: Optional[int] = None,
        show_progress: bool = True,
        max_retries: int = 3
    ) -> tuple[List[np.ndarray], EmbeddingStats]:
        """
        Generate embeddings for multiple texts in batches

        Args:
            texts: List of input texts
            batch_size: Batch size (default: 100 for balance of speed/safety)
            show_progress: Show progress indicators
            max_retries: Maximum retry attempts per batch

        Returns:
            Tuple of (embeddings list, statistics)

        Example:
            embeddings, stats = generator.generate_embeddings_batch(chunks)
            print(f"Cost: ${stats.cost_usd:.4f}")
            print(f"Speed: {stats.texts_per_second:.1f} texts/sec")
        """
        if not texts:
            return [], EmbeddingStats(0, 0, 0.0, 0.0, 0.0, 0.0)

        # Use conservative batch size by default
        if batch_size is None:
            batch_size = 100

        batch_size = min(batch_size, self.MAX_BATCH_SIZE)

        all_embeddings = []
        total_tokens = 0
        start_time = time.time()

        if show_progress:
            print(f"\n[EMBEDDINGS] Generating embeddings for {len(texts)} texts")
            print(f"[EMBEDDINGS] Model: {self.model} ({self.DIMENSIONS[self.model]} dimensions)")
            print(f"[EMBEDDINGS] Batch size: {batch_size}")

        # Process in batches
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(texts) + batch_size - 1) // batch_size

            # Retry logic for each batch
            for attempt in range(max_retries):
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=batch
                    )

                    # Extract embeddings
                    batch_embeddings = [
                        np.array(item.embedding)
                        for item in response.data
                    ]
                    all_embeddings.extend(batch_embeddings)

                    # Track tokens
                    batch_tokens = response.usage.total_tokens
                    total_tokens += batch_tokens

                    if show_progress:
                        progress = min(i + batch_size, len(texts))
                        pct = (progress / len(texts)) * 100
                        print(f"[PROGRESS] Batch {batch_num}/{total_batches}: "
                              f"{progress}/{len(texts)} texts ({pct:.1f}%) | "
                              f"{batch_tokens} tokens")

                    break  # Success, exit retry loop

                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"[RETRY] Batch {batch_num} attempt {attempt + 1}/{max_retries} failed: {e}")
                        print(f"[WAIT] Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise Exception(f"Batch {batch_num} failed after {max_retries} attempts: {e}")

        # Calculate statistics
        duration = time.time() - start_time
        cost = self.estimate_cost(total_tokens)

        stats = EmbeddingStats(
            total_texts=len(texts),
            total_tokens=total_tokens,
            cost_usd=cost,
            duration_seconds=duration,
            texts_per_second=len(texts) / duration if duration > 0 else 0,
            tokens_per_second=total_tokens / duration if duration > 0 else 0
        )

        if show_progress:
            print(f"\n[COMPLETE] Generated {len(all_embeddings)} embeddings")
            print(f"[STATS] Total tokens: {total_tokens:,}")
            print(f"[STATS] Cost: ${cost:.6f}")
            print(f"[STATS] Duration: {duration:.2f}s")
            print(f"[STATS] Speed: {stats.texts_per_second:.1f} texts/sec, "
                  f"{stats.tokens_per_second:.0f} tokens/sec\n")

        return all_embeddings, stats


# Convenience functions for simple usage
_default_generator = None

def get_default_generator() -> EmbeddingGenerator:
    """Get or create default generator instance"""
    global _default_generator
    if _default_generator is None:
        _default_generator = EmbeddingGenerator()
    return _default_generator


def generate_embedding_single(text: str, model: str = 'text-embedding-3-small') -> np.ndarray:
    """
    Generate embedding for single text (convenience function)

    Args:
        text: Input text
        model: Embedding model name

    Returns:
        Embedding vector as numpy array
    """
    generator = EmbeddingGenerator(model=model)
    return generator.generate_embedding_single(text)


def generate_embeddings_batch(
    texts: List[str],
    model: str = 'text-embedding-3-small',
    batch_size: int = 100,
    show_progress: bool = True
) -> List[np.ndarray]:
    """
    Generate embeddings for multiple texts (convenience function)

    Args:
        texts: List of input texts
        model: Embedding model name
        batch_size: Batch size
        show_progress: Show progress indicators

    Returns:
        List of embedding vectors
    """
    generator = EmbeddingGenerator(model=model)
    embeddings, stats = generator.generate_embeddings_batch(
        texts,
        batch_size=batch_size,
        show_progress=show_progress
    )
    return embeddings


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Calculate cosine similarity between two embeddings

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Cosine similarity score (0 to 1)
    """
    # Normalize vectors
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    # Calculate cosine similarity
    similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)

    # Clamp to [0, 1] range (handle floating point errors)
    return max(0.0, min(1.0, similarity))


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("OpenAI Embedding Generator - Test")
    print("=" * 80)
    print()

    # Test data
    test_texts = [
        "How to implement RAG with vector databases",
        "Claude 3.5 Sonnet API integration tutorial",
        "Python FastAPI best practices",
        "Supabase PostgreSQL with pgvector setup",
        "Machine learning model deployment strategies"
    ]

    print(f"Testing with {len(test_texts)} sample texts\n")

    # Generate embeddings
    generator = EmbeddingGenerator(model='text-embedding-3-small')
    embeddings, stats = generator.generate_embeddings_batch(test_texts)

    print("\n" + "=" * 80)
    print("Embedding Statistics")
    print("=" * 80)
    print(f"Total texts: {stats.total_texts}")
    print(f"Total tokens: {stats.total_tokens:,}")
    print(f"Cost: ${stats.cost_usd:.6f}")
    print(f"Duration: {stats.duration_seconds:.2f}s")
    print(f"Speed: {stats.texts_per_second:.1f} texts/sec")
    print()

    # Test similarity
    print("=" * 80)
    print("Similarity Test")
    print("=" * 80)
    sim_1_2 = cosine_similarity(embeddings[0], embeddings[1])
    sim_1_3 = cosine_similarity(embeddings[0], embeddings[2])

    print(f"Similarity (text 1 vs 2): {sim_1_2:.4f}")
    print(f"Similarity (text 1 vs 3): {sim_1_3:.4f}")
    print()

    print("✅ Test complete!")
