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

# Try to import moviepy
HAS_MOVIEPY = False
try:
    import moviepy.editor as mp
    HAS_MOVIEPY = True
except ImportError:
    try:
        # Create a custom VideoFileClip class if the editor module is not available
        class VideoFileClip:
            def __init__(self, filename):
                self.filename = filename
                self.audio = None
                
            def audio_write_audiofile(self, filename, **kwargs):
                import subprocess
                print(f"Extracting audio from {self.filename} to {filename} using ffmpeg...")
                subprocess.call(['ffmpeg', '-i', self.filename, '-q:a', '0', '-map', 'a', filename, '-y'])
                return filename
                
            def close(self):
                pass
        
        # Create a mock mp module
        class MockMP:
            def __init__(self):
                self.VideoFileClip = VideoFileClip
                
        mp = MockMP()
        HAS_MOVIEPY = True
        print("Warning: moviepy.editor not found. Using custom VideoFileClip implementation.")
    except Exception as e:
        HAS_MOVIEPY = False
        print(f"Warning: moviepy not found. Audio extraction will not work. Error: {e}")
        print("Please install with: pip install moviepy imageio-ffmpeg")

# Try to import LLM API if available
try:
    # First try direct import
    try:
        from hanx_tools.llm_api import query_llm
        HAS_LLM = True
    except ImportError:
        # Then try relative import
        try:
            from .llm_api import query_llm
            HAS_LLM = True
        except ImportError:
            # Finally try with path manipulation
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from hanx_tools.llm_api import query_llm
            HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("Warning: LLM API not found. Analysis will be limited.")

# Try to import our LLM wrapper
try:
    # First try direct import
    try:
        from hanx_tools.temp_tools.llm_wrapper import analyze_content, analyze_trading_strategy, analyze_framework_tool
        HAS_LLM_WRAPPER = True
    except ImportError:
        # Then try relative import
        try:
            from .temp_tools.llm_wrapper import analyze_content, analyze_trading_strategy, analyze_framework_tool
            HAS_LLM_WRAPPER = True
        except ImportError:
            # Finally try with path manipulation
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from hanx_tools.temp_tools.llm_wrapper import analyze_content, analyze_trading_strategy, analyze_framework_tool
            HAS_LLM_WRAPPER = True
except ImportError:
    HAS_LLM_WRAPPER = False
    print("Warning: LLM wrapper not found. Analysis will be limited.")

#<=====>#
# Constants
#<=====>#
DEFAULT_DOWNLOAD_DIR = "./youtube_downloads"
DEFAULT_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
VIDEO_TYPES = {
    "trading_strategy": "Trading strategy video",
    "framework_tool": "Framework or tool tutorial",
    "general": "General content"
}

# Prompt templates for different video types
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

#<=====>#
# Functions
#<=====>#
def extract_video_id(url_or_id):
    """
    Extract the YouTube video ID from a URL or return the ID if it's already just the ID.
    
    Args:
        url_or_id (str): YouTube URL or video ID
        
    Returns:
        str: YouTube video ID
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
    """
    Convert a YouTube video ID to a full URL.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        str: Full YouTube URL
    """
    return f"https://www.youtube.com/watch?v={video_id}"

def download_video(url_or_id, output_path=DEFAULT_DOWNLOAD_DIR):
    """
    Downloads a YouTube video in highest quality
    Args:
        url_or_id (str): YouTube video URL or ID
        output_path (str): Directory where the video will be downloaded
    Returns:
        str: Path to the downloaded video
    """
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
        
        # Get highest quality progressive stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = stream.download(output_path=output_path)
        print(f"Download completed: {video_path}")
        return video_path
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        return None

def extract_audio(video_path):
    """
    Extract audio from a video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        str: Path to the extracted audio file
    """
    if not HAS_MOVIEPY:
        print("Audio extraction is disabled because moviepy is not installed.")
        print("Please install with: pip install moviepy")
        return None
        
    try:
        print(f"Extracting audio from {video_path}...")
        
        # Create a temporary file for the audio
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        
        # Extract audio using moviepy
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        print(f"Audio extracted to {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None

def transcribe_audio(audio_path, model_size=DEFAULT_MODEL_SIZE):
    """
    Transcribe audio using Whisper.
    
    Args:
        audio_path: Path to the audio file
        model_size: Size of the Whisper model to use
        
    Returns:
        Dict: Transcription result
    """
    if not HAS_WHISPER:
        print("Transcription is disabled because whisper is not installed.")
        print("Please install with: pip install whisper openai-whisper")
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

def analyze_with_llm(transcription, video_type):
    """
    Analyze video transcription with LLM.
    
    Args:
        transcription (str): Transcription text
        video_type (str): Type of video content
        
    Returns:
        dict: Analysis results
    """
    if not transcription:
        return None
    
    try:
        # Select the appropriate analysis function based on video type
        if video_type == "trading_strategy":
            if HAS_LLM_WRAPPER:
                return analyze_trading_strategy(transcription)
            else:
                prompt = """
                Analyze this trading strategy video transcription and extract the following information:
                
                1. Strategy Name: Identify the name of the trading strategy discussed
                2. Market/Instrument: What market or financial instrument is this strategy designed for?
                3. Timeframe: What timeframe(s) is this strategy designed for?
                4. Indicators Used: List all technical indicators mentioned
                5. Entry Conditions: What are the specific conditions for entering a trade?
                6. Exit Conditions: What are the specific conditions for exiting a trade?
                7. Risk Management: What risk management techniques are mentioned?
                8. Backtest Results: Any mentioned backtest results or performance metrics
                9. Pros and Cons: List the advantages and disadvantages of this strategy
                10. Key Insights: What are the most important takeaways from this strategy?
                
                Format your response as JSON with these fields. If information for a field is not available, use null.
                
                Transcription:
                {transcription}
                """
        elif video_type == "framework_tool":
            if HAS_LLM_WRAPPER:
                return analyze_framework_tool(transcription)
            else:
                prompt = """
                Analyze this framework/tool tutorial video transcription and extract the following information:
                
                1. Tool Name: Identify the name of the framework or tool discussed
                2. Purpose: What is the main purpose of this framework/tool?
                3. Target Users: Who is this framework/tool designed for?
                4. Key Features: List the main features of this framework/tool
                5. Installation Steps: What are the steps to install this framework/tool?
                6. Usage Examples: What examples of usage are provided?
                7. Dependencies: What dependencies or prerequisites are mentioned?
                8. Limitations: What limitations or constraints are mentioned?
                9. Alternatives: What alternative frameworks/tools are mentioned?
                10. Resources: What additional resources (documentation, tutorials, etc.) are mentioned?
                
                Format your response as JSON with these fields. If information for a field is not available, use null.
                
                Transcription:
                {transcription}
                """
        else:  # general
            if HAS_LLM_WRAPPER:
                return analyze_content(transcription, """
                Analyze this video transcription and extract the following information:
                
                1. Summary: Provide a concise summary of the content
                2. Key Points: List the main points discussed
                3. Topics: Identify the main topics covered
                4. Insights: Extract any valuable insights or takeaways
                5. Questions Answered: What questions does this content answer?
                6. References: Identify any references to external sources, tools, or resources
                
                Format your response as JSON with these fields. If information for a field is not available, use null.
                
                Transcription:
                {transcription}
                """)
            else:
                prompt = """
                Analyze this video transcription and extract the following information:
                
                1. Summary: Provide a concise summary of the content
                2. Key Points: List the main points discussed
                3. Topics: Identify the main topics covered
                4. Insights: Extract any valuable insights or takeaways
                5. Questions Answered: What questions does this content answer?
                6. References: Identify any references to external sources, tools, or resources
                
                Format your response as JSON with these fields. If information for a field is not available, use null.
                
                Transcription:
                {transcription}
                """
        
        # If we have the LLM wrapper but didn't use a specialized function, use the general analyze_content
        if HAS_LLM_WRAPPER and video_type not in ["trading_strategy", "framework_tool"]:
            return analyze_content(transcription, prompt)
        
        # If we have the LLM API but not the wrapper, use the API directly
        if HAS_LLM and not HAS_LLM_WRAPPER:
            try:
                response = query_llm(prompt.format(transcription=transcription), provider="anthropic")
                
                # Try to parse the response as JSON
                try:
                    # Try to extract JSON from the response
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        json_str = response
                    
                    # Clean up the JSON string
                    json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL)
                    
                    # Parse the JSON
                    return json.loads(json_str)
                except Exception as e:
                    print(f"Error parsing LLM response: {e}")
                    return fallback_analysis(transcription)
            except Exception as e:
                print(f"Error using LLM API: {e}")
                return fallback_analysis(transcription)
        
        # If we don't have the LLM API or wrapper, use a fallback
        return fallback_analysis(transcription)
    except Exception as e:
        print(f"Error analyzing transcription: {e}")
        return fallback_analysis(transcription)

def fallback_analysis(content):
    """
    Fallback analysis when LLM API is not available.
    
    Args:
        content (str): The content to analyze
        
    Returns:
        dict: Basic analysis results
    """
    # Extract the first 200 characters as a summary
    summary = content[:200] + "..."
    
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

def process_youtube_video(url_or_id, video_type="general", output_dir=DEFAULT_DOWNLOAD_DIR, model_size=DEFAULT_MODEL_SIZE):
    """
    Process a YouTube video: download, transcribe, and analyze.
    
    Args:
        url_or_id: YouTube video URL or ID
        video_type: Type of video content
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
        
        # Initialize result dictionary
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

def main():
    parser = argparse.ArgumentParser(description="Download and analyze YouTube videos")
    parser.add_argument("video", help="YouTube video URL or ID")
    parser.add_argument("--type", choices=["trading_strategy", "framework_tool", "general"], default="general", help="Type of video content")
    parser.add_argument("--output-dir", default="./youtube_downloads", help="Output directory for downloaded files")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing video: {args.video}")
        print(f"Video type: {args.type}")
        print(f"Output directory: {args.output_dir}")
        print(f"Whisper model size: {args.model}")
        
        # Print dependency status
        print(f"PyTubeFix available: {HAS_PYTUBEFIX}")
        print(f"MoviePy available: {HAS_MOVIEPY}")
        print(f"Whisper available: {HAS_WHISPER}")
        print(f"LLM API available: {HAS_LLM}")
        print(f"LLM Wrapper available: {HAS_LLM_WRAPPER}")
    
    process_youtube_video(args.video, args.type, args.output_dir, args.model)

#<=====>#
# Default Run
#<=====>#
if __name__ == "__main__":
    main()


