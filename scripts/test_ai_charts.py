#!/usr/bin/env python3
"""
Test AI-powered chart selection.
Sends test questions and checks if AI selects better chart types.
"""

import requests
import json
from typing import Dict, Any

API_URL = "http://localhost:8000"

def test_chart_selection(question: str, expected_type: str = None) -> Dict[str, Any]:
    """Test a question and print chart recommendation."""
    
    payload = {
        "question": question,
        "company_id": "electronics",
        "section_ids": []
    }
    
    print(f"\n{'='*80}")
    print(f"Question: {question}")
    print(f"{'='*80}")
    
    try:
        response = requests.post(f"{API_URL}/ask", json=payload)
        response.raise_for_status()
        
        data = response.json()
        charts = data.get("charts", [])
        
        if charts:
            chart = charts[0]
            print(f"✅ Chart Detected:")
            print(f"   Type: {chart['type']}")
            print(f"   Title: {chart['title']}")
            print(f"   X-axis: {chart['x_column']}")
            print(f"   Y-axis: {', '.join(chart['y_columns'])}")
            print(f"   Confidence: {chart['confidence']:.0%}")
            print(f"   Data points: {len(chart['data'])}")
            
            if expected_type:
                if chart['type'] == expected_type:
                    print(f"   ✅ CORRECT: Expected {expected_type}, got {chart['type']}")
                else:
                    print(f"   ❌ WRONG: Expected {expected_type}, got {chart['type']}")
        else:
            print("❌ No chart detected")
            
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}


def main():
    """Run test suite."""
    
    print("\n" + "="*80)
    print("AI CHART SELECTION TEST SUITE")
    print("="*80)
    
    # Test 1: Comparison query (should be BAR, not PIE)
    test_chart_selection(
        "Compare top 3 and bottom 3 products by revenue",
        expected_type="bar"
    )
    
    # Test 2: Ranking query (should be BAR)
    test_chart_selection(
        "Rank employees by salary",
        expected_type="bar"
    )
    
    # Test 3: Time series (should be LINE)
    test_chart_selection(
        "Show sales trend over time",
        expected_type="line"
    )
    
    # Test 4: Small categorical breakdown (PIE ok)
    test_chart_selection(
        "Show revenue by department",
        expected_type="pie"  # Only 3-4 departments
    )
    
    # Test 5: Many categories (should be BAR, not PIE)
    test_chart_selection(
        "Show revenue by product category",
        expected_type="bar"  # Many product categories
    )
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
