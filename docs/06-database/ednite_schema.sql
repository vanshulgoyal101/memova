-- EdNite Test Results Database Schema
-- Generated: 2025-11-06
-- Database: ednite_company.db
-- Description: Student test performance for Classes 5-10

-- ================================================
-- Table: classes
-- Description: Class metadata and aggregate statistics
-- ================================================
CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY,
    class_name TEXT NOT NULL,
    total_students INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 90
);

-- Sample Data
INSERT INTO classes (class_id, class_name, total_students, total_questions) VALUES
(5, 'Class 5', 473, 90),
(6, 'Class 6', 437, 90),
(7, 'Class 7', 401, 90),
(8, 'Class 8', 418, 90),
(9, 'Class 9', 418, 90),
(10, 'Class 10', 393, 90);

-- ================================================
-- Table: questions
-- Description: Question metadata with correct answers
-- ================================================
CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_number INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    correct_answer TEXT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    UNIQUE(question_number, class_id)
);

-- Indexes for performance
CREATE INDEX idx_questions_class ON questions(class_id);

-- Sample Data
-- INSERT INTO questions (question_number, class_id, correct_answer) VALUES
-- (1, 5, 'd'),
-- (1, 6, 'c'),
-- (1, 7, 'b'),
-- (2, 5, 'a'),
-- (2, 6, 'b,d'),  -- Multiple correct answers
-- ...

-- ================================================
-- Table: students
-- Description: Student metadata and class enrollment
-- ================================================
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_number TEXT UNIQUE NOT NULL,
    class_id INTEGER NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Indexes for performance
CREATE INDEX idx_students_class ON students(class_id);

-- Sample Data
-- INSERT INTO students (roll_number, class_id) VALUES
-- ('1001', 5),
-- ('1002', 5),
-- ('2001', 6),
-- ...

-- ================================================
-- Table: student_answers
-- Description: Individual student responses to questions
-- ================================================
CREATE TABLE student_answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    question_number INTEGER NOT NULL,
    student_answer TEXT DEFAULT '',  -- Empty string if unanswered
    is_correct INTEGER,  -- 1=correct, 0=incorrect, NULL=unanswered
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    UNIQUE(student_id, question_number)
);

-- Indexes for performance
CREATE INDEX idx_answers_student ON student_answers(student_id);
CREATE INDEX idx_answers_question ON student_answers(question_number);

-- Sample Data
-- INSERT INTO student_answers (student_id, question_number, student_answer, is_correct) VALUES
-- (1, 1, 'c', 0),     -- incorrect
-- (1, 2, 'd', 0),     -- incorrect
-- (1, 3, 'a', 1),     -- correct
-- (1, 4, '', NULL),   -- unanswered
-- ...

-- ================================================
-- Table: performance_summary
-- Description: Pre-calculated performance metrics per student
-- ================================================
CREATE TABLE performance_summary (
    student_id INTEGER PRIMARY KEY,
    class_id INTEGER NOT NULL,
    roll_number TEXT NOT NULL,
    total_questions INTEGER NOT NULL,
    questions_attempted INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    incorrect_answers INTEGER DEFAULT 0,
    unanswered INTEGER DEFAULT 0,
    score_percentage REAL DEFAULT 0.0,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Indexes for performance
CREATE INDEX idx_performance_class ON performance_summary(class_id);

-- Sample Data
-- INSERT INTO performance_summary VALUES
-- (1, 5, '1001', 90, 79, 21, 58, 11, 23.33),
-- (2, 5, '1002', 90, 82, 24, 58, 8, 26.67),
-- ...

-- ================================================
-- Common Queries
-- ================================================

-- 1. Top 10 Students by Score
-- SELECT roll_number, score_percentage
-- FROM performance_summary
-- ORDER BY score_percentage DESC
-- LIMIT 10;

-- 2. Average Score by Class
-- SELECT c.class_name, AVG(ps.score_percentage) as avg_score
-- FROM performance_summary ps
-- JOIN classes c ON c.class_id = ps.class_id
-- GROUP BY c.class_id, c.class_name
-- ORDER BY c.class_id;

-- 3. Question Difficulty (Success Rate < 30%)
-- SELECT 
--     q.question_number,
--     c.class_name,
--     COUNT(CASE WHEN sa.is_correct = 1 THEN 1 END) as correct_count,
--     COUNT(sa.student_id) as total_attempts,
--     ROUND(100.0 * COUNT(CASE WHEN sa.is_correct = 1 THEN 1 END) / COUNT(sa.student_id), 2) as success_rate
-- FROM questions q
-- JOIN classes c ON c.class_id = q.class_id
-- LEFT JOIN student_answers sa ON sa.question_number = q.question_number
-- JOIN students s ON s.student_id = sa.student_id AND s.class_id = q.class_id
-- WHERE sa.student_answer IS NOT NULL AND sa.student_answer != ''
-- GROUP BY q.question_number, c.class_name
-- HAVING success_rate < 30
-- ORDER BY success_rate ASC;

-- 4. Students with Low Scores but High Attempts
-- SELECT 
--     roll_number,
--     questions_attempted,
--     correct_answers,
--     score_percentage
-- FROM performance_summary
-- WHERE questions_attempted > 70 AND score_percentage < 30
-- ORDER BY questions_attempted DESC, score_percentage ASC;

-- 5. Class-wise Performance Distribution
-- SELECT 
--     c.class_name,
--     COUNT(CASE WHEN ps.score_percentage >= 80 THEN 1 END) as excellent,
--     COUNT(CASE WHEN ps.score_percentage >= 60 AND ps.score_percentage < 80 THEN 1 END) as good,
--     COUNT(CASE WHEN ps.score_percentage >= 40 AND ps.score_percentage < 60 THEN 1 END) as average,
--     COUNT(CASE WHEN ps.score_percentage < 40 THEN 1 END) as needs_improvement
-- FROM performance_summary ps
-- JOIN classes c ON c.class_id = ps.class_id
-- GROUP BY c.class_id, c.class_name
-- ORDER BY c.class_id;

-- ================================================
-- Statistics
-- ================================================
-- Total Students: 2,540
-- Total Questions: 540 (90 per class × 6 classes)
-- Total Answers: 228,600
-- Average Score: 26.89%
-- Database Size: ~15 MB
