# hanx_tools

This directory contains utility tools for the hanx project. These tools provide various functionalities that can be used by agents and other components.

## Available Tools

- `tool_token_tracker.py`: Token usage tracking
  - Track token usage for LLM calls
  - Estimate costs for different providers
  - Generate usage reports

- `tool_search_engine.py`: Web search functionality
  - Perform web searches with various parameters
  - Format and process search results
  - Handle pagination and result filtering

- `tool_web_scraper.py`: Web scraping functionality
  - Scrape content from web pages
  - Handle different content types and structures
  - Process and clean scraped content

- `tool_screenshot_utils.py`: Screenshot capture
  - Capture screenshots of web pages
  - Customize screenshot dimensions and format
  - Process and analyze screenshots

- `tool_document_processors.py`: Document processing
  - Process various document formats (PDF, DOCX, etc.)
  - Extract text and metadata
  - Convert between formats

- `tool_file_processors.py`: File operations
  - Read and write files with proper encoding
  - Process file contents
  - Handle different file formats

- `tool_system_info.py`: System information
  - Get information about the system
  - Monitor system resources
  - Handle platform-specific operations

- `tool_platform.py`: Platform utilities
  - Handle platform-specific operations
  - Provide cross-platform compatibility
  - Detect and adapt to different environments

- `tool_mysql_db.py`, `tool_mysql_access.py`, `tool_mysql_utils.py`: MySQL database utilities
  - Connect to MySQL databases
  - Execute queries and process results
  - Handle database operations

- `tool_oracle_db.py`: Oracle database utilities
  - Connect to Oracle databases
  - Execute queries and process results
  - Handle database operations

## Usage

Import tools in your code using the following pattern:

```python
from hanx_tools.tool_token_tracker import get_token_tracker
from hanx_tools.tool_search_engine import search_web
```

## Adding New Tools

When adding new tools to this directory, follow these guidelines:

1. Use the `tool_` prefix for all tool files
2. Create a corresponding usage documentation file (e.g., `tool_name_usage.md`)
3. Follow the established patterns for error handling, logging, and configuration
4. Add the new tool to this README with a brief description
5. Update the `hanx_learned.md` file with any lessons learned during implementation

## Temporary Tools

For project-specific or experimental tools, use the `hanx_tools/temp_tools/` directory. These tools don't need to follow the same strict guidelines as the main tools, but should still be documented in their respective files.

## Documentation

Each tool should include:

1. Docstrings for all public functions and classes
2. A usage documentation file with examples
3. Information about required dependencies
4. Common error scenarios and how to handle them 