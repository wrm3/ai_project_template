# Perplexity API Tool

The `perplexity_api.py` provides access to Perplexity's AI models for research queries, code generation, and more.

## Basic Usage

```python
from tools.perplexity_api import PerplexityAPI

# Initialize the API client
api = PerplexityAPI()

# Simple query
response = api.query("What is the capital of France?")
print(response)

# Research query with sources
response = api.research_query(
    "What are the latest developments in quantum computing?",
    require_sources=True
)
print(response)
print("Sources:", response.get("sources", []))
```

## Key Features

- Access to multiple Perplexity models
- Research queries with source citations
- Code generation capabilities
- Cost-effective model selection
- Streaming responses
- Error handling and retries

## Available Models

The API supports these models with different cost profiles:

- **sonar-medium-online**: $0.0025 per 1K tokens (best for up-to-date information)
- **sonar-medium-context**: $0.0025 per 1K tokens (best for context-heavy queries)
- **mixtral-8x7b-instruct**: $0.0007 per 1K tokens (cost-effective general purpose)
- **codellama-34b-instruct**: $0.0007 per 1K tokens (specialized for code)

## When to Use

Use the Perplexity API ONLY in these scenarios:
1. When other LLMs have failed to provide satisfactory answers
2. For research queries requiring up-to-date information with source citations
3. When specialized technical knowledge is needed and other models show uncertainty
4. As a last resort for complex queries after exhausting other options

## Advanced Usage

### Model Selection

```python
from tools.perplexity_api import PerplexityAPI

api = PerplexityAPI()

# Use sonar model for up-to-date information
response = api.query(
    "What are the current interest rates set by the Federal Reserve?",
    model="sonar-medium-online"
)
print(response)

# Use codellama for code generation
code_response = api.query(
    "Write a Python function to find the longest palindromic substring",
    model="codellama-34b-instruct"
)
print(code_response)
```

### Research Queries with Sources

```python
from tools.perplexity_api import PerplexityAPI

api = PerplexityAPI()

# Research query with sources
response = api.research_query(
    "What are the environmental impacts of electric vehicles?",
    require_sources=True,
    max_sources=5
)

print(response["answer"])
print("\nSources:")
for source in response.get("sources", []):
    print(f"- {source['title']}: {source['url']}")
```

### Streaming Responses

```python
from tools.perplexity_api import PerplexityAPI

api = PerplexityAPI()

# Stream the response as it's generated
for chunk in api.stream_query(
    "Explain the theory of relativity in simple terms",
    model="mixtral-8x7b-instruct"
):
    print(chunk, end="", flush=True)
```

### Cost Estimation

```python
from tools.perplexity_api import PerplexityAPI, estimate_cost

api = PerplexityAPI()

# Estimate cost before running a query
query = "Provide a detailed analysis of climate change impacts on agriculture"
estimated_tokens = len(query.split()) * 1.5  # Rough estimate
input_tokens = estimated_tokens
output_tokens = estimated_tokens * 3  # Assuming output is 3x input
model = "sonar-medium-online"

cost = estimate_cost(model, input_tokens, output_tokens)
print(f"Estimated cost: ${cost:.4f}")

# Proceed if cost is acceptable
if cost < 0.05:  # Example threshold
    response = api.query(query, model=model)
    print(response)
```

## Example: Research Assistant

```python
from tools.perplexity_api import PerplexityAPI
import json
from datetime import datetime

class ResearchAssistant:
    def __init__(self):
        self.api = PerplexityAPI()
        self.research_history = []
    
    def research_topic(self, topic, require_sources=True):
        """Research a topic and save the results.
        
        Args:
            topic: The research topic or question
            require_sources: Whether to require source citations
            
        Returns:
            Dictionary containing the research results
        """
        print(f"Researching: {topic}")
        
        response = self.api.research_query(
            topic,
            require_sources=require_sources,
            model="sonar-medium-online"
        )
        
        # Format and save the research
        research = {
            "topic": topic,
            "answer": response["answer"],
            "sources": response.get("sources", []),
            "timestamp": datetime.now().isoformat()
        }
        
        self.research_history.append(research)
        
        # Save history to file
        with open("research_history.json", "w", encoding="utf-8") as f:
            json.dump(self.research_history, f, indent=2)
        
        return research
    
    def summarize_sources(self, research_index=-1):
        """Summarize the sources from a research entry.
        
        Args:
            research_index: Index in the research history (default: latest)
            
        Returns:
            Summary of the sources
        """
        if not self.research_history:
            return "No research history available"
        
        research = self.research_history[research_index]
        sources = research.get("sources", [])
        
        if not sources:
            return "No sources available for this research"
        
        summary = f"Sources for '{research['topic']}':\n\n"
        for i, source in enumerate(sources, 1):
            summary += f"{i}. {source.get('title', 'Untitled')}\n"
            summary += f"   URL: {source.get('url', 'No URL')}\n"
            summary += f"   Snippet: {source.get('snippet', 'No snippet')[:100]}...\n\n"
        
        return summary

# Example usage
if __name__ == "__main__":
    assistant = ResearchAssistant()
    
    # Research a topic
    research = assistant.research_topic(
        "What are the most promising renewable energy technologies for 2025?"
    )
    
    print("\nAnswer:")
    print(research["answer"])
    
    print("\nSource Summary:")
    print(assistant.summarize_sources())
``` 