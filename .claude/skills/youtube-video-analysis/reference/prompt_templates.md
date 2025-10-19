# LLM Prompt Templates

## Trading Strategy Prompt

```
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
```

## Framework/Tool Prompt

```
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
```

## General Content Prompt

```
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
```

---

**Last Updated**: 2025-10-19  
**Source**: User's Hanx tools (youtube_harvest_data.py)

