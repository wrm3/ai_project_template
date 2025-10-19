"""
YouTube Video Processor

This module provides functionality for:
1. Downloading YouTube videos
2. Transcribing video content
3. Analyzing and summarizing video content
4. Integrating with RAG systems

It supports different processing workflows based on video content type:
- Trading strategy videos: Summarized for key points and strategies
- Framework/tool videos: Analyzed for technical details and integrated with RAG
"""

import os
import sys
import json
import time
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any

# Import required libraries
try:
    from pytubefix import YouTube
    import whisper
    from moviepy.editor import VideoFileClip
    from pydub import AudioSegment
except ImportError:
    print("Required libraries not found. Please install with:")
    print("pip install pytubefix whisper openai-whisper moviepy pydub")
    sys.exit(1)

# Add parent directory to path to import from hanx_tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try to import RAG utilities if available
try:
    from rag_utils import add_to_knowledge_base
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    print("Warning: RAG utilities not found. RAG integration will be disabled.")

# Constants
DEFAULT_DOWNLOAD_DIR = "./youtube_downloads"
DEFAULT_MODEL_SIZE = "base"  # Options: tiny, base, small, medium, large
VIDEO_TYPES = {
    "trading_strategy": "Trading strategy video",
    "framework_tool": "Framework or tool tutorial",
    "general": "General content"
}

class YouTubeProcessor:
    """
    A class for processing YouTube videos, including downloading, transcription,
    and analysis.
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
        self.whisper_model = None
        
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        print(f"YouTube Processor initialized with download directory: {os.path.abspath(download_dir)}")
        print(f"Using Whisper model size: {model_size}")
    
    def _load_whisper_model(self):
        """Load the Whisper model for transcription."""
        if self.whisper_model is None:
            print(f"Loading Whisper model ({self.model_size})...")
            self.whisper_model = whisper.load_model(self.model_size)
            print("Whisper model loaded successfully.")
    
    def download_video(self, url: str) -> str:
        """
        Download a YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            str: Path to the downloaded video file
        """
        try:
            yt = YouTube(url)
            print(f"Downloading: {yt.title}")
            
            # Get highest quality progressive stream
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            # Download the video
            video_path = stream.download(output_path=self.download_dir)
            print(f"Download completed: {video_path}")
            
            return video_path
        
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            raise
    
    def extract_audio(self, video_path: str) -> str:
        """
        Extract audio from a video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        try:
            print(f"Extracting audio from {video_path}...")
            
            # Create a temporary file for the audio
            audio_path = os.path.splitext(video_path)[0] + ".mp3"
            
            # Extract audio using moviepy
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            
            print(f"Audio extracted to {audio_path}")
            return audio_path
        
        except Exception as e:
            print(f"Error extracting audio: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dict: Transcription result
        """
        try:
            print(f"Transcribing audio {audio_path}...")
            
            # Load the Whisper model
            self._load_whisper_model()
            
            # Transcribe the audio
            result = self.whisper_model.transcribe(audio_path)
            
            print(f"Transcription completed: {len(result['text'])} characters")
            return result
        
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            raise
    
    def analyze_content(self, transcription: Dict[str, Any], video_type: str = "general") -> Dict[str, Any]:
        """
        Analyze the transcribed content based on video type.
        
        Args:
            transcription: Transcription result from Whisper
            video_type: Type of video content (trading_strategy, framework_tool, general)
            
        Returns:
            Dict: Analysis result
        """
        try:
            print(f"Analyzing content as {VIDEO_TYPES.get(video_type, 'Unknown type')}...")
            
            # Basic analysis structure
            analysis = {
                "video_type": video_type,
                "transcription": transcription["text"],
                "summary": "",
                "key_points": [],
                "technical_details": {},
                "timestamps": []
            }
            
            # Extract timestamps from segments
            for segment in transcription["segments"]:
                analysis["timestamps"].append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                })
            
            # TODO: Implement more sophisticated analysis based on video type
            # This would typically involve using an LLM to analyze the content
            
            print(f"Content analysis completed for {video_type} video")
            return analysis
        
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            raise
    
    def save_analysis(self, analysis: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """
        Save the analysis to a JSON file.
        
        Args:
            analysis: Analysis result
            output_path: Path to save the analysis (optional)
            
        Returns:
            str: Path to the saved analysis file
        """
        if output_path is None:
            # Generate a filename based on video type
            filename = f"analysis_{analysis['video_type']}_{int(time.time())}.json"
            output_path = os.path.join(self.download_dir, filename)
        
        try:
            print(f"Saving analysis to {output_path}...")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"Analysis saved to {output_path}")
            return output_path
        
        except Exception as e:
            print(f"Error saving analysis: {str(e)}")
            raise
    
    def add_to_rag(self, analysis: Dict[str, Any], collection_name: str = "youtube_videos") -> bool:
        """
        Add the analysis to the RAG system.
        
        Args:
            analysis: Analysis result
            collection_name: Name of the RAG collection
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not HAS_RAG:
            print("RAG integration is not available.")
            return False
        
        try:
            print(f"Adding analysis to RAG collection '{collection_name}'...")
            
            # Prepare document for RAG
            document = {
                "content": analysis["transcription"],
                "metadata": {
                    "video_type": analysis["video_type"],
                    "summary": analysis["summary"],
                    "key_points": analysis["key_points"],
                    "technical_details": analysis["technical_details"]
                }
            }
            
            # Add to knowledge base
            add_to_knowledge_base(document, collection_name)
            
            print(f"Analysis added to RAG collection '{collection_name}'")
            return True
        
        except Exception as e:
            print(f"Error adding to RAG: {str(e)}")
            return False
    
    def process_video(self, url: str, video_type: str = "general", 
                     add_to_rag: bool = False, collection_name: str = "youtube_videos") -> Dict[str, Any]:
        """
        Process a YouTube video: download, transcribe, analyze, and optionally add to RAG.
        
        Args:
            url: YouTube video URL
            video_type: Type of video content
            add_to_rag: Whether to add the analysis to RAG
            collection_name: Name of the RAG collection
            
        Returns:
            Dict: Analysis result
        """
        try:
            # Download the video
            video_path = self.download_video(url)
            
            # Extract audio
            audio_path = self.extract_audio(video_path)
            
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

# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process YouTube videos")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--type", choices=VIDEO_TYPES.keys(), default="general",
                        help="Type of video content")
    parser.add_argument("--model", default=DEFAULT_MODEL_SIZE,
                        help="Whisper model size (tiny, base, small, medium, large)")
    parser.add_argument("--output-dir", default=DEFAULT_DOWNLOAD_DIR,
                        help="Directory to save downloaded videos and analysis")
    parser.add_argument("--rag", action="store_true",
                        help="Add analysis to RAG system")
    parser.add_argument("--collection", default="youtube_videos",
                        help="RAG collection name")
    
    args = parser.parse_args()
    
    processor = YouTubeProcessor(download_dir=args.output_dir, model_size=args.model)
    
    start_time = time.time()
    result = processor.process_video(args.url, args.type, args.rag, args.collection)
    end_time = time.time()
    
    print(f"\nProcessing completed in {end_time - start_time:.2f} seconds")
    print(f"Video saved to: {result['video_path']}")
    print(f"Analysis saved to: {result['analysis_path']}")
    
    if args.rag:
        print(f"Analysis added to RAG collection: {args.collection}") 