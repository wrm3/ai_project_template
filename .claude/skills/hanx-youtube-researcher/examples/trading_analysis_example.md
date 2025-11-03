# Example: Trading Strategy Analysis

## Scenario

You found a YouTube video explaining a profitable RSI divergence strategy and want to extract the specific entry/exit rules and risk management parameters.

## Command

```bash
python specialized_analyzer.py \
    --url https://youtu.be/example_rsi_strategy \
    --type trading \
    --output ./trading_strategies
```

## Workflow

### Step 1: Transcript Extraction

```
================================================================================
STEP 1: Get Video Transcript
================================================================================

Running youtube-video-analysis skill...
Downloading video: https://youtu.be/example_rsi_strategy
Extracting audio...
Transcribing with Whisper (base model)...

[OK] Transcript loaded: 8,721 characters
```

### Step 2: Trading Strategy Analysis

```
================================================================================
STEP 2: Query LLM for Analysis
================================================================================

Using LLM provider: openai
Applying trading strategy analysis prompt template...
Extracting: entry conditions, exit conditions, indicators, risk management...

[OK] Received response: 1,823 characters
```

### Step 3: Save Results

```
================================================================================
STEP 3: Save Results
================================================================================

[OK] Saved JSON: ./trading_strategies/trading_analysis_20251101_140000.json
[OK] Saved Markdown: ./trading_strategies/trading_analysis_20251101_140000.md

Results saved to: ./trading_strategies
```

## Output: JSON

```json
{
  "video_url": "https://youtu.be/example_rsi_strategy",
  "analysis_type": "trading",
  "timestamp": "2025-11-01T14:00:00Z",
  "metadata": {
    "title": "RSI Divergence Strategy - 67% Win Rate",
    "duration": 982,
    "author": "Crypto Trading Academy"
  },
  "analysis": {
    "strategy_name": "RSI Divergence Reversal Strategy",
    "markets": [
      "Cryptocurrency (BTC, ETH)",
      "Forex (major pairs)",
      "Stock indices"
    ],
    "timeframes": [
      "1-hour (H1)",
      "4-hour (H4)",
      "Daily (D1)"
    ],
    "indicators": [
      "RSI (14 period)",
      "Volume indicator",
      "Support/Resistance levels",
      "200 EMA (trend filter)"
    ],
    "entry_conditions": [
      "Identify bullish divergence: price makes lower low, RSI makes higher low",
      "Wait for price to reach established support level",
      "Confirm RSI is below 30 (oversold)",
      "Volume spike on potential reversal candle",
      "Price above 200 EMA for bullish bias (optional filter)",
      "Enter on break above previous candle high"
    ],
    "exit_conditions": [
      "Take profit 1: RSI reaches 70 (overbought) - close 50% position",
      "Take profit 2: Price hits resistance level - close remaining 50%",
      "Stop loss: 2 ATR below entry (or 2-3% below entry price)",
      "Trailing stop: Once up 1:1, move stop to breakeven",
      "Time-based exit: Close if trade hasn't moved in 24-48 hours"
    ],
    "risk_management": [
      "Maximum 2% risk per trade",
      "Minimum 1:2 risk/reward ratio (target 1:3 or better)",
      "Position sizing based on ATR volatility",
      "Maximum 3 concurrent positions",
      "No trading during major news events",
      "Daily loss limit: 6% of account (stop trading for the day)"
    ],
    "backtest_results": "Backtested on BTC/USDT H4 from Jan 2023 - Oct 2025. 67% win rate over 103 trades. Average R:R 1:2.3. Maximum drawdown 18%. Profit factor 2.1.",
    "pros": [
      "Works well in ranging and trending markets",
      "Clear, objective entry and exit rules",
      "Good risk/reward ratio",
      "Can be automated with alerts",
      "Multiple confirmation signals reduce false entries"
    ],
    "cons": [
      "False divergences common in strong trends",
      "Requires patience - may wait days for setup",
      "Multiple indicators can lead to missed opportunities",
      "Subjective support/resistance identification",
      "Doesn't work well in low volatility periods"
    ],
    "key_insights": [
      "H4 timeframe shows best results - fewer false signals than H1",
      "200 EMA trend filter improved win rate by 12% but reduced trade frequency",
      "Volume confirmation is critical - divergences without volume often fail",
      "Most profitable during market transitions (consolidation to trend)",
      "Combine with higher timeframe analysis for context",
      "RSI divergence is early signal - price may continue against you briefly"
    ]
  }
}
```

## Output: Markdown

See `trading_analysis_template.md` for formatted output.

## Use Cases

**Trading Strategy Videos:**
- Technical analysis tutorials
- Strategy backtesting videos
- Trading indicator guides
- Risk management discussions
- Market analysis content

**When to Use:**
- You need specific entry/exit rules
- You want to document a strategy for backtesting
- You're building a strategy library
- You need risk management parameters

**Next Steps:**

1. **Validate Strategy:**
   - Verify backtest results independently
   - Check if strategy makes sense for your market
   - Assess if risk parameters fit your account size

2. **Implement:**
   - Code strategy for backtesting platform
   - Set up alerts for entry conditions
   - Create trading plan document
   - Test on demo account first

3. **Document:**
   - Add to personal strategy library
   - Note any modifications you make
   - Track performance over time
   - Refine based on results

**⚠️ Important Notes:**

- This is for educational purposes only - not financial advice
- Always backtest strategies yourself before trading
- Past performance doesn't guarantee future results
- Start with small position sizes when testing new strategies
- Never risk more than you can afford to lose
