#!/usr/bin/env python3
"""
Test AI Business Insights Feature
Demonstrates automatic routing between data and analytical queries
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.query_engine import QueryEngine
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_question(engine, question, expected_type):
    """Test a single question and display results"""
    console.print(f"\n[bold cyan]Question:[/] {question}")
    console.print(f"[dim]Expected type: {expected_type}[/]")
    
    result = engine.ask(question)
    actual_type = result.get('query_type', 'unknown')
    
    # Check if routing worked correctly
    status = "✅" if actual_type == expected_type else "❌"
    console.print(f"{status} Actual type: [bold]{actual_type}[/]")
    
    if actual_type == 'data':
        # Data query result
        console.print(f"[dim]SQL:[/] {result.get('sql', 'N/A')[:80]}...")
        console.print(f"[dim]Rows returned:[/] {len(result.get('results', []))}")
        
    elif actual_type == 'analytical':
        # Analytical query result
        analysis = result.get('analysis', {})
        
        # Display insights
        if analysis.get('insights'):
            console.print("\n[bold yellow]🔍 Key Insights:[/]")
            for i, insight in enumerate(analysis['insights'][:3], 1):
                console.print(f"  {i}. {insight[:80]}...")
        
        # Display recommendations
        if analysis.get('recommendations'):
            console.print("\n[bold green]💡 Recommendations:[/]")
            for i, rec in enumerate(analysis['recommendations'][:3], 1):
                console.print(f"  {i}. {rec[:80]}...")
        
        # Display metrics
        if analysis.get('data_points'):
            console.print(f"\n[dim]Data points analyzed:[/] {len(analysis['data_points'])}")
            for dp in analysis['data_points'][:3]:
                console.print(f"  - {dp['name']}: {dp['value']:,}")
    
    return actual_type == expected_type

def main():
    """Run test suite"""
    console.print(Panel.fit(
        "[bold]AI Business Insights - Test Suite[/]\n"
        "Automatic routing between data and analytical queries",
        border_style="cyan"
    ))
    
    # Initialize query engine
    db_path = "data/database/electronics_company.db"
    
    if not Path(db_path).exists():
        console.print(f"[red]Error: Database not found at {db_path}[/]")
        console.print("Run 'make generate' to create test data")
        return 1
    
    engine = QueryEngine(db_path=db_path)
    
    # Test cases: (question, expected_type)
    test_cases = [
        # Data queries (should return SQL results)
        ("How many products are there?", "data"),
        ("Show top 5 products by revenue", "data"),
        ("What is the average order value?", "data"),
        
        # Analytical queries (should return insights)
        ("Give me insights to improve sales", "analytical"),
        ("Recommend strategies to grow revenue", "analytical"),
        ("What actionable steps can I take to boost customer satisfaction?", "analytical"),
        ("Analyze product performance and suggest improvements", "analytical"),
    ]
    
    # Run tests
    results = []
    for question, expected_type in test_cases:
        passed = test_question(engine, question, expected_type)
        results.append(passed)
    
    # Summary
    console.print("\n" + "="*60)
    passed_count = sum(results)
    total_count = len(results)
    
    if passed_count == total_count:
        console.print(f"[bold green]✅ All tests passed ({passed_count}/{total_count})[/]")
        return 0
    else:
        console.print(f"[bold red]❌ Some tests failed ({passed_count}/{total_count})[/]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
