"""
extract_code MCP tool handler
Extract code snippets from video transcripts and frames
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import asyncio
import logging
import re
import json

# Add scripts directory to path
SKILL_ROOT = Path(__file__).parent.parent.parent.resolve()
SCRIPTS_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from get_transcript import get_transcript_handler, extract_video_id


async def extract_code_handler(
    video_url: str,
    language: Optional[str] = None,
    include_frames: bool = True,
    output_dir: Optional[str] = None,
    logger: Optional[logging.Logger] = None
) -> Dict[str, Any]:
    """
    Extract code snippets from video transcript and optionally frames

    Args:
        video_url: YouTube URL or video ID
        language: Filter by programming language
        include_frames: Whether to extract code from frames using OCR
        output_dir: Output directory
        logger: Logger instance

    Returns:
        dict with extracted code snippets
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    start_time = datetime.now()

    try:
        # Get transcript first
        logger.info(f"Extracting code from video: {video_url}")
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

        # Create code output directory
        code_dir = output_path / "code"
        code_dir.mkdir(exist_ok=True)

        # Extract code from transcript
        logger.info("Extracting code from transcript...")
        transcript_code = extract_code_from_transcript(transcript, language, logger)

        # Optionally extract from frames
        frame_code = []
        if include_frames:
            logger.info("Extracting code from video frames...")
            try:
                frame_code = await extract_code_from_frames(video_url, output_path, language, logger)
            except Exception as e:
                logger.warning(f"Frame code extraction failed (non-fatal): {e}")

        # Combine and deduplicate code snippets
        all_code = transcript_code + frame_code
        all_code = deduplicate_code(all_code, logger)

        # Filter by language if specified
        if language:
            all_code = [c for c in all_code if c["language"].lower() == language.lower()]

        # Save code snippets to files
        output_files = []
        for i, snippet in enumerate(all_code):
            lang = snippet["language"]
            ext = get_file_extension(lang)
            filename = code_dir / f"snippet_{i+1:03d}.{ext}"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(snippet["code"])

            output_files.append(str(filename))
            snippet["saved_to"] = str(filename)

        # Generate summary
        languages_found = list(set(c["language"] for c in all_code))
        snippets_by_source = {}
        for c in all_code:
            source = c["source"]
            snippets_by_source[source] = snippets_by_source.get(source, 0) + 1

        total_lines = sum(c["line_count"] for c in all_code)

        # Save JSON manifest
        manifest_path = code_dir / "code_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump({
                "video_id": video_id,
                "video_title": transcript_result["title"],
                "extracted_at": datetime.now().isoformat(),
                "code_snippets": all_code,
                "summary": {
                    "total_snippets": len(all_code),
                    "languages_found": languages_found,
                    "snippets_by_source": snippets_by_source,
                    "total_lines_of_code": total_lines
                }
            }, indent=2, ensure_ascii=False)

        output_files.append(str(manifest_path))

        processing_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"Code extraction complete: Found {len(all_code)} snippets in {len(languages_found)} languages")

        return {
            "success": True,
            "video_id": video_id,
            "video_title": transcript_result["title"],
            "code_snippets": all_code,
            "summary": {
                "total_snippets": len(all_code),
                "languages_found": languages_found,
                "snippets_by_source": snippets_by_source,
                "total_lines_of_code": total_lines
            },
            "output_files": output_files,
            "output_directory": str(code_dir),
            "processing_time_seconds": round(processing_time, 2)
        }

    except Exception as e:
        logger.exception(f"Error extracting code: {e}")
        return {
            "success": False,
            "error": str(e),
            "video_url": video_url
        }


def extract_code_from_transcript(transcript: str, language_filter: Optional[str], logger: logging.Logger) -> List[dict]:
    """Extract code snippets from transcript text"""
    logger.info("Analyzing transcript for code blocks...")

    code_snippets = []
    snippet_id = 0

    # Pattern 1: Code blocks with language tags (common in descriptions)
    # ```python ... ``` or ```javascript ... ```
    code_block_pattern = r'```(\w+)?\n(.*?)```'
    matches = re.finditer(code_block_pattern, transcript, re.DOTALL)

    for match in matches:
        lang = match.group(1) or "unknown"
        code = match.group(2).strip()

        if code:
            snippet_id += 1
            snippet = create_code_snippet(
                snippet_id=snippet_id,
                language=lang,
                code=code,
                source="transcript",
                context=extract_context(transcript, match.start(), match.end())
            )
            code_snippets.append(snippet)

    # Pattern 2: Indented code blocks (common in speech-to-text)
    # Multiple consecutive lines starting with 4+ spaces
    indented_pattern = r'(?:^|\n)((?:    .+\n)+)'
    matches = re.finditer(indented_pattern, transcript, re.MULTILINE)

    for match in matches:
        code = match.group(1).strip()

        # Filter out likely non-code content
        if len(code.split('\n')) > 2 and has_code_indicators(code):
            snippet_id += 1
            lang = detect_language(code)

            snippet = create_code_snippet(
                snippet_id=snippet_id,
                language=lang,
                code=code,
                source="transcript",
                context=extract_context(transcript, match.start(), match.end())
            )
            code_snippets.append(snippet)

    # Pattern 3: Inline code mentions (single-line code snippets)
    # Looking for code-like patterns: function names, variable assignments, etc.
    inline_patterns = [
        r'`([^`]+)`',  # Backtick code
        r'def\s+\w+\([^)]*\):',  # Python function
        r'function\s+\w+\([^)]*\)',  # JavaScript function
        r'const\s+\w+\s*=',  # JS const
        r'let\s+\w+\s*=',  # JS let
        r'var\s+\w+\s*=',  # JS var
    ]

    for pattern in inline_patterns:
        matches = re.finditer(pattern, transcript)
        for match in matches:
            code = match.group(0).strip()

            if len(code) > 10:  # Minimum length to be meaningful
                snippet_id += 1
                lang = detect_language(code)

                snippet = create_code_snippet(
                    snippet_id=snippet_id,
                    language=lang,
                    code=code,
                    source="transcript",
                    context=extract_context(transcript, match.start(), match.end())
                )
                code_snippets.append(snippet)

    logger.info(f"Found {len(code_snippets)} code snippets in transcript")
    return code_snippets


async def extract_code_from_frames(video_url: str, output_path: Path, language_filter: Optional[str], logger: logging.Logger) -> List[dict]:
    """Extract code from video frames using OCR"""
    logger.info("Extracting code from video frames...")

    try:
        # Import frame extraction and OCR
        from smart_frame_selector import SmartFrameSelector
        import pytesseract
        from PIL import Image

        video_path = output_path / "video.mp4"
        frames_dir = output_path / "code_frames"

        # Extract frames with code
        selector = SmartFrameSelector(output_dir=str(frames_dir))
        frames = selector.select_frames(
            str(video_path),
            {"video_id": extract_video_id(video_url)},
            enable_ocr=True
        )

        # Filter frames that likely contain code
        code_frames = [f for f in frames if f.get("has_code", False) or f.get("has_text", False)]

        logger.info(f"Found {len(code_frames)} frames with potential code")

        code_snippets = []
        snippet_id = 1000  # Start at 1000 to differentiate from transcript snippets

        for frame in code_frames:
            frame_path = Path(frame["frame_path"])
            timestamp = frame.get("timestamp_seconds", 0)

            # Perform OCR
            try:
                image = Image.open(frame_path)
                text = pytesseract.image_to_string(image)

                # Check if extracted text looks like code
                if has_code_indicators(text):
                    snippet_id += 1
                    lang = detect_language(text)

                    snippet = create_code_snippet(
                        snippet_id=snippet_id,
                        language=lang,
                        code=text.strip(),
                        source="frame",
                        timestamp=timestamp,
                        frame_number=frame.get("frame_number"),
                        context=f"Extracted from video frame at {timestamp}s"
                    )
                    code_snippets.append(snippet)

            except Exception as e:
                logger.warning(f"OCR failed for frame {frame_path}: {e}")
                continue

        logger.info(f"Extracted {len(code_snippets)} code snippets from frames")
        return code_snippets

    except ImportError as e:
        logger.warning(f"Frame extraction dependencies not available: {e}")
        return []


def create_code_snippet(snippet_id: int, language: str, code: str, source: str, **kwargs) -> dict:
    """Create standardized code snippet dict"""
    lines = code.split('\n')

    snippet = {
        "snippet_id": snippet_id,
        "language": language,
        "source": source,
        "code": code,
        "timestamp": kwargs.get("timestamp"),
        "frame_number": kwargs.get("frame_number"),
        "context": kwargs.get("context", ""),
        "line_count": len(lines),
        "has_imports": has_imports(code),
        "has_functions": has_functions(code),
        "has_classes": has_classes(code)
    }

    return snippet


def detect_language(code: str) -> str:
    """Detect programming language from code content"""
    code_lower = code.lower()

    # Python indicators
    if any(kw in code_lower for kw in ['def ', 'import ', 'from ', 'print(', 'self.', 'class ']):
        return "python"

    # JavaScript/TypeScript indicators
    if any(kw in code_lower for kw in ['function', 'const ', 'let ', 'var ', '=>', 'console.log']):
        return "javascript"

    # SQL indicators
    if any(kw in code_lower for kw in ['select ', 'from ', 'where ', 'insert ', 'update ', 'delete ']):
        return "sql"

    # HTML indicators
    if '<' in code and '>' in code and any(tag in code_lower for tag in ['<div', '<html', '<head', '<body', '<p>', '<a ']):
        return "html"

    # CSS indicators
    if '{' in code and '}' in code and ':' in code and ';' in code:
        if any(prop in code_lower for prop in ['color:', 'font-', 'margin:', 'padding:', 'background:']):
            return "css"

    # Bash/shell indicators
    if code.startswith('#!') or any(cmd in code_lower for cmd in ['#!/bin/bash', 'echo ', 'export ', 'cd ', 'ls ']):
        return "bash"

    # Default
    return "auto-detected"


def has_code_indicators(text: str) -> bool:
    """Check if text looks like code"""
    indicators = [
        r'\b(def|class|function|const|let|var|import|from|return|if|else|for|while)\b',
        r'[{}\[\]();]',
        r'=\s*[\'"]\w+[\'"]',
        r'->\s*\w+',
        r':\s*\w+',
        r'\b(public|private|protected|static|async|await)\b'
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in indicators)


def has_imports(code: str) -> bool:
    """Check if code has import statements"""
    return bool(re.search(r'\b(import|from|require|include|using)\b', code, re.IGNORECASE))


def has_functions(code: str) -> bool:
    """Check if code has function definitions"""
    return bool(re.search(r'\b(def|function|fn|func)\s+\w+', code, re.IGNORECASE))


def has_classes(code: str) -> bool:
    """Check if code has class definitions"""
    return bool(re.search(r'\bclass\s+\w+', code, re.IGNORECASE))


def extract_context(text: str, start: int, end: int, window: int = 100) -> str:
    """Extract context around code snippet"""
    context_start = max(0, start - window)
    context_end = min(len(text), end + window)

    context = text[context_start:context_end].strip()
    return context[:200] + "..." if len(context) > 200 else context


def deduplicate_code(snippets: List[dict], logger: logging.Logger) -> List[dict]:
    """Remove duplicate code snippets"""
    seen_code = set()
    unique_snippets = []

    for snippet in snippets:
        # Normalize code for comparison
        normalized = snippet["code"].strip().lower()

        if normalized not in seen_code:
            seen_code.add(normalized)
            unique_snippets.append(snippet)

    removed = len(snippets) - len(unique_snippets)
    if removed > 0:
        logger.info(f"Removed {removed} duplicate code snippets")

    return unique_snippets


def get_file_extension(language: str) -> str:
    """Get file extension for programming language"""
    extensions = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "csharp": "cs",
        "go": "go",
        "rust": "rs",
        "ruby": "rb",
        "php": "php",
        "sql": "sql",
        "html": "html",
        "css": "css",
        "bash": "sh",
        "shell": "sh",
        "json": "json",
        "xml": "xml",
        "yaml": "yml"
    }

    return extensions.get(language.lower(), "txt")
