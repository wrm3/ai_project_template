#!/bin/bash
# agent-error hook
# Triggered when an SDK agent encounters an error
# Event data is passed as JSON via stdin

# Read event data
EVENT_DATA=$(cat)

# Extract fields
AGENT=$(echo "$EVENT_DATA" | jq -r '.agent' 2>/dev/null || echo "unknown")
TASK=$(echo "$EVENT_DATA" | jq -r '.data.context.task' 2>/dev/null || echo "unknown")
ERROR=$(echo "$EVENT_DATA" | jq -r '.data.error' 2>/dev/null || echo "unknown error")
TIMESTAMP=$(echo "$EVENT_DATA" | jq -r '.timestamp' 2>/dev/null || echo "$(date -Iseconds)")

# Log error
LOG_DIR=".claude/logs"
mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] [ERROR] Agent: $AGENT | Task: $TASK | Error: $ERROR" >> "$LOG_DIR/agent_lifecycle.log"
echo "[$TIMESTAMP] [ERROR] Agent: $AGENT | Task: $TASK | Error: $ERROR" >> "$LOG_DIR/agent_errors.log"

# Optional: Collect error metrics
METRICS_DIR=".claude/metrics"
mkdir -p "$METRICS_DIR"

echo "$EVENT_DATA" >> "$METRICS_DIR/agent_errors.jsonl"
echo "$(date -Iseconds),$AGENT,error,$ERROR" >> "$METRICS_DIR/errors.csv"

# Optional: Send alert notification
# if [ -n "$SLACK_WEBHOOK_URL" ]; then
#     curl -X POST -H 'Content-type: application/json' \
#          --data "{\"text\":\"⚠️ Agent $AGENT error: $TASK - $ERROR\"}" \
#          "$SLACK_WEBHOOK_URL" 2>/dev/null
# fi

# Optional: Send email alert for critical errors
# if [ -n "$ADMIN_EMAIL" ]; then
#     echo "Agent: $AGENT\nTask: $TASK\nError: $ERROR\nTimestamp: $TIMESTAMP" | \
#          mail -s "Agent Error Alert" "$ADMIN_EMAIL"
# fi

echo "[agent-error] Agent $AGENT encountered error: $ERROR" >&2
exit 0
