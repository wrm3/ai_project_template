#!/usr/bin/env python3
"""
Resource Cost Calculator
"""

def calculate_cloud_costs(usage_months=24):
    """Calculate total cloud credits available"""
    aws = 100000
    gcp = 100000
    azure = 150000
    
    total = aws + gcp + azure
    monthly = total / usage_months
    
    print("\n=== Cloud Credits Available ===")
    print(f"AWS Activate: ${aws:,}")
    print(f"Google Cloud: ${gcp:,}")
    print(f"Microsoft Azure: ${azure:,}")
    print(f"Total: ${total:,}")
    print(f"\nMonthly budget (over {usage_months} months): ${monthly:,.0f}/month")
    return total

def calculate_lab_costs(benches=1, location="sf", months=12):
    """Calculate lab space costs"""
    costs = {
        "sf": {"min": 2000, "max": 3000},
        "boston": {"min": 2000, "max": 3000},
        "nyc": {"min": 2000, "max": 3000},
        "other": {"min": 1200, "max": 2000},
    }
    
    loc = location.lower()
    if loc not in costs:
        loc = "other"
    
    monthly_min = benches * costs[loc]["min"]
    monthly_max = benches * costs[loc]["max"]
    total_min = monthly_min * months
    total_max = monthly_max * months
    
    print(f"\n=== Lab Space Costs ({location.upper()}) ===")
    print(f"Benches: {benches}")
    print(f"Monthly: ${monthly_min:,} - ${monthly_max:,}")
    print(f"Total ({months} months): ${total_min:,} - ${total_max:,}")
    
    return (monthly_min + monthly_max) / 2

def calculate_grant_potential(stage="seed"):
    """Calculate potential grant funding"""
    if stage == "pre-seed":
        i_corps = 50000
        phase1 = 250000
        total = i_corps + phase1
        print("\n=== Grant Potential (Pre-Seed) ===")
        print(f"NSF I-Corps: ${i_corps:,}")
        print(f"SBIR Phase I: ${phase1:,}")
        print(f"Total (Year 1): ${total:,}")
    elif stage == "seed":
        phase1 = 250000
        phase2 = 1500000
        total = phase1 + phase2
        print("\n=== Grant Potential (Seed) ===")
        print(f"SBIR Phase I: ${phase1:,}")
        print(f"SBIR Phase II: ${phase2:,}")
        print(f"Total (2-3 years): ${total:,}")
    
    return total

def total_non_dilutive_resources(stage="seed"):
    """Calculate total non-dilutive resources"""
    cloud = calculate_cloud_costs()
    grants = calculate_grant_potential(stage)
    total = cloud + grants
    
    print(f"\n=== TOTAL NON-DILUTIVE RESOURCES ===")
    print(f"Cloud Credits: ${cloud:,}")
    print(f"Grant Funding: ${grants:,}")
    print(f"TOTAL: ${total:,}")
    print(f"\nThis extends runway by 12-24 months without dilution!")
    
    return total

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        stage = sys.argv[1]
    else:
        stage = "seed"
    
    total_non_dilutive_resources(stage)
