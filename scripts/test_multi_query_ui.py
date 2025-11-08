#!/usr/bin/env python3
"""
Quick test script for multi-query API endpoints.
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_simple_question():
    """Test simple question (single query)"""
    print("=" * 60)
    print("TEST 1: Simple Question (single query)")
    print("=" * 60)
    
    response = requests.post(f"{API_BASE}/ask", json={
        "question": "How many employees are there?",
        "company_id": "electronics",
        "section_ids": []
    })
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Multi-query: {data['meta'].get('multi_query', False)}")
        print(f"Query count: {data['meta'].get('query_count', 1)}")
        print(f"Has query_plan: {data.get('query_plan') is not None}")
        print(f"Answer: {data['answer_text'][:100]}...")
    else:
        print(f"Error: {response.text}")
    print()

def test_comparison_question():
    """Test comparison question (multi-query)"""
    print("=" * 60)
    print("TEST 2: Comparison Question (multi-query)")
    print("=" * 60)
    
    response = requests.post(f"{API_BASE}/ask", json={
        "question": "Compare IT vs Sales department employee counts",
        "company_id": "electronics",
        "section_ids": []
    })
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Multi-query: {data['meta'].get('multi_query', False)}")
        print(f"Query count: {data['meta'].get('query_count', 1)}")
        print(f"Has query_plan: {data.get('query_plan') is not None}")
        
        if data.get('query_plan'):
            plan = data['query_plan']
            print(f"\nQuery Plan Details:")
            print(f"  Total queries: {len(plan['queries'])}")
            print(f"  Final query: {plan['final_query_id']}")
            print(f"  Is complete: {plan['is_complete']}")
            print(f"  Has errors: {plan['has_errors']}")
            print(f"  Total time: {plan['total_execution_time_ms']}ms")
            
            print(f"\n  Query Steps:")
            for q in plan['queries']:
                print(f"    - {q['id']}: {q['description']} ({q['status']})")
                if q['row_count'] is not None:
                    print(f"      Rows: {q['row_count']}, Time: {q['execution_time_ms']}ms")
        
        print(f"\nAnswer: {data['answer_text'][:150]}...")
    else:
        print(f"Error: {response.text}")
    print()

if __name__ == "__main__":
    print("\n🧪 Testing Multi-Query API Integration\n")
    
    try:
        test_simple_question()
        test_comparison_question()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\n💡 Now test in the browser at http://localhost:3000")
        print("   Try asking: 'Compare IT vs Sales departments'\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
