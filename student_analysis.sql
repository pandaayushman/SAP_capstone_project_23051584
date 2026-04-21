
CREATE TABLE IF NOT EXISTS students (
    student_id   INTEGER PRIMARY KEY,
    name         TEXT,
    department   TEXT,
    math         INTEGER,
    science      INTEGER,
    programming  INTEGER,
    attendance   INTEGER
);

INSERT OR REPLACE INTO students VALUES
(1, 'Amit',  'CS', 78, 85, 90, 92),
(2, 'Riya',  'CS', 88, 79, 85, 90),
(3, 'Karan', 'IT', 65, 70, 72, 80),
(4, 'Pooja', 'IT', 92, 91, 95, 96),
(5, 'Rahul', 'CS', 55, 60, 58, 70);


-- Task 1: Display all student records

SELECT * FROM students;


-- Task 2: Average marks for each student

SELECT
    student_id,
    name,
    department,
    ROUND((math + science + programming) / 3.0, 2) AS average_marks
FROM students
ORDER BY average_marks DESC;

-- ─────────────────────────────────────────────
-- Task 3: Top-performing student (highest average)
-- ─────────────────────────────────────────────
SELECT
    student_id,
    name,
    department,
    ROUND((math + science + programming) / 3.0, 2) AS average_marks
FROM students
ORDER BY average_marks DESC
LIMIT 1;

-- ─────────────────────────────────────────────
-- Task 4: Department-wise average marks
-- ─────────────────────────────────────────────
SELECT
    department,
    ROUND(AVG(math), 2)        AS avg_math,
    ROUND(AVG(science), 2)     AS avg_science,
    ROUND(AVG(programming), 2) AS avg_programming,
    ROUND(AVG((math + science + programming) / 3.0), 2) AS dept_avg_marks
FROM students
GROUP BY department
ORDER BY dept_avg_marks DESC;

-- ─────────────────────────────────────────────
-- Task 5: Students scoring below 60 in any subject
-- ─────────────────────────────────────────────
SELECT
    student_id,
    name,
    department,
    math,
    science,
    programming
FROM students
WHERE math < 60
   OR science < 60
   OR programming < 60;


-- Task 6: Overall class average marks

SELECT
    ROUND(AVG((math + science + programming) / 3.0), 2) AS class_average_marks
FROM students;
