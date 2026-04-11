USE student_db;

INSERT INTO Courses (course_name) VALUES
('Math'),
('English');

INSERT INTO Students (student_id, first_name, middle_name, last_name) VALUES
(1, 'Alex', NULL, 'Carter'),
(2, 'Brianna', 'J', 'Lewis'),
(3, 'Caleb', NULL, 'Young'),
(4, 'Dana', 'M', 'Hill'),
(5, 'Ethan', NULL, 'King');

INSERT INTO Enrollments (student_id, course_id, score) VALUES
(1, 1, 86.50),
(1, 2, 90.00),
(2, 1, 91.00),
(3, 1, 74.25),
(3, 2, 81.50),
(4, 1, 88.00),
(5, 1, 93.50);