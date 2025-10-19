"""
YouTube Tools

A comprehensive module for working with YouTube videos, including:
1. Downloading YouTube videos
2. Transcribing video content
3. Analyzing and summarizing video content
4. Integrating with RAG systems

This module combines functionality from:
- youtube_processor.py: Core video processing functionality
- youtube_analyzer.py: LLM-based content analysis
- youtube_harvester.py: End-to-end workflow integration

Usage:
    from hanx_tools.tool_youtube import YouTubeProcessor, process_video, enhance_analysis
    
    # Process a single video
    result = process_video("https://youtu.be/example", video_type="trading_strategy")
    
    # Or use the processor directly
    processor = YouTubeProcessor()
    video_path = processor.download_video("https://youtu.be/example")

GitHub Usage Notes:
1. This tool requires several dependencies that will be installed via requirements.txt
2. FFMPEG is handled automatically by imageio-ffmpeg
3. For transcription, you need to have the Whisper model installed
4. The tool will create a youtube_downloads directory in your project

Installation:
    pip install -r requirements.txt
"""

import os
import sys
import json
import time
import tempfile
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any
import imageio_ffmpeg

# Silently get current working directory for internal use
cwd = os.getcwd()

# Load environment variables if available
env_files = ['.env.local', '.env', '.env.example']
for env_file in env_files:
    env_path = os.path.join(cwd, env_file)
    if os.path.exists(env_path):
        try:
            import dotenv
            dotenv.load_dotenv(env_path)
            # Silently loaded environment variables
        except ImportError:
            pass
        except Exception:
            pass

# Import required libraries
try:
    from pytubefix import YouTube
    # Try different whisper import options
    try:
        import whisper
    except ImportError:
        try:
            import whisper
        except ImportError:
            whisper = None
    
    try:
        from moviepy import VideoFileClip
    except ImportError:
        VideoFileClip = None
        
    try:
        from pydub import AudioSegment
    except ImportError:
        AudioSegment = None
except ImportError as e:
    print(f"Required libraries not found: {str(e)}")
    print("Please install with:")
    print("pip install pytubefix openai-whisper moviepy pydub")
    # Don't exit immediately to allow for better error handling
    # sys.exit(1)

# Try to import RAG utilities if available
try:
    from tool_rag_utils import add_to_knowledge_base, create_collection_if_not_exists
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    print("Warning: RAG utilities not found. RAG integration will be disabled.")

# Try to import LLM API
try:
    from hanx_apis.api_llm import query_llm
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("Warning: LLM API not found. Using mock analysis.")

# Constants
DEFAULT_DOWNLOAD_DIR = "./youtube_downloads"
DEFAULT_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
VIDEO_TYPES = {
    "general": "General content",
    "trading_strategy": "Trading strategy tutorial",
    "framework_tool": "Framework or tool tutorial",
    "educational": "Educational content",
    "product_review": "Product review",
    "news": "News content"
}

# Set FFMPEG path - use a more portable approach
try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
except Exception as e:
    print(f"Warning: Could not set FFMPEG path: {str(e)}")
    print("FFMPEG will be downloaded automatically by imageio-ffmpeg if needed")

#
# PART 1: YOUTUBE PROCESSOR
#

class YouTubeProcessor:
    """
    Process YouTube videos: download, extract audio, transcribe, and analyze.
    """
    
    def __init__(self, download_dir: str = DEFAULT_DOWNLOAD_DIR, model_size: str = DEFAULT_MODEL_SIZE):
        """
        Initialize the YouTube processor.
        
        Args:
            download_dir: Directory to save downloaded videos
            model_size: Size of the Whisper model to use for transcription
        """
        self.download_dir = download_dir
        self.model_size = model_size
        self.model = None
        
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
    
    def _load_whisper_model(self):
        """Load the Whisper model for transcription."""
        if self.model is None:
            if 'whisper' not in globals() or whisper is None:
                print("Whisper is not available. Please install with: pip install openai-whisper")
                return None
            
            try:
                print(f"Loading Whisper model ({self.model_size})...")
                self.model = whisper.load_model(self.model_size)
            except Exception as e:
                print(f"Error loading Whisper model: {str(e)}")
                print("Transcription will not be available.")
                return None
        return self.model
    
    def download_video(self, url: str) -> str:
        """
        Download a YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            str: Path to the downloaded video file or None if download fails
        """
        try:
            print(f"Downloading video: {url}")
            yt = YouTube(url)
            
            # Get video metadata
            title = yt.title
            author = yt.author
            length = yt.length
            
            print(f"Video title: {title}")
            print(f"Channel: {author}")
            print(f"Duration: {length // 60}:{length % 60:02d}")
            
            # Download the highest resolution video
            video_stream = yt.streams.get_highest_resolution()
            video_path = video_stream.download(output_path=self.download_dir)
            
            print(f"Video downloaded to: {video_path}")
            return video_path
            
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None
    
    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from a video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        try:
            print(f"Extracting audio from video: {os.path.basename(video_path)}")
            
            # Check if VideoFileClip is available
            if 'VideoFileClip' not in globals() or VideoFileClip is None:
                print("Error: MoviePy not available. Cannot extract audio.")
                return None
            
            # Create output path for audio
            audio_path = os.path.splitext(video_path)[0] + ".mp3"
            
            # Extract audio using moviepy
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, codec='mp3')
            
            print(f"Audio extracted to: {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"Error extracting audio: {str(e)}")
            return None
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dict: Transcription result
        """
        try:
            print(f"Transcribing audio: {os.path.basename(audio_path)}")
            
            # Load the Whisper model
            model = self._load_whisper_model()
            if model is None:
                print("Whisper model not available. Returning empty transcription.")
                return {
                    "text": "Transcription not available. Whisper model could not be loaded.",
                    "segments": []
                }
            
            # Transcribe the audio
            print("This may take a while depending on the audio length...")
            result = model.transcribe(audio_path)
            
            print(f"Transcription completed: {len(result['text'])} characters")
            return result
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return {
                "text": f"Error during transcription: {str(e)}",
                "segments": []
            }
    
    def analyze_content(self, transcription: Dict[str, Any], video_type: str = "general") -> Dict[str, Any]:
        """
        Analyze video content based on transcription.
        
        Args:
            transcription: Transcription result from Whisper
            video_type: Type of video content
            
        Returns:
            Dict: Analysis result
        """
        try:
            print(f"Analyzing content for video type: {video_type}")
            
            # Basic analysis without LLM
            text = transcription["text"]
            segments = transcription.get("segments", [])
            
            # Extract timestamps and segments
            timestamped_segments = []
            for segment in segments:
                timestamped_segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                })
            
            # Create basic analysis
            analysis = {
                "video_type": video_type,
                "transcription": text,
                "segments": timestamped_segments,
                "word_count": len(text.split()),
                "duration": segments[-1]["end"] if segments else 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "summary": "Transcription completed. Use enhance_analysis() for LLM-based analysis.",
                "key_points": []
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            raise
    
    def save_analysis(self, analysis: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Save analysis to a JSON file.
        
        Args:
            analysis: Analysis result
            output_path: Path to save the analysis (optional)
            
        Returns:
            str: Path to the saved analysis file
        """
        try:
            # Create output path if not provided
            if output_path is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                video_type = analysis.get("video_type", "general")
                filename = f"analysis_{video_type}_{timestamp}.json"
                output_path = os.path.join(self.download_dir, filename)
            
            # Save analysis to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"Analysis saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")
            raise
    
    def add_to_rag(self, analysis: Dict[str, Any], collection_name: str = "youtube_videos") -> bool:
        """
        Add analysis to RAG system.
        
        Args:
            analysis: Analysis result
            collection_name: Name of the RAG collection
            
        Returns:
            bool: True if successful
        """
        if not HAS_RAG:
            print("RAG integration not available. Skipping.")
            return False
        
        try:
            print(f"Adding analysis to RAG collection: {collection_name}")
            
            # Create collection if it doesn't exist
            if 'create_collection_if_not_exists' in globals():
                create_collection_if_not_exists(collection_name)
            
            # Prepare document for RAG
            document = {
                "content": analysis["transcription"],
                "metadata": {
                    "video_type": analysis["video_type"],
                    "summary": analysis.get("summary", ""),
                    "key_points": analysis.get("key_points", []),
                    "processed_at": analysis.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
                }
            }
            
            # Add type-specific metadata
            if analysis["video_type"] == "trading_strategy" and "trading_details" in analysis:
                document["metadata"]["trading_details"] = analysis["trading_details"]
            elif analysis["video_type"] == "framework_tool" and "technical_details" in analysis:
                document["metadata"]["technical_details"] = analysis["technical_details"]
            
            # Add to knowledge base
            add_to_knowledge_base(document, collection_name)
            print(f"Analysis added to RAG collection: {collection_name}")
            return True
            
        except Exception as e:
            print(f"Error adding to RAG: {str(e)}")
            return False
    
    def process_video(self, url: str, video_type: str = "general", 
                     add_to_rag: bool = False, collection_name: str = "youtube_videos") -> Dict[str, Any]:
        """
        Process a YouTube video: download, transcribe, analyze.
        
        Args:
            url: YouTube video URL
            video_type: Type of video content
            add_to_rag: Whether to add the analysis to RAG
            collection_name: Name of the RAG collection
            
        Returns:
            Dict: Processing result
        """
        try:
            # Download the video
            video_path = self.download_video(url)
            if not video_path:
                raise Exception("Failed to download video")
            
            # Extract audio
            audio_path = self.extract_audio(video_path)
            if not audio_path:
                print("Warning: Audio extraction failed. Skipping transcription.")
                # Create a minimal analysis without transcription
                analysis = {
                    "video_type": video_type,
                    "transcription": "Audio extraction failed. No transcription available.",
                    "segments": [],
                    "word_count": 0,
                    "duration": 0,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": "Audio extraction failed. No transcription available.",
                    "key_points": ["Audio extraction failed"]
                }
                
                # Save analysis
                analysis_path = self.save_analysis(analysis)
                
                return {
                    "video_path": video_path,
                    "audio_path": None,
                    "analysis_path": analysis_path,
                    "analysis": analysis
                }
            
            # Transcribe audio
            transcription = self.transcribe_audio(audio_path)
            
            # Analyze content
            analysis = self.analyze_content(transcription, video_type)
            
            # Save analysis
            analysis_path = self.save_analysis(analysis)
            
            # Add to RAG if requested
            if add_to_rag:
                self.add_to_rag(analysis, collection_name)
            
            return {
                "video_path": video_path,
                "audio_path": audio_path,
                "analysis_path": analysis_path,
                "analysis": analysis
            }
            
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            raise

#
# PART 2: YOUTUBE ANALYZER
#

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
  "pros_and_cons": {{
    "pros": ["...", "..."],
    "cons": ["...", "..."]
  }}
}}
"""

FRAMEWORK_TOOL_PROMPT = """
You are analyzing a framework or tool tutorial video. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the framework/tool (max 200 words)
2. Key Points: The main points about the framework/tool (bullet points)
3. Installation: Installation steps or requirements
4. Core Features: Main features of the framework/tool
5. Use Cases: Common use cases
6. Code Examples: Any code examples mentioned (if applicable)
7. Alternatives: Mentioned alternatives
8. Pros and Cons: Advantages and disadvantages

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "installation": ["...", "..."],
  "core_features": ["...", "..."],
  "use_cases": ["...", "..."],
  "code_examples": ["...", "..."],
  "alternatives": ["...", "..."],
  "pros_and_cons": {{
    "pros": ["...", "..."],
    "cons": ["...", "..."]
  }}
}}
"""

GENERAL_PROMPT = """
You are analyzing a video. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the video content (max 200 words)
2. Key Points: The main points discussed in the video (bullet points)
3. Topics: Main topics covered
4. Insights: Key insights or takeaways
5. Questions: Questions that might arise from the content

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "topics": ["...", "..."],
  "insights": ["...", "..."],
  "questions": ["...", "..."]
}}
"""

EDUCATIONAL_PROMPT = """
You are analyzing an educational video. The transcription is provided below.
Extract the following information:
1. Summary: A concise summary of the educational content (max 200 words)
2. Key Points: The main educational points (bullet points)
3. Concepts: Key concepts explained
4. Examples: Examples provided in the video
5. Applications: Real-world applications mentioned
6. Prerequisites: Any prerequisite knowledge mentioned
7. Further Resources: Any mentioned resources for further learning

Transcription:
{transcription}

Format your response as a JSON object with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "concepts": ["...", "..."],
  "examples": ["...", "..."],
  "applications": ["...", "..."],
  "prerequisites": ["...", "..."],
  "further_resources": ["...", "..."]
}}
"""

def get_prompt_for_video_type(video_type: str, transcription: str) -> str:
    """
    Get the appropriate prompt template for a video type.
    
    Args:
        video_type: Type of video content
        transcription: Video transcription
        
    Returns:
        str: Formatted prompt
    """
    prompts = {
        "trading_strategy": TRADING_STRATEGY_PROMPT,
        "framework_tool": FRAMEWORK_TOOL_PROMPT,
        "educational": EDUCATIONAL_PROMPT,
        "general": GENERAL_PROMPT
    }
    
    # Get the prompt template or default to general
    prompt_template = prompts.get(video_type, GENERAL_PROMPT)
    
    # Format the prompt with the transcription
    return prompt_template.format(transcription=transcription)

def analyze_with_llm(transcription: str, video_type: str = "general", 
                    provider: str = "anthropic", max_tokens: int = 2000) -> Dict[str, Any]:
    """
    Analyze video transcription using LLM.
    
    Args:
        transcription: Video transcription
        video_type: Type of video content
        provider: LLM provider
        max_tokens: Maximum tokens for LLM response
        
    Returns:
        Dict: Analysis result
    """
    if not HAS_LLM:
        print("LLM API not available. Using mock analysis.")
        return {
            "summary": "Mock summary for " + video_type + " video.",
            "key_points": ["Mock key point 1", "Mock key point 2"],
            "analysis_type": "mock"
        }
    
    try:
        print(f"Analyzing transcription with LLM ({provider})...")
        
        # Get the appropriate prompt
        prompt = get_prompt_for_video_type(video_type, transcription)
        
        # Truncate transcription if too long
        if len(transcription) > 15000:
            print("Transcription too long, truncating to 15,000 characters...")
            transcription = transcription[:15000] + "..."
            prompt = get_prompt_for_video_type(video_type, transcription)
        
        # Query the LLM
        response = query_llm(
            prompt=prompt,
            provider=provider
        )
        
        # Parse the response as JSON
        try:
            # Extract JSON from the response if needed
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].strip()
            else:
                json_str = response.strip()
            
            analysis = json.loads(json_str)
            analysis["analysis_type"] = "llm"
            return analysis
            
        except json.JSONDecodeError:
            print("Error parsing LLM response as JSON. Using raw response.")
            return {
                "summary": response[:500],
                "key_points": [response[500:1000]],
                "raw_response": response,
                "analysis_type": "raw"
            }
            
    except Exception as e:
        print(f"Error analyzing with LLM: {str(e)}")
        return {
            "summary": "Error analyzing with LLM: " + str(e),
            "key_points": ["Error occurred during analysis"],
            "analysis_type": "error"
        }

def enhance_analysis(analysis: Dict[str, Any], transcription: str, video_type: str = "general") -> Dict[str, Any]:
    """
    Enhance basic analysis with LLM-based analysis.
    
    Args:
        analysis: Basic analysis from YouTubeProcessor
        transcription: Video transcription
        video_type: Type of video content
        
    Returns:
        Dict: Enhanced analysis
    """
    try:
        print(f"Enhancing analysis for video type: {video_type}")
        
        # Get LLM analysis
        llm_analysis = analyze_with_llm(transcription, video_type)
        
        # Merge basic analysis with LLM analysis
        enhanced = analysis.copy()
        
        # Add LLM analysis fields
        for key, value in llm_analysis.items():
            if key not in enhanced or not enhanced[key]:
                enhanced[key] = value
        
        # Add type-specific fields
        if video_type == "trading_strategy":
            enhanced["trading_details"] = {
                "entry_criteria": llm_analysis.get("entry_criteria", []),
                "exit_criteria": llm_analysis.get("exit_criteria", []),
                "risk_management": llm_analysis.get("risk_management", []),
                "timeframes": llm_analysis.get("timeframes", []),
                "markets": llm_analysis.get("markets", []),
                "indicators": llm_analysis.get("indicators", [])
            }
        elif video_type == "framework_tool":
            enhanced["technical_details"] = {
                "installation": llm_analysis.get("installation", []),
                "core_features": llm_analysis.get("core_features", []),
                "use_cases": llm_analysis.get("use_cases", []),
                "code_examples": llm_analysis.get("code_examples", []),
                "alternatives": llm_analysis.get("alternatives", [])
            }
        
        return enhanced
        
    except Exception as e:
        print(f"Error enhancing analysis: {str(e)}")
        # Return original analysis if enhancement fails
        return analysis

#
# PART 3: YOUTUBE HARVESTER (END-TO-END WORKFLOW)
#

def process_video(url: str, video_type: str = "general", 
                 download_dir: str = "./youtube_downloads",
                 model_size: str = "base",
                 add_to_rag: bool = False,
                 collection_name: str = "youtube_videos",
                 llm_provider: str = "anthropic") -> Dict[str, Any]:
    """
    Process a YouTube video: download, transcribe, analyze, and optionally add to RAG.
    
    Args:
        url: YouTube video URL
        video_type: Type of video content
        download_dir: Directory to save downloaded videos
        model_size: Size of the Whisper model to use for transcription
        add_to_rag: Whether to add the analysis to RAG
        collection_name: Name of the RAG collection
        llm_provider: LLM provider for analysis
        
    Returns:
        Dict: Processing result
    """
    try:
        print(f"\n{'='*80}")
        print(f"Processing YouTube video: {url}")
        print(f"Video type: {VIDEO_TYPES.get(video_type, 'Unknown type')}")
        print(f"{'='*80}\n")
        
        # Initialize the YouTube processor
        processor = YouTubeProcessor(download_dir=download_dir, model_size=model_size)
        
        # Process the video (download, extract audio, transcribe)
        print("\n--- Step 1: Basic Processing ---")
        result = processor.process_video(url, video_type)
        
        # Enhance the analysis with LLM
        print("\n--- Step 2: Enhanced Analysis ---")
        enhanced_analysis = enhance_analysis(
            result["analysis"], 
            result["analysis"]["transcription"], 
            video_type
        )
        
        # Save the enhanced analysis
        enhanced_path = os.path.splitext(result["analysis_path"])[0] + "_enhanced.json"
        with open(enhanced_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_analysis, f, indent=2, ensure_ascii=False)
        
        print(f"Enhanced analysis saved to: {enhanced_path}")
        
        # Add to RAG if requested
        if add_to_rag and HAS_RAG:
            print("\n--- Step 3: RAG Integration ---")
            
            # Create collection if it doesn't exist
            if 'create_collection_if_not_exists' in globals():
                create_collection_if_not_exists(collection_name)
            
            # Prepare document for RAG
            document = {
                "content": enhanced_analysis["transcription"],
                "metadata": {
                    "video_type": enhanced_analysis["video_type"],
                    "summary": enhanced_analysis["summary"],
                    "key_points": enhanced_analysis["key_points"],
                    "url": url,
                    "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
            # Add type-specific metadata
            if video_type == "trading_strategy" and "trading_details" in enhanced_analysis:
                document["metadata"]["trading_details"] = enhanced_analysis["trading_details"]
            elif video_type == "framework_tool" and "technical_details" in enhanced_analysis:
                document["metadata"]["technical_details"] = enhanced_analysis["technical_details"]
            
            # Add to knowledge base
            add_to_knowledge_base(document, collection_name)
            print(f"Analysis added to RAG collection: {collection_name}")
        
        # Generate a summary report
        print("\n--- Summary Report ---")
        print(f"Video URL: {url}")
        print(f"Video type: {VIDEO_TYPES.get(video_type, 'Unknown type')}")
        print(f"Video file: {os.path.basename(result['video_path'])}")
        print(f"Analysis file: {os.path.basename(enhanced_path)}")
        print(f"Summary: {enhanced_analysis['summary'][:200]}...")
        print(f"Key points: {len(enhanced_analysis['key_points'])}")
        
        if add_to_rag and HAS_RAG:
            print(f"Added to RAG collection: {collection_name}")
        
        return {
            "video_path": result["video_path"],
            "audio_path": result["audio_path"],
            "analysis_path": enhanced_path,
            "analysis": enhanced_analysis,
            "rag_integration": add_to_rag and HAS_RAG
        }
    
    except Exception as e:
        print(f"Error processing video: {str(e)}")
        raise

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Process YouTube videos")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--type", choices=VIDEO_TYPES.keys(), default="general",
                        help="Type of video content")
    parser.add_argument("--model", default="base",
                        help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--output-dir", default="./youtube_downloads",
                        help="Directory to save downloaded videos and analysis")
    parser.add_argument("--rag", action="store_true",
                        help="Add analysis to RAG system")
    parser.add_argument("--collection", default="youtube_videos",
                        help="RAG collection name")
    parser.add_argument("--llm", default="anthropic",
                        help="LLM provider for analysis (anthropic, openai, etc.)")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Process the video
    start_time = time.time()
    
    try:
        result = process_video(
            args.url,
            args.type,
            args.output_dir,
            args.model,
            args.rag,
            args.collection,
            args.llm
        )
        
        end_time = time.time()
        print(f"\nProcessing completed in {end_time - start_time:.2f} seconds")
        
        # Print summary information
        print("\nOutput files:")
        print(f"- Video: {result['video_path']}")
        print(f"- Audio: {result['audio_path']}")
        print(f"- Analysis: {result['analysis_path']}")
        
        # Print a sample of the analysis
        print("\nAnalysis summary:")
        print(f"{result['analysis']['summary'][:500]}...")
        
        print("\nTo view the full analysis, open the JSON file:")
        print(f"  {result['analysis_path']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 