-- Inactive legacy schema file kept for reference only.
-- The active Docker-backed schema path uses 01_schema.sql and 02_data.sql.
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NULL,
  last_name VARCHAR(50) NOT NULL,
  student_id INT NOT NULL,
  course_score DECIMAL(5,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_students_student_id UNIQUE (student_id),
  CONSTRAINT chk_student_id_range CHECK (student_id BETWEEN 1 AND 10),
  CONSTRAINT chk_course_score_range CHECK (course_score BETWEEN 0 AND 100)
);
