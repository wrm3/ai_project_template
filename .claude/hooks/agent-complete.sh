#!/bin/bash
# agent-complete hook
# Triggered when an SDK agent completes processing
# Event data is passed as JSON via stdin

# Read event data
EVENT_DATA=$(cat)

# Extract fields
AGENT=$(echo "$EVENT_DATA" | jq -r '.agent' 2>/dev/null || echo "unknown")
TASK=$(echo "$EVENT_DATA" | jq -r '.data.context.task' 2>/dev/null || echo "unknown")
STATUS=$(echo "$EVENT_DATA" | jq -r '.data.result.status' 2>/dev/null || echo "unknown")
TIMESTAMP=$(echo "$EVENT_DATA" | jq -r '.timestamp' 2>/dev/null || echo "$(date -Iseconds)")

# Log agent completion
LOG_DIR=".claude/logs"
mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] [COMPLETE] Agent: $AGENT | Task: $TASK | Status: $STATUS" >> "$LOG_DIR/agent_lifecycle.log"

# Optional: Collect metrics
METRICS_DIR=".claude/metrics"
mkdir -p "$METRICS_DIR"

# Write completion event to metrics
echo "$EVENT_DATA" >> "$METRICS_DIR/agent_completions.jsonl"

# Extract performance metrics if available
FILES_CREATED=$(echo "$EVENT_DATA" | jq -r '.data.result.files_created // 0' 2>/dev/null)
TESTS_PASSING=$(echo "$EVENT_DATA" | jq -r '.data.result.tests_passing // false' 2>/dev/null)

echo "$(date -Iseconds),$AGENT,$STATUS,$FILES_CREATED,$TESTS_PASSING" >> "$METRICS_DIR/completions.csv"

# Optional: Send notification
# if [ "$STATUS" = "success" ] && [ -n "$SLACK_WEBHOOK_URL" ]; then
#     curl -X POST -H 'Content-type: application/json' \
#          --data "{\"text\":\"✓ Agent $AGENT completed: $TASK\"}" \
#          "$SLACK_WEBHOOK_URL" 2>/dev/null
# fi

echo "[agent-complete] Agent $AGENT completed: $TASK ($STATUS)"
exit 0
