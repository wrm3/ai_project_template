# Web Scraper Tool

The `web_scraper.py` provides functionality for scraping content from web pages, with support for concurrent requests and various content extraction options.

## Basic Usage

```python
from tools.web_scraper import scrape_url, scrape_urls

# Scrape a single URL
result = scrape_url("https://example.com")
print(result["title"])  # Page title
print(result["text"])   # Main text content
print(result["html"])   # Full HTML

# Scrape multiple URLs concurrently
urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]
results = scrape_urls(urls, max_concurrent=3)

for url, result in results.items():
    print(f"URL: {url}")
    print(f"Title: {result['title']}")
    print(f"Content length: {len(result['text'])}")
    print("-" * 50)
```

## Command Line Usage

```bash
# Scrape a single URL
py -3 ./tools/web_scraper.py https://example.com

# Scrape multiple URLs
py -3 ./tools/web_scraper.py --max-concurrent 3 https://example.com https://example.org https://example.net

# Save results to a file
py -3 ./tools/web_scraper.py --output results.json https://example.com
```

## Key Features

- Concurrent scraping of multiple URLs
- Automatic handling of rate limiting and retries
- Content extraction options (HTML, text, metadata)
- User-agent rotation to avoid blocking
- Proxy support for anonymity
- Customizable request headers
- Error handling and reporting

## Advanced Usage

### Custom Headers and Cookies

```python
from tools.web_scraper import scrape_url

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

cookies = {
    "session_id": "abc123",
    "preference": "dark_mode"
}

result = scrape_url(
    "https://example.com",
    headers=headers,
    cookies=cookies
)
print(result["text"])
```

### Using Proxies

```python
from tools.web_scraper import scrape_urls

proxies = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080"
]

urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]

results = scrape_urls(
    urls,
    max_concurrent=3,
    proxies=proxies,
    proxy_rotation=True
)

for url, result in results.items():
    print(f"URL: {url}, Status: {result['status']}")
```

### Content Extraction Options

```python
from tools.web_scraper import scrape_url

# Get only the main article content
result = scrape_url(
    "https://example.com/blog/article",
    extract_article=True,
    include_html=False,
    include_links=True
)

print(f"Article title: {result['title']}")
print(f"Article content: {result['text']}")
print(f"Article links: {result['links']}")

# Get structured data
result = scrape_url(
    "https://example.com/product",
    extract_metadata=True,
    extract_json_ld=True
)

print(f"Metadata: {result['metadata']}")
print(f"JSON-LD: {result['json_ld']}")
```

### Handling JavaScript-Heavy Pages

```python
from tools.web_scraper import scrape_url_with_browser

# Use browser automation for JavaScript-heavy pages
result = scrape_url_with_browser(
    "https://example.com/spa",
    wait_for_selector=".content-loaded",
    wait_time=5,
    scroll_to_bottom=True
)

print(result["text"])
```

## Example: Building a Simple News Aggregator

```python
from tools.web_scraper import scrape_urls
import json
from datetime import datetime

def aggregate_news(news_sites):
    """Aggregate news from multiple sites.
    
    Args:
        news_sites: List of news site URLs
    
    Returns:
        List of news articles
    """
    results = scrape_urls(
        news_sites,
        max_concurrent=5,
        extract_article=True,
        include_links=True
    )
    
    articles = []
    
    for site, result in results.items():
        if result["status"] == "success":
            articles.append({
                "source": site,
                "title": result["title"],
                "content": result["text"][:500] + "...",  # Truncate content
                "url": site,
                "scraped_at": datetime.now().isoformat()
            })
    
    return articles

# Example usage
if __name__ == "__main__":
    news_sites = [
        "https://example.com/news",
        "https://example.org/news",
        "https://example.net/news"
    ]
    
    articles = aggregate_news(news_sites)
    
    # Save to file
    with open("news_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print(f"Aggregated {len(articles)} news articles") 