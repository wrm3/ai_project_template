#!/usr/bin/env python
"""
YouTube Harvester

A comprehensive tool for extracting, analyzing, and storing information from YouTube videos.
This script integrates the YouTube processor and analyzer to provide a complete workflow.

Usage:
    python youtube_harvester.py <youtube_url> --type <video_type> [options]

Example:
    python youtube_harvester.py https://youtu.be/Ecd3S-DXsjY --type trading_strategy
    python youtube_harvester.py https://youtu.be/H0NUYzN41Yo --type framework_tool --rag
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path to import from hanx_tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import YouTube processor and analyzer
try:
    from temp_tools.youtube_processor import YouTubeProcessor, VIDEO_TYPES
    from temp_tools.youtube_analyzer import enhance_analysis
except ImportError:
    print("Error: Required modules not found.")
    print("Make sure youtube_processor.py and youtube_analyzer.py are in the temp_tools directory.")
    sys.exit(1)

# Try to import RAG utilities if available
try:
    from rag_utils import add_to_knowledge_base, create_collection_if_not_exists
    HAS_RAG = True
except ImportError:
    HAS_RAG = False
    print("Warning: RAG utilities not found. RAG integration will be disabled.")

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