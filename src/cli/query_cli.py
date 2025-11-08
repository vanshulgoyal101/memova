"""
Command-line interface for the query engine
Production-ready with proper formatting and error handling
"""

import sys
from typing import Dict, Any, Optional

from src.core.query_engine import QueryEngine
from src.utils.logger import setup_logger
from src.utils.exceptions import AppException

logger = setup_logger(__name__)


class QueryCLI:
    """Command-line interface for natural language queries"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize CLI
        
        Args:
            db_path: Optional path to database file
        """
        self.engine = None
        self.db_path = db_path
    
    def _init_engine(self):
        """Initialize query engine with error handling"""
        if self.engine is not None:
            return
        
        try:
            print("🔄 Initializing query engine...")
            self.engine = QueryEngine(db_path=self.db_path)
            print(f"✅ Connected to Google AI Studio")
            print(f"📦 Using model: {self.engine.model_name}")
            print(f"🗄️  Database: {self.engine.db_manager.db_path}\n")
            
        except AppException as e:
            print(f"\n❌ Error: {e}\n")
            sys.exit(1)
        except Exception as e:
            logger.exception("Unexpected error during initialization")
            print(f"\n❌ Unexpected error: {e}\n")
            sys.exit(1)
    
    def print_results(self, result: Dict[str, Any]):
        """
        Pretty print query results
        
        Args:
            result: Query result dictionary
        """
        if not result['success']:
            print(f"❌ Error: {result.get('error', 'Unknown error')}\n")
            return
        
        results = result['results']
        
        # Print metadata
        print(f"✅ Success! ({result['row_count']} rows in {result['execution_time']:.3f}s)")
        
        if result.get('truncated'):
            print(f"⚠️  Results truncated to {len(results)} rows\n")
        else:
            print()
        
        if not results:
            print("No results found.\n")
            return
        
        # Get columns
        columns = list(results[0].keys())
        
        # Calculate column widths
        widths = {col: len(col) for col in columns}
        for row in results[:50]:  # Check first 50 for width
            for col in columns:
                val = str(row[col]) if row[col] is not None else "NULL"
                widths[col] = min(max(widths[col], len(val)), 50)  # Max width 50
        
        # Print header
        header = " | ".join(col.ljust(widths[col]) for col in columns)
        separator = "-+-".join("-" * widths[col] for col in columns)
        
        print(header)
        print(separator)
        
        # Print rows (limit display to 50)
        display_limit = min(50, len(results))
        for row in results[:display_limit]:
            line = " | ".join(
                str(row[col])[:50].ljust(widths[col]) if row[col] is not None
                else "NULL".ljust(widths[col])
                for col in columns
            )
            print(line)
        
        if len(results) > display_limit:
            print(f"\n... ({len(results) - display_limit} more rows not shown)")
        print()
    
    def interactive_mode(self):
        """Run interactive query mode"""
        print("=" * 70)
        print("  🤖 NATURAL LANGUAGE DATABASE QUERY")
        print("=" * 70)
        print("\n  Ask questions in plain English!")
        print("  Commands:")
        print("    - Type question to query")
        print("    - 'tables' - List available tables")
        print("    - 'schema' - Show database schema")
        print("    - 'exit' or 'quit' - Exit")
        print("\n" + "=" * 70 + "\n")
        
        self._init_engine()
        
        while True:
            try:
                question = input("💬 Question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!\n")
                    break
                
                if question.lower() == 'tables':
                    tables = self.engine.get_available_tables()
                    print(f"\n📋 Available tables ({len(tables)}):")
                    for table in tables:
                        count = self.engine.db_manager.get_row_count(table)
                        print(f"  - {table} ({count} rows)")
                    print()
                    continue
                
                if question.lower() == 'schema':
                    print(f"\n{self.engine.get_schema_info()}")
                    continue
                
                # Process question
                print()
                result = self.engine.ask(question)
                
                # Show generated SQL
                if result['success']:
                    print(f"📝 SQL: {result['sql']}\n")
                
                self.print_results(result)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                logger.exception("Error in interactive mode")
                print(f"\n❌ Error: {e}\n")
    
    def single_query(self, question: str):
        """
        Execute a single query
        
        Args:
            question: Natural language question
        """
        self._init_engine()
        
        print(f"🤔 Question: {question}\n")
        
        result = self.engine.ask(question)
        
        if result['success']:
            print(f"📝 SQL: {result['sql']}\n")
        
        self.print_results(result)


def main():
    """Main entry point"""
    cli = QueryCLI()
    
    if len(sys.argv) > 1:
        # Single question mode
        question = " ".join(sys.argv[1:])
        cli.single_query(question)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
