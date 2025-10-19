# Video Types and Analysis Templates

## Supported Video Types

### 1. Trading Strategy (`trading_strategy`)

**Description**: Videos explaining trading strategies, technical analysis, or market analysis.

**Extracted Information**:
- Strategy name and overview
- Entry and exit criteria
- Technical indicators used
- Risk management rules
- Recommended timeframes
- Recommended markets
- Backtest results (if mentioned)
- Pros and cons

**Example Videos**:
- "RSI Divergence Strategy Explained"
- "How to Trade the Ichimoku Cloud"
- "Fibonacci Retracement Strategy"
- "Day Trading with MACD"

### 2. Framework/Tool Tutorial (`framework_tool`)

**Description**: Videos teaching technical frameworks, programming tools, or software.

**Extracted Information**:
- Tool/framework name and purpose
- Installation steps
- Basic usage examples
- Advanced features
- Code examples
- Best practices
- Limitations
- Alternatives
- Resources and documentation

**Example Videos**:
- "FastAPI Tutorial for Beginners"
- "React Hooks Explained"
- "Docker Compose Tutorial"
- "VS Code Extensions You Need"

### 3. General Educational Content (`general`)

**Description**: Any other educational or informational video.

**Extracted Information**:
- Content summary
- Key points and takeaways
- Main topics covered
- Insights and lessons
- Questions answered
- References and resources

**Example Videos**:
- "How Claude Skills Work"
- "Understanding Machine Learning"
- "Project Management Best Practices"
- "History of the Internet"

## Output Schemas

### Trading Strategy Schema

```json
{
  "strategy_name": "string",
  "summary": "string (max 200 words)",
  "key_points": ["string", "..."],
  "entry_criteria": ["string", "..."],
  "exit_criteria": ["string", "..."],
  "risk_management": ["string", "..."],
  "timeframes": ["string", "..."],
  "markets": ["string", "..."],
  "indicators": ["string", "..."],
  "pros": ["string", "..."],
  "cons": ["string", "..."],
  "backtest_results": "string (optional)",
  "implementation_notes": "string (optional)"
}
```

### Framework/Tool Schema

```json
{
  "tool_name": "string",
  "summary": "string (max 200 words)",
  "key_features": ["string", "..."],
  "installation": ["string", "..."],
  "basic_usage": ["string", "..."],
  "advanced_usage": ["string", "..."],
  "limitations": ["string", "..."],
  "alternatives": ["string", "..."],
  "use_cases": ["string", "..."],
  "code_examples": ["string", "..."],
  "best_practices": ["string", "..."],
  "resources": ["string", "..."]
}
```

### General Content Schema

```json
{
  "title": "string",
  "summary": "string (max 200 words)",
  "key_points": ["string", "..."],
  "topics": ["string", "..."],
  "insights": ["string", "..."],
  "questions_answered": ["string", "..."],
  "references": ["string", "..."],
  "action_items": ["string", "..."]
}
```

---

**Last Updated**: 2025-10-19

