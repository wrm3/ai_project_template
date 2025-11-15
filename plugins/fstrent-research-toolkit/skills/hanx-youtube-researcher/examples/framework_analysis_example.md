# Example: Framework/Tool Analysis

## Scenario

You discovered a comprehensive FastAPI tutorial and want to extract installation steps, features, and usage patterns to create a setup guide for your team.

## Command

```bash
python specialized_analyzer.py \
    --url https://youtu.be/example_fastapi_tutorial \
    --type framework \
    --output ./framework_docs
```

## Workflow

### Step 1: Transcript Extraction

```
================================================================================
STEP 1: Get Video Transcript
================================================================================

Running youtube-video-analysis skill...
Downloading video: https://youtu.be/example_fastapi_tutorial
Extracting audio...
Transcribing with Whisper (base model)...

[OK] Transcript loaded: 15,234 characters
```

### Step 2: Framework Analysis

```
================================================================================
STEP 2: Query LLM for Analysis
================================================================================

Using LLM provider: openai
Applying framework/tool analysis prompt template...
Extracting: installation, features, usage, limitations, alternatives...

[OK] Received response: 2,567 characters
```

### Step 3: Save Results

```
================================================================================
STEP 3: Save Results
================================================================================

[OK] Saved JSON: ./framework_docs/framework_analysis_20251101_160000.json
[OK] Saved Markdown: ./framework_docs/framework_analysis_20251101_160000.md

Results saved to: ./framework_docs
```

## Output: JSON

```json
{
  "video_url": "https://youtu.be/example_fastapi_tutorial",
  "analysis_type": "framework",
  "timestamp": "2025-11-01T16:00:00Z",
  "metadata": {
    "title": "FastAPI Complete Guide - Build Production APIs",
    "duration": 2341,
    "author": "Tech With Tim"
  },
  "analysis": {
    "tool_name": "FastAPI",
    "purpose": "Modern, high-performance Python web framework for building APIs with automatic interactive documentation, type hints validation, and async support out of the box.",
    "target_users": [
      "Python developers building REST APIs",
      "Backend engineers migrating from Flask/Django",
      "Teams needing automatic API documentation",
      "Developers building microservices",
      "Projects requiring high performance (async I/O)"
    ],
    "key_features": [
      "Automatic interactive API documentation (Swagger UI and ReDoc)",
      "Type hints validation using Pydantic models",
      "Async/await support for high concurrency",
      "Dependency injection system",
      "OAuth2 and JWT authentication built-in",
      "WebSocket support",
      "Background tasks",
      "CORS middleware included",
      "SQL database integration (SQLAlchemy)",
      "Automatic request/response validation"
    ],
    "installation": [
      "Install FastAPI: pip install fastapi",
      "Install ASGI server: pip install uvicorn[standard]",
      "Optional: pip install python-multipart (for form data)",
      "Optional: pip install pydantic[email] (for email validation)",
      "For databases: pip install sqlalchemy databases",
      "For testing: pip install pytest httpx"
    ],
    "basic_usage": [
      "Import FastAPI: from fastapi import FastAPI",
      "Create app instance: app = FastAPI()",
      "Define route with decorator: @app.get('/')",
      "Add request/response models with Pydantic",
      "Run with uvicorn: uvicorn main:app --reload",
      "Access docs at: http://localhost:8000/docs",
      "Use path parameters: @app.get('/items/{item_id}')",
      "Query parameters automatically parsed from function args",
      "Request body via Pydantic models",
      "Return Python dicts - automatically converted to JSON"
    ],
    "advanced_features": [
      "Dependency injection for database sessions, auth, etc.",
      "Background tasks with BackgroundTasks",
      "Custom middleware for logging, monitoring",
      "WebSocket endpoints for real-time communication",
      "File uploads and downloads",
      "Response models with custom schemas",
      "Error handling with HTTPException",
      "Database migrations with Alembic",
      "Testing with TestClient",
      "Deployment with Docker and Kubernetes"
    ],
    "limitations": [
      "Relatively new (2018) - smaller ecosystem than Django/Flask",
      "Learning curve for developers unfamiliar with type hints",
      "Async programming paradigm can be challenging",
      "Limited built-in admin interface (unlike Django)",
      "Fewer third-party packages compared to Flask",
      "Documentation sometimes lacks real-world examples"
    ],
    "alternatives": [
      "Flask - Simpler but less features, no async, no auto docs",
      "Django REST Framework - Full-featured but slower, more opinionated",
      "Tornado - Good for async but lower-level, less convenient",
      "Starlette - FastAPI is built on Starlette (lower-level ASGI framework)",
      "aiohttp - Another async option but less batteries-included"
    ],
    "resources": [
      "Official docs: https://fastapi.tiangolo.com",
      "GitHub repo: https://github.com/tiangolo/fastapi",
      "Full course: 'FastAPI - The Complete Guide' (Udemy)",
      "Tutorial series: Real Python FastAPI guides",
      "Community: FastAPI Discord server",
      "Examples: fastapi/examples in GitHub repo"
    ]
  }
}
```

## Output: Markdown

See `framework_analysis_template.md` for formatted output.

## Use Cases

**Framework/Tool Videos:**
- Framework tutorials
- Library demonstrations
- Installation guides
- Tool comparisons
- Best practices videos

**When to Use:**
- You need setup instructions
- You're evaluating a new framework
- You want to document tool capabilities
- You're creating onboarding guides
- You need feature comparisons

**Next Steps:**

1. **Create Setup Guide:**
   ```markdown
   # FastAPI Setup Guide

   ## Installation
   [Extracted installation steps]

   ## Quick Start
   [Extracted basic usage]

   ## Features
   [Extracted key features]
   ```

2. **Build Example Project:**
   - Follow basic usage to create hello world
   - Implement key features one by one
   - Test advanced features
   - Document learnings

3. **Team Documentation:**
   - Add to internal knowledge base
   - Create code templates
   - Share alternatives comparison
   - Note limitations for architecture decisions

4. **Integration Planning:**
   - Assess if framework fits project needs
   - Check compatibility with existing stack
   - Review limitations vs requirements
   - Plan migration path if applicable

## Team Benefits

**For Developers:**
- Quick reference for installation and setup
- Feature list for capability planning
- Alternatives for informed decisions
- Resources for deeper learning

**For Architects:**
- Limitations for risk assessment
- Target users for team fit evaluation
- Advanced features for scalability planning
- Alternatives for technology comparisons

**For Project Managers:**
- Purpose and value proposition
- Learning curve assessment (limitations)
- Resource availability (documentation, community)
- Integration complexity (installation, basic usage)
