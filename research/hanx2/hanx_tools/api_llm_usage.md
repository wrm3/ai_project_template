# LLM API Tool

The `llm_api.py` provides a unified interface to interact with various Large Language Model (LLM) providers.

## Usage

```python
from tools.llm_api import query_llm

# Basic query with default provider (OpenAI)
response = query_llm("What is the capital of France?")
print(response)

# Specify a different provider
response = query_llm(
    "Explain quantum computing in simple terms",
    provider="anthropic"
)
print(response)

# Include an image with the query (for providers that support it)
response = query_llm(
    "What's in this image?",
    provider="openai",
    image_path="path/to/image.jpg"
)
print(response)
```

## Command Line Usage

```bash
# Basic query with default provider
py -3 ./tools/llm_api.py --prompt "What is the capital of France?"

# Specify a different provider
py -3 ./tools/llm_api.py --prompt "Explain quantum computing" --provider "anthropic"

# Include an image with the query
py -3 ./tools/llm_api.py --prompt "What's in this image?" --provider "openai" --image "path/to/image.jpg"
```

## Supported Providers

- **OpenAI** (default, model: gpt-4o)
- **Azure OpenAI** (model: configured via AZURE_OPENAI_MODEL_DEPLOYMENT)
- **DeepSeek** (model: deepseek-chat)
- **Anthropic** (model: claude-3-sonnet-20240229)
- **Gemini** (model: gemini-pro)
- **Local LLM** (model: Qwen/Qwen2.5-32B-Instruct-AWQ)

## Environment Variables

The tool uses these environment variables:

```
# OpenAI
OPENAI_API_KEY=your_api_key

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_MODEL_DEPLOYMENT=your_model_deployment

# Anthropic
ANTHROPIC_API_KEY=your_api_key

# DeepSeek
DEEPSEEK_API_KEY=your_api_key

# Google (Gemini)
GOOGLE_API_KEY=your_api_key

# Local LLM
LOCAL_LLM_URL=http://localhost:8000/v1
```

## Advanced Usage

### Custom System Prompts

```python
from tools.llm_api import query_llm

response = query_llm(
    "Write a function to calculate the Fibonacci sequence",
    provider="anthropic",
    system_prompt="You are an expert Python programmer. Provide clean, efficient, and well-documented code."
)
print(response)
```

### Streaming Responses

```python
from tools.llm_api import stream_llm_response

# Stream the response as it's generated
for chunk in stream_llm_response(
    "Write a short story about a robot learning to paint",
    provider="openai"
):
    print(chunk, end="", flush=True)
```

### Multi-Provider Fallback

```python
from tools.llm_api import query_with_fallback

# Try multiple providers in sequence until one succeeds
response = query_with_fallback(
    "Explain the theory of relativity",
    providers=["openai", "anthropic", "deepseek"]
)
print(response)
```

### Batch Processing

```python
from tools.llm_api import batch_process_queries

queries = [
    "What is machine learning?",
    "Explain neural networks",
    "What is deep learning?"
]

# Process multiple queries in parallel
results = batch_process_queries(
    queries,
    provider="anthropic",
    max_concurrent=3
)

for query, response in zip(queries, results):
    print(f"Query: {query}")
    print(f"Response: {response}")
    print("-" * 50)
```

## Example: Code Generation

```python
from tools.llm_api import query_llm

def generate_code(description, language="python"):
    """Generate code based on a description.
    
    Args:
        description: Description of the code to generate
        language: Programming language (default: python)
    
    Returns:
        Generated code as a string
    """
    prompt = f"Write {language} code that {description}. Provide only the code without explanations."
    system_prompt = f"You are an expert {language} programmer. Write clean, efficient, and well-documented code."
    
    response = query_llm(
        prompt,
        provider="openai",
        system_prompt=system_prompt
    )
    
    return response

# Example usage
if __name__ == "__main__":
    code = generate_code("reads a CSV file, calculates the average of each column, and writes the results to a new file")
    print(code)
``` 