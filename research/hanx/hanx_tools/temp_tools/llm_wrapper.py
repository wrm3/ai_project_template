"""
LLM API Wrapper for YouTube Harvester

This module provides a wrapper for the LLM API to use in the YouTube harvester.
It handles different LLM providers and fallbacks.
"""

import os
import sys
import json
import re

# Try to import the LLM API
HAS_LLM = False
try:
    # Try direct import
    from tools.llm_api import query_llm
    HAS_LLM = True
except ImportError:
    try:
        # Try relative import
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from tools.llm_api import query_llm
        HAS_LLM = True
    except ImportError:
        try:
            # Try with path manipulation
            tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools')
            sys.path.append(tools_dir)
            from llm_api import query_llm
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
        print(f"Error analyzing content: {e}")
        return fallback_analysis(content)

def analyze_trading_strategy(content):
    """
    Specialized analysis for trading strategy videos.
    
    Args:
        content (str): The transcription content to analyze
        
    Returns:
        dict: The analysis results with trading-specific information
    """
    try:
        if HAS_LLM:
            # Format the prompt for trading strategy analysis
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
            
            # Query the LLM
            response = query_llm(prompt, provider="anthropic")
            
            # Parse the response
            try:
                # Try to extract JSON from the response
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = response
                
                # Clean up the JSON string
                json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL)
                
                # Parse the JSON
                analysis = json.loads(json_str)
                
                # Add a summary
                if "summary" not in analysis:
                    analysis["summary"] = content[:200] + "..."
                
                return analysis
            except Exception as e:
                print(f"Error parsing LLM response: {e}")
                return fallback_trading_analysis(content)
        else:
            # Fallback to local analysis
            return fallback_trading_analysis(content)
    except Exception as e:
        print(f"Error analyzing trading strategy: {e}")
        return fallback_trading_analysis(content)

def analyze_framework_tool(content):
    """
    Specialized analysis for framework tool videos.
    
    Args:
        content (str): The transcription content to analyze
        
    Returns:
        dict: The analysis results with framework-specific information
    """
    try:
        if HAS_LLM:
            # Format the prompt for framework tool analysis
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
            
            # Query the LLM
            response = query_llm(prompt, provider="anthropic")
            
            # Parse the response
            try:
                # Try to extract JSON from the response
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = response
                
                # Clean up the JSON string
                json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL)
                
                # Parse the JSON
                analysis = json.loads(json_str)
                
                # Add a summary
                if "summary" not in analysis:
                    analysis["summary"] = content[:200] + "..."
                
                return analysis
            except Exception as e:
                print(f"Error parsing LLM response: {e}")
                return fallback_framework_analysis(content)
        else:
            # Fallback to local analysis
            return fallback_framework_analysis(content)
    except Exception as e:
        print(f"Error analyzing framework tool: {e}")
        return fallback_framework_analysis(content)

def parse_llm_response(response, content):
    """
    Parse the LLM response to extract structured data.
    
    Args:
        response (str): The LLM response
        content (str): The original content
        
    Returns:
        dict: The parsed response
    """
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response
        
        # Clean up the JSON string
        json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL)
        
        # Parse the JSON
        analysis = json.loads(json_str)
        
        # Add a summary if not present
        if "summary" not in analysis:
            analysis["summary"] = content[:200] + "..."
        
        return analysis
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return fallback_analysis(content)

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

def fallback_trading_analysis(content):
    """
    Fallback analysis for trading strategy videos when LLM API is not available.
    
    Args:
        content (str): The content to analyze
        
    Returns:
        dict: Basic trading strategy analysis results
    """
    # Extract the first 200 characters as a summary
    summary = content[:200] + "..."
    
    # Extract the first 5 sentences as key points
    sentences = re.split(r'[.!?]', content)
    key_points = [s.strip() for s in sentences[:5] if s.strip()]
    
    # Try to extract indicators using regex
    indicators = []
    indicator_patterns = [
        r'\b(RSI|Relative Strength Index)\b',
        r'\b(MACD|Moving Average Convergence Divergence)\b',
        r'\b(EMA|Exponential Moving Average)\b',
        r'\b(SMA|Simple Moving Average)\b',
        r'\b(Bollinger Bands)\b',
        r'\b(Stochastic)\b',
        r'\b(Fibonacci)\b',
        r'\b(ATR|Average True Range)\b',
        r'\b(ADX|Average Directional Index)\b',
        r'\b(Ichimoku)\b',
        r'\b(MFI|Money Flow Index)\b',
        r'\b(OBV|On-Balance Volume)\b',
        r'\b(CCI|Commodity Channel Index)\b',
        r'\b(Williams %R)\b',
        r'\b(Parabolic SAR)\b',
        r'\b(Pivot Points)\b',
        r'\b(Volume Profile)\b',
        r'\b(Oscillator)\b',
        r'\b(Momentum)\b',
        r'\b(Divergence)\b'
    ]
    
    for pattern in indicator_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        indicators.extend(matches)
    
    # Remove duplicates
    indicators = list(set(indicators))
    
    # Try to extract timeframes using regex
    timeframes = []
    timeframe_patterns = [
        r'\b(1 minute|1 min|1m|1M)\b',
        r'\b(5 minute|5 min|5m|5M)\b',
        r'\b(15 minute|15 min|15m|15M)\b',
        r'\b(30 minute|30 min|30m|30M)\b',
        r'\b(1 hour|1h|1H)\b',
        r'\b(4 hour|4h|4H)\b',
        r'\b(daily|1 day|1d|1D)\b',
        r'\b(weekly|1 week|1w|1W)\b',
        r'\b(monthly|1 month|1M)\b'
    ]
    
    for pattern in timeframe_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        timeframes.extend(matches)
    
    # Remove duplicates
    timeframes = list(set(timeframes))
    
    # Try to extract markets using regex
    markets = []
    market_patterns = [
        r'\b(forex|FX)\b',
        r'\b(stocks|stock market|equities)\b',
        r'\b(crypto|cryptocurrency|bitcoin|ethereum)\b',
        r'\b(futures|futures market)\b',
        r'\b(options|options market)\b',
        r'\b(commodities|commodity market)\b',
        r'\b(indices|index)\b',
        r'\b(bonds|bond market)\b',
        r'\b(ETFs|ETF)\b'
    ]
    
    for pattern in market_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        markets.extend(matches)
    
    # Remove duplicates
    markets = list(set(markets))
    
    # Return a basic trading strategy analysis
    return {
        "strategy_name": "Unknown Strategy",
        "market_instrument": markets if markets else "Unknown",
        "timeframe": timeframes if timeframes else "Unknown",
        "indicators_used": indicators if indicators else ["Unknown"],
        "entry_conditions": ["Basic analysis - no entry conditions extracted"],
        "exit_conditions": ["Basic analysis - no exit conditions extracted"],
        "risk_management": ["Basic analysis - no risk management extracted"],
        "backtest_results": None,
        "pros_and_cons": {
            "pros": ["Basic analysis - no pros extracted"],
            "cons": ["Basic analysis - no cons extracted"]
        },
        "key_insights": ["Basic analysis - no key insights extracted"],
        "summary": summary,
        "key_points": key_points
    }

def fallback_framework_analysis(content):
    """
    Fallback analysis for framework tool videos when LLM API is not available.
    
    Args:
        content (str): The content to analyze
        
    Returns:
        dict: Basic framework tool analysis results
    """
    # Extract the first 200 characters as a summary
    summary = content[:200] + "..."
    
    # Extract the first 5 sentences as key points
    sentences = re.split(r'[.!?]', content)
    key_points = [s.strip() for s in sentences[:5] if s.strip()]
    
    # Try to extract tool name using regex
    tool_name = None
    tool_name_patterns = [
        r'called\s+([A-Za-z0-9_-]+)',
        r'framework\s+([A-Za-z0-9_-]+)',
        r'tool\s+([A-Za-z0-9_-]+)',
        r'([A-Za-z0-9_-]+)\s+framework',
        r'([A-Za-z0-9_-]+)\s+tool'
    ]
    
    for pattern in tool_name_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            tool_name = matches[0]
            break
    
    # Try to extract installation steps
    installation_steps = []
    installation_patterns = [
        r'(pip install [A-Za-z0-9_-]+)',
        r'(npm install [A-Za-z0-9_-]+)',
        r'(git clone [A-Za-z0-9_-]+)',
        r'(docker run [A-Za-z0-9_-]+)',
        r'(brew install [A-Za-z0-9_-]+)'
    ]
    
    for pattern in installation_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        installation_steps.extend(matches)
    
    # Remove duplicates
    installation_steps = list(set(installation_steps))
    
    # Try to extract dependencies
    dependencies = []
    dependency_patterns = [
        r'(requires|need|dependency|dependencies|prerequisite|prerequisites)\s+([A-Za-z0-9_-]+)',
        r'(install|download)\s+([A-Za-z0-9_-]+)\s+(first|before)'
    ]
    
    for pattern in dependency_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if len(match) > 1:
                dependencies.append(match[1])
    
    # Remove duplicates
    dependencies = list(set(dependencies))
    
    # Return a basic framework tool analysis
    return {
        "tool_name": tool_name if tool_name else "Unknown Tool",
        "purpose": "Basic analysis - no purpose extracted",
        "target_users": "Basic analysis - no target users extracted",
        "key_features": ["Basic analysis - no key features extracted"],
        "installation_steps": installation_steps if installation_steps else ["Basic analysis - no installation steps extracted"],
        "usage_examples": ["Basic analysis - no usage examples extracted"],
        "dependencies": dependencies if dependencies else ["Basic analysis - no dependencies extracted"],
        "limitations": ["Basic analysis - no limitations extracted"],
        "alternatives": ["Basic analysis - no alternatives extracted"],
        "resources": ["Basic analysis - no resources extracted"],
        "summary": summary,
        "key_points": key_points
    } 