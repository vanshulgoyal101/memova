"""
Unit Tests for Domain Validation (Hallucination Prevention)

Tests the pre-validation system that prevents the LLM from hallucinating
answers on wrong databases by checking if question keywords match the schema.
"""

import pytest
from pathlib import Path

from src.core.query_engine import QueryEngine
from src.utils.config import Config
from src.utils.exceptions import QueryError


class TestDomainValidation:
    """Test domain validation across all databases"""
    
    @pytest.fixture
    def electronics_engine(self):
        """Query engine for electronics database"""
        db_path = Config.DATABASE_DIR / 'electronics_company.db'
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def airline_engine(self):
        """Query engine for airline database"""
        db_path = Config.DATABASE_DIR / 'airline_company.db'
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def edtech_engine(self):
        """Query engine for edtech database"""
        db_path = Config.DATABASE_DIR / 'edtech_company.db'
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def ednite_engine(self):
        """Query engine for ednite database"""
        db_path = Config.DATABASE_DIR / 'ednite_company.db'
        return QueryEngine(db_path=str(db_path))
    
    @pytest.fixture
    def liqo_engine(self):
        """Query engine for liqo database"""
        db_path = Config.DATABASE_DIR / 'liqo_company.db'
        return QueryEngine(db_path=str(db_path))
    
    # ===== NEGATIVE TESTS: Should Fail Validation =====
    
    def test_electronics_rejects_student_questions(self, electronics_engine):
        """Electronics DB should reject questions about students"""
        question = "Show me top 10 students by score"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'student'" in error_msg.lower()
        assert "available tables" in error_msg.lower()
    
    def test_electronics_rejects_class_questions(self, electronics_engine):
        """Electronics DB should reject questions about classes/courses"""
        question = "Show me students in class 10"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert ("class" in error_msg.lower() or "student" in error_msg.lower())
    
    def test_electronics_rejects_question_analysis(self, electronics_engine):
        """Electronics DB should reject questions about test questions"""
        question = "What are the top 3 most difficult questions?"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'question'" in error_msg.lower()
    
    def test_airline_rejects_student_questions(self, airline_engine):
        """Airline DB should reject questions about students"""
        question = "Show me students enrolled in courses"
        with pytest.raises(QueryError) as exc_info:
            airline_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'student'" in error_msg.lower()
    
    def test_liqo_rejects_student_questions(self, liqo_engine):
        """Liqo DB should reject questions about students"""
        question = "Show me students with highest scores"
        with pytest.raises(QueryError) as exc_info:
            liqo_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'student'" in error_msg.lower()
    
    # ===== MULTI-QUERY PATH VALIDATION =====
    
    def test_multiquery_rejects_mismatched_domain(self, electronics_engine):
        """Multi-query generation should also validate domain"""
        question = "Compare top 3 difficult and easy test questions"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate_query_plan(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about" in error_msg.lower()
    
    # ===== ANALYST PATH VALIDATION =====
    
    def test_analyst_rejects_mismatched_domain(self, electronics_engine):
        """Business analyst should also validate domain"""
        question = "How can I improve student test scores?"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.analyst.analyze(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'student'" in error_msg.lower()
    
    # ===== ERROR MESSAGE QUALITY =====
    
    def test_error_message_includes_available_tables(self, electronics_engine):
        """Error message should list available tables"""
        question = "Show me students"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "available tables" in error_msg.lower()
        assert ("products" in error_msg.lower() or 
                "customers" in error_msg.lower() or 
                "employees" in error_msg.lower())
    
    def test_error_message_includes_tip(self, electronics_engine):
        """Error message should include helpful tip"""
        question = "Show me students"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "tip:" in error_msg.lower() or "switch" in error_msg.lower()
    
    # ===== KEYWORD VARIATIONS =====
    
    def test_detects_enrollment_keyword(self, electronics_engine):
        """Should detect 'enrollment' as student-related"""
        question = "Show me course enrollments"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'student'" in error_msg.lower()
    
    def test_detects_quiz_keyword(self, electronics_engine):
        """Should detect 'quiz' as question-related"""
        question = "Show me quiz results"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'question'" in error_msg.lower()
    
    def test_detects_exam_keyword(self, electronics_engine):
        """Should detect 'exam' as question-related"""
        question = "Show me exam scores"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert ("question" in error_msg.lower() or "score" in error_msg.lower())
    
    def test_detects_teacher_keyword(self, liqo_engine):
        """Should detect 'teacher' as education-related"""
        question = "Show me teacher assignments"
        with pytest.raises(QueryError) as exc_info:
            liqo_engine.sql_generator.generate(question)
        
        error_msg = str(exc_info.value)
        assert "does not contain data about 'teacher'" in error_msg.lower()
    
    # ===== EDGE CASES =====
    
    def test_case_insensitive_detection(self, electronics_engine):
        """Domain validation should be case-insensitive"""
        question = "Show me STUDENTS"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        # Should still detect despite uppercase
        error_msg = str(exc_info.value)
        assert "does not contain data about" in error_msg.lower()
    
    def test_multiple_mismatches(self, electronics_engine):
        """Should detect multiple mismatched keywords"""
        question = "Show me students and teachers for each class"
        with pytest.raises(QueryError) as exc_info:
            electronics_engine.sql_generator.generate(question)
        
        # Should detect at least one of the keywords
        error_msg = str(exc_info.value).lower()
        assert ("student" in error_msg or 
                "teacher" in error_msg or 
                "class" in error_msg)


class TestDomainValidationIntegration:
    """Integration tests for domain validation with real databases"""
    
    def test_all_databases_exist(self):
        """Verify all databases are accessible"""
        databases = ['electronics_company.db', 'airline_company.db', 
                     'edtech_company.db', 'ednite_company.db', 'liqo_company.db']
        
        for db_name in databases:
            db_path = Config.DATABASE_DIR / db_name
            assert db_path.exists(), f"Database not found: {db_name}"
    
    def test_can_initialize_all_engines(self):
        """Verify all databases can have query engines initialized"""
        databases = {
            'electronics': Config.DATABASE_DIR / 'electronics_company.db',
            'airline': Config.DATABASE_DIR / 'airline_company.db',
            'edtech': Config.DATABASE_DIR / 'edtech_company.db',
            'ednite': Config.DATABASE_DIR / 'ednite_company.db',
            'liqo': Config.DATABASE_DIR / 'liqo_company.db',
        }
        
        for name, path in databases.items():
            engine = QueryEngine(db_path=str(path))
            assert engine.sql_generator.schema_text is not None, f"Failed to load schema for {name}"
            assert "Table:" in engine.sql_generator.schema_text, f"Schema format incorrect for {name}"
