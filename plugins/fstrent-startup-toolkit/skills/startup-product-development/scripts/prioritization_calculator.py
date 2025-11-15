#!/usr/bin/env python3
"""
Prioritization Calculator
Calculate RICE scores and MoSCoW categorization
"""

def calculate_rice(reach, impact, confidence, effort):
    """Calculate RICE score"""
    return (reach * impact * confidence) / effort

if __name__ == "__main__":
    print("RICE Prioritization Calculator")
    print("See SKILL.md for usage")
