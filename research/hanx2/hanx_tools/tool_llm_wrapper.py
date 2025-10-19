"""
LLM API Wrapper for Content Analysis

This module provides a wrapper for the LLM API to analyze various types of content.
It handles different LLM providers and includes fallback mechanisms.
Part of the hanx_tools collection.
"""

import os
import sys
import json
import re

# Try to import the LLM API
HAS_LLM = False
try:
    # Try to import from hanx_apis
    from hanx_apis.api_llm import query_llm
    HAS_LLM = True
except ImportError:
    try:
        # Try relative import
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from hanx_apis.api_llm import query_llm
        HAS_LLM = True
    except ImportError:
        print("Warning: LLM API not found. Analysis will be limited.")
        HAS_LLM = False

def analyze_content(content, prompt_template):
    """
    Analyze content using the LLM API.
    
    Args:
        content (str): The content to analyze
        prompt_template (str): The prompt template to use for analysis
        
    Returns:
        dict: The analysis results
    """
    try:
        if HAS_LLM:
            # Format the prompt
            prompt = prompt_template.format(transcription=content)
            
            # Query the LLM
            response = query_llm(prompt, provider="anthropic")
            
            # Parse the response
            return parse_llm_response(response, content)
        else:
            # Fallback to local analysis
            return fallback_analysis(content)
    except Exception as e:
        print(f"Error during analysis: {e}")
        return fallback_analysis(content)

def analyze_trading_strategy(content):
    """
    Analyze a trading strategy using the LLM API.
    
    Args:
        content (str): The trading strategy content to analyze
        
    Returns:
        dict: The analysis results
    """
    prompt_template = """
    Analyze the following trading strategy transcription and extract key information:
    
    {transcription}
    
    Please provide a structured analysis with the following sections:
    1. Summary (2-3 sentences)
    2. Key Points (bullet points)
    3. Strategy Components (list the main components)
    4. Risk Management (identify risk management approaches)
    5. Market Conditions (when this strategy works best)
    6. Potential Improvements (suggestions to enhance the strategy)
    
    Format your response as JSON with the following structure:
    {
        "summary": "Brief summary here",
        "key_points": ["point 1", "point 2", ...],
        "strategy_components": ["component 1", "component 2", ...],
        "risk_management": ["approach 1", "approach 2", ...],
        "market_conditions": ["condition 1", "condition 2", ...],
        "potential_improvements": ["improvement 1", "improvement 2", ...]
    }
    """
    
    return analyze_content(content, prompt_template)

def analyze_framework_tool(content):
    """
    Analyze a framework or tool tutorial using the LLM API.
    
    Args:
        content (str): The framework/tool content to analyze
        
    Returns:
        dict: The analysis results
    """
    prompt_template = """
    Analyze the following framework/tool tutorial transcription and extract key information:
    
    {transcription}
    
    Please provide a structured analysis with the following sections:
    1. Summary (2-3 sentences)
    2. Key Points (bullet points)
    3. Main Features (list the main features)
    4. Use Cases (identify primary use cases)
    5. Installation/Setup (steps for installation if mentioned)
    6. Code Examples (extract any code examples)
    7. Best Practices (identify best practices mentioned)
    
    Format your response as JSON with the following structure:
    {
        "summary": "Brief summary here",
        "key_points": ["point 1", "point 2", ...],
        "main_features": ["feature 1", "feature 2", ...],
        "use_cases": ["use case 1", "use case 2", ...],
        "installation": ["step 1", "step 2", ...],
        "code_examples": ["example 1", "example 2", ...],
        "best_practices": ["practice 1", "practice 2", ...]
    }
    """
    
    return analyze_content(content, prompt_template)

def parse_llm_response(response, content):
    """
    Parse the LLM response into a structured format.
    
    Args:
        response (str): The LLM response
        content (str): The original content
        
    Returns:
        dict: The parsed response
    """
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'({[\s\S]*})', response)
        if json_match:
            json_str = json_match.group(1)
            return json.loads(json_str)
        
        # If no JSON found, return a basic structure
        return {
            "summary": response[:200] + "...",
            "key_points": [line.strip() for line in response.split('\n') if line.strip().startswith('-')],
            "topics": [],
            "insights": [],
            "questions_answered": [],
            "references": []
        }
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return fallback_analysis(content)

def fallback_analysis(content):
    """
    Perform a basic analysis when LLM is not available.
    
    Args:
        content (str): The content to analyze
        
    Returns:
        dict: The analysis results
    """
    # Split content into lines and filter out empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Extract potential key points (sentences ending with periods)
    key_points = []
    for line in lines[:20]:  # Look at first 20 lines
        sentences = line.split('.')
        for sentence in sentences:
            if len(sentence.strip()) > 30:  # Only consider substantial sentences
                key_points.append(sentence.strip())
    
    # Limit to 5 key points
    key_points = key_points[:5]
    
    # Create a basic summary (first 200 chars)
    summary = content[:200] + "..." if len(content) > 200 else content
    
    # Return the analysis
    return {
        "summary": summary,
        "key_points": key_points,
        "topics": [],
        "insights": [],
        "questions_answered": [],
        "references": []
    }

def fallback_trading_analysis(content):
    """
    Perform a basic trading strategy analysis when LLM is not available.
    
    Args:
        content (str): The trading strategy content to analyze
        
    Returns:
        dict: The analysis results
    """
    # Get basic analysis
    basic = fallback_analysis(content)
    
    # Look for trading-related keywords
    trading_keywords = [
        "buy", "sell", "trade", "market", "stock", "forex", "crypto", "cryptocurrency",
        "bitcoin", "ethereum", "indicator", "chart", "candle", "pattern", "support",
        "resistance", "trend", "breakout", "reversal", "bullish", "bearish",
        "long", "short", "position", "entry", "exit", "stop loss", "take profit",
        "risk", "reward", "ratio", "volatility", "volume", "liquidity", "timeframe"
    ]
    
    # Extract strategy components
    strategy_components = []
    for keyword in trading_keywords:
        if keyword in content.lower():
            # Find the sentence containing the keyword
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            if sentences:
                strategy_components.append(sentences[0].strip().capitalize())
    
    # Limit to 5 components
    strategy_components = list(set(strategy_components))[:5]
    
    # Extract risk management approaches
    risk_keywords = ["stop loss", "risk", "manage", "management", "position size", "leverage"]
    risk_management = []
    for keyword in risk_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            if sentences:
                risk_management.append(sentences[0].strip().capitalize())
    
    # Limit to 3 risk approaches
    risk_management = list(set(risk_management))[:3]
    
    # Extract market conditions
    market_keywords = ["trend", "ranging", "volatile", "quiet", "bullish", "bearish", "momentum"]
    market_conditions = []
    for keyword in market_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            if sentences:
                market_conditions.append(sentences[0].strip().capitalize())
    
    # Limit to 3 market conditions
    market_conditions = list(set(market_conditions))[:3]
    
    # Return the analysis
    return {
        "summary": basic["summary"],
        "key_points": basic["key_points"],
        "strategy_components": strategy_components,
        "risk_management": risk_management,
        "market_conditions": market_conditions,
        "potential_improvements": ["Consider backtesting this strategy", "Add more specific entry/exit rules", "Define position sizing more clearly"]
    }

def fallback_framework_analysis(content):
    """
    Perform a basic framework/tool analysis when LLM is not available.
    
    Args:
        content (str): The framework/tool content to analyze
        
    Returns:
        dict: The analysis results
    """
    # Get basic analysis
    basic = fallback_analysis(content)
    
    # Look for code examples
    code_examples = re.findall(r'```[\s\S]*?```', content)
    if not code_examples:
        # Try to find code-like text
        code_examples = re.findall(r'(?:import|from|def|class|function|var|let|const)[\s\S]*?(?:\n\n|\Z)', content)
    
    # Limit to 3 code examples
    code_examples = [example.strip() for example in code_examples][:3]
    
    # Look for installation steps
    install_keywords = ["install", "setup", "configure", "pip", "npm", "yarn", "apt", "brew"]
    installation = []
    for keyword in install_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            for sentence in sentences:
                if len(sentence) > 10:
                    installation.append(sentence.strip().capitalize())
    
    # Limit to 3 installation steps
    installation = list(set(installation))[:3]
    
    # Look for features
    feature_keywords = ["feature", "capability", "function", "method", "api", "interface"]
    main_features = []
    for keyword in feature_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            for sentence in sentences:
                if len(sentence) > 10:
                    main_features.append(sentence.strip().capitalize())
    
    # Limit to 5 features
    main_features = list(set(main_features))[:5]
    
    # Look for use cases
    usecase_keywords = ["use case", "example", "scenario", "application", "usage"]
    use_cases = []
    for keyword in usecase_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            for sentence in sentences:
                if len(sentence) > 10:
                    use_cases.append(sentence.strip().capitalize())
    
    # Limit to 3 use cases
    use_cases = list(set(use_cases))[:3]
    
    # Look for best practices
    practice_keywords = ["best practice", "recommend", "should", "tip", "advice"]
    best_practices = []
    for keyword in practice_keywords:
        if keyword in content.lower():
            sentences = re.findall(r'[^.!?]*' + keyword + r'[^.!?]*[.!?]', content.lower())
            for sentence in sentences:
                if len(sentence) > 10:
                    best_practices.append(sentence.strip().capitalize())
    
    # Limit to 3 best practices
    best_practices = list(set(best_practices))[:3]
    
    # Return the analysis
    return {
        "summary": basic["summary"],
        "key_points": basic["key_points"],
        "main_features": main_features,
        "use_cases": use_cases,
        "installation": installation,
        "code_examples": code_examples,
        "best_practices": best_practices
    } 