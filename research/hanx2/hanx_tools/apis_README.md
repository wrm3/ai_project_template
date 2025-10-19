# hanx_apis

This directory contains API integration modules for the hanx project. These modules provide standardized interfaces to various external services and APIs.

## Available APIs

- `api_llm.py`: Language Model API integration
  - Supports OpenAI, Anthropic, Azure OpenAI, DeepSeek, Gemini, and local LLMs
  - Provides functions for querying LLMs with various parameters
  - Handles token tracking and cost estimation

- `api_jira.py`: Jira API integration
  - Create, update, and query Jira issues
  - Manage Jira projects and workflows

- `api_trello.py`: Trello API integration
  - Create and manage Trello boards, lists, and cards
  - Handle Trello automation and workflows

- `api_bitbucket.py`: Bitbucket API integration
  - Manage repositories, branches, and pull requests
  - Handle code reviews and CI/CD integration

- `api_confluence.py`: Confluence API integration
  - Create, update, and query Confluence pages
  - Manage Confluence spaces and permissions

- `api_perplexity.py`: Perplexity AI API integration
  - Query the Perplexity AI service for enhanced search results
  - Process and format search responses

## Usage

Import APIs in your code using the following pattern:

```python
from hanx_apis.api_llm import query_llm
from hanx_apis.api_jira import create_issue
```

## Adding New APIs

When adding new API integrations to this directory, follow these guidelines:

1. Use the `api_` prefix for all API files
2. Create a corresponding usage documentation file (e.g., `api_name_usage.md`)
3. Follow the established patterns for error handling, authentication, and configuration
4. Add the new API to this README with a brief description
5. Update the `hanx_learned.md` file with any lessons learned during implementation

## Authentication

Most APIs require authentication. Store API keys and credentials in the `.env` file (see `.env.example` for the format). Never commit API keys or credentials to the repository.

## Error Handling

All API modules should implement robust error handling, including:

1. Connection errors and timeouts
2. Authentication failures
3. Rate limiting and quota issues
4. Malformed responses
5. Service unavailability

## Documentation

Each API module should include:

1. Docstrings for all public functions and classes
2. A usage documentation file with examples
3. Information about required environment variables
4. Common error scenarios and how to handle them 