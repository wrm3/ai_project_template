# Example: General Video Analysis

## Scenario

You found an interesting conference talk on Python async programming and want to extract the key insights.

## Command

```bash
python specialized_analyzer.py \
    --url https://youtu.be/example_python_talk \
    --type general \
    --output ./python_async_analysis
```

## Workflow

### Step 1: Transcript Extraction

```
================================================================================
STEP 1: Get Video Transcript
================================================================================

Running youtube-video-analysis skill...
Downloading video: https://youtu.be/example_python_talk
Extracting audio...
Transcribing with Whisper (base model)...

[OK] Transcript loaded: 12,543 characters
```

### Step 2: LLM Analysis

```
================================================================================
STEP 2: Query LLM for Analysis
================================================================================

Using LLM provider: openai
Applying general analysis prompt template...

[OK] Received response: 2,341 characters
```

### Step 3: Save Results

```
================================================================================
STEP 3: Save Results
================================================================================

[OK] Saved JSON: ./python_async_analysis/general_analysis_20251101_120000.json
[OK] Saved Markdown: ./python_async_analysis/general_analysis_20251101_120000.md

Results saved to: ./python_async_analysis
```

## Output: JSON

```json
{
  "video_url": "https://youtu.be/example_python_talk",
  "analysis_type": "general",
  "timestamp": "2025-11-01T12:00:00Z",
  "metadata": {
    "title": "Async Python Made Simple",
    "duration": 1845,
    "author": "PyCon 2025"
  },
  "analysis": {
    "summary": "This talk demystifies Python's async/await syntax by building a simple async framework from scratch. The speaker explains event loops, coroutines, and common pitfalls, making async programming accessible to intermediate Python developers.",
    "key_points": [
      "Event loops are the heart of async programming - they schedule and run coroutines",
      "Async/await is syntactic sugar over generators and yield expressions",
      "Common mistake: mixing blocking I/O with async code breaks concurrency",
      "Use asyncio.gather() for concurrent task execution",
      "Async is best for I/O-bound tasks, not CPU-bound tasks"
    ],
    "topics": [
      "Event Loops",
      "Coroutines and Generators",
      "Async/Await Syntax",
      "asyncio Library",
      "Concurrency vs Parallelism",
      "Non-blocking I/O"
    ],
    "insights": [
      "Async doesn't make code faster - it makes waiting more efficient",
      "You can build a simple event loop in ~50 lines of Python",
      "The GIL still applies to async code - only one coroutine runs at a time",
      "Debugging async code requires special tools like asyncio debug mode"
    ],
    "questions_answered": [
      "When should I use async instead of threading?",
      "How do event loops actually work under the hood?",
      "Why can't I just await any function?",
      "What's the difference between concurrency and parallelism?"
    ],
    "references": [
      "David Beazley's 'Build Your Own Async' talk",
      "PEP 492 - Coroutines with async/await syntax",
      "asyncio documentation",
      "Trio library as asyncio alternative"
    ]
  }
}
```

## Output: Markdown

```markdown
# Video Analysis: General

## Video Information

**URL:** https://youtu.be/example_python_talk
**Title:** Async Python Made Simple
**Author:** PyCon 2025
**Duration:** 1845 seconds
**Analyzed:** 2025-11-01T12:00:00Z

---

## Summary

This talk demystifies Python's async/await syntax by building a simple async framework from scratch. The speaker explains event loops, coroutines, and common pitfalls, making async programming accessible to intermediate Python developers.

## Key Points

- Event loops are the heart of async programming - they schedule and run coroutines
- Async/await is syntactic sugar over generators and yield expressions
- Common mistake: mixing blocking I/O with async code breaks concurrency
- Use asyncio.gather() for concurrent task execution
- Async is best for I/O-bound tasks, not CPU-bound tasks

## Topics Covered

- Event Loops
- Coroutines and Generators
- Async/Await Syntax
- asyncio Library
- Concurrency vs Parallelism
- Non-blocking I/O

## Insights

- Async doesn't make code faster - it makes waiting more efficient
- You can build a simple event loop in ~50 lines of Python
- The GIL still applies to async code - only one coroutine runs at a time
- Debugging async code requires special tools like asyncio debug mode

## Questions Answered

- When should I use async instead of threading?
- How do event loops actually work under the hood?
- Why can't I just await any function?
- What's the difference between concurrency and parallelism?

## References

- David Beazley's 'Build Your Own Async' talk
- PEP 492 - Coroutines with async/await syntax
- asyncio documentation
- Trio library as asyncio alternative

---

*Analysis generated by Hanx YouTube Researcher Skill*
```

## Use Cases

**Educational Content:**
- Conference talks
- Tutorial videos
- Interviews
- Product demos
- Research presentations

**When to Use:**
- You want broad understanding of video content
- You need to extract main ideas quickly
- You're building a knowledge base
- You want to identify follow-up questions

**Next Steps:**
- Review the analysis to understand main concepts
- Use references to dive deeper into topics
- Create tasks based on insights (e.g., "Learn about event loops")
- Store analysis in RAG system for future reference
