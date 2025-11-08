#!/usr/bin/env python3
"""
Example queries demonstrating various SQL query types
"""

from llm_query import DatabaseQueryEngine


EXAMPLE_QUESTIONS = [
    # Simple queries
    "How many employees do we have?",
    "List all product categories",
    "Show me customers from California",
    
    # Aggregations
    "What is the total revenue from all sales?",
    "Calculate average salary by department",
    "How many products in each category?",
    
    # Complex joins
    "Show me the top 10 customers by total purchase amount",
    "Which employees processed the most orders?",
    "What products have less than 50 units in inventory?",
    
    # Analytics
    "What is the average order value?",
    "Which warehouse has the highest inventory value?",
    "Show me pending customer service tickets",
    
    # Time-based
    "List employees hired in 2024",
    "Show sales from the last 30 days",
]


def run_examples():
    """Run all example queries"""
    print("\n" + "=" * 70)
    print("  📚 EXAMPLE QUERIES")
    print("=" * 70 + "\n")
    
    try:
        engine = DatabaseQueryEngine()
    except Exception as e:
        print(f"❌ {e}\n")
        return
    
    for i, question in enumerate(EXAMPLE_QUESTIONS, 1):
        print("=" * 70)
        print(f"EXAMPLE {i}/{len(EXAMPLE_QUESTIONS)}")
        print("=" * 70 + "\n")
        
        result = engine.ask(question)
        engine.print_results(result)
        
        if i < len(EXAMPLE_QUESTIONS):
            input("Press Enter for next example...\n")
    
    print("=" * 70)
    print("  ✨ All Examples Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_examples()
