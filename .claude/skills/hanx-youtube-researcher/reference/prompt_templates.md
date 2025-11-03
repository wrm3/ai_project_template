# Prompt Templates Reference

This document contains the complete prompt templates used by the Hanx YouTube Researcher skill. These templates are extracted from the hanx YouTube Researcher Agent (agent_youtube_researcher.py lines 109-199).

## General Analysis Prompt

**Purpose:** Comprehensive video analysis for any content type

**Use Case:** Educational videos, conference talks, interviews, product demos

**Fields Extracted:**
- `summary` - Concise overview of video content
- `key_points` - Main arguments or ideas presented
- `topics` - List of subjects discussed
- `insights` - Notable takeaways or observations
- `questions_answered` - Problems or questions addressed
- `references` - External sources, people, or concepts mentioned

**Prompt Template:**

```
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
{
  "summary": "...",
  "key_points": ["...", "..."],
  "topics": ["...", "..."],
  "insights": ["...", "..."],
  "questions_answered": ["...", "..."],
  "references": ["...", "..."]
}
```

**Expected Output Schema:**

```json
{
  "summary": "string",
  "key_points": ["string"],
  "topics": ["string"],
  "insights": ["string"],
  "questions_answered": ["string"],
  "references": ["string"]
}
```

## Trading Strategy Analysis Prompt

**Purpose:** Extract structured trading methodology information

**Use Case:** Trading strategy videos, technical analysis tutorials, indicator guides

**Fields Extracted:**
- `strategy_name` - Name or description of the strategy
- `markets` - Applicable markets (crypto, forex, stocks, etc.)
- `timeframes` - Recommended timeframes (1H, 4H, D1, etc.)
- `indicators` - Technical indicators used
- `entry_conditions` - Specific entry rules
- `exit_conditions` - Specific exit rules
- `risk_management` - Risk management principles
- `backtest_results` - Historical performance data
- `pros` - Advantages of the strategy
- `cons` - Disadvantages or limitations
- `key_insights` - Important notes or observations

**Prompt Template:**

```
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
{
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
}
```

**Expected Output Schema:**

```json
{
  "strategy_name": "string",
  "markets": ["string"],
  "timeframes": ["string"],
  "indicators": ["string"],
  "entry_conditions": ["string"],
  "exit_conditions": ["string"],
  "risk_management": ["string"],
  "backtest_results": "string",
  "pros": ["string"],
  "cons": ["string"],
  "key_insights": ["string"]
}
```

## Framework/Tool Analysis Prompt

**Purpose:** Extract technical documentation from framework/tool tutorials

**Use Case:** Framework tutorials, library demos, installation guides, technical walkthroughs

**Fields Extracted:**
- `tool_name` - Name of the tool or framework
- `purpose` - Problem the tool solves
- `target_users` - Intended audience
- `key_features` - Main capabilities
- `installation` - Setup and installation steps
- `basic_usage` - Getting started guide
- `advanced_features` - Advanced capabilities
- `limitations` - Constraints or drawbacks
- `alternatives` - Competing tools or frameworks
- `resources` - Documentation, links, repositories

**Prompt Template:**

```
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
{
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
}
```

**Expected Output Schema:**

```json
{
  "tool_name": "string",
  "purpose": "string",
  "target_users": ["string"],
  "key_features": ["string"],
  "installation": ["string"],
  "basic_usage": ["string"],
  "advanced_features": ["string"],
  "limitations": ["string"],
  "alternatives": ["string"],
  "resources": ["string"]
}
```

## Usage Guidelines

### Choosing the Right Prompt

**Use General Analysis when:**
- Video covers broad topics
- Content is conceptual/educational
- No specific methodology is presented
- Goal is knowledge extraction

**Use Trading Strategy Analysis when:**
- Video presents specific trading rules
- Technical indicators are discussed
- Entry/exit conditions are mentioned
- Risk management is covered

**Use Framework/Tool Analysis when:**
- Video demonstrates specific tool/framework
- Installation steps are provided
- Features are enumerated
- Code examples are shown

### Prompt Customization

These prompts are designed to work with most LLM providers. If customization is needed:

**Do:**
- Add more specific instructions for your domain
- Adjust JSON schema for additional fields
- Clarify ambiguous instructions
- Add examples in the prompt

**Don't:**
- Remove existing fields (breaks schema)
- Change field names (breaks templates)
- Make prompts too long (token limits)
- Remove JSON formatting instruction

### LLM Provider Compatibility

**Tested With:**
- OpenAI GPT-4 (recommended)
- OpenAI GPT-3.5-turbo (works well)
- Anthropic Claude 3 (excellent results)
- Anthropic Claude 2 (good results)

**Best Practices:**
- Use temperature 0.7 for balance of creativity and accuracy
- Increase max_tokens for longer videos (4000+ recommended)
- Enable JSON mode if provider supports it
- Retry on parse errors with adjusted prompt

### Error Handling

**Common Issues:**

1. **Non-JSON Response:**
   - LLM may include explanation before/after JSON
   - Solution: Extract JSON block with regex
   - Fallback: Return raw_response field

2. **Missing Fields:**
   - LLM may omit fields without data
   - Solution: Validate and add empty arrays/strings
   - Report: Log which fields were missing

3. **Incorrect Field Types:**
   - LLM may return string instead of array
   - Solution: Convert single strings to arrays
   - Validate: Check types match schema

## Version History

**v1.0.0 (2025-11-01):**
- Initial release
- Three prompt templates: general, trading, framework
- Extracted from hanx YouTube Researcher Agent
- Compatible with OpenAI and Anthropic LLMs

---

**Source:** research/hanx/hanx_tools/agent_youtube_researcher.py (lines 109-199)
**Last Updated:** 2025-11-01
**Schema Version:** 1.0.0
