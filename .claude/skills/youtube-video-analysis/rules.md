---
description: Implementation rules for YouTube video analysis, based on proven patterns from Hanx tools
globs:
alwaysApply: true
---

# YouTube Video Analysis - Implementation Rules

This document provides detailed implementation guidance for the YouTube Video Analysis Skill, based on battle-tested patterns from the user's Hanx tools (4 months of production use).

## Core Architecture

### Graceful Dependency Handling

**CRITICAL PATTERN**: Always use feature flags for optional dependencies to ensure graceful degradation.

```python
# Pattern from user's youtube_harvest_data.py
try:
    from pytubefix import YouTube
    HAS_PYTUBEFIX = True
except ImportError:
    HAS_PYTUBEFIX = False
    print("Warning: pytubefix not found. Video downloading will not work.")

try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False
    print("Warning: whisper not found. Transcription will be disabled.")

try:
    import moviepy.editor as mp
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False
    print("Warning: moviepy not found. Audio extraction will not work.")
```

**Why This Matters**:
- User may not have all dependencies installed
- Allows partial functionality (e.g., analyze existing transcripts without downloading)
- Provides clear error messages about what's missing
- Enables testing without full stack

### FFmpeg Fallback Pattern

**CRITICAL PATTERN**: If moviepy unavailable, fall back to direct ffmpeg subprocess calls.

```python
# Pattern from user's code - moviepy fallback
if not HAS_MOVIEPY:
    class VideoFileClip:
        def __init__(self, filename):
            self.filename = filename
            self.audio = None
            
        def audio_write_audiofile(self, filename, **kwargs):
            import subprocess
            print(f"Extracting audio from {self.filename} to {filename} using ffmpeg...")
            # Skill's bundled ffmpeg location
            ffmpeg_path = ".claude/skills/youtube-video-analysis/bin/ffmpeg.exe"
            subprocess.call([ffmpeg_path, '-i', self.filename, '-q:a', '0', '-map', 'a', filename, '-y'])
            return filename
            
        def close(self):
            pass
```

**FFmpeg Path Resolution**:
1. Try skill's bundled ffmpeg first: `.claude/skills/youtube-video-analysis/bin/ffmpeg.exe`
2. Fall back to imageio-ffmpeg bundled version
3. Fall back to system PATH
4. Provide clear error if none found

## Video Download

### URL Parsing

**Pattern**: Support multiple YouTube URL formats and video IDs.

```python
def extract_video_id(url_or_id):
    """
    Extract YouTube video ID from URL or return ID if already just the ID.
    Supports: youtube.com, youtu.be, embed URLs, or raw 11-character IDs.
    """
    # Check if it's already just a video ID (11 characters)
    if re.match(r'^[0-9A-Za-z_-]{11}$', url_or_id):
        return url_or_id
    
    # Try to extract the video ID from the URL
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard YouTube URL
        r'(?:embed\/)([0-9A-Za-z_-]{11})',  # Embedded YouTube URL
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # Shortened YouTube URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None

def get_youtube_url(video_id):
    """Convert a YouTube video ID to a full URL."""
    return f"https://www.youtube.com/watch?v={video_id}"
```

### Download Function

**Pattern**: Use pytubefix with highest quality progressive stream.

```python
def download_video(url_or_id, output_path="./youtube_downloads"):
    """
    Download YouTube video in highest quality.
    
    Args:
        url_or_id: YouTube video URL or ID
        output_path: Directory where the video will be downloaded
        
    Returns:
        str: Path to the downloaded video, or None if failed
    """
    if not HAS_PYTUBEFIX:
        print("Error: pytubefix is required for downloading videos.")
        print("Install with: pip install pytubefix")
        return None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Extract video ID and convert to URL if needed
        video_id = extract_video_id(url_or_id)
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {url_or_id}")
        
        url = get_youtube_url(video_id)
        
        yt = YouTube(url)
        print(f"Downloading: {yt.title}")
        print(f"Download directory: {os.path.abspath(output_path)}")
        
        # Get highest quality progressive stream (video + audio)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = stream.download(output_path=output_path)
        
        print(f"Download completed: {video_path}")
        return video_path
        
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        return None
```

## Audio Extraction

### Extraction Function

**Pattern**: Use moviepy with ffmpeg fallback.

```python
def extract_audio(video_path):
    """
    Extract audio from a video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        str: Path to the extracted audio file, or None if failed
    """
    if not HAS_MOVIEPY:
        print("Audio extraction is disabled because moviepy is not installed.")
        print("Please install with: pip install moviepy imageio-ffmpeg")
        return None
        
    try:
        print(f"Extracting audio from {video_path}...")
        
        # Create a temporary file for the audio
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        
        # Extract audio using moviepy (or ffmpeg fallback)
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        video.close()
        
        print(f"Audio extracted to {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None
```

## Transcription

### Whisper Integration

**Pattern**: Support multiple model sizes with clear performance trade-offs.

```python
DEFAULT_MODEL_SIZE = "base"  # Recommended default

def transcribe_audio(audio_path, model_size=DEFAULT_MODEL_SIZE):
    """
    Transcribe audio using Whisper.
    
    Args:
        audio_path: Path to the audio file
        model_size: Size of the Whisper model to use (tiny, base, small, medium, large)
        
    Returns:
        Dict: Transcription result with 'text' key
    """
    if not HAS_WHISPER:
        print("Transcription is disabled because whisper is not installed.")
        print("Please install with: pip install openai-whisper")
        return {"text": "Transcription not available"}
        
    try:
        print(f"Transcribing audio {audio_path}...")
        print(f"Loading Whisper model ({model_size})...")
        
        # Load the Whisper model
        model = whisper.load_model(model_size)
        print("Whisper model loaded successfully.")
        
        # Transcribe the audio
        result = model.transcribe(audio_path)
        
        print(f"Transcription completed: {len(result['text'])} characters")
        return result
    
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        return {"text": f"Error during transcription: {str(e)}"}
```

**Model Size Guidelines**:
- **tiny**: Quick preview, lower accuracy (~1GB RAM, ~32x realtime)
- **base**: Recommended default, balanced (~2GB RAM, ~16x realtime)
- **small**: Better accuracy (~5GB RAM, ~6x realtime)
- **medium**: High accuracy (~10GB RAM, ~2x realtime)
- **large**: Best accuracy (~20GB RAM, ~1x realtime)

## LLM Analysis

### Video Type Templates

**Pattern**: Use structured prompts for different video types.

```python
VIDEO_TYPES = {
    "trading_strategy": "Trading strategy video",
    "framework_tool": "Framework or tool tutorial",
    "general": "General content"
}

# Trading Strategy Prompt Template
TRADING_STRATEGY_PROMPT = """
You are analyzing a trading strategy video. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the trading strategy (max 200 words)
2. Key Points: The main points of the strategy (bullet points)
3. Entry Criteria: When to enter a trade
4. Exit Criteria: When to exit a trade
5. Risk Management: How to manage risk
6. Timeframes: Recommended timeframes for the strategy
7. Markets: Recommended markets for the strategy
8. Indicators: Technical indicators used in the strategy
9. Pros and Cons: Advantages and disadvantages of the strategy

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "entry_criteria": ["...", "..."],
  "exit_criteria": ["...", "..."],
  "risk_management": ["...", "..."],
  "timeframes": ["...", "..."],
  "markets": ["...", "..."],
  "indicators": ["...", "..."],
  "pros": ["...", "..."],
  "cons": ["...", "..."]
}}
"""

# Framework/Tool Prompt Template
FRAMEWORK_TOOL_PROMPT = """
You are analyzing a tutorial about a technical framework or tool. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the framework/tool (max 200 words)
2. Key Features: The main features of the framework/tool
3. Installation: Installation steps or requirements
4. Basic Usage: How to use the framework/tool for basic tasks
5. Advanced Usage: How to use the framework/tool for advanced tasks
6. Limitations: Limitations or constraints of the framework/tool
7. Alternatives: Alternative frameworks/tools mentioned
8. Use Cases: Ideal use cases for the framework/tool
9. Code Examples: Any code examples mentioned (if applicable)

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_features": ["...", "..."],
  "installation": ["...", "..."],
  "basic_usage": ["...", "..."],
  "advanced_usage": ["...", "..."],
  "limitations": ["...", "..."],
  "alternatives": ["...", "..."],
  "use_cases": ["...", "..."],
  "code_examples": ["...", "..."]
}}
"""

# General Content Prompt Template
GENERAL_PROMPT = """
You are analyzing a video. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the video content (max 200 words)
2. Key Points: The main points discussed in the video
3. Topics: The main topics covered
4. Insights: Any interesting insights or takeaways
5. Questions Answered: Questions that are answered in the video
6. References: Any references or sources mentioned

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "topics": ["...", "..."],
  "insights": ["...", "..."],
  "questions_answered": ["...", "..."],
  "references": ["...", "..."]
}}
"""
```

### Analysis Function

**Pattern**: Use Claude API with fallback analysis.

```python
def analyze_with_llm(transcription, video_type="general"):
    """
    Analyze video transcription with LLM.
    
    Args:
        transcription: Transcription text
        video_type: Type of video content (trading_strategy, framework_tool, general)
        
    Returns:
        dict: Analysis results
    """
    if not transcription:
        return None
    
    try:
        # Select the appropriate prompt template
        if video_type == "trading_strategy":
            prompt_template = TRADING_STRATEGY_PROMPT
        elif video_type == "framework_tool":
            prompt_template = FRAMEWORK_TOOL_PROMPT
        else:
            prompt_template = GENERAL_PROMPT
        
        # Format the prompt
        prompt = prompt_template.format(transcription=transcription)
        
        # Use Claude API
        try:
            from anthropic import Anthropic
            client = Anthropic()
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            
            # Try to parse as JSON
            try:
                # Try to extract JSON from markdown code blocks
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = content
                
                return json.loads(json_str)
            except Exception as e:
                print(f"Error parsing LLM response: {e}")
                return fallback_analysis(transcription)
                
        except Exception as e:
            print(f"Error using Claude API: {e}")
            return fallback_analysis(transcription)
    
    except Exception as e:
        print(f"Error analyzing transcription: {e}")
        return fallback_analysis(transcription)

def fallback_analysis(content):
    """
    Fallback analysis when LLM API is not available.
    Extracts basic information using text processing.
    
    Args:
        content: The content to analyze
        
    Returns:
        dict: Basic analysis results
    """
    # Extract the first 200 characters as a summary
    summary = content[:200] + "..." if len(content) > 200 else content
    
    # Extract the first 5 sentences as key points
    import re
    sentences = re.split(r'[.!?]', content)
    key_points = [s.strip() for s in sentences[:5] if s.strip()]
    
    # Return a basic analysis
    return {
        "summary": summary,
        "key_points": key_points,
        "topics": ["Basic analysis - no topics extracted"],
        "insights": ["Basic analysis - no insights extracted"],
        "questions_answered": ["Basic analysis - no questions extracted"],
        "references": ["Basic analysis - no references extracted"]
    }
```

## End-to-End Processing

### Main Processing Function

**Pattern**: Orchestrate all steps with clear progress reporting.

```python
def process_youtube_video(url_or_id, video_type="general", output_dir="./youtube_downloads", model_size="base"):
    """
    Process a YouTube video: download, transcribe, and analyze.
    
    Args:
        url_or_id: YouTube video URL or ID
        video_type: Type of video content (trading_strategy, framework_tool, general)
        output_dir: Directory to save downloaded videos
        model_size: Size of the Whisper model to use
        
    Returns:
        Dict: Processing result
    """
    start_time = time.time()
    result = {
        "video_path": None,
        "audio_path": None,
        "transcription": None,
        "analysis": None
    }
    
    try:
        # Extract video ID and convert to URL if needed
        video_id = extract_video_id(url_or_id)
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {url_or_id}")
        
        url = get_youtube_url(video_id)
        
        print(f"\n{'='*80}")
        print(f"Processing YouTube video: {url}")
        print(f"Video ID: {video_id}")
        print(f"Video type: {VIDEO_TYPES.get(video_type, 'Unknown type')}")
        print(f"{'='*80}\n")
        
        # Step 1: Download the video
        print("\n--- Step 1: Download Video ---")
        video_path = download_video(video_id, output_dir)
        if not video_path:
            return {"error": "Failed to download video"}
        
        result["video_path"] = video_path
        
        # Step 2: Extract audio (if moviepy is available)
        if HAS_MOVIEPY:
            print("\n--- Step 2: Extract Audio ---")
            audio_path = extract_audio(video_path)
            result["audio_path"] = audio_path
            
            # Step 3: Transcribe audio (if whisper is available and audio extraction succeeded)
            if HAS_WHISPER and audio_path:
                print("\n--- Step 3: Transcribe Audio ---")
                transcription = transcribe_audio(audio_path, model_size)
                result["transcription"] = transcription["text"]
                
                # Step 4: Analyze content (if transcription succeeded)
                if transcription["text"]:
                    print("\n--- Step 4: Analyze Content ---")
                    analysis = analyze_with_llm(transcription["text"], video_type)
                    result["analysis"] = analysis
        
        # Step 5: Save results
        print("\n--- Step 5: Save Results ---")
        
        # Save to JSON file
        result_path = os.path.join(output_dir, f"{os.path.basename(video_path)}_analysis.json")
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Analysis saved to: {result_path}")
        
        # Generate a summary report
        print("\n--- Summary Report ---")
        print(f"Video URL: {url}")
        print(f"Video type: {VIDEO_TYPES.get(video_type, 'Unknown type')}")
        print(f"Video file: {os.path.basename(video_path)}")
        print(f"Analysis file: {os.path.basename(result_path)}")
        
        if result["analysis"] and "summary" in result["analysis"]:
            print(f"Summary: {result['analysis']['summary'][:200]}...")
        
        end_time = time.time()
        print(f"Processing completed in {end_time - start_time:.2f} seconds")
        
        return result
    
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        return {"error": str(e)}
```

## Windows-Specific Considerations

### Path Handling

**Pattern**: Use os.path.join and Path for cross-platform compatibility.

```python
import os
from pathlib import Path

# Good: Cross-platform
output_path = os.path.join(base_dir, "youtube_downloads", "video.mp4")

# Good: Modern Python
output_path = Path(base_dir) / "youtube_downloads" / "video.mp4"

# Bad: Windows-specific
output_path = base_dir + "\\youtube_downloads\\video.mp4"
```

### FFmpeg Path on Windows

**Pattern**: Handle Windows paths with backslashes.

```python
# User's ffmpeg location (Windows)
FFMPEG_PATH = r"research\ffmpeg-2025-03-27-git-114fccc4a5-full_build\bin\ffmpeg.exe"

# Or use Path
from pathlib import Path
FFMPEG_PATH = Path("research") / "ffmpeg-2025-03-27-git-114fccc4a5-full_build" / "bin" / "ffmpeg.exe"

# Check if exists
if not os.path.exists(FFMPEG_PATH):
    print(f"FFmpeg not found at: {FFMPEG_PATH}")
    # Fall back to imageio-ffmpeg
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
```

### PowerShell Compatibility

**Pattern**: Use subprocess with proper shell handling.

```python
import subprocess
import sys

# Windows-safe subprocess call
if sys.platform == "win32":
    # Use shell=True for Windows
    subprocess.call([FFMPEG_PATH, '-i', input_file, output_file], shell=False)
else:
    # Unix-like systems
    subprocess.call([FFMPEG_PATH, '-i', input_file, output_file])
```

## Error Handling

### Network Errors

**Pattern**: Retry logic with exponential backoff.

```python
import time

def download_with_retry(url, max_retries=3, initial_delay=1):
    """Download with retry logic."""
    for attempt in range(max_retries):
        try:
            return download_video(url)
        except Exception as e:
            if attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt)
                print(f"Download failed (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...")
                time.sleep(delay)
            else:
                print(f"Download failed after {max_retries} attempts: {e}")
                return None
```

### Processing Errors

**Pattern**: Continue with partial results.

```python
def process_with_partial_results(url):
    """Process video, returning partial results if some steps fail."""
    result = {"url": url, "status": "partial"}
    
    # Try download
    try:
        result["video_path"] = download_video(url)
        result["download_status"] = "success"
    except Exception as e:
        result["download_status"] = f"failed: {e}"
        return result  # Can't continue without video
    
    # Try audio extraction
    try:
        result["audio_path"] = extract_audio(result["video_path"])
        result["audio_status"] = "success"
    except Exception as e:
        result["audio_status"] = f"failed: {e}"
        return result  # Can't continue without audio
    
    # Try transcription
    try:
        result["transcription"] = transcribe_audio(result["audio_path"])
        result["transcription_status"] = "success"
    except Exception as e:
        result["transcription_status"] = f"failed: {e}"
        return result  # Can't continue without transcription
    
    # Try analysis
    try:
        result["analysis"] = analyze_with_llm(result["transcription"]["text"])
        result["analysis_status"] = "success"
        result["status"] = "complete"
    except Exception as e:
        result["analysis_status"] = f"failed: {e}"
    
    return result
```

## Performance Optimization

### Caching

**Pattern**: Cache downloaded videos and transcriptions.

```python
import hashlib

def get_cache_key(url):
    """Generate cache key from URL."""
    return hashlib.md5(url.encode()).hexdigest()

def check_cache(url, cache_dir="./cache"):
    """Check if video already processed."""
    cache_key = get_cache_key(url)
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

def save_to_cache(url, result, cache_dir="./cache"):
    """Save processing result to cache."""
    os.makedirs(cache_dir, exist_ok=True)
    cache_key = get_cache_key(url)
    cache_file = os.path.join(cache_dir, f"{cache_key}.json")
    
    with open(cache_file, 'w') as f:
        json.dump(result, f, indent=2)
```

### Parallel Processing

**Pattern**: Process multiple videos concurrently.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_multiple_videos(urls, max_workers=3):
    """Process multiple videos in parallel."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_url = {
            executor.submit(process_youtube_video, url): url
            for url in urls
        }
        
        # Process results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results[url] = result
                print(f"Completed: {url}")
            except Exception as e:
                results[url] = {"error": str(e)}
                print(f"Failed: {url} - {e}")
    
    return results
```

## Integration with fstrent_spec_tasks

### Task Generation

**Pattern**: Generate tasks from video analysis.

```python
def generate_tasks_from_analysis(analysis, video_url):
    """Generate fstrent_spec_tasks tasks from video analysis."""
    tasks = []
    
    if "implementation_notes" in analysis:
        # Create implementation task
        task = {
            "title": f"Implement features from video",
            "type": "feature",
            "status": "pending",
            "priority": "medium",
            "source": "youtube_video",
            "video_url": video_url,
            "description": analysis.get("summary", ""),
            "acceptance_criteria": analysis.get("key_points", [])
        }
        tasks.append(task)
    
    if "code_examples" in analysis:
        # Create code review task
        task = {
            "title": f"Review code examples from video",
            "type": "task",
            "status": "pending",
            "priority": "low",
            "source": "youtube_video",
            "video_url": video_url,
            "code_examples": analysis["code_examples"]
        }
        tasks.append(task)
    
    return tasks
```

### PRD Generation

**Pattern**: Generate PRD from product video.

```python
def generate_prd_from_video(analysis, video_url):
    """Generate PRD from video analysis."""
    prd = f"""# PRD: {analysis.get('title', 'Feature from Video')}

## 1. Product Overview
### 1.1 Document Title and Version
- PRD: {analysis.get('title', 'Feature from Video')}
- Version: 1.0
- Source: {video_url}

### 1.2 Product Summary
{analysis.get('summary', 'No summary available')}

## 2. Goals
### 2.1 Business Goals
{chr(10).join('- ' + goal for goal in analysis.get('goals', ['No goals extracted']))}

### 2.2 User Goals
{chr(10).join('- ' + goal for goal in analysis.get('user_goals', ['No user goals extracted']))}

## 3. Features
### 3.1 Core Features
{chr(10).join('- ' + feature for feature in analysis.get('key_features', ['No features extracted']))}

## 4. Technical Considerations
{analysis.get('technical_notes', 'No technical considerations extracted')}
"""
    return prd
```

---

**Status**: Production-ready patterns from 4 months of user's Hanx tools  
**Last Updated**: 2025-10-19  
**Maintainer**: Richard (Pied Piper)

