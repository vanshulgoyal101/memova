# EdNite Test Results Database Schema

**Database**: `ednite_company.db`  
**Last Updated**: November 6, 2025  
**Data Source**: Student test results for Classes 5-10

---

## Overview

The EdNite database contains student test performance data for 2,540 students across 6 classes (5-10), with 90 questions per test. The schema is designed for performance analysis, question difficulty assessment, and class-wise comparisons.

### Key Statistics
- **Students**: 2,540
- **Classes**: 6 (Class 5 through Class 10)
- **Questions**: 90 per class (540 total answer keys)
- **Total Answers**: 228,600
- **Average Score**: 26.89%

---

## Schema Diagram

```
┌─────────────────┐
│    classes      │
│─────────────────│
│ class_id (PK)   │
│ class_name      │
│ total_students  │
│ total_questions │
└────────┬────────┘
         │
         │ 1:N
         ↓
┌─────────────────┐         ┌──────────────────┐
│   questions     │         │    students      │
│─────────────────│         │──────────────────│
│ question_id(PK) │         │ student_id (PK)  │
│ question_number │         │ roll_number      │
│ class_id (FK)   │         │ class_id (FK)    │
│ correct_answer  │         └────────┬─────────┘
└─────────────────┘                  │
                                     │ 1:N
                                     ↓
                         ┌───────────────────────┐
                         │   student_answers     │
                         │───────────────────────│
                         │ answer_id (PK)        │
                         │ student_id (FK)       │
                         │ question_number       │
                         │ student_answer        │
                         │ is_correct            │
                         └───────────────────────┘
                                     │
                                     │ 1:1
                                     ↓
                         ┌───────────────────────┐
                         │ performance_summary   │
                         │───────────────────────│
                         │ student_id (PK/FK)    │
                         │ class_id (FK)         │
                         │ roll_number           │
                         │ total_questions       │
                         │ questions_attempted   │
                         │ correct_answers       │
                         │ incorrect_answers     │
                         │ unanswered            │
                         │ score_percentage      │
                         └───────────────────────┘
```

---

## Tables

### 1. classes
Stores class metadata and aggregate statistics.

| Column | Type | Description |
|--------|------|-------------|
| `class_id` | INTEGER | Primary key (5-10) |
| `class_name` | TEXT | Display name (e.g., "Class 5") |
| `total_students` | INTEGER | Number of students in class |
| `total_questions` | INTEGER | Number of questions for class |

**Sample Data**:
```sql
class_id | class_name | total_students | total_questions
---------|------------|----------------|----------------
5        | Class 5    | 473            | 90
6        | Class 6    | 437            | 90
7        | Class 7    | 401            | 90
```

**Indexes**: Primary key on `class_id`

---

### 2. questions
Stores question metadata with correct answers per class.

| Column | Type | Description |
|--------|------|-------------|
| `question_id` | INTEGER | Primary key (auto-increment) |
| `question_number` | INTEGER | Question number (1-90) |
| `class_id` | INTEGER | Foreign key to `classes` |
| `correct_answer` | TEXT | Correct answer (lowercase, e.g., "a", "b,c") |

**Sample Data**:
```sql
question_id | question_number | class_id | correct_answer
------------|-----------------|----------|---------------
1           | 1               | 5        | d
2           | 1               | 6        | c
3           | 1               | 7        | b
91          | 2               | 5        | a
```

**Notes**:
- Some questions have multiple correct answers (comma-separated)
- Unique constraint on `(question_number, class_id)`

**Indexes**: 
- Primary key on `question_id`
- Index on `class_id`

---

### 3. students
Stores student metadata and class enrollment.

| Column | Type | Description |
|--------|------|-------------|
| `student_id` | INTEGER | Primary key (auto-increment) |
| `roll_number` | TEXT | Student roll number (e.g., "1001") |
| `class_id` | INTEGER | Foreign key to `classes` |

**Sample Data**:
```sql
student_id | roll_number | class_id
-----------|-------------|----------
1          | 1001        | 5
2          | 1002        | 5
3          | 1003        | 5
```

**Notes**:
- `roll_number` is unique across all classes
- Roll numbers range from 1001 to ~8540

**Indexes**: 
- Primary key on `student_id`
- Index on `class_id`

---

### 4. student_answers
Stores individual student responses to questions.

| Column | Type | Description |
|--------|------|-------------|
| `answer_id` | INTEGER | Primary key (auto-increment) |
| `student_id` | INTEGER | Foreign key to `students` |
| `question_number` | INTEGER | Question number (1-90) |
| `student_answer` | TEXT | Student's answer (lowercase, empty if unanswered) |
| `is_correct` | INTEGER | 1 = correct, 0 = incorrect, NULL = unanswered |

**Sample Data**:
```sql
answer_id | student_id | question_number | student_answer | is_correct
----------|------------|-----------------|----------------|------------
1         | 1          | 1               | c              | 0
2         | 1          | 2               | d              | 0
3         | 1          | 3               | a              | 1
228600    | 2540       | 90              |                | NULL
```

**Notes**:
- Empty `student_answer` indicates question not attempted
- `is_correct` is NULL for unanswered questions
- Unique constraint on `(student_id, question_number)`

**Indexes**: 
- Primary key on `answer_id`
- Index on `student_id`
- Index on `question_number`

---

### 5. performance_summary
Pre-calculated performance metrics per student (for fast queries).

| Column | Type | Description |
|--------|------|-------------|
| `student_id` | INTEGER | Primary key, foreign key to `students` |
| `class_id` | INTEGER | Foreign key to `classes` |
| `roll_number` | TEXT | Student roll number (denormalized) |
| `total_questions` | INTEGER | Total questions for their class |
| `questions_attempted` | INTEGER | Number of questions answered |
| `correct_answers` | INTEGER | Number of correct answers |
| `incorrect_answers` | INTEGER | Number of incorrect answers |
| `unanswered` | INTEGER | Number of unanswered questions |
| `score_percentage` | REAL | (correct / total) × 100 |

**Sample Data**:
```sql
student_id | roll_number | total_qs | attempted | correct | incorrect | unanswered | score_%
-----------|-------------|----------|-----------|---------|-----------|------------|--------
1          | 1001        | 90       | 79        | 21      | 58        | 11         | 23.33
2          | 1002        | 90       | 82        | 24      | 58        | 8          | 26.67
3          | 1003        | 90       | 79        | 23      | 56        | 11         | 25.56
```

**Notes**:
- Updated via `calculate_performance_summary()` function
- Enables fast aggregate queries without JOIN operations

**Indexes**: 
- Primary key on `student_id`
- Index on `class_id`

---

## Example Queries

### Basic Queries

**1. Count students per class**:
```sql
SELECT class_name, total_students
FROM classes
ORDER BY class_id;
```

**2. Top 10 performers**:
```sql
SELECT roll_number, score_percentage
FROM performance_summary
ORDER BY score_percentage DESC
LIMIT 10;
```

**3. Average score by class**:
```sql
SELECT c.class_name, AVG(ps.score_percentage) as avg_score
FROM performance_summary ps
JOIN classes c ON c.class_id = ps.class_id
GROUP BY c.class_id, c.class_name
ORDER BY c.class_id;
```

### Advanced Queries

**4. Question difficulty analysis (hardest questions)**:
```sql
SELECT 
    q.question_number,
    c.class_name,
    COUNT(CASE WHEN sa.is_correct = 1 THEN 1 END) as correct_count,
    COUNT(sa.student_id) as total_attempts,
    ROUND(100.0 * COUNT(CASE WHEN sa.is_correct = 1 THEN 1 END) / COUNT(sa.student_id), 2) as success_rate
FROM questions q
JOIN classes c ON c.class_id = q.class_id
LEFT JOIN student_answers sa ON sa.question_number = q.question_number
JOIN students s ON s.student_id = sa.student_id AND s.class_id = q.class_id
WHERE sa.student_answer IS NOT NULL AND sa.student_answer != ''
GROUP BY q.question_number, c.class_name
HAVING success_rate < 30
ORDER BY success_rate ASC;
```

**5. Students with improvement potential (attempted many, scored low)**:
```sql
SELECT 
    roll_number,
    questions_attempted,
    correct_answers,
    score_percentage
FROM performance_summary
WHERE questions_attempted > 70 AND score_percentage < 30
ORDER BY questions_attempted DESC, score_percentage ASC;
```

---

## Data Quality Notes

1. **Missing Answers**: Some students have unanswered questions (average 11 per student)
2. **Multiple Correct Answers**: Some questions accept multiple answers (e.g., "a,d")
3. **Low Scores**: Average score is 26.89%, indicating difficult test or need for more preparation
4. **Answer Format**: All answers standardized to lowercase, comma-separated if multiple

---

## Performance Optimization

1. **Indexed Columns**: All foreign keys and frequently queried columns indexed
2. **Denormalized Summary**: `performance_summary` pre-calculates metrics
3. **Query Patterns**: Use `performance_summary` for student-level aggregates, avoid JOINs when possible

---

## Related Files

- **Data Generator**: `src/data/ednite_generators.py`
- **Source Data**: `data/excel/ednite/AnswerKeys.csv`, `Result.csv`
- **Database File**: `data/database/ednite_company.db`

---

## Update History

| Date | Change | Author |
|------|--------|--------|
| 2025-11-06 | Initial schema created | System |
| 2025-11-06 | Added 2,540 students, 228,600 answers | Data Generator |
