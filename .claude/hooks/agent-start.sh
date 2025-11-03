#!/bin/bash
# agent-start hook
# Triggered when an SDK agent starts processing
# Event data is passed as JSON via stdin

# Read event data
EVENT_DATA=$(cat)

# Extract fields
AGENT=$(echo "$EVENT_DATA" | jq -r '.agent' 2>/dev/null || echo "unknown")
TASK=$(echo "$EVENT_DATA" | jq -r '.data.context.task' 2>/dev/null || echo "unknown")
TIMESTAMP=$(echo "$EVENT_DATA" | jq -r '.timestamp' 2>/dev/null || echo "$(date -Iseconds)")

# Log agent start
LOG_DIR=".claude/logs"
mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] [START] Agent: $AGENT | Task: $TASK" >> "$LOG_DIR/agent_lifecycle.log"

# Optional: Validate prerequisites
# Example: Check if required services are running
# if ! pg_isready -h localhost > /dev/null 2>&1; then
#     echo "ERROR: PostgreSQL not running" >&2
#     exit 1
# fi

# Optional: Send notification
# if [ -n "$SLACK_WEBHOOK_URL" ]; then
#     curl -X POST -H 'Content-type: application/json' \
#          --data "{\"text\":\"Agent $AGENT started: $TASK\"}" \
#          "$SLACK_WEBHOOK_URL" 2>/dev/null
# fi

echo "[agent-start] Agent $AGENT started processing: $TASK"
exit 0
