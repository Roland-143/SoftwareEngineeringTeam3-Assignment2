-- Inactive legacy seed file kept for reference only.
-- The active Docker-backed seed path uses 01_schema.sql and 02_data.sql.
INSERT INTO students (first_name, middle_name, last_name, student_id, course_score)
VALUES
  ('Alex', NULL, 'Carter', 1, 86.50),
  ('Brianna', 'J', 'Lewis', 2, 91.00),
  ('Caleb', NULL, 'Young', 3, 74.25),
  ('Dana', 'M', 'Hill', 4, 88.00),
  ('Ethan', NULL, 'King', 5, 93.50);
