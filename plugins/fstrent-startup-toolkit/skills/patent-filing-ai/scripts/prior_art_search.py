#!/usr/bin/env python3
"""
Prior Art Search Tool for Patent Filing

Searches USPTO and Google Patents for relevant prior art.
Helps identify existing patents before filing your application.

Usage:
    python prior_art_search.py "transformer attention mechanism"
    python prior_art_search.py "neural network training" --limit 20
"""

import sys
import argparse
import webbrowser
from urllib.parse import quote_plus

def search_uspto(query, limit=10):
    """
    Search USPTO patent database

    Args:
        query: Search keywords
        limit: Number of results to display

    Returns:
        URL to USPTO search results
    """
    # USPTO PatFT advanced search
    encoded_query = quote_plus(query)
    url = f"https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l={limit}&TERM1={encoded_query}&FIELD1=&co1=AND&TERM2=&FIELD2=&d=PTXT"

    return url

def search_google_patents(query, limit=10):
    """
    Search Google Patents

    Args:
        query: Search keywords
        limit: Number of results to display

    Returns:
        URL to Google Patents search results
    """
    encoded_query = quote_plus(query)
    url = f"https://patents.google.com/?q={encoded_query}&num={limit}"

    return url

def search_academic(query):
    """
    Search academic papers (Google Scholar)

    Args:
        query: Search keywords

    Returns:
        URL to Google Scholar search results
    """
    encoded_query = quote_plus(query)
    url = f"https://scholar.google.com/scholar?q={encoded_query}"

    return url

def generate_search_tips(query):
    """
    Generate search tips and alternative queries

    Args:
        query: Original search query

    Returns:
        List of search tips
    """
    tips = [
        "\n📋 SEARCH TIPS:",
        "-" * 50,
        "",
        "1. Try Different Keywords:",
        f"   Original: \"{query}\"",
        "   Alternative terms for the same concept",
        "   Synonyms and related terms",
        "",
        "2. Search Strategies:",
        "   - Start broad, then narrow down",
        "   - Use technical terms from your field",
        "   - Search inventor names if you know competitors",
        "   - Check citations of relevant patents",
        "",
        "3. What to Look For:",
        "   - Similar technical approaches",
        "   - Same problem being solved",
        "   - Related architectures or methods",
        "   - Claims that overlap with your invention",
        "",
        "4. Document Your Findings:",
        "   - Patent number and title",
        "   - Key claims (what they protect)",
        "   - How your invention is different",
        "   - Filing date (affects priority)",
        "",
        "5. Advanced Searches:",
        "   - USPTO: Use field codes (TTL/, ABST/, ACLM/)",
        "   - Google Patents: Use filters (date, assignee)",
        "   - Check patent classifications (CPC codes)",
    ]

    return "\n".join(tips)

def format_output(query, uspto_url, google_url, scholar_url):
    """
    Format search results for display

    Args:
        query: Search query
        uspto_url: USPTO search URL
        google_url: Google Patents URL
        scholar_url: Google Scholar URL

    Returns:
        Formatted output string
    """
    output = [
        "",
        "="  * 70,
        "PRIOR ART SEARCH RESULTS",
        "=" * 70,
        "",
        f"Search Query: \"{query}\"",
        "",
        "-" * 70,
        "📌 USPTO Patent Database",
        "-" * 70,
        "",
        "URL:",
        uspto_url,
        "",
        "What to Check:",
        "- US patents and published applications",
        "- Official US prior art",
        "- Download full patent PDFs",
        "",
        "-" * 70,
        "📌 Google Patents (Comprehensive)",
        "-" * 70,
        "",
        "URL:",
        google_url,
        "",
        "What to Check:",
        "- Global patents (US, EP, WO, CN, JP, etc.)",
        "- Better search interface",
        "- PDF download available",
        "- Related patents suggestions",
        "",
        "-" * 70,
        "📌 Academic Literature (Google Scholar)",
        "-" * 70,
        "",
        "URL:",
        scholar_url,
        "",
        "What to Check:",
        "- Published papers (also count as prior art!)",
        "- Conference proceedings",
        "- Technical reports",
        "- ArXiv preprints",
    ]

    return "\n".join(output)

def analyze_findings_template():
    """
    Provide template for documenting prior art findings

    Returns:
        Template string
    """
    template = [
        "",
        "=" * 70,
        "PRIOR ART ANALYSIS TEMPLATE",
        "=" * 70,
        "",
        "Use this template to document each relevant patent/paper you find:",
        "",
        "-" * 70,
        "",
        "FINDING #1:",
        "",
        "Reference: [Patent number or paper citation]",
        "Title: [Title of patent/paper]",
        "Date: [Filing/publication date]",
        "Assignee/Author: [Company or author names]",
        "",
        "What it does:",
        "[Brief description of the invention]",
        "",
        "Key claims/contributions:",
        "- [Claim 1]",
        "- [Claim 2]",
        "- [Claim 3]",
        "",
        "Similarities to my invention:",
        "- [Similarity 1]",
        "- [Similarity 2]",
        "",
        "Differences from my invention:",
        "- [Difference 1 - explain why yours is novel]",
        "- [Difference 2 - explain advantages]",
        "- [Difference 3 - explain technical distinctions]",
        "",
        "Overall assessment:",
        "[ ] Not relevant",
        "[ ] Somewhat related",
        "[ ] Closely related - need to emphasize differences",
        "[ ] Blocks my invention - need to file anyway or abandon",
        "",
        "-" * 70,
        "",
        "Repeat for each relevant finding...",
        "",
    ]

    return "\n".join(template)

def main():
    parser = argparse.ArgumentParser(
        description="Search for prior art in patents and academic literature",
        epilog="Example: python prior_art_search.py \"transformer attention mechanism\""
    )

    parser.add_argument(
        "query",
        help="Search query (keywords describing your invention)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of results to retrieve (default: 10)"
    )

    parser.add_argument(
        "--open",
        action="store_true",
        help="Automatically open search URLs in browser"
    )

    parser.add_argument(
        "--template",
        action="store_true",
        help="Show prior art analysis template"
    )

    args = parser.parse_args()

    # Generate search URLs
    uspto_url = search_uspto(args.query, args.limit)
    google_url = search_google_patents(args.query, args.limit)
    scholar_url = search_academic(args.query)

    # Display results
    print(format_output(args.query, uspto_url, google_url, scholar_url))
    print(generate_search_tips(args.query))

    # Show template if requested
    if args.template:
        print(analyze_findings_template())

    # Open in browser if requested
    if args.open:
        print("\n🌐 Opening search results in browser...")
        webbrowser.open(google_url)  # Google Patents has best interface
        print("✓ Opened Google Patents")
        print("\nNote: Also check USPTO and Google Scholar using URLs above")

    # Next steps
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("")
    print("1. Click the URLs above to search each database")
    print("2. Review the first 20-30 results")
    print("3. For each relevant patent/paper:")
    print("   - Read the abstract")
    print("   - Scan the claims (most important!)")
    print("   - Note how your invention differs")
    print("4. Use the analysis template (--template flag) to document findings")
    print("5. If you find blocking prior art:")
    print("   - Emphasize what makes yours different")
    print("   - Focus claims on novel aspects")
    print("   - Consider filing anyway with narrow claims")
    print("")
    print("💡 TIP: Finding prior art is GOOD - it helps you:")
    print("   - Refine your claims to be more specific")
    print("   - Understand the patent landscape")
    print("   - Make your patent stronger")
    print("")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, show help
        print("Prior Art Search Tool")
        print("=" * 50)
        print("")
        print("Usage:")
        print("  python prior_art_search.py \"your search query\"")
        print("")
        print("Examples:")
        print("  python prior_art_search.py \"transformer attention mechanism\"")
        print("  python prior_art_search.py \"neural network training\" --limit 20")
        print("  python prior_art_search.py \"BERT language model\" --open")
        print("  python prior_art_search.py \"GPT architecture\" --template")
        print("")
        print("Options:")
        print("  --limit N     Number of results (default: 10)")
        print("  --open        Open search in browser automatically")
        print("  --template    Show prior art analysis template")
        print("")
        print("Searches:")
        print("  • USPTO Patent Database (US patents)")
        print("  • Google Patents (global patents)")
        print("  • Google Scholar (academic papers)")
        print("")
        sys.exit(0)

    main()
