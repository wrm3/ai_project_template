# YouTube Video Analysis - Examples

This directory contains comprehensive examples demonstrating all features of the YouTube Multi-Modal RAG Intelligence Platform.

## 📚 Example Index

### 1. Basic Analysis Examples

#### [`tutorial_analysis_example.json`](tutorial_analysis_example.json)
**Use Case**: Framework/tool tutorial analysis

- **Video Type**: Technical tutorial (React framework)
- **Features Demonstrated**:
  - Transcript extraction
  - Framework-specific insights
  - Installation steps
  - Key concepts extraction
  - Code examples identification
- **Processing Time**: ~90 seconds
- **Cost**: ~$0.02 (Claude API)

**When to use**: Analyzing technical tutorials, framework guides, or tool demonstrations

---

#### [`trading_strategy_analysis.json`](trading_strategy_analysis.json)
**Use Case**: Trading/finance video analysis

- **Video Type**: Trading strategy explanation
- **Features Demonstrated**:
  - Strategy extraction (RSI Divergence)
  - Entry/exit criteria
  - Risk management rules
  - Timeframe identification
  - Backtest results
- **Processing Time**: ~80 seconds
- **Cost**: ~$0.02

**When to use**: Extracting trading strategies, financial analysis, market commentary

---

### 2. Multi-Modal Analysis Examples

#### [`multimodal_output_example.json`](multimodal_output_example.json)
**Use Case**: Combined visual + audio analysis

- **Video Type**: Technical presentation with code
- **Features Demonstrated**:
  - Frame extraction + transcript alignment
  - Visual-audio synchronization
  - Code detection in frames
  - Diagram identification
  - Gap analysis (visual not explained, explained not shown)
  - Alignment quality scoring
- **Processing Time**: ~3-4 minutes
- **Output Formats**: JSON, Markdown, HTML timeline, comparison table

**When to use**: Analyzing videos with significant visual content (code demos, architecture diagrams, presentations)

---

#### [`comparison_table_example.md`](comparison_table_example.md)
**Use Case**: Visual vs Audio content comparison

- **Format**: Markdown table
- **Features Demonstrated**:
  - Side-by-side visual and audio content
  - Alignment quality indicators
  - Segment type classification
  - Timestamp references

**When to use**: Quick reference for what's shown vs what's explained

---

### 3. Workflow Examples

#### [`rag_workflow_example.py`](rag_workflow_example.py)
**Use Case**: Complete RAG ingestion pipeline

- **Features Demonstrated**:
  - Video download and transcription
  - Multi-modal analysis
  - Embedding generation (for vector database)
  - Metadata extraction
  - Storage in vector database
  - Retrieval testing
- **Vector Databases Supported**: Supabase pgvector, Chroma, Pinecone, Weaviate

**When to use**: Building a searchable knowledge base from YouTube videos

---

#### [`batch_processing_example.py`](batch_processing_example.py)
**Use Case**: Processing multiple videos (playlists/channels)

- **Features Demonstrated**:
  - Playlist processing
  - Channel video processing
  - Progress tracking with tqdm
  - Error recovery
  - Batch statistics
  - Results aggregation
- **Processing Modes**: metadata-only, transcript-only, full RAG

**When to use**: Processing multiple videos from a playlist or channel

---

### 4. Working Workflows

#### [`sample_workflow.md`](sample_workflow.md)
**Use Case**: Step-by-step analysis walkthrough

- **Format**: Tutorial with code snippets
- **Features Demonstrated**:
  - Complete analysis pipeline
  - Time estimates for each step
  - Output structure examples
  - Next steps (task generation, skill templates)

**When to use**: Learning the complete workflow from start to finish

---

## 🚀 Quick Start

### Basic Transcript Analysis
```bash
python analyze_video.py https://www.youtube.com/watch?v=VIDEO_ID
```

### Multi-Modal Analysis (with frames)
```bash
python analyze_video.py https://www.youtube.com/watch?v=VIDEO_ID \
    --multimodal --smart-frames
```

### Batch Processing (playlist)
```bash
python batch_processor.py \
    --playlist "https://youtube.com/playlist?list=..." \
    --max-videos 10
```

### RAG Ingestion
```python
from rag_workflow_example import ingest_video_to_rag

result = ingest_video_to_rag(
    video_url="https://www.youtube.com/watch?v=VIDEO_ID",
    vector_db="supabase",  # or "chroma", "pinecone", etc.
    collection_name="youtube_knowledge"
)
```

---

## 📊 Feature Comparison

| Feature | Basic | Multi-Modal | RAG | Batch |
|---------|-------|-------------|-----|-------|
| Transcript | ✅ | ✅ | ✅ | ✅ |
| Frame Extraction | ❌ | ✅ | ✅ | ✅ |
| Smart Frame Selection | ❌ | ✅ | ✅ | ✅ |
| Visual Analysis | ❌ | ✅ | ✅ | ✅ |
| Alignment Analysis | ❌ | ✅ | ✅ | ✅ |
| Gap Detection | ❌ | ✅ | ✅ | ✅ |
| Embeddings | ❌ | ❌ | ✅ | ✅ |
| Vector DB Storage | ❌ | ❌ | ✅ | ✅ |
| Progress Bars | ✅ | ✅ | ✅ | ✅ |
| Error Recovery | ✅ | ✅ | ✅ | ✅ |
| Caching | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 Use Case Guide

### "I want to analyze a single video"
→ Use [`tutorial_analysis_example.json`](tutorial_analysis_example.json) or [`trading_strategy_analysis.json`](trading_strategy_analysis.json) as template

### "I want to extract code from a tutorial"
→ Use [`multimodal_output_example.json`](multimodal_output_example.json) with `--multimodal --smart-frames`

### "I want to build a searchable knowledge base"
→ Use [`rag_workflow_example.py`](rag_workflow_example.py) with vector database

### "I want to process an entire playlist"
→ Use [`batch_processing_example.py`](batch_processing_example.py)

### "I want to see what's shown vs what's explained"
→ Use [`comparison_table_example.md`](comparison_table_example.md) format

---

## 💡 Pro Tips

1. **Choose the right model**: `base` for general use, `small` for important content, `tiny` for testing
2. **Use smart frame selection**: Reduces frames by 70-80% while maintaining quality
3. **Enable caching**: Reuse transcripts and embeddings across runs
4. **Batch with caution**: Start with a few videos to test settings
5. **Review gaps**: Check alignment analysis to identify missing explanations

---

## 📝 Output Formats

### JSON (structured data)
- Complete analysis with all metadata
- Machine-readable format
- Best for: API integration, data processing

### Markdown (human-readable)
- Executive summary + detailed segments
- Easy to read and share
- Best for: Documentation, sharing insights

### HTML (interactive)
- Timeline visualization with filtering
- Click to navigate segments
- Best for: Presentations, interactive exploration

### Comparison Table (quick reference)
- Side-by-side visual vs audio
- Alignment quality indicators
- Best for: Quick scanning, gap identification

---

## 🔧 Customization

All examples can be customized by modifying:

- **Whisper model**: `tiny`, `base`, `small`, `medium`, `large`
- **Frame interval**: Default 30 seconds (adjustable)
- **Alignment window**: Default ±30 seconds (adjustable)
- **Smart selection thresholds**: Scene detection, code detection
- **Batch processing**: Concurrent workers, error handling

See individual example files for customization options.

---

## 📚 Related Documentation

- [SKILL.md](../SKILL.md) - Main skill documentation
- [REFACTOR_NOTES.md](../REFACTOR_NOTES.md) - Architecture and design decisions
- [reference/video_types.md](../reference/video_types.md) - Supported video types
- [reference/prompt_templates.md](../reference/prompt_templates.md) - Analysis prompts

---

**Last Updated**: 2025-11-01
**Version**: 2.0 (Multi-Modal RAG Platform)
