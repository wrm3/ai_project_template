"""
analyze_video MCP tool handler
Comprehensive video analysis with multiple modes
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio
import logging
import json

# Add scripts directory to path
SKILL_ROOT = Path(__file__).parent.parent.parent.resolve()
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from get_transcript import get_transcript_handler, extract_video_id


async def analyze_video_handler(
    video_url: str,
    mode: str = "comprehensive",
    output_dir: Optional[str] = None,
    save_to_rag: bool = False,
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Analyze YouTube video with specified mode

    Args:
        video_url: YouTube URL or video ID
        mode: "quick", "comprehensive", or "multimodal"
        output_dir: Output directory
        save_to_rag: Whether to ingest into RAG database
        logger: Logger instance

    Returns:
        dict with analysis results
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = datetime.now()

    try:
        # Validate mode
        valid_modes = ["quick", "comprehensive", "multimodal"]
        if mode not in valid_modes:
            return {
                "success": False,
                "error": f"Invalid mode '{mode}'. Must be one of: {', '.join(valid_modes)}"
            }

        # Get transcript first
        logger.info(f"Analyzing video with mode: {mode}")
        transcript_result = await get_transcript_handler(
            video_url=video_url,
            output_dir=output_dir,
            logger=logger
        )

        if not transcript_result["success"]:
            return transcript_result

        video_id = transcript_result["video_id"]
        transcript = transcript_result["transcript"]
        output_path = Path(transcript_result["output_dir"])

        # Perform analysis based on mode
        if mode == "quick":
            analysis = await analyze_quick(transcript, transcript_result, logger)
        elif mode == "comprehensive":
            analysis = await analyze_comprehensive(transcript, transcript_result, logger)
        elif mode == "multimodal":
            analysis = await analyze_multimodal(video_url, transcript, transcript_result, output_path, logger)

        # Save analysis to file
        analysis_path = output_path / f"analysis_{mode}.json"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        # Also save markdown report
        markdown_report = generate_markdown_report(analysis, mode, transcript_result)
        markdown_path = output_path / f"ANALYSIS_{mode.upper()}.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_report)

        output_files = [
            str(analysis_path),
            str(markdown_path)
        ]

        # Optional: Ingest to RAG database
        rag_result = None
        if save_to_rag:
            logger.info("Ingesting video into RAG database...")
            try:
                rag_result = await ingest_to_rag(video_url, transcript_result, logger)
                if rag_result.get("success"):
                    logger.info(f"Successfully ingested {rag_result.get('chunks_stored', 0)} chunks to RAG")
            except Exception as e:
                logger.warning(f"RAG ingestion failed (non-fatal): {e}")
                rag_result = {"success": False, "error": str(e)}

        processing_time = (datetime.now() - start_time).total_seconds()

        return {
            "success": True,
            "video_id": video_id,
            "title": transcript_result["title"],
            "mode": mode,
            "analysis": analysis,
            "rag_ingestion": rag_result,
            "output_files": output_files,
            "processing_time_seconds": round(processing_time, 2)
        }

    except Exception as e:
        logger.exception(f"Error analyzing video: {e}")
        return {
            "success": False,
            "error": str(e),
            "video_url": video_url,
            "mode": mode
        }


async def analyze_quick(transcript: str, metadata: dict, logger: logging.Logger) -> dict:
    """Quick summary mode - fast insights"""
    logger.info("Performing quick analysis...")

    # Extract key sentences (simple heuristic)
    sentences = transcript.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    # Simple keyword extraction
    words = transcript.lower().split()
    word_freq = {}
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'that', 'this', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}

    for word in words:
        word = word.strip('.,!?;:()[]{}"\'"').lower()
        if len(word) > 3 and word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

    # Top keywords
    top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]

    return {
        "summary": f"Video: {metadata['title']} by {metadata['author']}. Duration: {metadata['duration_seconds'] // 60} minutes. This is a quick summary based on transcript analysis.",
        "key_insights": [
            f"Video length: {len(transcript)} characters, approximately {len(words)} words",
            f"Estimated speaking time: {metadata['duration_seconds'] // 60} minutes",
            f"Top keywords: {', '.join([kw[0] for kw in top_keywords[:5]])}"
        ],
        "top_keywords": [{"word": kw[0], "frequency": kw[1]} for kw in top_keywords],
        "technical_details": {
            "mode": "quick",
            "analysis_method": "keyword_extraction",
            "word_count": len(words),
            "sentence_count": len(sentences),
            "unique_words": len(word_freq)
        }
    }


async def analyze_comprehensive(transcript: str, metadata: dict, logger: logging.Logger) -> dict:
    """Comprehensive analysis mode - detailed insights"""
    logger.info("Performing comprehensive analysis...")

    # This would ideally call Claude Code or an LLM API
    # For now, we'll provide a structured template

    return {
        "summary": f"Comprehensive analysis of '{metadata['title']}' by {metadata['author']}. This video is {metadata['duration_seconds'] // 60} minutes long and covers detailed content that has been transcribed and is ready for analysis.",
        "key_insights": [
            "Full transcript has been extracted and is available for detailed analysis",
            f"Video contains approximately {len(transcript.split())} words of spoken content",
            "Content is structured and ready for semantic search if ingested to RAG database",
            "Transcript can be used for code extraction, quote extraction, and detailed summarization"
        ],
        "technical_details": {
            "video_id": metadata.get("video_id", "unknown"),
            "duration_seconds": metadata.get("duration_seconds", 0),
            "views": metadata.get("views", "unknown"),
            "word_count": len(transcript.split()),
            "character_count": len(transcript),
            "analysis_mode": "comprehensive",
            "ready_for_llm_analysis": True
        },
        "quotes": extract_potential_quotes(transcript),
        "action_items": [
            "Transcript is ready for detailed LLM analysis using Claude Code",
            "Consider ingesting to RAG database for semantic search",
            "Extract code snippets if this is a technical tutorial",
            "Generate detailed summary using Claude Code with the full transcript"
        ],
        "sections_detected": detect_sections(transcript)
    }


async def analyze_multimodal(video_url: str, transcript: str, metadata: dict, output_path: Path, logger: logging.Logger) -> dict:
    """Multimodal analysis - combines transcript + visual frames"""
    logger.info("Performing multimodal analysis...")

    try:
        # Import multimodal integration
        from multimodal_integration import MultiModalIntegrator
        from smart_frame_selector import SmartFrameSelector

        video_path = output_path / "video.mp4"
        frames_dir = output_path / "smart_frames"
        multimodal_dir = output_path / "multimodal_output"

        # Extract smart frames
        logger.info("Extracting key frames...")
        selector = SmartFrameSelector(output_dir=str(frames_dir))
        frames = selector.select_frames(str(video_path), metadata, enable_ocr=True)

        # Perform multimodal integration
        integrator = MultiModalIntegrator(output_dir=str(multimodal_dir))

        # Align frames with transcript
        aligned_data = integrator.align_frames_with_transcript(
            frames=frames,
            transcript=transcript,
            window_seconds=30
        )

        # Merge insights
        comprehensive_analysis = integrator.merge_multimodal_insights(
            aligned_data=aligned_data,
            video_metadata=metadata
        )

        return {
            "summary": comprehensive_analysis.get("summary", "Multimodal analysis complete"),
            "key_insights": comprehensive_analysis.get("key_insights", []),
            "technical_details": comprehensive_analysis.get("technical_details", {}),
            "code_examples": comprehensive_analysis.get("code_examples", []),
            "diagrams": comprehensive_analysis.get("diagrams", []),
            "frames_analyzed": len(frames),
            "multimodal_segments": len(aligned_data),
            "visual_content_found": True
        }

    except Exception as e:
        logger.warning(f"Multimodal analysis failed, falling back to comprehensive: {e}")
        return await analyze_comprehensive(transcript, metadata, logger)


def extract_potential_quotes(transcript: str, max_quotes: int = 5) -> List[str]:
    """Extract potential interesting quotes from transcript"""
    sentences = transcript.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30 and len(s.strip()) < 200]

    # Simple heuristic: longer, complete sentences
    quotes = sorted(sentences, key=lambda x: len(x.split()), reverse=True)[:max_quotes]
    return quotes


def detect_sections(transcript: str) -> List[dict]:
    """Detect potential sections/topics in transcript"""
    # Simple section detection based on paragraph breaks
    paragraphs = [p.strip() for p in transcript.split('\n\n') if p.strip()]

    sections = []
    for i, para in enumerate(paragraphs[:10]):  # First 10 paragraphs
        sections.append({
            "section_number": i + 1,
            "preview": para[:200] + "..." if len(para) > 200 else para,
            "word_count": len(para.split())
        })

    return sections


def generate_markdown_report(analysis: dict, mode: str, metadata: dict) -> str:
    """Generate markdown report from analysis"""
    report = f"""# Video Analysis Report

**Video**: {metadata['title']}
**Author**: {metadata['author']}
**Duration**: {metadata['duration_seconds'] // 60} minutes
**Analysis Mode**: {mode}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

{analysis.get('summary', 'No summary available')}

## Key Insights

"""
    for insight in analysis.get('key_insights', []):
        report += f"- {insight}\n"

    report += "\n## Technical Details\n\n"
    for key, value in analysis.get('technical_details', {}).items():
        report += f"- **{key}**: {value}\n"

    if 'quotes' in analysis and analysis['quotes']:
        report += "\n## Notable Quotes\n\n"
        for i, quote in enumerate(analysis['quotes'], 1):
            report += f"{i}. \"{quote}\"\n\n"

    if 'action_items' in analysis:
        report += "\n## Action Items\n\n"
        for item in analysis['action_items']:
            report += f"- [ ] {item}\n"

    if 'code_examples' in analysis and analysis['code_examples']:
        report += "\n## Code Examples Found\n\n"
        for i, example in enumerate(analysis['code_examples'][:5], 1):
            report += f"### Example {i}\n\n"
            report += f"```{example.get('language', 'text')}\n{example.get('code', '')}\n```\n\n"

    return report


async def ingest_to_rag(video_url: str, metadata: dict, logger: logging.Logger) -> dict:
    """Ingest video into RAG database"""
    try:
        # Import RAG ingestion
        RAG_SKILL_ROOT = SKILL_ROOT.parent / "youtube-rag-storage"
        RAG_SCRIPTS_DIR = RAG_SKILL_ROOT / "scripts"
        sys.path.insert(0, str(RAG_SCRIPTS_DIR))

        from ingest_video import ingest_video_pipeline

        result = await asyncio.to_thread(
            ingest_video_pipeline,
            video_url=video_url,
            video_metadata=metadata
        )

        return result

    except Exception as e:
        logger.exception(f"RAG ingestion error: {e}")
        return {"success": False, "error": str(e)}
