#!/usr/bin/env python3
"""
Test script to verify prompt caching is working in the intelligent analyst

This script:
1. Runs a simple data query (1 LLM call)
2. Runs an analytical query (3 LLM calls)
3. Runs another analytical query (3 LLM calls, should use cache)
4. Shows token usage for each call

Expected results WITH caching:
- Data query: ~1,550 tokens (schema in system message)
- Analytical query 1 (cold):
  - Call 1: ~2,600 tokens (schema cached)
  - Call 2: ~250 tokens (schema from cache)
  - Call 3: ~500 tokens (schema from cache)
  - Total: ~3,350 tokens
- Analytical query 2 (warm):
  - Call 1: ~100 tokens (schema from cache)
  - Call 2: ~250 tokens (schema from cache)
  - Call 3: ~500 tokens (schema from cache)
  - Total: ~850 tokens

Expected results WITHOUT caching:
- Each call: ~1,500-2,500 tokens (full schema every time)
"""

import sys
import time
sys.path.insert(0, '.')

from src.core.query_engine import QueryEngine

def main():
    print("=" * 80)
    print("TOKEN USAGE TEST - PROMPT CACHING VERIFICATION")
    print("=" * 80)
    print()
    
    engine = QueryEngine(db_path='data/database/electronics_company.db')
    
    # Test 1: Simple data query (baseline)
    print("📊 TEST 1: Simple Data Query (1 LLM call)")
    print("-" * 80)
    question1 = "How many products do we have?"
    print(f"Question: \"{question1}\"")
    print()
    
    start = time.time()
    result1 = engine.ask(question1)
    time1 = time.time() - start
    
    print(f"Time: {time1:.2f}s")
    print(f"Success: {result1.get('success')}")
    print(f"Query Type: {result1.get('query_type')}")
    print()
    print("Look for: 🔢 Groq tokens in logs above")
    print()
    
    # Test 2: First analytical query (3 LLM calls, should cache schema)
    print("=" * 80)
    print("🧠 TEST 2: First Analytical Query (3 LLM calls - COLD, caches schema)")
    print("-" * 80)
    question2 = "My sales are declining"
    print(f"Question: \"{question2}\"")
    print()
    
    start = time.time()
    result2 = engine.ask(question2)
    time2 = time.time() - start
    
    print()
    print(f"Time: {time2:.2f}s")
    print(f"Success: {result2.get('success')}")
    print(f"Query Type: {result2.get('query_type')}")
    
    if 'analysis' in result2:
        analysis = result2['analysis']
        print(f"Hypotheses: {len(analysis.get('hypotheses', []))}")
        print(f"Custom Queries: {len(analysis.get('queries_used', []))}")
        print(f"Insights: {len(analysis.get('insights', []))}")
        print(f"Recommendations: {len(analysis.get('recommendations', []))}")
    
    print()
    print("Expected token usage:")
    print("  Call 1 (interpret): ~2,600 tokens (schema cached)")
    print("  Call 2 (plan):      ~250 tokens (schema from cache)")
    print("  Call 3 (analyze):   ~500 tokens (schema from cache)")
    print("  Total:              ~3,350 tokens")
    print()
    
    # Test 3: Second analytical query (3 LLM calls, should use cache)
    print("=" * 80)
    print("🧠 TEST 3: Second Analytical Query (3 LLM calls - WARM, uses cache)")
    print("-" * 80)
    question3 = "Revenue is too low"
    print(f"Question: \"{question3}\"")
    print()
    
    start = time.time()
    result3 = engine.ask(question3)
    time3 = time.time() - start
    
    print()
    print(f"Time: {time3:.2f}s")
    print(f"Success: {result3.get('success')}")
    print(f"Query Type: {result3.get('query_type')}")
    
    if 'analysis' in result3:
        analysis = result3['analysis']
        print(f"Hypotheses: {len(analysis.get('hypotheses', []))}")
        print(f"Custom Queries: {len(analysis.get('queries_used', []))}")
        print(f"Insights: {len(analysis.get('insights', []))}")
        print(f"Recommendations: {len(analysis.get('recommendations', []))}")
    
    print()
    print("Expected token usage:")
    print("  Call 1 (interpret): ~100 tokens (schema from cache)")
    print("  Call 2 (plan):      ~250 tokens (schema from cache)")
    print("  Call 3 (analyze):   ~500 tokens (schema from cache)")
    print("  Total:              ~850 tokens")
    print()
    
    # Summary
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print()
    print(f"Test 1 (data query):       {time1:.2f}s")
    print(f"Test 2 (analytical cold):  {time2:.2f}s")
    print(f"Test 3 (analytical warm):  {time3:.2f}s")
    print()
    
    if time3 < time2:
        speedup = ((time2 - time3) / time2) * 100
        print(f"⚡ Speedup: {speedup:.1f}% faster (warm vs cold)")
        if speedup > 20:
            print("✅ Caching appears to be working!")
        else:
            print("⚠️  Modest speedup - may indicate caching not fully optimized")
    else:
        print("⚠️  Warm run was slower than cold - unexpected")
    
    print()
    print("📝 NOTES:")
    print("- Look for '🔢 Groq tokens:' lines in logs above")
    print("- If you see 'Cache hit:' messages, caching is working!")
    print("- If using Gemini (fallback), Groq limits may still be hit")
    print("- Token counts should decrease significantly on warm runs")
    print()
    print("Expected total tokens (with caching):")
    print("  Cold run:  ~3,350 tokens")
    print("  Warm run:  ~850 tokens")
    print("  Savings:   ~75% reduction!")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
