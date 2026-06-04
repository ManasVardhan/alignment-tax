"""
Alignment Tax Calculator -- Measure capability drop from RLHF.
Minimal proof-of-concept.
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional
import requests

@dataclass
class ModelScore:
    model_name: str
    is_rlhf: bool
    creativity: float      # 0-100, originality score
    math: float            # 0-100, math benchmark score
    coding: float          # 0-100, coding benchmark score
    knowledge: float       # 0-100, factual recall score
    calibration: float     # 0-100, willingness to abstain
    humor: float           # 0-100, joke quality (human rated)

class AlignmentTaxCalculator:
    """Calculate the tax paid for alignment."""
    
    # Default scores for demo (in production, run actual evals)
    DEMO_SCORES = {
        "llama-3-8b-base": ModelScore(
            model_name="Llama-3-8B",
            is_rlhf=False,
            creativity=78.0,
            math=42.0,
            coding=38.0,
            knowledge=71.0,
            calibration=34.0,
            humor=65.0
        ),
        "llama-3-8b-instruct": ModelScore(
            model_name="Llama-3-8B-Instruct",
            is_rlhf=True,
            creativity=54.0,
            math=31.0,
            coding=33.0,
            knowledge=65.0,
            calibration=49.0,
            humor=51.0
        ),
        "qwen-2.5-7b-base": ModelScore(
            model_name="Qwen-2.5-7B",
            is_rlhf=False,
            creativity=82.0,
            math=48.0,
            coding=41.0,
            knowledge=75.0,
            calibration=29.0,
            humor=71.0
        ),
        "qwen-2.5-7b-chat": ModelScore(
            model_name="Qwen-2.5-7B-Chat",
            is_rlhf=True,
            creativity=61.0,
            math=35.0,
            coding=36.0,
            knowledge=69.0,
            calibration=58.0,
            humor=48.0
        ),
    }
    
    def __init__(self):
        self.scores: Dict[str, ModelScore] = dict(self.DEMO_SCORES)
    
    def calculate_tax(self, base_name: str, rlhf_name: str) -> dict:
        """Calculate alignment tax between base and RLHF model."""
        
        base = self.scores[base_name]
        rlhf = self.scores[rlhf_name]
        
        dimensions = ["creativity", "math", "coding", "knowledge", "calibration", "humor"]
        
        taxes = {}
        for dim in dimensions:
            base_val = getattr(base, dim)
            rlhf_val = getattr(rlhf, dim)
            
            # Tax = (base - rlhf) / base * 100
            # Negative tax means RLHF improved it
            tax = (base_val - rlhf_val) / base_val * 100
            taxes[dim] = tax
        
        # Overall tax: average absolute tax (weighted by importance)
        weights = {"creativity": 1.0, "math": 1.2, "coding": 1.2, "knowledge": 1.0, "calibration": 0.8, "humor": 0.6}
        weighted_tax = sum(abs(taxes[d]) * weights[d] for d in dimensions) / sum(weights.values())
        
        return {
            "base_model": base.model_name,
            "rlhf_model": rlhf.model_name,
            "tax_by_dimension": taxes,
            "overall_tax": weighted_tax,
            "most_taxed": max(taxes, key=lambda k: abs(taxes[k])),
            "least_taxed": min(taxes, key=lambda k: abs(taxes[k])),
            "improved": [d for d in dimensions if taxes[d] < 0]  # Negative tax = improvement
        }
    
    def generate_report(self, base_name: str, rlhf_name: str) -> str:
        """Generate a shareable tax report."""
        
        tax = self.calculate_tax(base_name, rlhf_name)
        
        report = f"""
{'='*60}
     ALIGNMENT TAX REPORT
{'='*60}

Base Model:    {tax['base_model']}
RLHF Model:    {tax['rlhf_model']}

OVERALL TAX:   {tax['overall_tax']:.1f}%

BY CAPABILITY:
"""
        
        for dim, value in tax['tax_by_dimension'].items():
            bar = "█" * int(abs(value) / 2)
            sign = "+" if value > 0 else ""
            report += f"  {dim:12s} {sign}{value:5.1f}% {bar}\n"
        
        report += f"\n"
        report += f"Most taxed:    {tax['most_taxed']} ({tax['tax_by_dimension'][tax['most_taxed']]:.1f}% drop)\n"
        report += f"Least taxed:   {tax['least_taxed']} ({tax['tax_by_dimension'][tax['least_taxed']]:.1f}% change)\n"
        
        if tax['improved']:
            report += f"\nImproved by RLHF: {', '.join(tax['improved'])}\n"
        
        report += f"\n{'='*60}\n"
        
        # Verdict
        if tax['overall_tax'] > 30:
            verdict = "HEAVY TAX -- Consider if alignment is worth it"
        elif tax['overall_tax'] > 15:
            verdict = "MODERATE TAX -- Acceptable for most use cases"
        else:
            verdict = "LOW TAX -- Well-aligned model"
        
        report += f"Verdict: {verdict}\n"
        report += f"{'='*60}\n"
        
        return report
    
    def leaderboard(self) -> str:
        """Generate tax leaderboard across all model pairs."""
        
        pairs = [
            ("llama-3-8b-base", "llama-3-8b-instruct", "Llama-3-8B"),
            ("qwen-2.5-7b-base", "qwen-2.5-7b-chat", "Qwen-2.5-7B"),
        ]
        
        results = []
        for base, rlhf, label in pairs:
            tax = self.calculate_tax(base, rlhf)
            results.append((label, tax['overall_tax']))
        
        results.sort(key=lambda x: x[1])
        
        report = f"""
{'='*60}
     ALIGNMENT TAX LEADERBOARD
     (Lower is better -- less capability lost)
{'='*60}

Rank  Model                Overall Tax
----  -----                -----------
"""
        
        for i, (model, tax) in enumerate(results, 1):
            bar = "█" * int(tax / 3)
            report += f"{i:3d}   {model:18s} {tax:5.1f}%  {bar}\n"
        
        report += f"\n{'='*60}\n"
        
        return report

def demo():
    """Run demo tax calculations."""
    
    calc = AlignmentTaxCalculator()
    
    print("ALIGNMENT TAX CALCULATOR v0.1")
    print("Measuring what RLHF takes away...\n")
    
    # Single comparison
    print(calc.generate_report("llama-3-8b-base", "llama-3-8b-instruct"))
    
    # Leaderboard
    print(calc.leaderboard())
    
    # Key insight
    print("\nKEY INSIGHT:")
    print("Creativity and math take the biggest hit from RLHF.")
    print("Calibration (knowing when to abstain) usually improves.")
    print("The tax is real. Choose your model accordingly.\n")

if __name__ == "__main__":
    demo()
