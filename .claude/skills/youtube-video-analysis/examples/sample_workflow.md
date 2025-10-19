# Sample Workflow: Analyzing a Claude Skills Tutorial

## Scenario

You found a YouTube video titled "How to Create Effective Claude Skills" and want to extract knowledge from it to implement your own skills.

**Video URL**: `https://youtu.be/example456`

## Step-by-Step Process

### Step 1: Initiate Analysis

```python
from youtube_video_analysis import process_youtube_video

result = process_youtube_video(
    url_or_id="https://youtu.be/example456",
    video_type="framework_tool",
    model_size="base",
    output_dir="./youtube_analysis"
)
```

### Step 2: Download Video

```
--- Step 1: Download Video ---
Downloading: How to Create Effective Claude Skills
Download directory: C:\git\project\youtube_analysis
Download completed: C:\git\project\youtube_analysis\How to Create Effective Claude Skills.mp4
```

**Time**: ~30 seconds (depends on internet speed)

### Step 3: Extract Audio

```
--- Step 2: Extract Audio ---
Extracting audio from C:\git\project\youtube_analysis\How to Create Effective Claude Skills.mp4...
Audio extracted to C:\git\project\youtube_analysis\How to Create Effective Claude Skills.mp3
```

**Time**: ~10 seconds

### Step 4: Transcribe Audio

```
--- Step 3: Transcribe Audio ---
Transcribing audio C:\git\project\youtube_analysis\How to Create Effective Claude Skills.mp3...
Loading Whisper model (base)...
Whisper model loaded successfully.
Transcription completed: 8,432 characters
```

**Time**: ~40 seconds (CPU) or ~8 seconds (GPU)

### Step 5: Analyze Content

```
--- Step 4: Analyze Content ---
Analyzing transcription for video type: framework_tool
Using framework/tool analysis template
Using Claude API for analysis
```

**Time**: ~15 seconds

### Step 6: Save Results

```
--- Step 5: Save Results ---
Analysis saved to: C:\git\project\youtube_analysis\How to Create Effective Claude Skills.mp4_analysis.json

--- Summary Report ---
Video URL: https://youtu.be/example456
Video type: Framework or tool tutorial
Video file: How to Create Effective Claude Skills.mp4
Analysis file: How to Create Effective Claude Skills.mp4_analysis.json
Summary: This tutorial covers the fundamentals of creating effective Claude Skills, including the SKILL.md structure, YAML frontmatter requirements, progressive disclosure patterns, and best practices for organizing reference materials and examples...

Processing completed in 95.2 seconds
```

## Output Analysis

### Generated JSON Structure

```json
{
  "video_id": "example456",
  "video_url": "https://youtu.be/example456",
  "video_title": "How to Create Effective Claude Skills",
  "video_type": "framework_tool",
  "transcription": "Welcome to this tutorial on creating Claude Skills...",
  "analysis": {
    "tool_name": "Claude Skills",
    "summary": "Claude Skills are self-contained packages that extend Claude's capabilities...",
    "key_features": [
      "SKILL.md file with YAML frontmatter",
      "Progressive disclosure pattern",
      "Reference materials for detailed documentation",
      "Example files for practical demonstrations"
    ],
    "installation": [
      "Create .claude/skills/ directory",
      "Add SKILL.md file with proper structure",
      "Include reference/ and examples/ folders"
    ],
    "basic_usage": [
      "Define skill name and description in YAML",
      "Write clear instructions in markdown",
      "Specify when skill should be triggered"
    ],
    "code_examples": [
      "---\nname: my-skill\ndescription: Brief description\n---\n\n# My Skill\n\n## Instructions\n..."
    ]
  }
}
```

### Next Steps: Generate Implementation Tasks

```python
# Generate tasks from analysis
tasks = generate_tasks_from_analysis(result["analysis"], result["video_url"])

# Tasks created:
# 1. Create SKILL.md with YAML frontmatter
# 2. Add skill description and usage examples
# 3. Create reference/ folder with documentation
# 4. Add examples/ folder with sample files
# 5. Test skill with Claude
```

### Next Steps: Create Skill Template

```python
# Generate skill template from analysis
template = generate_skill_template(result["analysis"])

# Creates:
# .claude/skills/my-new-skill/SKILL.md
# .claude/skills/my-new-skill/reference/
# .claude/skills/my-new-skill/examples/
```

## Total Time Breakdown

- **Download**: 30 seconds
- **Audio Extraction**: 10 seconds
- **Transcription**: 40 seconds (CPU) or 8 seconds (GPU)
- **Analysis**: 15 seconds
- **Save Results**: <1 second

**Total (CPU)**: ~96 seconds (~1.6 minutes)  
**Total (GPU)**: ~64 seconds (~1 minute)

## Cost Breakdown

- **Download**: Free (YouTube)
- **Transcription**: Free (local Whisper)
- **Analysis**: ~$0.02 (Claude API, ~4K tokens)

**Total Cost**: ~$0.02 per video

## Tips for Best Results

1. **Choose the right video type**: Use `framework_tool` for tutorials, `trading_strategy` for trading videos, `general` for everything else

2. **Select appropriate model size**: Use `base` for general use, `small` for important content

3. **Check audio quality**: Videos with clear speech and minimal background noise work best

4. **Review and refine**: LLM analysis is good but not perfect - review and refine the output

5. **Cache results**: Save the analysis JSON for future reference

---

**Last Updated**: 2025-10-19  
**Example Type**: Framework/Tool Tutorial Analysis

