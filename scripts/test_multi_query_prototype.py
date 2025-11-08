"""
Manual test script for multi-query prototype.

Demonstrates multi-query execution without AI integration.
Tests hardcoded query plans to validate the core execution logic.
"""

from pathlib import Path
from src.core.query_engine import QueryEngine
from src.core.query_plan import QueryPlan, QueryStep, create_comparison_plan
import json


def test_simple_single_query():
    """Test 1: Simple single-query plan (backward compatibility)"""
    print("\n" + "="*70)
    print("TEST 1: Simple Single Query")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    plan = QueryPlan.create_simple_plan(
        sql="SELECT COUNT(*) as total_employees FROM employees",
        question="How many employees do we have?"
    )
    
    print(f"Question: {plan.question}")
    print(f"Plan: {len(plan.queries)} query")
    
    executed_plan = engine.execute_plan(plan)
    
    print(f"Status: {'✅ Success' if executed_plan.is_complete() else '❌ Failed'}")
    print(f"Execution time: {executed_plan.total_execution_time_ms:.1f}ms")
    
    results = executed_plan.get_final_results()
    if results:
        print(f"Results: {results['rows'][0][0]} employees")
    
    return executed_plan.is_complete()


def test_department_comparison():
    """Test 2: Compare two departments (independent queries + merge)"""
    print("\n" + "="*70)
    print("TEST 2: Department Comparison (3-step plan)")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    plan = QueryPlan(
        queries=[
            QueryStep(
                id="q1",
                description="Get IT employee count",
                sql="SELECT COUNT(*) as count, AVG(salary) as avg_salary FROM employees WHERE department = 'IT'",
                depends_on=[]
            ),
            QueryStep(
                id="q2",
                description="Get Sales employee count",
                sql="SELECT COUNT(*) as count, AVG(salary) as avg_salary FROM employees WHERE department = 'Sales'",
                depends_on=[]
            ),
            QueryStep(
                id="q3",
                description="Compare departments",
                sql="""
                    SELECT 
                        'IT' as dept1,
                        (SELECT count FROM q1) as it_count,
                        ROUND((SELECT avg_salary FROM q1), 2) as it_avg_salary,
                        'Sales' as dept2,
                        (SELECT count FROM q2) as sales_count,
                        ROUND((SELECT avg_salary FROM q2), 2) as sales_avg_salary,
                        ((SELECT count FROM q1) - (SELECT count FROM q2)) as count_diff,
                        ROUND((SELECT avg_salary FROM q1) - (SELECT avg_salary FROM q2), 2) as salary_diff
                """,
                depends_on=["q1", "q2"]
            )
        ],
        final_query_id="q3",
        question="Compare IT vs Sales departments"
    )
    
    print(f"Question: {plan.question}")
    print(f"Plan: {len(plan.queries)} queries")
    print(f"Execution order: {[q.id for q in plan.get_execution_order()]}")
    
    executed_plan = engine.execute_plan(plan)
    
    print(f"Status: {'✅ Success' if executed_plan.is_complete() else '❌ Failed'}")
    print(f"Execution time: {executed_plan.total_execution_time_ms:.1f}ms")
    
    # Show intermediate results
    for query in executed_plan.queries:
        print(f"\n  {query.id}: {query.description}")
        print(f"    Status: {query.status.value}")
        print(f"    Time: {query.execution_time_ms:.1f}ms")
        print(f"    Rows: {query.row_count}")
    
    # Show final comparison
    results = executed_plan.get_final_results()
    if results:
        print("\n  Final Comparison:")
        row = results["rows"][0]
        print(f"    Raw row data: {row}")
        # Handle potential None values safely
        it_count = row[1] if row[1] is not None else 0
        it_salary = row[2] if row[2] is not None else 0
        sales_count = row[4] if row[4] is not None else 0
        sales_salary = row[5] if row[5] is not None else 0
        count_diff = row[6] if row[6] is not None else 0
        salary_diff = row[7] if row[7] is not None else 0
        
        print(f"    IT: {it_count} employees, avg salary ${it_salary:,.2f}")
        print(f"    Sales: {sales_count} employees, avg salary ${sales_salary:,.2f}")
        print(f"    Difference: {count_diff} employees, ${salary_diff:,.2f} salary")
    
    return executed_plan.is_complete()


def test_chained_dependencies():
    """Test 3: Linear dependency chain (q1 -> q2 -> q3)"""
    print("\n" + "="*70)
    print("TEST 3: Chained Dependencies (Linear)")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    plan = QueryPlan(
        queries=[
            QueryStep(
                id="q1",
                description="Calculate average salary",
                sql="SELECT AVG(salary) as avg_salary FROM employees",
                depends_on=[]
            ),
            QueryStep(
                id="q2",
                description="Count employees above average",
                sql="SELECT COUNT(*) as above_avg_count FROM employees WHERE salary > (SELECT avg_salary FROM q1)",
                depends_on=["q1"]
            ),
            QueryStep(
                id="q3",
                description="Calculate what % are above average",
                sql="""
                    SELECT 
                        (SELECT COUNT(*) FROM employees) as total,
                        (SELECT above_avg_count FROM q2) as above_avg,
                        ROUND((SELECT above_avg_count FROM q2) * 100.0 / (SELECT COUNT(*) FROM employees), 1) as pct_above_avg
                """,
                depends_on=["q2"]
            )
        ],
        final_query_id="q3",
        question="What percentage of employees earn above average?"
    )
    
    print(f"Question: {plan.question}")
    print(f"Plan: {len(plan.queries)} queries (linear chain)")
    print(f"Execution order: {' -> '.join([q.id for q in plan.get_execution_order()])}")
    
    executed_plan = engine.execute_plan(plan)
    
    print(f"Status: {'✅ Success' if executed_plan.is_complete() else '❌ Failed'}")
    print(f"Execution time: {executed_plan.total_execution_time_ms:.1f}ms")
    
    # Show each step
    for query in executed_plan.queries:
        print(f"\n  {query.id}: {query.description}")
        print(f"    Result: {query.results['rows'][0] if query.results else 'N/A'}")
    
    # Show final answer
    results = executed_plan.get_final_results()
    if results:
        total, above_avg, pct = results["rows"][0]
        print(f"\n  Final Answer: {above_avg}/{total} employees ({pct}%) earn above average")
    
    return executed_plan.is_complete()


def test_plan_serialization():
    """Test 4: Verify plan can be serialized to JSON"""
    print("\n" + "="*70)
    print("TEST 4: Plan Serialization")
    print("="*70)
    
    engine = QueryEngine(db_path="data/database/electronics_company.db")
    
    plan = QueryPlan.create_simple_plan(
        sql="SELECT department, COUNT(*) as count FROM employees GROUP BY department ORDER BY count DESC LIMIT 3",
        question="What are the top 3 departments?"
    )
    
    executed_plan = engine.execute_plan(plan)
    
    # Serialize to JSON
    plan_dict = executed_plan.to_dict()
    json_str = json.dumps(plan_dict, indent=2)
    
    print("Serialized plan (first 500 chars):")
    print(json_str[:500] + "...")
    
    print(f"\nSerialization: ✅ Success")
    print(f"JSON size: {len(json_str)} bytes")
    
    return True


def main():
    """Run all prototype tests"""
    print("\n" + "="*70)
    print("MULTI-QUERY PROTOTYPE TESTS")
    print("Testing QueryPlan execution without AI integration")
    print("="*70)
    
    tests = [
        ("Simple single query", test_simple_single_query),
        ("Department comparison", test_department_comparison),
        ("Chained dependencies", test_chained_dependencies),
        ("Plan serialization", test_plan_serialization)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
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
        print("\n🎉 All prototype tests passed! Multi-query execution works.")
        print("Next step: Add AI-powered query plan generation.")
    else:
        print("\n⚠️  Some tests failed. Review errors above.")


if __name__ == "__main__":
    main()
