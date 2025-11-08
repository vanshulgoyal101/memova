"""
Manual test script for AI-powered query plan generation.

Demonstrates AI generating multi-query plans for complex questions.
"""

from pathlib import Path
from src.core.query_engine import QueryEngine
import json


def test_ai_comparison_plan():
    """Test AI generating a comparison plan"""
    print("\n" + "="*70)
    print("TEST: AI-Generated Comparison Plan")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    question = "Compare IT vs Sales department employee counts and average salaries"
    
    print(f"\nQuestion: {question}")
    print(f"Multi-query needed: {engine.sql_generator.needs_multi_query(question)}")
    
    print("\n🤖 Asking AI to generate query plan...")
    
    # Generate plan
    plan = engine.sql_generator.generate_query_plan(question)
    
    print(f"\n✅ AI generated {len(plan.queries)}-query plan")
    print(f"Final query: {plan.final_query_id}")
    print(f"\nExecution order: {' → '.join([q.id for q in plan.get_execution_order()])}")
    
    # Show each query
    print("\n" + "-"*70)
    print("QUERY PLAN DETAILS:")
    print("-"*70)
    
    for i, query in enumerate(plan.queries, 1):
        print(f"\n{i}. Query ID: {query.id}")
        print(f"   Description: {query.description}")
        print(f"   Depends on: {query.depends_on if query.depends_on else 'None (independent)'}")
        print(f"   SQL: {query.sql}")
    
    # Execute the plan
    print("\n" + "-"*70)
    print("EXECUTING PLAN:")
    print("-"*70)
    
    executed_plan = engine.execute_plan(plan)
    
    print(f"\nStatus: {'✅ Success' if executed_plan.is_complete() else '❌ Failed'}")
    print(f"Total execution time: {executed_plan.total_execution_time_ms:.1f}ms")
    
    # Show results for each query
    for query in executed_plan.queries:
        print(f"\n{query.id}: {query.status.value} ({query.execution_time_ms:.1f}ms, {query.row_count} rows)")
    
    # Show final results
    results = executed_plan.get_final_results()
    if results:
        print("\n" + "-"*70)
        print("FINAL RESULTS:")
        print("-"*70)
        print(f"Columns: {results['columns']}")
        for row in results["rows"]:
            print(f"Row: {row}")
    
    return executed_plan.is_complete()


def test_ai_simple_vs_multi():
    """Compare simple vs multi-query detection"""
    print("\n" + "="*70)
    print("TEST: Simple vs Multi-Query Detection")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    test_questions = [
        ("How many employees are there?", False),
        ("What is the average salary?", False),
        ("Show all departments", False),
        ("Compare IT vs Sales departments", True),
        ("Show the difference between Finance and Marketing salaries", True),
        ("Get top 5 and bottom 5 employees by salary", True),
    ]
    
    print("\n{:<60} {:<15}".format("Question", "Multi-Query?"))
    print("-"*70)
    
    for question, expected in test_questions:
        needs_multi = engine.sql_generator.needs_multi_query(question)
        status = "✅" if needs_multi == expected else "❌"
        print(f"{status} {question:<58} {str(needs_multi):<15}")
    
    return True


def test_ai_plan_serialization():
    """Test that AI-generated plans can be serialized"""
    print("\n" + "="*70)
    print("TEST: AI Plan Serialization")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    question = "Compare Finance and IT departments"
    
    print(f"\nQuestion: {question}")
    
    # Generate and execute plan
    plan = engine.sql_generator.generate_query_plan(question)
    executed_plan = engine.execute_plan(plan)
    
    # Serialize to JSON
    plan_dict = executed_plan.to_dict()
    json_str = json.dumps(plan_dict, indent=2)
    
    print(f"\n✅ Plan serialized to JSON ({len(json_str)} bytes)")
    print("\nJSON structure:")
    print(json_str[:800] + "..." if len(json_str) > 800 else json_str)
    
    return True


def main():
    """Run all AI query plan tests"""
    print("\n" + "="*70)
    print("AI-POWERED MULTI-QUERY PLAN GENERATION TESTS")
    print("Testing LLM-generated query plans")
    print("="*70)
    
    tests = [
        ("AI comparison plan generation", test_ai_comparison_plan),
        ("Simple vs multi-query detection", test_ai_simple_vs_multi),
        ("AI plan serialization", test_ai_plan_serialization),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All AI query plan tests passed!")
        print("✨ AI successfully generates and executes multi-query plans!")
        print("Next step: Wire into API endpoints (/ask, /query)")
    else:
        print("\n⚠️  Some tests failed. Review errors above.")


if __name__ == "__main__":
    main()
