-- Starter schema for assignment-aligned local development.
-- Update only through a documented decision in docs/ARCHITECTURE_DECISIONS.md.
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NULL,
  last_name VARCHAR(50) NOT NULL,
  student_id INT NOT NULL,
  course_score DECIMAL(5,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT chk_student_id_range CHECK (student_id BETWEEN 1 AND 10),
  CONSTRAINT chk_course_score_range CHECK (course_score BETWEEN 0 AND 100)
);
