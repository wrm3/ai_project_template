#!/usr/bin/env python3
"""
Accelerator Matcher - Match startups to accelerators
"""

# Accelerator database
ACCELERATORS = {
    "general": [
        {"name": "Y Combinator", "investment": "500k for 7%", "focus": "High-growth tech", "acceptance": "1.5%", "url": "ycombinator.com"},
        {"name": "Techstars", "investment": "120k for 6%", "focus": "Various industries", "acceptance": "1-2%", "url": "techstars.com"},
        {"name": "500 Global", "investment": "150k for 6%", "focus": "Growth marketing", "acceptance": "2-3%", "url": "500.co"},
    ],
    "biotech": [
        {"name": "IndieBio", "investment": "250k for 8%", "focus": "Biotech, food tech", "acceptance": "5-10%", "url": "indiebio.co"},
        {"name": "Y Combinator", "investment": "500k for 7%", "focus": "Bio track available", "acceptance": "1.5%", "url": "ycombinator.com"},
    ],
    "hardware": [
        {"name": "HAX", "investment": "120-250k", "focus": "Hardware, IoT", "acceptance": "5-10%", "url": "hax.co"},
    ],
    "health": [
        {"name": "Rock Health", "investment": "100-150k for 4-5%", "focus": "Digital health", "acceptance": "10-15%", "url": "rockhealth.com"},
    ],
}

def match_accelerator(industry, stage="seed"):
    """Match startup to accelerators"""
    industry = industry.lower()
    
    print(f"\nAccelerators for {industry.capitalize()} startups:\n")
    
    # Show industry-specific accelerators
    if industry in ACCELERATORS:
        print(f"=== {industry.capitalize()}-Specific Accelerators ===\n")
        for acc in ACCELERATORS[industry]:
            print(f"• {acc['name']}")
            print(f"  Investment: {acc['investment']}")
            print(f"  Focus: {acc['focus']}")
            print(f"  Acceptance: ~{acc['acceptance']}")
            print(f"  Apply: {acc['url']}")
            print()
    
    # Always show general accelerators
    print("=== General Accelerators (All Industries) ===\n")
    for acc in ACCELERATORS["general"]:
        print(f"• {acc['name']}")
        print(f"  Investment: {acc['investment']}")
        print(f"  Focus: {acc['focus']}")
        print(f"  Acceptance: ~{acc['acceptance']}")
        print(f"  Apply: {acc['url']}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python accelerator_matcher.py <industry>")
        print("Industries: biotech, hardware, health, energy, general")
        sys.exit(1)
    
    industry = sys.argv[1]
    match_accelerator(industry)
