#!/usr/bin/env python3
"""
Resource Acquisition Timeline Planner
"""

from datetime import datetime, timedelta

def print_timeline(stage="seed", industry="tech"):
    """Generate timeline for resource acquisition"""
    
    start_date = datetime.now()
    
    print(f"\n=== Resource Acquisition Timeline ===")
    print(f"Stage: {stage.capitalize()}")
    print(f"Industry: {industry.capitalize()}")
    print(f"Start Date: {start_date.strftime('%B %Y')}\n")
    
    # Month 1-3
    m1 = start_date
    m3 = start_date + timedelta(days=90)
    
    print("MONTH 1-3: FOUNDATION")
    print(f"  {m1.strftime('%b %Y')} - {m3.strftime('%b %Y')}")
    print("  [ ] Apply for cloud credits (AWS, GCP, Azure)")
    
    if industry in ["biotech", "hardware"]:
        print("  [ ] Research lab space options")
        print("  [ ] Visit 3-5 lab facilities")
        print("  [ ] Apply to lab spaces")
    
    print("  [ ] Research grant programs")
    if stage == "pre-seed":
        print("  [ ] Apply for NSF I-Corps ($50k)")
    
    print("  [ ] Apply to accelerators (if appropriate)")
    print()
    
    # Month 4-6
    m4 = start_date + timedelta(days=90)
    m6 = start_date + timedelta(days=180)
    
    print("MONTH 4-6: EXECUTION")
    print(f"  {m4.strftime('%b %Y')} - {m6.strftime('%b %Y')}")
    print("  [ ] Receive cloud credits ($350k)")
    
    if industry in ["biotech", "hardware"]:
        print("  [ ] Secure lab space")
        print("  [ ] Move into lab")
    
    if industry == "hardware":
        print("  [ ] Source manufacturing partners (Alibaba, Thomasnet)")
        print("  [ ] Order samples from 5-10 manufacturers")
    
    print("  [ ] Submit SBIR Phase I applications")
    print()
    
    # Month 7-12
    m7 = start_date + timedelta(days=180)
    m12 = start_date + timedelta(days=365)
    
    print("MONTH 7-12: SCALE")
    print(f"  {m7.strftime('%b %Y')} - {m12.strftime('%b %Y')}")
    
    if industry == "hardware":
        print("  [ ] Select manufacturer")
        print("  [ ] Place pilot order (500-1,000 units)")
        print("  [ ] Quality inspection")
    
    print("  [ ] Receive SBIR Phase I award ($150-300k)")
    print("  [ ] Begin Phase I execution")
    
    if industry in ["biotech", "hardware"]:
        print("  [ ] Expand lab space if needed")
    
    print()
    
    # Year 2
    y2_start = start_date + timedelta(days=365)
    y2_end = start_date + timedelta(days=730)
    
    print("YEAR 2: GROWTH")
    print(f"  {y2_start.strftime('%b %Y')} - {y2_end.strftime('%b %Y')}")
    print("  [ ] Complete SBIR Phase I")
    print("  [ ] Apply for SBIR Phase II ($750k-1.5M)")
    
    if industry == "hardware":
        print("  [ ] Scale manufacturing (10,000+ units)")
    
    print("  [ ] Raise Series A (leveraging SBIR validation)")
    print()
    
    # Summary
    print("=== RESOURCES SECURED ===")
    resources = []
    
    resources.append(("Cloud Credits", 350000))
    
    if stage == "pre-seed":
        resources.append(("NSF I-Corps", 50000))
    
    resources.append(("SBIR Phase I", 250000))
    resources.append(("SBIR Phase II", 1500000))
    
    total = sum(r[1] for r in resources)
    
    for name, amount in resources:
        print(f"  {name}: ${amount:,}")
    
    print(f"\n  TOTAL NON-DILUTIVE: ${total:,}")
    print(f"  Timeline: 24-36 months")
    print(f"  Equity saved: ~15-20% (vs. raising all from VCs)")
    print()

if __name__ == "__main__":
    import sys
    
    stage = sys.argv[1] if len(sys.argv) > 1 else "seed"
    industry = sys.argv[2] if len(sys.argv) > 2 else "tech"
    
    print_timeline(stage, industry)
