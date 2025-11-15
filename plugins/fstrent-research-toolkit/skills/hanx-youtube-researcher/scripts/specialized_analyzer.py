#!/usr/bin/env python3
"""
Specialized YouTube Video Analyzer
Performs domain-specific analysis using structured prompts from hanx YouTube Researcher Agent

Supports three analysis types:
1. General - Comprehensive video analysis
2. Trading - Trading strategy extraction
3. Framework - Technical documentation extraction
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# Prompt templates from hanx YouTube Researcher Agent (agent_youtube_researcher.py lines 109-199)
GENERAL_PROMPT = """
Analyze the following video transcript and provide a comprehensive analysis:

Transcript:
{transcription}

Please provide:
1. Summary: A concise summary of the video content
2. Key Points: The main points or arguments presented
3. Topics Covered: List of topics discussed
4. Insights: Any notable insights or takeaways
5. Questions Answered: What questions does this video answer?
6. References: Any references to external sources, people, or concepts

Format your response as JSON with the following structure:
{{
  "summary": "...",
  "key_points": ["...", "..."],
  "topics": ["...", "..."],
  "insights": ["...", "..."],
  "questions_answered": ["...", "..."],
  "references": ["...", "..."]
}}
"""

TRADING_STRATEGY_PROMPT = """
Analyze the following trading strategy video transcript and provide a detailed breakdown:

Transcript:
{transcription}

Please extract and provide:
1. Strategy Name: The name of the trading strategy discussed
2. Markets: Which markets this strategy is designed for (crypto, forex, stocks, etc.)
3. Timeframes: Which timeframes this strategy works best on
4. Indicators Used: List all technical indicators mentioned
5. Entry Conditions: Specific conditions for entering a trade
6. Exit Conditions: Specific conditions for exiting a trade
7. Risk Management: Any risk management rules mentioned
8. Backtest Results: Any backtest results or historical performance mentioned
9. Pros and Cons: Advantages and disadvantages of this strategy
10. Key Insights: Notable insights about this strategy

Format your response as JSON with the following structure:
{{
  "strategy_name": "...",
  "markets": ["...", "..."],
  "timeframes": ["...", "..."],
  "indicators": ["...", "..."],
  "entry_conditions": ["...", "..."],
  "exit_conditions": ["...", "..."],
  "risk_management": ["...", "..."],
  "backtest_results": "...",
  "pros": ["...", "..."],
  "cons": ["...", "..."],
  "key_insights": ["...", "..."]
}}
"""

FRAMEWORK_TOOL_PROMPT = """
Analyze the following framework/tool tutorial video transcript and provide a detailed breakdown:

Transcript:
{transcription}

Please extract and provide:
1. Tool/Framework Name: The name of the tool or framework discussed
2. Purpose: What problem does this tool solve?
3. Target Users: Who is this tool designed for?
4. Key Features: List the main features of the tool
5. Installation Process: How to install or set up the tool
6. Basic Usage: How to use the tool for basic tasks
7. Advanced Features: Any advanced features or capabilities
8. Limitations: Any limitations or constraints mentioned
9. Alternatives: Any alternative tools mentioned
10. Resources: Links, documentation, or resources mentioned

Format your response as JSON with the following structure:
{{
  "tool_name": "...",
  "purpose": "...",
  "target_users": ["...", "..."],
  "key_features": ["...", "..."],
  "installation": ["...", "..."],
  "basic_usage": ["...", "..."],
  "advanced_features": ["...", "..."],
  "limitations": ["...", "..."],
  "alternatives": ["...", "..."],
  "resources": ["...", "..."]
}}
"""


class SpecializedAnalyzer:
    """Specialized YouTube video analyzer using domain-specific prompts"""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_transcript(self, url: str, model_size: str = "base") -> Dict:
        """
        Get video transcript using youtube-video-analysis skill

        Args:
            url: YouTube video URL
            model_size: Whisper model size (tiny, base, small, medium, large)

        Returns:
            Dict with transcript and metadata
        """
        print("=" * 80)
        print("STEP 1: Get Video Transcript")
        print("=" * 80)
        print()

        # Find youtube-video-analysis skill
        skill_dir = Path(__file__).parent.parent.parent / "youtube-video-analysis"
        analyze_script = skill_dir / "scripts" / "analyze_video.py"

        if not analyze_script.exists():
            raise FileNotFoundError(
                f"youtube-video-analysis skill not found at {skill_dir}\n"
                "Please install youtube-video-analysis skill first"
            )

        # Create temporary output directory for youtube-video-analysis
        temp_dir = self.output_dir / "temp_transcript"
        temp_dir.mkdir(exist_ok=True)

        # Call youtube-video-analysis script
        import subprocess
        cmd = [
            sys.executable,
            str(analyze_script),
            url,
            "--output", str(temp_dir),
            "--model", model_size
        ]

        print(f"Running: {' '.join(cmd)}")
        print()

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Failed to get transcript:\n{result.stderr}")

        # Load transcript and metadata
        transcript_path = temp_dir / "transcript.txt"
        metadata_path = temp_dir / "metadata.json"

        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found at {transcript_path}")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()

        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

        print(f"[OK] Transcript loaded: {len(transcript)} characters")
        print()

        return {
            "transcript": transcript,
            "metadata": metadata,
            "url": url
        }

    def query_llm(self, prompt: str, provider: str = "openai") -> str:
        """
        Query LLM with prompt

        Args:
            prompt: Prompt to send to LLM
            provider: LLM provider (openai, anthropic, etc.)

        Returns:
            LLM response text
        """
        print("=" * 80)
        print("STEP 2: Query LLM for Analysis")
        print("=" * 80)
        print()

        # Try to use hanx LLM API if available
        try:
            # Try to import from hanx_tools
            parent_dir = Path(__file__).parent.parent.parent.parent.parent / "research" / "hanx"
            sys.path.insert(0, str(parent_dir))

            from hanx_apis.api_llm import query_llm

            print(f"Using LLM provider: {provider}")
            response = query_llm(prompt, provider=provider)
            print(f"[OK] Received response: {len(response)} characters")
            print()

            return response

        except ImportError:
            print("[WARN] hanx LLM API not available")
            print("Attempting to use OpenAI API directly...")
            print()

            # Fallback to direct OpenAI API call
            try:
                import openai
                from dotenv import load_dotenv

                load_dotenv()
                openai.api_key = os.getenv("OPENAI_API_KEY")

                if not openai.api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment")

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                result = response.choices[0].message.content
                print(f"[OK] Received response: {len(result)} characters")
                print()

                return result

            except Exception as e:
                print(f"[FAIL] Could not query LLM: {e}")
                print()
                print("Please ensure you have either:")
                print("  1. hanx_tools/hanx_apis installed, OR")
                print("  2. openai package + OPENAI_API_KEY environment variable")
                print()
                raise

    def analyze_general(self, url: str, transcript: Optional[str] = None, model_size: str = "base") -> Dict:
        """
        Perform general video analysis

        Args:
            url: YouTube video URL
            transcript: Optional pre-fetched transcript
            model_size: Whisper model size if transcript not provided

        Returns:
            Analysis result dict
        """
        # Get transcript if not provided
        if transcript is None:
            data = self.get_transcript(url, model_size)
            transcript = data["transcript"]
            metadata = data["metadata"]
        else:
            metadata = {}

        # Format prompt
        prompt = GENERAL_PROMPT.format(transcription=transcript)

        # Query LLM
        response = self.query_llm(prompt)

        # Parse JSON response
        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            print("[WARN] Response is not valid JSON, returning raw response")
            analysis = {"raw_response": response}

        # Add metadata
        result = {
            "video_url": url,
            "analysis_type": "general",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "analysis": analysis
        }

        return result

    def analyze_trading(self, url: str, transcript: Optional[str] = None, model_size: str = "base") -> Dict:
        """
        Perform trading strategy analysis

        Args:
            url: YouTube video URL
            transcript: Optional pre-fetched transcript
            model_size: Whisper model size if transcript not provided

        Returns:
            Analysis result dict
        """
        # Get transcript if not provided
        if transcript is None:
            data = self.get_transcript(url, model_size)
            transcript = data["transcript"]
            metadata = data["metadata"]
        else:
            metadata = {}

        # Format prompt
        prompt = TRADING_STRATEGY_PROMPT.format(transcription=transcript)

        # Query LLM
        response = self.query_llm(prompt)

        # Parse JSON response
        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            print("[WARN] Response is not valid JSON, returning raw response")
            analysis = {"raw_response": response}

        # Add metadata
        result = {
            "video_url": url,
            "analysis_type": "trading",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "analysis": analysis
        }

        return result

    def analyze_framework(self, url: str, transcript: Optional[str] = None, model_size: str = "base") -> Dict:
        """
        Perform framework/tool analysis

        Args:
            url: YouTube video URL
            transcript: Optional pre-fetched transcript
            model_size: Whisper model size if transcript not provided

        Returns:
            Analysis result dict
        """
        # Get transcript if not provided
        if transcript is None:
            data = self.get_transcript(url, model_size)
            transcript = data["transcript"]
            metadata = data["metadata"]
        else:
            metadata = {}

        # Format prompt
        prompt = FRAMEWORK_TOOL_PROMPT.format(transcription=transcript)

        # Query LLM
        response = self.query_llm(prompt)

        # Parse JSON response
        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            print("[WARN] Response is not valid JSON, returning raw response")
            analysis = {"raw_response": response}

        # Add metadata
        result = {
            "video_url": url,
            "analysis_type": "framework",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata,
            "analysis": analysis
        }

        return result

    def format_markdown(self, result: Dict, template_name: str) -> str:
        """
        Format analysis result as markdown using template

        Args:
            result: Analysis result dict
            template_name: Template name (general, trading, framework)

        Returns:
            Formatted markdown string
        """
        # Load template
        template_dir = Path(__file__).parent.parent / "templates"
        template_path = template_dir / f"{template_name}_analysis_template.md"

        if not template_path.exists():
            # Generate simple markdown without template
            return self._generate_simple_markdown(result)

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Replace placeholders in template
        # This is a simple implementation - could be enhanced with Jinja2
        markdown = template

        # Replace metadata placeholders
        for key, value in result.get("metadata", {}).items():
            markdown = markdown.replace(f"{{{key}}}", str(value))

        # Replace analysis placeholders
        analysis = result.get("analysis", {})
        for key, value in analysis.items():
            if isinstance(value, list):
                # Format list as markdown bullet points
                formatted = "\n".join(f"- {item}" for item in value)
                markdown = markdown.replace(f"{{{key}}}", formatted)
            else:
                markdown = markdown.replace(f"{{{key}}}", str(value))

        return markdown

    def _generate_simple_markdown(self, result: Dict) -> str:
        """Generate simple markdown output without template"""
        analysis = result.get("analysis", {})
        metadata = result.get("metadata", {})

        lines = []
        lines.append(f"# Video Analysis: {result['analysis_type'].title()}")
        lines.append("")
        lines.append(f"**URL:** {result['video_url']}")
        lines.append(f"**Analyzed:** {result['timestamp']}")
        lines.append("")

        if metadata:
            lines.append("## Video Metadata")
            lines.append("")
            for key, value in metadata.items():
                lines.append(f"- **{key.title()}:** {value}")
            lines.append("")

        lines.append("## Analysis")
        lines.append("")

        for key, value in analysis.items():
            lines.append(f"### {key.replace('_', ' ').title()}")
            lines.append("")

            if isinstance(value, list):
                for item in value:
                    lines.append(f"- {item}")
            else:
                lines.append(str(value))

            lines.append("")

        return "\n".join(lines)

    def save_results(self, result: Dict, formats: List[str] = ["json", "markdown"]) -> Dict[str, Path]:
        """
        Save analysis results to files

        Args:
            result: Analysis result dict
            formats: List of output formats (json, markdown, yaml)

        Returns:
            Dict mapping format names to file paths
        """
        print("=" * 80)
        print("STEP 3: Save Results")
        print("=" * 80)
        print()

        # Generate base filename
        analysis_type = result["analysis_type"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{analysis_type}_analysis_{timestamp}"

        saved_files = {}

        # Save JSON
        if "json" in formats:
            json_path = self.output_dir / f"{base_name}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            saved_files["json"] = json_path
            print(f"[OK] Saved JSON: {json_path}")

        # Save Markdown
        if "markdown" in formats:
            markdown = self.format_markdown(result, analysis_type)
            md_path = self.output_dir / f"{base_name}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            saved_files["markdown"] = md_path
            print(f"[OK] Saved Markdown: {md_path}")

        # Save YAML
        if "yaml" in formats:
            try:
                import yaml
                yaml_path = self.output_dir / f"{base_name}.yaml"
                with open(yaml_path, 'w', encoding='utf-8') as f:
                    yaml.dump(result, f, default_flow_style=False, allow_unicode=True)
                saved_files["yaml"] = yaml_path
                print(f"[OK] Saved YAML: {yaml_path}")
            except ImportError:
                print("[WARN] PyYAML not installed, skipping YAML output")

        print()
        print(f"Results saved to: {self.output_dir}")
        print()

        return saved_files


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Specialized YouTube Video Analyzer - Domain-specific analysis with structured prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # General analysis
  python specialized_analyzer.py --url https://youtu.be/example --type general

  # Trading strategy analysis
  python specialized_analyzer.py --url https://youtu.be/example --type trading

  # Framework/tool analysis
  python specialized_analyzer.py --url https://youtu.be/example --type framework

  # Custom output directory
  python specialized_analyzer.py --url https://youtu.be/example --type trading --output ./trading_analysis

Analysis Types:
  general   - Comprehensive video analysis (summary, key points, topics, insights)
  trading   - Trading strategy extraction (entry/exit rules, indicators, risk management)
  framework - Technical documentation (installation, features, usage, limitations)
        """
    )

    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--type", choices=["general", "trading", "framework"], required=True,
                       help="Analysis type")
    parser.add_argument("--output", "-o", default="./output",
                       help="Output directory (default: ./output)")
    parser.add_argument("--model", "-m", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--formats", nargs="+", default=["json", "markdown"],
                       choices=["json", "markdown", "yaml"],
                       help="Output formats (default: json markdown)")
    parser.add_argument("--provider", default="openai",
                       help="LLM provider (default: openai)")

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = SpecializedAnalyzer(output_dir=args.output)

    # Print header
    print("=" * 80)
    print(f"Specialized YouTube Video Analyzer - {args.type.upper()} Analysis")
    print("=" * 80)
    print()
    print(f"Video URL: {args.url}")
    print(f"Analysis Type: {args.type}")
    print(f"Whisper Model: {args.model}")
    print(f"Output Directory: {args.output}")
    print(f"Output Formats: {', '.join(args.formats)}")
    print()

    try:
        # Perform analysis based on type
        if args.type == "general":
            result = analyzer.analyze_general(args.url, model_size=args.model)
        elif args.type == "trading":
            result = analyzer.analyze_trading(args.url, model_size=args.model)
        elif args.type == "framework":
            result = analyzer.analyze_framework(args.url, model_size=args.model)
        else:
            raise ValueError(f"Invalid analysis type: {args.type}")

        # Save results
        saved_files = analyzer.save_results(result, formats=args.formats)

        # Print summary
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print()
        print("Results:")
        for format_name, file_path in saved_files.items():
            print(f"  {format_name.upper()}: {file_path}")
        print()

    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
