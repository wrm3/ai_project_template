"""
YouTube Video Content Analyzer

This module provides LLM-based analysis of YouTube video transcriptions,
with specialized processing for different video types:
1. Trading strategy videos - Extract key strategies, risk management approaches, etc.
2. Framework/tool tutorials - Extract technical details, installation steps, etc.
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional

# Add parent directory to path to import from hanx_tools
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try to import LLM API
try:
    from llm_api import query_llm
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    print("Warning: LLM API not found. Using mock analysis.")

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

# Mock analysis for when LLM is not available
MOCK_ANALYSIS = {
    "trading_strategy": {
        "summary": "This is a mock analysis of a trading strategy video.",
        "key_points": ["Mock key point 1", "Mock key point 2"],
        "entry_criteria": ["Mock entry criterion"],
        "exit_criteria": ["Mock exit criterion"],
        "risk_management": ["Mock risk management approach"],
        "timeframes": ["Daily", "4-hour"],
        "markets": ["Forex", "Crypto"],
        "indicators": ["RSI", "MACD"],
        "pros": ["Mock advantage"],
        "cons": ["Mock disadvantage"]
    },
    "framework_tool": {
        "summary": "This is a mock analysis of a framework/tool tutorial.",
        "key_features": ["Mock feature 1", "Mock feature 2"],
        "installation": ["Mock installation step"],
        "basic_usage": ["Mock basic usage example"],
        "advanced_usage": ["Mock advanced usage example"],
        "limitations": ["Mock limitation"],
        "alternatives": ["Mock alternative"],
        "use_cases": ["Mock use case"],
        "code_examples": ["Mock code example"]
    },
    "general": {
        "summary": "This is a mock analysis of a general video.",
        "key_points": ["Mock key point 1", "Mock key point 2"],
        "topics": ["Mock topic 1", "Mock topic 2"],
        "insights": ["Mock insight"],
        "questions_answered": ["Mock question"],
        "references": ["Mock reference"]
    }
}

def get_prompt_for_video_type(video_type: str, transcription: str) -> str:
    """
    Get the appropriate prompt template for the video type.
    
    Args:
        video_type: Type of video (trading_strategy, framework_tool, general)
        transcription: Video transcription
        
    Returns:
        str: Formatted prompt
    """
    if video_type == "trading_strategy":
        return TRADING_STRATEGY_PROMPT.format(transcription=transcription)
    elif video_type == "framework_tool":
        return FRAMEWORK_TOOL_PROMPT.format(transcription=transcription)
    else:
        return GENERAL_PROMPT.format(transcription=transcription)

def analyze_with_llm(transcription: str, video_type: str = "general", 
                    provider: str = "anthropic", max_tokens: int = 2000) -> Dict[str, Any]:
    """
    Analyze video transcription using LLM.
    
    Args:
        transcription: Video transcription
        video_type: Type of video content
        provider: LLM provider (anthropic, openai, etc.)
        max_tokens: Maximum tokens for LLM response
        
    Returns:
        Dict: Analysis result
    """
    if not HAS_LLM:
        print("LLM API not available. Using mock analysis.")
        return MOCK_ANALYSIS[video_type]
    
    try:
        print(f"Analyzing {video_type} video with LLM ({provider})...")
        
        # Get the appropriate prompt
        prompt = get_prompt_for_video_type(video_type, transcription)
        
        # Query the LLM
        response = query_llm(prompt, provider=provider, max_tokens=max_tokens)
        
        # Parse the JSON response
        try:
            # Try to extract JSON from the response
            # First, look for JSON block
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            analysis = json.loads(json_str)
            print("LLM analysis completed successfully.")
            return analysis
        
        except json.JSONDecodeError:
            print("Error parsing LLM response as JSON. Using mock analysis.")
            return MOCK_ANALYSIS[video_type]
    
    except Exception as e:
        print(f"Error analyzing with LLM: {str(e)}")
        return MOCK_ANALYSIS[video_type]

def enhance_analysis(analysis: Dict[str, Any], transcription: str, video_type: str = "general") -> Dict[str, Any]:
    """
    Enhance the basic analysis with LLM-generated insights.
    
    Args:
        analysis: Basic analysis from YouTubeProcessor
        transcription: Video transcription
        video_type: Type of video content
        
    Returns:
        Dict: Enhanced analysis
    """
    try:
        print(f"Enhancing analysis for {video_type} video...")
        
        # Get LLM analysis
        llm_analysis = analyze_with_llm(transcription, video_type)
        
        # Merge the analyses
        enhanced = analysis.copy()
        
        # Update with LLM analysis
        if video_type == "trading_strategy":
            enhanced.update({
                "summary": llm_analysis.get("summary", ""),
                "key_points": llm_analysis.get("key_points", []),
                "trading_details": {
                    "entry_criteria": llm_analysis.get("entry_criteria", []),
                    "exit_criteria": llm_analysis.get("exit_criteria", []),
                    "risk_management": llm_analysis.get("risk_management", []),
                    "timeframes": llm_analysis.get("timeframes", []),
                    "markets": llm_analysis.get("markets", []),
                    "indicators": llm_analysis.get("indicators", []),
                    "pros": llm_analysis.get("pros", []),
                    "cons": llm_analysis.get("cons", [])
                }
            })
        
        elif video_type == "framework_tool":
            enhanced.update({
                "summary": llm_analysis.get("summary", ""),
                "key_points": llm_analysis.get("key_features", []),
                "technical_details": {
                    "installation": llm_analysis.get("installation", []),
                    "basic_usage": llm_analysis.get("basic_usage", []),
                    "advanced_usage": llm_analysis.get("advanced_usage", []),
                    "limitations": llm_analysis.get("limitations", []),
                    "alternatives": llm_analysis.get("alternatives", []),
                    "use_cases": llm_analysis.get("use_cases", []),
                    "code_examples": llm_analysis.get("code_examples", [])
                }
            })
        
        else:  # general
            enhanced.update({
                "summary": llm_analysis.get("summary", ""),
                "key_points": llm_analysis.get("key_points", []),
                "topics": llm_analysis.get("topics", []),
                "insights": llm_analysis.get("insights", []),
                "questions_answered": llm_analysis.get("questions_answered", []),
                "references": llm_analysis.get("references", [])
            })
        
        print("Analysis enhancement completed.")
        return enhanced
    
    except Exception as e:
        print(f"Error enhancing analysis: {str(e)}")
        return analysis

# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze YouTube video transcription")
    parser.add_argument("input_file", help="Path to transcription or analysis JSON file")
    parser.add_argument("--type", choices=["trading_strategy", "framework_tool", "general"], 
                        default="general", help="Type of video content")
    parser.add_argument("--provider", default="anthropic", 
                        help="LLM provider (anthropic, openai, etc.)")
    parser.add_argument("--output", help="Path to save enhanced analysis")
    
    args = parser.parse_args()
    
    # Load input file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if input is a transcription or an analysis
    if "transcription" in data:
        # Input is an analysis with transcription
        transcription = data["transcription"]
        enhanced = enhance_analysis(data, transcription, args.type)
    else:
        # Input is just a transcription
        transcription = data["text"] if "text" in data else json.dumps(data)
        analysis = {
            "video_type": args.type,
            "transcription": transcription,
            "timestamps": []
        }
        enhanced = enhance_analysis(analysis, transcription, args.type)
    
    # Save enhanced analysis
    output_path = args.output or f"enhanced_{args.type}_{int(time.time())}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enhanced, f, indent=2, ensure_ascii=False)
    
    print(f"Enhanced analysis saved to {output_path}") 