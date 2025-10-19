#!/usr/bin/env python3
"""
YouTube Researcher Agent

This agent downloads and processes YouTube videos, extracting information and generating analysis.
"""

#<=====>#
# Description
#<=====>#
"""
YouTube video downloader and analyzer
Downloads videos and extracts information using transcription and LLM analysis
"""

#<=====>#
# Known To Do List
#<=====>#
# TODO: Add progress bar
# TODO: Add support for playlists
# TODO: Improve error handling

#<=====>#
# Imports
#<=====>#
import os
import sys
import json
import time
import argparse
from pathlib import Path
import re
from datetime import datetime

# Import required libraries
try:
    from pytubefix import YouTube
    HAS_PYTUBEFIX = True
except ImportError:
    HAS_PYTUBEFIX = False
    print("Warning: pytubefix not found. Video downloading will not work.")

# Optional imports - we'll check for these before using them
try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False
    print("Warning: whisper not found. Transcription will be disabled.")

try:
    from moviepy import VideoFileClip
    HAS_MOVIEPY = True
except ImportError:
    HAS_MOVIEPY = False
    print("Warning: moviepy not found. Audio extraction will be disabled.")
    
    # Fallback implementation for basic functionality
    class VideoFileClip:
        """Fallback implementation of VideoFileClip when moviepy is not available."""
        def __init__(self, filename):
            self.filename = filename
            print(f"Created fallback VideoFileClip for {filename}")
        
        def audio_write_audiofile(self, filename, **kwargs):
            print(f"Warning: Cannot extract audio to {filename} without moviepy.")
            print("Trying to use ffmpeg directly...")
            self._extract_audio_with_ffmpeg(filename)
        
        def close(self):
            pass
        
        def _extract_audio_with_ffmpeg(self, output_file):
            try:
                import subprocess
                try:
                    from imageio_ffmpeg import get_ffmpeg_exe
                    ffmpeg_exe = get_ffmpeg_exe()
                except ImportError:
                    ffmpeg_exe = "ffmpeg"  # Hope it's in the PATH
                
                cmd = [ffmpeg_exe, "-i", self.filename, "-q:a", "0", "-map", "a", output_file, "-y"]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"Successfully extracted audio to {output_file} using ffmpeg directly.")
                return True
            except Exception as e:
                print(f"Failed to extract audio with ffmpeg: {e}")
                return False

# Add the parent directory to the path so we can import from hanx_tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import from hanx_tools if available
try:
    from hanx_tools.tool_rag_utils import add_text
    from hanx_apis.api_llm import query_llm
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    print("Warning: RAG utilities not found. RAG integration will be disabled.")

# Constants
DEFAULT_DOWNLOAD_DIR = os.path.join(os.getcwd(), "youtube_downloads")
DEFAULT_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large

# Prompt templates for different video types
GENERAL_PROMPT = """
Analyze the following video transcript and provide a comprehensive analysis:

Transcript:
{transcription}

Please provide:
1. Summary: A concise summary of the video content
2. Key Points: The main points or arguments presented
3. Topics Covered: List of topics discussed
4. Insights: Any notable insights or takeaways
5. Questions Answered: What questions does this video answer?
6. References: Any references to external sources, people, or concepts

Format your response as JSON with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "topics": ["...", "..."],
  "insights": ["...", "..."],
  "questions_answered": ["...", "..."],
  "references": ["...", "..."]
}}
"""

TRADING_STRATEGY_PROMPT = """
Analyze the following trading strategy video transcript and provide a detailed breakdown:

Transcript:
{transcription}

Please extract and provide:
1. Strategy Name: The name of the trading strategy discussed
2. Markets: Which markets this strategy is designed for (crypto, forex, stocks, etc.)
3. Timeframes: Which timeframes this strategy works best on
4. Indicators Used: List all technical indicators mentioned
5. Entry Conditions: Specific conditions for entering a trade
6. Exit Conditions: Specific conditions for exiting a trade
7. Risk Management: Any risk management rules mentioned
8. Backtest Results: Any backtest results or historical performance mentioned
9. Pros and Cons: Advantages and disadvantages of this strategy
10. Key Insights: Notable insights about this strategy

Format your response as JSON with the following structure:
{{
  "strategy_name": "...",
  "markets": ["...", "..."],
  "timeframes": ["...", "..."],
  "indicators": ["...", "..."],
  "entry_conditions": ["...", "..."],
  "exit_conditions": ["...", "..."],
  "risk_management": ["...", "..."],
  "backtest_results": "...",
  "pros": ["...", "..."],
  "cons": ["...", "..."],
  "key_insights": ["...", "..."]
}}
"""

FRAMEWORK_TOOL_PROMPT = """
Analyze the following framework/tool tutorial video transcript and provide a detailed breakdown:

Transcript:
{transcription}

Please extract and provide:
1. Tool/Framework Name: The name of the tool or framework discussed
2. Purpose: What problem does this tool solve?
3. Target Users: Who is this tool designed for?
4. Key Features: List the main features of the tool
5. Installation Process: How to install or set up the tool
6. Basic Usage: How to use the tool for basic tasks
7. Advanced Features: Any advanced features or capabilities
8. Limitations: Any limitations or constraints mentioned
9. Alternatives: Any alternative tools mentioned
10. Resources: Links, documentation, or resources mentioned

Format your response as JSON with the following structure:
{{
  "tool_name": "...",
  "purpose": "...",
  "target_users": ["...", "..."],
  "key_features": ["...", "..."],
  "installation": ["...", "..."],
  "basic_usage": ["...", "..."],
  "advanced_features": ["...", "..."],
  "limitations": ["...", "..."],
  "alternatives": ["...", "..."],
  "resources": ["...", "..."]
}}
"""

def extract_video_id(url_or_id):
    """
    Extract the YouTube video ID from a URL or return the ID if it's already just the ID.
    
    Args:
        url_or_id: A YouTube URL or video ID
        
    Returns:
        The YouTube video ID
    """
    if not url_or_id:
        return None
    
    # Check if it's already just the ID (11 characters)
    if len(url_or_id) == 11 and re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Extract from youtu.be URL
    match = re.search(r'youtu\.be/([A-Za-z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)
    
    # Extract from youtube.com URL
    match = re.search(r'youtube\.com/.*[?&]v=([A-Za-z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)
    
    # Extract from embed URL
    match = re.search(r'youtube\.com/embed/([A-Za-z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)
    
    return url_or_id  # Return as is if we couldn't parse it

def get_youtube_url(video_id):
    """
    Get the YouTube URL for a video ID.
    
    Args:
        video_id: The YouTube video ID
        
    Returns:
        The YouTube URL
    """
    return f"https://www.youtube.com/watch?v={video_id}"

def download_video(url_or_id, output_path=DEFAULT_DOWNLOAD_DIR):
    """
    Download a YouTube video.
    
    Args:
        url_or_id: YouTube URL or video ID
        output_path: Directory to save the video
        
    Returns:
        Path to the downloaded video file, or None if download failed
    """
    if not HAS_PYTUBEFIX:
        print("Error: pytubefix is required for downloading videos.")
        return None
    
    video_id = extract_video_id(url_or_id)
    url = get_youtube_url(video_id)
    
    print(f"Downloading video: {url}")
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Download the video
        yt = YouTube(url)
        print(f"Video title: {yt.title}")
        
        # Get the highest resolution stream with both video and audio
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        video_path = stream.download(output_path=output_path)
        print(f"Downloaded video to: {video_path}")
        
        return video_path
    
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def extract_audio(video_path):
    """
    Extract audio from a video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the extracted audio file, or None if extraction failed
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return None
    
    try:
        # Create output path for audio
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        
        print(f"Extracting audio from: {video_path}")
        
        # Extract audio using moviepy or fallback
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
        
        print(f"Extracted audio to: {audio_path}")
        
        return audio_path
    
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_audio(audio_path, model_size=DEFAULT_MODEL_SIZE):
    """
    Transcribe audio using Whisper.
    
    Args:
        audio_path: Path to the audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        
    Returns:
        Transcription text, or None if transcription failed
    """
    if not HAS_WHISPER:
        print("Error: whisper is required for transcription.")
        return None
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}")
        return None
    
    try:
        print(f"Transcribing audio: {audio_path}")
        print(f"Using Whisper model: {model_size}")
        
        # Load the model
        model = whisper.load_model(model_size)
        
        # Transcribe the audio
        result = model.transcribe(audio_path)
        
        # Save the transcription to a file
        transcription_path = os.path.splitext(audio_path)[0] + ".txt"
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print(f"Saved transcription to: {transcription_path}")
        
        return result["text"]
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def analyze_with_llm(transcription, video_type):
    """
    Analyze the transcription using an LLM.
    
    Args:
        transcription: The video transcription
        video_type: Type of video (general, trading, framework)
        
    Returns:
        Analysis results, or None if analysis failed
    """
    if not transcription:
        print("Error: No transcription provided for analysis.")
        return None
    
    try:
        print(f"Analyzing transcription for video type: {video_type}")
        
        # Select the appropriate prompt template
        if video_type.lower() == "trading" or video_type.lower() == "trading_strategy":
            prompt_template = TRADING_STRATEGY_PROMPT
            print("Using trading strategy analysis template")
        elif video_type.lower() == "framework" or video_type.lower() == "framework_tool":
            prompt_template = FRAMEWORK_TOOL_PROMPT
            print("Using framework/tool analysis template")
        else:
            prompt_template = GENERAL_PROMPT
            print("Using general analysis template")
        
        # Format the prompt
        prompt = prompt_template.format(transcription=transcription)
        
        # Try to use the LLM API if available
        try:
            from hanx_apis.api_llm import query_llm
            
            print("Using LLM API for analysis")
            response = query_llm(prompt, provider="openai")
            
            # Try to parse the response as JSON
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                print("Warning: LLM response is not valid JSON. Using raw response.")
                return {"raw_response": response}
        
        except ImportError:
            print("Warning: LLM API not available. Using fallback analysis.")
            return fallback_analysis(transcription)
        
        except Exception as e:
            print(f"Error using LLM API: {e}")
            print("Using fallback analysis.")
            return fallback_analysis(transcription)
    
    except Exception as e:
        print(f"Error analyzing transcription: {e}")
        return None

def fallback_analysis(content):
    """
    Fallback analysis when LLM API is not available.
    
    Args:
        content: The content to analyze
        
    Returns:
        Basic analysis results
    """
    print("Performing fallback analysis")
    
    # Extract potential topics (capitalized words or phrases)
    topics = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*\b', content)
    topics = list(set([t for t in topics if len(t) > 3]))[:10]  # Deduplicate and limit
    
    # Extract potential key points (sentences ending with periods)
    sentences = re.split(r'(?<=[.!?])\s+', content)
    key_points = [s for s in sentences if len(s) > 50 and len(s) < 200][:5]  # Select medium-length sentences
    
    # For trading strategies, try to extract indicators
    indicators = []
    indicator_patterns = [
        r'\b(?:RSI|MACD|EMA|SMA|Bollinger Bands|Stochastic|ADX|ATR|OBV|Ichimoku|Fibonacci)\b',
        r'\b\d+(?:-day|day|-period|period)\s+(?:moving average|MA|EMA|SMA)\b',
    ]
    for pattern in indicator_patterns:
        indicators.extend(re.findall(pattern, content, re.IGNORECASE))
    
    # For trading strategies, try to extract timeframes
    timeframes = re.findall(r'\b(?:1-minute|5-minute|15-minute|30-minute|1-hour|4-hour|daily|weekly|monthly)\b', content, re.IGNORECASE)
    
    # For trading strategies, try to extract markets
    markets = re.findall(r'\b(?:crypto|cryptocurrency|bitcoin|ethereum|forex|stocks|indices|commodities|futures|options)\b', content, re.IGNORECASE)
    
    # For framework tools, try to extract tool names
    tools = re.findall(r'\b(?:Python|JavaScript|React|Angular|Vue|Django|Flask|Node\.js|Express|TensorFlow|PyTorch|Keras|Kubernetes|AWS|Azure|GCP)\b', content)
    
    # Create a basic summary (first 200 characters)
    summary = content[:200] + "..." if len(content) > 200 else content
    
    # Return the results
    return {
        "summary": summary,
        "key_points": key_points,
        "topics": topics,
        "indicators": list(set(indicators)) if indicators else [],
        "timeframes": list(set(timeframes)) if timeframes else [],
        "markets": list(set(markets)) if markets else [],
        "tools": list(set(tools)) if tools else [],
    }

def process_youtube_video(url_or_id, video_type="general", output_dir=DEFAULT_DOWNLOAD_DIR, model_size=DEFAULT_MODEL_SIZE):
    """
    Process a YouTube video: download, extract audio, transcribe, and analyze.
    
    Args:
        url_or_id: YouTube URL or video ID
        video_type: Type of video (general, trading, framework)
        output_dir: Directory to save the output files
        model_size: Whisper model size (tiny, base, small, medium, large)
        
    Returns:
        Dictionary with processing results
    """
    start_time = time.time()
    
    # Extract video ID
    video_id = extract_video_id(url_or_id)
    if not video_id:
        return {"error": "Invalid YouTube URL or video ID"}
    
    print(f"Processing YouTube video: {video_id}")
    print(f"Video type: {video_type}")
    print(f"Output directory: {output_dir}")
    print(f"Whisper model size: {model_size}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize results
    results = {
        "video_id": video_id,
        "video_url": get_youtube_url(video_id),
        "video_type": video_type,
        "output_dir": output_dir,
        "model_size": model_size,
        "timestamp": datetime.now().isoformat(),
    }
    
    # Download the video
    video_path = download_video(video_id, output_dir)
    if not video_path:
        results["error"] = "Failed to download video"
        return results
    
    results["video_path"] = video_path
    
    # Extract audio
    audio_path = extract_audio(video_path)
    if not audio_path:
        results["error"] = "Failed to extract audio"
        return results
    
    results["audio_path"] = audio_path
    
    # Transcribe audio
    transcription = transcribe_audio(audio_path, model_size)
    if not transcription:
        results["error"] = "Failed to transcribe audio"
        return results
    
    results["transcription"] = transcription
    
    # Save transcription to a file
    transcription_path = os.path.splitext(audio_path)[0] + ".txt"
    with open(transcription_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    
    results["transcription_path"] = transcription_path
    
    # Analyze the transcription
    analysis = analyze_with_llm(transcription, video_type)
    if not analysis:
        results["error"] = "Failed to analyze transcription"
        return results
    
    results["analysis"] = analysis
    
    # Save analysis to a file
    analysis_path = os.path.splitext(audio_path)[0] + "_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)
    
    results["analysis_path"] = analysis_path
    
    # Add to RAG if requested and available
    if HAS_RAG and "--rag" in sys.argv:
        try:
            # Prepare content for RAG
            rag_content = f"YouTube Video: {video_id}\n\nTranscription:\n{transcription}\n\nAnalysis:\n{json.dumps(analysis, indent=2)}"
            
            # Add to RAG
            metadata = {
                "source": "youtube",
                "video_id": video_id,
                "video_url": get_youtube_url(video_id),
                "video_type": video_type,
            }
            
            doc_id = add_text(rag_content, metadata)
            results["rag_doc_id"] = doc_id
            print(f"Added to RAG with document ID: {doc_id}")
        
        except Exception as e:
            print(f"Error adding to RAG: {e}")
    
    # Calculate processing time
    end_time = time.time()
    processing_time = end_time - start_time
    results["processing_time"] = processing_time
    
    print(f"Processing completed in {processing_time:.2f} seconds")
    
    return results

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="YouTube Researcher Agent")
    parser.add_argument("url_or_id", help="YouTube URL or video ID")
    parser.add_argument("--type", choices=["general", "trading", "framework"], default="general",
                        help="Type of video content (default: general)")
    parser.add_argument("--output", default=DEFAULT_DOWNLOAD_DIR,
                        help=f"Output directory (default: {DEFAULT_DOWNLOAD_DIR})")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"], default=DEFAULT_MODEL_SIZE,
                        help=f"Whisper model size (default: {DEFAULT_MODEL_SIZE})")
    parser.add_argument("--rag", action="store_true", help="Add to RAG system")
    
    args = parser.parse_args()
    
    # Process the video
    results = process_youtube_video(args.url_or_id, args.type, args.output, args.model)
    
    # Print results summary
    print("\nProcessing Results:")
    print(f"Video ID: {results.get('video_id')}")
    print(f"Video URL: {results.get('video_url')}")
    print(f"Video Path: {results.get('video_path')}")
    print(f"Audio Path: {results.get('audio_path')}")
    print(f"Transcription Path: {results.get('transcription_path')}")
    print(f"Analysis Path: {results.get('analysis_path')}")
    
    if "error" in results:
        print(f"Error: {results['error']}")
    
    if "rag_doc_id" in results:
        print(f"RAG Document ID: {results['rag_doc_id']}")
    
    print(f"Processing Time: {results.get('processing_time', 0):.2f} seconds")

def analyze_content_with_llm(content, prompt_template, provider="openai"):
    """
    Analyze content with an LLM using a prompt template.
    
    Args:
        content: The content to analyze
        prompt_template: The prompt template to use
        provider: The LLM provider to use
        
    Returns:
        Analysis results
    """
    try:
        # Format the prompt
        prompt = prompt_template.format(transcription=content)
        
        # Use the LLM API
        from hanx_apis.api_llm import query_llm
        response = query_llm(prompt, provider=provider)
        
        # Try to parse the response as JSON
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError:
            return {"raw_response": response}
    
    except Exception as e:
        print(f"Error analyzing content with LLM: {e}")
        return fallback_analysis(content)

if __name__ == "__main__":
    main() 