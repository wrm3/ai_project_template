#!/usr/bin/env python3
"""
Grant Finder - Find relevant grants by industry and stage
"""

# Grant database
GRANTS = {
    "biotech": {
        "pre-seed": [
            {"name": "NSF I-Corps", "amount": "50k", "timeline": "6-8 weeks", "url": "nsf.gov/i-corps"},
            {"name": "NIH SBIR Phase I", "amount": "300k", "timeline": "9-12 months", "url": "sbir.nih.gov"},
        ],
        "seed": [
            {"name": "NIH SBIR Phase I", "amount": "300k", "timeline": "9-12 months", "url": "sbir.nih.gov"},
            {"name": "NIH SBIR Phase II", "amount": "1.8M", "timeline": "12 months after Phase I", "url": "sbir.nih.gov"},
        ],
    },
    "energy": {
        "pre-seed": [
            {"name": "DOE SBIR Phase I", "amount": "200k", "timeline": "9-12 months", "url": "sbir.er.doe.gov"},
            {"name": "NSF SBIR Phase I", "amount": "256k", "timeline": "6-9 months", "url": "seedfund.nsf.gov"},
        ],
        "seed": [
            {"name": "DOE ARPA-E", "amount": "500k-10M", "timeline": "12+ months", "url": "arpa-e.energy.gov"},
            {"name": "DOE SBIR Phase II", "amount": "1.15M", "timeline": "12 months after Phase I", "url": "sbir.er.doe.gov"},
        ],
    },
    "tech": {
        "pre-seed": [
            {"name": "NSF I-Corps", "amount": "50k", "timeline": "6-8 weeks", "url": "nsf.gov/i-corps"},
            {"name": "NSF SBIR Phase I", "amount": "256k", "timeline": "6-9 months", "url": "seedfund.nsf.gov"},
        ],
        "seed": [
            {"name": "NSF SBIR Phase II", "amount": "1M", "timeline": "12 months after Phase I", "url": "seedfund.nsf.gov"},
        ],
    },
}

def find_grants(industry, stage):
    """Find grants matching industry and stage"""
    industry = industry.lower()
    stage = stage.lower()
    
    if industry not in GRANTS:
        print(f"Industry '{industry}' not found. Available: {', '.join(GRANTS.keys())}")
        return
    
    if stage not in GRANTS[industry]:
        print(f"Stage '{stage}' not found for {industry}. Available: {', '.join(GRANTS[industry].keys())}")
        return
    
    grants = GRANTS[industry][stage]
    print(f"\nGrants for {industry.capitalize()} startups at {stage.capitalize()} stage:\n")
    
    for i, grant in enumerate(grants, 1):
        print(f"{i}. {grant['name']}")
        print(f"   Amount: ${grant['amount']}")
        print(f"   Timeline: {grant['timeline']}")
        print(f"   URL: {grant['url']}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python grant_finder.py <industry> <stage>")
        print("Industries: biotech, energy, tech")
        print("Stages: pre-seed, seed")
        sys.exit(1)
    
    industry = sys.argv[1]
    stage = sys.argv[2]
    
    find_grants(industry, stage)
