# YouTube Intel MCP Server - Usage Examples

Real-world examples of using the YouTube Intel MCP server with Claude Desktop.

## Example 1: Basic Transcript Extraction

**User Request**:
```
Get the transcript for this FastAPI tutorial: https://www.youtube.com/watch?v=0sOvCWFmrtA
```

**Claude Desktop Response**:
```
I'll get the transcript for that FastAPI tutorial video.

[Uses youtube-intel.get_transcript]

The video "FastAPI Tutorial - Building RESTful APIs with Python" by Tech With Tim
is 1 hour and 32 minutes long. I've successfully downloaded and transcribed it.

Key details:
- Duration: 92 minutes
- Word count: 13,248 words
- Transcript saved to: ./output/0sOvCWFmrtA/transcript.txt

The transcript is now available. Would you like me to:
1. Summarize the key topics covered?
2. Extract code examples?
3. Create a detailed analysis?
```

## Example 2: Comprehensive Video Analysis

**User Request**:
```
Analyze this video in comprehensive mode and save it to the RAG database:
https://www.youtube.com/watch?v=7LncLYIbcss
```

**Claude Desktop Response**:
```
I'll perform a comprehensive analysis of "Building Production RAG Systems"
and ingest it into the knowledge base.

[Uses youtube-intel.analyze_video with mode="comprehensive" and save_to_rag=true]

Analysis complete! Here's what I found:

## Summary
This 45-minute tutorial by AI Jason covers building production-ready RAG systems
using vector databases, embeddings, and LLMs.

## Key Insights
1. RAG systems require three core components: vector database, embedding model,
   and chunking strategy
2. OpenAI's text-embedding-3-small provides best cost/performance ratio
3. Chunk size of 400-1000 tokens preserves context while enabling efficient search
4. Production systems need caching, error handling, and monitoring

## Technical Details
- Technologies: Supabase (pgvector), OpenAI embeddings, LangChain
- Performance: <100ms search latency for 100K chunks
- Cost: ~$0.002 per video for embeddings
- Best practices: Use semantic chunking, not fixed-size chunks

## Notable Quotes
1. "Vector databases are just PostgreSQL with the pgvector extension"
2. "Embedding quality matters more than database choice"
3. "Always chunk documents semantically, not arbitrarily"

## RAG Ingestion
✅ Successfully ingested 87 chunks into the knowledge base
- Processing time: 12.3 seconds
- Cost: $0.0017 for embeddings
- Now searchable via semantic search

The video is now in your knowledge base and can be searched!
```

## Example 3: Semantic Search Across Videos

**User Request**:
```
Search my video knowledge base for information about implementing
caching in FastAPI applications
```

**Claude Desktop Response**:
```
I'll search across all ingested videos for FastAPI caching implementations.

[Uses youtube-intel.search_videos with query="caching in FastAPI applications"]

Found 8 relevant segments across 3 videos:

### Top Results

1. **"FastAPI Advanced Patterns" by ArjanCodes** (similarity: 0.91)
   Timestamp: 23:45
   "When implementing caching in FastAPI, you have several options. Redis is
   the most popular choice for production applications. You can use the
   @cache decorator from fastapi-cache2 library to automatically cache
   responses based on request parameters..."

2. **"Production FastAPI Tutorial" by Tech With Tim** (similarity: 0.87)
   Timestamp: 41:20
   "For caching FastAPI endpoints, I recommend using Redis with TTL-based
   expiration. Here's a complete example showing how to cache database queries
   and API responses..."

3. **"FastAPI Performance Optimization" by Patrick Loeber** (similarity: 0.84)
   Timestamp: 15:30
   "The caching strategy you choose depends on your use case. For read-heavy
   applications, implement Redis caching with appropriate TTLs. For
   write-heavy apps, consider write-through caching..."

[5 more results...]

Would you like me to:
1. Extract the code examples from these segments?
2. Compare the different caching approaches?
3. Generate a summary document?
```

## Example 4: Video Comparison

**User Request**:
```
Compare these three Python async tutorials and tell me which one is best
for intermediate developers:

1. https://www.youtube.com/watch?v=ftmdDlwMwwQ
2. https://www.youtube.com/watch?v=2IW-ZEui4h4
3. https://www.youtube.com/watch?v=t5Bo1Je9EmE
```

**Claude Desktop Response**:
```
I'll analyze and compare all three Python async tutorials for you.

[Uses youtube-intel.compare_videos with aspects=["complexity", "completeness", "approach"]]

## Video Comparison: Python Async Tutorials

### Overview
- **Video 1**: "Python Async/Await" by Tech With Tim (25 min)
- **Video 2**: "Asyncio Complete Guide" by ArjanCodes (48 min)
- **Video 3**: "Async Python Tutorial" by Corey Schafer (32 min)

### Comparison Table

| Aspect | Video 1 (Tim) | Video 2 (Arjan) | Video 3 (Corey) |
|--------|--------------|-----------------|-----------------|
| **Complexity** | Medium density (120 wpm) - moderate pace | High density (145 wpm) - fast-paced | Medium density (115 wpm) - detailed pace |
| **Completeness** | Moderate coverage (25min, 3,200 words) | Comprehensive (48min, 7,100 words) | Moderate coverage (32min, 3,800 words) |
| **Approach** | Practical approach, tutorial focusing on examples | Advanced approach with theoretical foundations | Practical approach, beginner-friendly examples |
| **Tools** | asyncio, aiohttp, FastAPI | asyncio, aiofiles, httpx, anyio | asyncio, aiohttp |
| **Code Quality** | Code-heavy (45 code keywords) | Code-heavy (78 code keywords) | Moderate code (38 code keywords) |

### Recommendation for Intermediate Developers

**Best Choice: Video 2 - "Asyncio Complete Guide" by ArjanCodes**

**Reasons:**
1. ✅ Most comprehensive coverage (48 minutes, 7,100 words)
2. ✅ Advanced concepts explained clearly (event loops, executors, context managers)
3. ✅ Production-ready patterns (error handling, testing, best practices)
4. ✅ Modern tools (httpx, anyio, aiofiles)
5. ✅ Real-world examples (API clients, file I/O, concurrent processing)

**Why not the others:**
- **Video 1** (Tim): Good for beginners but lacks advanced patterns
- **Video 3** (Corey): Excellent fundamentals but less modern tooling

**Learning Path:**
For intermediate developers, I recommend:
1. Start with Video 2 (ArjanCodes) - 48 min comprehensive guide
2. Reference Video 3 (Corey) for clarifying fundamentals - 32 min
3. Use Video 1 (Tim) for quick FastAPI integration examples - 25 min

Total learning time: ~1h 45min for complete async mastery
```

## Example 5: Code Extraction

**User Request**:
```
Extract all Python code from this FastAPI tutorial and save it to files
https://www.youtube.com/watch?v=0sOvCWFmrtA
```

**Claude Desktop Response**:
```
I'll extract all Python code snippets from the FastAPI tutorial.

[Uses youtube-intel.extract_code with language="python" and include_frames=true]

Code extraction complete! Found 23 Python code snippets.

## Summary

### Extracted Code
- **Total snippets**: 23
- **Languages**: Python (23)
- **Total lines of code**: 487 lines
- **Sources**:
  - Transcript: 18 snippets
  - Video frames (OCR): 5 snippets

### Code Breakdown
- ✅ Import statements: 23 snippets
- ✅ Function definitions: 18 snippets
- ✅ Class definitions: 4 snippets

### Sample Snippets

**Snippet 1** (Main FastAPI app setup):
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

**Snippet 5** (Database connection):
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
Base = declarative_base()
```

**Snippet 12** (CRUD operations):
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

[20 more snippets...]

### Saved Files
All code has been saved to: `./output/0sOvCWFmrtA/code/`

- snippet_001.py - Main app setup
- snippet_002.py - Models definition
- snippet_003.py - Database connection
- snippet_004.py - CRUD operations
- snippet_005.py - Authentication
- ... (23 total files)

### Code Manifest
Complete catalog: `./output/0sOvCWFmrtA/code/code_manifest.json`

Would you like me to:
1. Organize the code into a complete working project?
2. Add documentation and comments?
3. Create a requirements.txt from the imports?
```

## Example 6: Research Workflow

**User Request**:
```
I want to learn about building production-grade RAG systems. Find relevant
videos, analyze them, and create a learning roadmap.
```

**Claude Desktop Response**:
```
I'll help you build a comprehensive learning roadmap for production RAG systems.
Let me search for relevant content in the knowledge base.

[Uses youtube-intel.search_videos multiple times with different queries]

Step 1: Searching for RAG system fundamentals...
Step 2: Searching for vector database content...
Step 3: Searching for production best practices...

## RAG Systems Learning Roadmap

Based on analysis of 12 relevant videos in your knowledge base:

### Phase 1: Fundamentals (3-4 hours)
**Goal**: Understand core RAG concepts

1. **"Building Production RAG Systems"** by AI Jason (45 min)
   - Topics: RAG architecture, embeddings, vector databases
   - Why: Best comprehensive introduction
   - [Analyzed and stored in knowledge base]

2. **"Vector Databases Explained"** by Coding with Cole (28 min)
   - Topics: Similarity search, HNSW, IVFFlat indexes
   - Why: Deep dive into vector DB internals
   - Code: 15 Python examples extracted

3. **"OpenAI Embeddings Guide"** by TechLead (35 min)
   - Topics: text-embedding-3-small, chunking strategies
   - Why: Practical embedding implementation
   - Key quote: "Chunk size affects semantic coherence"

### Phase 2: Implementation (4-5 hours)
**Goal**: Build working RAG system

4. **"FastAPI + Supabase RAG"** by Tech With Tim (1h 12min)
   - Build complete RAG API
   - Full code extracted: 487 lines

5. **"LangChain RAG Tutorial"** by Sam Witteveen (52 min)
   - Production patterns
   - Error handling, caching

### Phase 3: Production Deployment (2-3 hours)

6. **"RAG System Optimization"** by ArjanCodes (38 min)
7. **"Monitoring RAG in Production"** by AI Engineer (25 min)

### Learning Path Summary

**Total Time**: 9-12 hours
**Prerequisites**: Python, basic SQL, API knowledge
**Technologies**: FastAPI, Supabase, OpenAI, LangChain

**Code Resources**:
- 89 Python code snippets extracted and organized
- Complete project templates from videos 4 & 5
- Production deployment scripts from videos 6 & 7

**Next Steps**:
1. Start with video 1 (45 min)
2. Extract and run code from video 4
3. Build your own system using learned patterns

Would you like me to:
1. Extract all code and organize into a starter project?
2. Create detailed notes for each video?
3. Compare different approaches mentioned across videos?
```

## Example 7: Multi-Modal Analysis

**User Request**:
```
Analyze this coding tutorial using multi-modal mode to extract both spoken
content and code from screenshots:
https://www.youtube.com/watch?v=example_coding_video
```

**Claude Desktop Response**:
```
I'll perform a complete multi-modal analysis, combining transcript analysis
with visual frame extraction.

[Uses youtube-intel.analyze_video with mode="multimodal"]

Processing:
1. Downloading and transcribing video... ✓
2. Extracting key frames with code screenshots... ✓
3. Running OCR on code frames... ✓
4. Aligning visual content with transcript... ✓
5. Generating comprehensive analysis... ✓

## Multi-Modal Analysis Complete

### Video Overview
- **Title**: "Building a REST API with FastAPI"
- **Duration**: 67 minutes
- **Content**: 52% spoken content, 48% visual code demos

### Transcript Analysis
- Total words: 9,234
- Key topics: FastAPI, Pydantic, SQLAlchemy, async/await
- Speaking pace: 138 words/min (well-paced)

### Visual Content Analysis
- **Total frames analyzed**: 47 frames
- **Code screenshots**: 32 frames
- **Diagram/architecture**: 8 frames
- **Terminal output**: 7 frames

### Extracted Code Examples

Found 28 code examples combining transcript + visual content:

**Example 1** (Timestamp: 5:30)
Source: Video frame + transcript context
```python
# The instructor explains: "Here's the basic FastAPI setup"
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Example 8** (Timestamp: 23:15)
Source: Code screenshot + OCR
```python
# Database models - shown on screen
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

[26 more examples...]

### Multi-Modal Insights

**Spoken Content**:
- Best practices: "Always validate input with Pydantic"
- Performance tips: "Use async for I/O-bound operations"
- Common mistakes: "Don't forget to close database connections"

**Visual Content**:
- Complete project structure shown at 15:20
- Testing workflow demonstrated at 42:30
- Deployment configuration at 58:45

### Synchronized Timeline

| Time | Spoken Content | Visual Content |
|------|----------------|----------------|
| 0:00-5:30 | Introduction & setup | Terminal commands |
| 5:30-15:20 | Basic routing | Code: route definitions |
| 15:20-28:45 | Database integration | Code: SQLAlchemy models |
| 28:45-42:30 | CRUD operations | Code: database queries |
| 42:30-58:45 | Testing | Code: pytest examples |
| 58:45-67:00 | Deployment | Docker & config files |

### Output Files
- Complete analysis: `./output/VIDEO_ID/multimodal_output/MULTIMODAL_ANALYSIS.md`
- All code extracted: `./output/VIDEO_ID/code/` (28 files)
- Frame screenshots: `./output/VIDEO_ID/smart_frames/` (47 images)
- Synchronized data: `./output/VIDEO_ID/multimodal_output/multimodal_data.json`

This multi-modal analysis captured content that transcript-only would have missed,
including visual diagrams, code formatting, and terminal demonstrations.
```

## Example 8: Batch Processing with SubAgent

**User Request**:
```
I have a playlist of 5 Python videos. Analyze all of them, extract the code,
and create a comparison of the teaching approaches.
```

**Claude Desktop Response**:
```
I'll process all 5 videos in the playlist and provide a comprehensive analysis.

[Uses youtube-intel tools in sequence for each video]

Processing playlist (5 videos)...

Video 1/5: "Python Basics" - Transcribing... ✓ (2.3 min)
Video 2/5: "Advanced Python" - Transcribing... ✓ (2.8 min)
Video 3/5: "Python Design Patterns" - Transcribing... ✓ (3.1 min)
Video 4/5: "FastAPI Tutorial" - Transcribing... ✓ (4.2 min)
Video 5/5: "Python Testing" - Transcribing... ✓ (2.5 min)

All videos ingested to knowledge base ✓

Extracting code from all videos...
- Total code snippets: 127
- Total lines of code: 2,847
- Languages: Python (127)

## Playlist Analysis

### Video Comparison

| Video | Duration | Complexity | Code Examples | Approach | Best For |
|-------|----------|------------|---------------|----------|----------|
| Python Basics | 25 min | Beginner | 15 | Tutorial | Newcomers |
| Advanced Python | 42 min | Advanced | 28 | Deep-dive | Experienced |
| Design Patterns | 38 min | Intermediate | 32 | Practical | Architects |
| FastAPI Tutorial | 67 min | Intermediate | 41 | Project-based | Web devs |
| Python Testing | 31 min | Intermediate | 11 | Hands-on | QA/DevOps |

### Teaching Approach Analysis

**Most Beginner-Friendly**: Video 1 (Python Basics)
- Clear explanations, simple examples
- Builds concepts incrementally
- Minimal prerequisites

**Best for Intermediate**: Video 4 (FastAPI Tutorial)
- Real-world project
- Production best practices
- Complete code examples

**Most Comprehensive**: Video 2 (Advanced Python)
- Covers advanced topics deeply
- Performance optimization
- Memory management

### Extracted Code Summary

All 127 code snippets organized by topic:
- `/code/basics/` - 15 examples from Video 1
- `/code/advanced/` - 28 examples from Video 2
- `/code/patterns/` - 32 examples from Video 3
- `/code/fastapi/` - 41 examples from Video 4
- `/code/testing/` - 11 examples from Video 5

### Recommended Learning Path

For Python developers:
1. Start: Video 1 (Basics) - 25 min
2. Then: Video 4 (FastAPI) - 67 min [hands-on practice]
3. Next: Video 3 (Patterns) - 38 min
4. Advanced: Video 2 - 42 min
5. Polish: Video 5 (Testing) - 31 min

Total: ~3.4 hours for complete Python mastery path

All videos are now searchable in your knowledge base!
```

---

These examples demonstrate the power and flexibility of the YouTube Intel MCP server
for learning, research, and knowledge management workflows.
