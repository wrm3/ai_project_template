# Executor Agent

The `agent_executor.py` provides task execution and progress reporting capabilities for the Hanx multi-agent system. It handles implementation details, runs tests, and reports progress back to the Planner by updating the plan file.

## Basic Usage

### Command Line Interface

```bash
# Report task completion
python hanx_agents/agent_executor.py --task "Implemented YouTube video downloader" --update-section "Current Status / Progress Tracking" --content "Implemented the YouTube video downloader with error handling and retry mechanism"

# Report task in progress
python hanx_agents/agent_executor.py --task "Implementing transcription feature" --update-section "Current Status / Progress Tracking" --content "Working on the transcription feature using Whisper" --status "in progress"

# Request assistance
python hanx_agents/agent_executor.py --task "Transcription API integration" --update-section "Executor's Feedback or Assistance Requests" --content "I'm encountering rate limiting issues with the Whisper API. Should we implement a queue system or switch to a different provider?"
```

### Python API

```python
from hanx_agents.agent_executor import ExecutorAgent

# Create an executor agent
executor = ExecutorAgent()

# Report task completion
executor.report_progress(
    task_description="Implemented YouTube video downloader",
    status="completed"
)

# Request assistance
executor.request_assistance(
    request_description="I'm encountering rate limiting issues with the Whisper API. Should we implement a queue system or switch to a different provider?"
)

# Update a specific section directly
executor.update_plan_section(
    section_name="Current Status / Progress Tracking",
    content="✅ Implemented the YouTube video downloader with error handling and retry mechanism",
    replace=False  # Append to existing content
)
```

## Parameters

The Executor Agent accepts the following parameters:

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `task` | Description of the task being executed | None | Yes |
| `update-section` | Section of the plan file to update | None | Yes |
| `content` | Content to add to the section | None | Yes |
| `status` | Status of the task (completed, in progress, blocked) | completed | No |
| `replace` | Replace the section content instead of appending | False | No |

## How It Works

1. The Executor Agent reads the current plan status from `hanx_plan.md`
2. It identifies the specified section in the plan file
3. It updates the section with the provided content (either appending or replacing)
4. It writes the updated plan back to the file
5. The Planner Agent can then review the updates and respond accordingly

## Integration with Multi-Agent System

The Executor Agent is designed to work with the Planner Agent in a coordinated workflow:

1. The Planner Agent creates or updates the plan in `hanx_plan.md`
2. The Executor Agent reads the plan and executes specific tasks
3. The Executor Agent updates the plan with progress and feedback using:
   - "Current Status / Progress Tracking" section for task progress
   - "Executor's Feedback or Assistance Requests" section for questions or issues
4. The Planner Agent reviews the progress and updates the plan accordingly

## Status Indicators

The Executor Agent uses emoji indicators to show task status:

| Status | Emoji | Description |
|--------|-------|-------------|
| completed | ✅ | Task has been successfully completed |
| in progress | 🔄 | Task is currently being worked on |
| blocked | ❌ | Task is blocked and requires assistance |
| other | ⏳ | Any other status |

## Best Practices

1. **Regular Updates**: Provide frequent updates on task progress
2. **Clear Descriptions**: Make task descriptions and status updates clear and specific
3. **Appropriate Sections**: Use the correct section for different types of updates
4. **Contextual Information**: Include relevant context in assistance requests
5. **Incremental Progress**: Report progress incrementally rather than waiting for full completion

## Example Workflow

```bash
# Initial task progress report
python hanx_agents/agent_executor.py --task "YouTube downloader implementation" --update-section "Current Status / Progress Tracking" --content "Started implementing the YouTube downloader module" --status "in progress"

# Request for clarification
python hanx_agents/agent_executor.py --task "YouTube downloader implementation" --update-section "Executor's Feedback or Assistance Requests" --content "Should we support playlist downloads or just individual videos?"

# Final completion report
python hanx_agents/agent_executor.py --task "YouTube downloader implementation" --update-section "Current Status / Progress Tracking" --content "Completed the YouTube downloader with support for both individual videos and playlists"
```

## Troubleshooting

- **Section Not Found**: Ensure you're using the exact section names as defined in the plan file
- **File Not Found**: Verify that `hanx_plan.md` exists in the current directory
- **Content Not Updated**: Check if the update was successful by examining the plan file
- **Permission Issues**: Ensure you have write permissions for the plan file 