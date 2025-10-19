# OpenManus Browser Use Module

The `browser_use.py` module provides web browsing and interaction capabilities for the Hanx project, leveraging the browser-use package. It enables automated web browsing, content extraction, and interaction with web elements.

## Installation

This module requires the browser-use package to be installed:

```bash
pip install browser-use
```

## Basic Usage

### Using the browser_use Function (via .cursorrules)

```python
# Navigate to a website
result = browser_use("navigate", url="https://example.com")
if result["success"]:
    print(f"Successfully navigated to {result['url']}")
    print(f"Page title: {result['title']}")
else:
    print(f"Error: {result['error']}")

# Extract text from the page
text_result = browser_use("extract_text")
if text_result["success"]:
    print(f"Page content: {text_result['text']}")

# Extract text from a specific element
element_text = browser_use("extract_text", selector="#main-content")
if element_text["success"]:
    print(f"Element content: {element_text['text']}")

# Extract links from the page
links_result = browser_use("extract_links")
if links_result["success"]:
    print("Links found:")
    for link in links_result["links"]:
        print(f"  {link['text']} -> {link['href']}")

# Click on an element
click_result = browser_use("click", selector="#submit-button")
if click_result["success"]:
    print("Successfully clicked on element")

# Type text into an input field
type_result = browser_use("type", selector="#search-input", text="search query")
if type_result["success"]:
    print("Successfully entered text")

# Take a screenshot
screenshot_result = browser_use("screenshot", path="screenshot.png")
if screenshot_result["success"]:
    print(f"Screenshot saved to {screenshot_result['path']}")

# Execute JavaScript
js_result = browser_use("execute_javascript", code="return document.title;")
if js_result["success"]:
    print(f"JavaScript result: {js_result['result']}")

# Close the browser
close_result = browser_use("close")
if close_result["success"]:
    print("Browser closed successfully")
```

### Using the BrowserUseTool Class Directly

```python
from hanx_tools.openmanus.browser_use import BrowserUseTool
import asyncio

async def browse_website():
    # Create a browser tool (non-headless for visualization)
    browser_tool = BrowserUseTool(headless=False)
    
    # Navigate to a website
    result = await browser_tool._run_async("navigate", url="https://example.com")
    if result["success"]:
        print(f"Successfully navigated to {result['url']}")
        
        # Extract text from the page
        text_result = await browser_tool._run_async("extract_text")
        print(f"Page content: {text_result['text'][:100]}...")
        
        # Close the browser
        await browser_tool._run_async("close")

# Run the async function
asyncio.run(browse_website())
```

## Available Actions

| Action | Description | Parameters | Return Value |
|--------|-------------|------------|--------------|
| `navigate` | Navigate to a URL | `url` (required): The URL to navigate to | `{"success": true, "url": "...", "title": "..."}` |
| `extract_text` | Extract text from the page | `selector` (optional): CSS selector to extract text from | `{"success": true, "text": "..."}` |
| `extract_links` | Extract links from the page | `selector` (optional): CSS selector to extract links from | `{"success": true, "links": [{"text": "...", "href": "..."}]}` |
| `click` | Click on an element | `selector` (required): CSS selector to click on | `{"success": true}` |
| `type` | Type text into an element | `selector` (required): CSS selector to type into<br>`text` (required): Text to type | `{"success": true}` |
| `screenshot` | Take a screenshot | `path` (required): Path to save the screenshot to | `{"success": true, "path": "..."}` |
| `execute_javascript` | Execute JavaScript code | `code` (required): JavaScript code to execute | `{"success": true, "result": ...}` |
| `close` | Close the browser | None | `{"success": true}` |

## Error Handling

All actions return a dictionary with a `success` key indicating whether the action was successful. If the action failed, the dictionary will also contain an `error` key with a description of the error.

```python
result = browser_use("navigate", url="https://example.com")
if not result["success"]:
    print(f"Error: {result['error']}")
    # Handle the error
```

## Integration with MCP Server

The BrowserUseTool class can be integrated with the MCP server through the OpenManus integration module:

```python
from hanx_tools.openmanus.integration import register_with_mcp_server

# Register all OpenManus tools (including BrowserUseTool) with the MCP server
register_with_mcp_server(mcp_server)
```

## Best Practices

1. **Browser Management**: Always close the browser when you're done to free up resources:

   ```python
   # After you're done with the browser
   browser_use("close")
   ```

2. **Selector Specificity**: Use specific CSS selectors to target elements precisely:

   ```python
   # Good: Specific selector
   browser_use("click", selector="#submit-button")
   
   # Better: Even more specific
   browser_use("click", selector="form#login-form button#submit-button")
   ```

3. **Error Handling**: Always check for success/error in the result:

   ```python
   result = browser_use("navigate", url="https://example.com")
   if not result["success"]:
       print(f"Error: {result['error']}")
       # Handle the error appropriately
   ```

4. **Headless Mode**: Use headless mode in production for better performance:

   ```python
   from hanx_tools.openmanus.browser_use import BrowserUseTool
   
   # Headless mode (default)
   browser_tool = BrowserUseTool(headless=True)
   
   # Non-headless mode (for debugging)
   browser_tool = BrowserUseTool(headless=False)
   ```

5. **Sequential Operations**: When performing multiple operations, check for success after each step:

   ```python
   # Navigate to the login page
   result = browser_use("navigate", url="https://example.com/login")
   if not result["success"]:
       print(f"Error navigating: {result['error']}")
       return
   
   # Enter username
   result = browser_use("type", selector="#username", text="user123")
   if not result["success"]:
       print(f"Error entering username: {result['error']}")
       return
   
   # Enter password
   result = browser_use("type", selector="#password", text="password123")
   if not result["success"]:
       print(f"Error entering password: {result['error']}")
       return
   
   # Click login button
   result = browser_use("click", selector="#login-button")
   if not result["success"]:
       print(f"Error clicking login button: {result['error']}")
       return
   ```

## Example: Web Scraping Workflow

```python
# Complete web scraping workflow
def scrape_product_info(url):
    # Navigate to the product page
    result = browser_use("navigate", url=url)
    if not result["success"]:
        return {"success": False, "error": result["error"]}
    
    # Extract product information
    product_info = {}
    
    # Get product title
    title_result = browser_use("extract_text", selector="h1.product-title")
    if title_result["success"]:
        product_info["title"] = title_result["text"]
    
    # Get product price
    price_result = browser_use("extract_text", selector=".product-price")
    if price_result["success"]:
        product_info["price"] = price_result["text"]
    
    # Get product description
    desc_result = browser_use("extract_text", selector=".product-description")
    if desc_result["success"]:
        product_info["description"] = desc_result["text"]
    
    # Get product images
    img_result = browser_use("execute_javascript", code="""
        return Array.from(document.querySelectorAll('.product-images img')).map(img => img.src);
    """)
    if img_result["success"]:
        product_info["images"] = img_result["result"]
    
    # Take a screenshot of the product
    screenshot_result = browser_use("screenshot", path=f"product_screenshot.png")
    if screenshot_result["success"]:
        product_info["screenshot"] = screenshot_result["path"]
    
    # Close the browser
    browser_use("close")
    
    return {"success": True, "product_info": product_info}

# Use the function
result = scrape_product_info("https://example.com/products/123")
if result["success"]:
    print(f"Product info: {result['product_info']}")
else:
    print(f"Error: {result['error']}")
```

## Troubleshooting

- **Browser Not Available**: If you see "browser-use package not available", install it with `pip install browser-use`.
- **Element Not Found**: If clicking or typing fails, check that the selector is correct and the element is visible.
- **Navigation Timeout**: If navigation fails, check the URL and your internet connection.
- **JavaScript Errors**: If execute_javascript fails, check the JavaScript code for syntax errors.
- **Screenshot Errors**: If screenshot fails, check that the path is writable. 