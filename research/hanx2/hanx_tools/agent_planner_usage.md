# Planner Agent

The `agent_planner.py` provides high-level planning capabilities for the Hanx multi-agent system. It analyzes the current plan status, breaks down tasks, defines success criteria, and evaluates progress using a high-intelligence model (OpenAI o1 by default).

## Basic Usage

### Command Line Interface

```bash
# Basic planning with a prompt
python hanx_agents/agent_planner.py --prompt "Create a Python script that downloads YouTube videos and transcribes them"

# Include a file in the context
python hanx_agents/agent_planner.py --prompt "Analyze this code and suggest improvements" --file path/to/code.py

# Use a different LLM provider
python hanx_agents/agent_planner.py --prompt "Design a database schema for a social media app" --provider anthropic

# Specify a particular model
python hanx_agents/agent_planner.py --prompt "Create a test plan for this API" --provider openai --model gpt-4o
```

### Python API

```python
from hanx_agents.agent_planner import PlannerAgent

# Create a planner agent
planner = PlannerAgent()

# Run with just a prompt
response = planner.run({
    "prompt": "Create a Python script that downloads YouTube videos and transcribes them"
})
print(response)

# Run with a file and specific provider
response = planner.run({
    "prompt": "Analyze this code and suggest improvements",
    "file": "path/to/code.py",
    "provider": "anthropic"
})
print(response)
```

## Parameters

The Planner Agent accepts the following parameters:

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `prompt` | The planning prompt to send to the LLM | None | Yes |
| `file` | Path to a file to include in the context | None | No |
| `provider` | LLM provider to use (openai, anthropic, gemini, deepseek, local) | openai | No |
| `model` | Specific model to use (provider-dependent) | None | No |

## How It Works

1. The Planner Agent reads the current plan status from `hanx_plan.md`
2. If a file is provided, it reads the file content
3. It constructs a prompt that includes:
   - The current plan content
   - The file content (if provided)
   - The user's planning prompt
4. It sends this prompt to the specified LLM provider
5. The LLM analyzes the plan and provides recommendations
6. The response is returned to the caller

## Integration with Multi-Agent System

The Planner Agent is designed to work with the Executor Agent in a coordinated workflow:

1. The Planner Agent creates or updates the plan in `hanx_plan.md`
2. The Executor Agent reads the plan and executes specific tasks
3. The Executor Agent updates the plan with progress and feedback
4. The Planner Agent reviews the progress and updates the plan accordingly

## Best Practices

1. **Be Specific**: Provide clear, specific prompts to get the best results
2. **Include Context**: When relevant, include file content to give the Planner more context
3. **Review Responses**: Always review the Planner's recommendations before implementing them
4. **Iterative Planning**: Use the Planner Agent iteratively as the project progresses
5. **Provider Selection**: Different LLM providers have different strengths; choose based on your needs

## Example Workflow

```bash
# Initial planning
python hanx_agents/agent_planner.py --prompt "Create a Python script that downloads YouTube videos and transcribes them"

# After some implementation, get feedback on the code
python hanx_agents/agent_planner.py --prompt "Review this implementation and suggest improvements" --file youtube_downloader.py

# After addressing feedback, plan the next phase
python hanx_agents/agent_planner.py --prompt "Now that we have the basic downloader working, plan how to add batch processing capabilities"
```

## Troubleshooting

- **Empty or Irrelevant Responses**: Try being more specific in your prompt or providing more context
- **Model Limitations**: If you're hitting limitations with one provider, try another
- **File Not Found**: Ensure file paths are correct and accessible
- **Plan File Issues**: If the `hanx_plan.md` file is missing or corrupted, the Planner will start with an empty plan 