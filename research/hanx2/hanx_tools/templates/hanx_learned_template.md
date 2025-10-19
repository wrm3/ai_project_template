# Lessons Learned

## Environment and Setup
- You have a uv python venv in ./.venv. Always use it when running python scripts. It's a uv venv, so use `uv pip install` to install packages. And you need to activate it first. When you see errors like `no such file or directory: .venv/bin/uv`, that means you didn't activate the venv.
- The project has a uv virtual environment in ./.uv-venv. Use the uv.bat script to manage it: `uv.bat activate` to activate, `uv.bat add <package>` to add packages.
- When running Python scripts that import from other local modules, use `PYTHONPATH=.` to ensure Python can find the modules. For example: `PYTHONPATH=. python hanx_tools/plan_exec_llm.py` instead of just `python hanx_tools/plan_exec_llm.py`. This is especially important when using relative imports.

## Best Practices
- Include info useful for debugging in the program output.
- Read the file before you try to edit it.
- Add debug information to stderr while keeping the main output clean in stdout for better pipeline integration
- For search results, ensure proper handling of different character encodings (UTF-8) for international queries

## Git and Version Control
- Due to Cursor's limit, when you use `git` and `gh` and need to submit a multiline commit message, first write the message in a file, and then use `git commit -F <filename>` or similar command to commit. And then remove the file. Include "[Cursor] " in the commit message and PR title.

## Model Usage
- Use `gpt-4o` as the model name for OpenAI. It is the latest GPT model and has vision capabilities as well. `o1` is the most advanced and expensive model from OpenAI. Use it when you need to do reasoning, planning, or get blocked.
- Use `claude-3-5-sonnet-20241022` as the model name for Claude. It is the latest Claude model and has vision capabilities as well.

## Library-Specific Notes
- When using seaborn styles in matplotlib, use 'seaborn-v0_8' instead of 'seaborn' as the style name due to recent seaborn version changes

## Tool Documentation

### Multi-Agent System
- The multi-agent system consists of a Planner and an Executor
- The Planner uses the `hanx_tools/plan_exec_llm.py` tool to generate plans
- The Executor executes the plans and reports back to the Planner
- Communication happens through the `hanx_plan.md` file

### YouTube Data Extraction
- The `hanx_tools/youtube_harvest_data.py` tool can download and analyze YouTube videos
- It supports different types of analysis for general videos, trading strategies, and framework tutorials
- Dependencies: pytubefix, moviepy, whisper (optional)

### UV Dependency Management
- The project uses UV for dependency management
- Use `uv.bat` (Windows) or `uv.sh` (Unix) to manage dependencies
- Commands: setup, create, compile, sync, add, activate, run

## Lessons
- Add your own lessons here as you learn them 