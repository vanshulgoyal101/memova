"""
EdNite India Test Results Data Generator

Converts raw CSV data (AnswerKeys.csv, Result.csv) into a normalized SQLite database
with proper schema for querying student performance, question analysis, and class comparisons.
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


def clean_answer(answer: str) -> str:
    """
    Clean and standardize answer format.
    
    Handles:
    - Multiple answers: "A,D" or "a,d" → "a,d"
    - Empty/NaN → ""
    - Whitespace
    
    Args:
        answer: Raw answer string
        
    Returns:
        Cleaned lowercase answer
    """
    if pd.isna(answer) or answer == '':
        return ''
    
    # Convert to string and lowercase
    answer = str(answer).lower().strip()
    
    # Handle multiple answers (comma-separated)
    if ',' in answer:
        parts = [a.strip() for a in answer.split(',')]
        return ','.join(sorted(parts))
    
    return answer


def create_ednite_schema(db_path: str) -> None:
    """
    Create normalized schema for EdNite test data.
    
    Schema:
    - classes: Class metadata (5-10)
    - questions: Question metadata with answer keys per class
    - students: Student metadata
    - student_answers: Student responses to questions
    - performance_summary: Calculated scores per student
    
    Args:
        db_path: Path to SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Classes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY,
            class_name TEXT NOT NULL UNIQUE,
            total_students INTEGER DEFAULT 0,
            total_questions INTEGER DEFAULT 0
        )
    """)
    
    # Questions table (with answer keys per class)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY,
            question_number INTEGER NOT NULL,
            class_id INTEGER NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(class_id),
            UNIQUE(question_number, class_id)
        )
    """)
    
    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            roll_number TEXT NOT NULL UNIQUE,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )
    """)
    
    # Student answers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_answers (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            student_answer TEXT,
            is_correct INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            UNIQUE(student_id, question_number)
        )
    """)
    
    # Performance summary table (pre-calculated for fast queries)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_summary (
            student_id INTEGER PRIMARY KEY,
            class_id INTEGER NOT NULL,
            roll_number TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            questions_attempted INTEGER NOT NULL,
            correct_answers INTEGER NOT NULL,
            incorrect_answers INTEGER NOT NULL,
            unanswered INTEGER NOT NULL,
            score_percentage REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (class_id) REFERENCES classes(class_id)
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_answers_student ON student_answers(student_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_answers_question ON student_answers(question_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_class ON questions(class_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_performance_class ON performance_summary(class_id)")
    
    conn.commit()
    conn.close()
    
    logger.info("✅ EdNite schema created successfully")


def load_answer_keys(csv_path: str, db_path: str) -> None:
    """
    Load answer keys from AnswerKeys.csv into questions table.
    
    CSV Format:
    Question No.,Class - 5,Class - 6,Class - 7,Class - 8,Class - 9,Class - 10
    1,d,c,b,a,e,b
    
    Args:
        csv_path: Path to AnswerKeys.csv
        db_path: Path to SQLite database
    """
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Extract class columns
    class_columns = [col for col in df.columns if col.startswith('Class -')]
    
    # Insert classes
    for col in class_columns:
        class_num = int(col.replace('Class - ', ''))
        cursor.execute("""
            INSERT OR IGNORE INTO classes (class_id, class_name)
            VALUES (?, ?)
        """, (class_num, f"Class {class_num}"))
    
    # Insert questions with answer keys
    questions_inserted = 0
    for _, row in df.iterrows():
        question_num = int(row['Question No.'])
        
        for col in class_columns:
            class_num = int(col.replace('Class - ', ''))
            correct_answer = clean_answer(row[col])
            
            cursor.execute("""
                INSERT OR IGNORE INTO questions (question_number, class_id, correct_answer)
                VALUES (?, ?, ?)
            """, (question_num, class_num, correct_answer))
            questions_inserted += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Loaded {len(df)} questions × {len(class_columns)} classes = {questions_inserted} answer keys")


def load_student_results(csv_path: str, db_path: str) -> None:
    """
    Load student results from Result.csv into students and student_answers tables.
    
    CSV Format:
    NewRollNo,Class,Question1,Question2,...,Question90
    1001,5,C,D,A,...
    
    Args:
        csv_path: Path to Result.csv
        db_path: Path to SQLite database
    """
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get answer keys for validation
    cursor.execute("SELECT question_number, class_id, correct_answer FROM questions")
    answer_keys = {}
    for q_num, class_id, correct in cursor.fetchall():
        answer_keys[(q_num, class_id)] = correct
    
    students_inserted = 0
    answers_inserted = 0
    
    for idx, row in df.iterrows():
        roll_number = str(row['NewRollNo'])
        class_id = int(row['Class'])
        
        # Insert student
        cursor.execute("""
            INSERT OR IGNORE INTO students (roll_number, class_id)
            VALUES (?, ?)
        """, (roll_number, class_id))
        
        # Get student_id
        cursor.execute("SELECT student_id FROM students WHERE roll_number = ?", (roll_number,))
        student_id = cursor.fetchone()[0]
        students_inserted += 1
        
        # Insert answers
        question_cols = [col for col in df.columns if col.startswith('Question')]
        
        for col in question_cols:
            question_num = int(col.replace('Question', ''))
            student_answer = clean_answer(row[col])
            
            # Get correct answer for this question/class
            correct_answer = answer_keys.get((question_num, class_id), '')
            
            # Check if correct
            is_correct = None
            if student_answer != '':
                is_correct = 1 if student_answer == correct_answer else 0
            
            cursor.execute("""
                INSERT OR IGNORE INTO student_answers 
                (student_id, question_number, student_answer, is_correct)
                VALUES (?, ?, ?, ?)
            """, (student_id, question_num, student_answer, is_correct))
            answers_inserted += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Loaded {students_inserted} students with {answers_inserted} answers")


def calculate_performance_summary(db_path: str) -> None:
    """
    Calculate and populate performance_summary table with student scores.
    
    Calculates:
    - Total questions for their class
    - Questions attempted (non-empty answer)
    - Correct/incorrect/unanswered counts
    - Score percentage
    
    Args:
        db_path: Path to SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing summary
    cursor.execute("DELETE FROM performance_summary")
    
    # Calculate performance for each student
    cursor.execute("""
        SELECT 
            s.student_id,
            s.class_id,
            s.roll_number,
            COUNT(DISTINCT q.question_number) as total_questions,
            COUNT(CASE WHEN sa.student_answer IS NOT NULL AND sa.student_answer != '' THEN 1 END) as attempted,
            COUNT(CASE WHEN sa.is_correct = 1 THEN 1 END) as correct,
            COUNT(CASE WHEN sa.is_correct = 0 THEN 1 END) as incorrect,
            COUNT(CASE WHEN sa.student_answer IS NULL OR sa.student_answer = '' THEN 1 END) as unanswered
        FROM students s
        JOIN questions q ON q.class_id = s.class_id
        LEFT JOIN student_answers sa ON sa.student_id = s.student_id AND sa.question_number = q.question_number
        GROUP BY s.student_id, s.class_id, s.roll_number
    """)
    
    summaries = cursor.fetchall()
    
    for student_id, class_id, roll_number, total, attempted, correct, incorrect, unanswered in summaries:
        score_percentage = (correct / total * 100) if total > 0 else 0
        
        cursor.execute("""
            INSERT INTO performance_summary 
            (student_id, class_id, roll_number, total_questions, questions_attempted, 
             correct_answers, incorrect_answers, unanswered, score_percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, class_id, roll_number, total, attempted, correct, incorrect, unanswered, score_percentage))
    
    # Update class statistics
    cursor.execute("""
        UPDATE classes
        SET total_students = (
            SELECT COUNT(*) FROM students WHERE students.class_id = classes.class_id
        ),
        total_questions = (
            SELECT COUNT(DISTINCT question_number) FROM questions WHERE questions.class_id = classes.class_id
        )
    """)
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Calculated performance summary for {len(summaries)} students")


def generate_ednite_database(
    source_dir: str = "data/excel/ednite",
    output_db: str = "data/database/ednite_company.db"
) -> None:
    """
    Main function to generate EdNite database from CSV files.
    
    Process:
    1. Create schema
    2. Load answer keys
    3. Load student results
    4. Calculate performance summary
    
    Args:
        source_dir: Directory containing AnswerKeys.csv and Result.csv
        output_db: Output SQLite database path
    """
    source_path = Path(source_dir)
    answer_keys_csv = source_path / "AnswerKeys.csv"
    results_csv = source_path / "Result.csv"
    
    # Validate files exist
    if not answer_keys_csv.exists():
        raise FileNotFoundError(f"AnswerKeys.csv not found in {source_dir}")
    if not results_csv.exists():
        raise FileNotFoundError(f"Result.csv not found in {source_dir}")
    
    # Ensure output directory exists
    output_path = Path(output_db)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Delete existing database
    if output_path.exists():
        output_path.unlink()
        logger.info(f"🗑️  Deleted existing database: {output_db}")
    
    logger.info("=" * 80)
    logger.info("🚀 Starting EdNite database generation")
    logger.info("=" * 80)
    
    # Step 1: Create schema
    logger.info("\n📋 Step 1: Creating schema...")
    create_ednite_schema(str(output_path))
    
    # Step 2: Load answer keys
    logger.info("\n🔑 Step 2: Loading answer keys...")
    load_answer_keys(str(answer_keys_csv), str(output_path))
    
    # Step 3: Load student results
    logger.info("\n👨‍🎓 Step 3: Loading student results...")
    load_student_results(str(results_csv), str(output_path))
    
    # Step 4: Calculate performance summary
    logger.info("\n📊 Step 4: Calculating performance summary...")
    calculate_performance_summary(str(output_path))
    
    logger.info("\n" + "=" * 80)
    logger.info(f"✨ Database created successfully: {output_db}")
    logger.info("=" * 80)
    
    # Print statistics
    conn = sqlite3.connect(str(output_path))
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM classes")
    class_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM questions")
    question_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM student_answers")
    answer_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(score_percentage) FROM performance_summary")
    avg_score = cursor.fetchone()[0]
    
    conn.close()
    
    logger.info(f"\n📊 Database Statistics:")
    logger.info(f"   Classes: {class_count}")
    logger.info(f"   Questions: {question_count}")
    logger.info(f"   Students: {student_count}")
    logger.info(f"   Total Answers: {answer_count}")
    logger.info(f"   Average Score: {avg_score:.2f}%")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # Generate database
    generate_ednite_database()
