USE student_db;

INSERT INTO Courses (course_name) VALUES
('Math'), ('Science'), ('History');

INSERT INTO Students VALUES
(1, 'John', 'A', 'Doe'),
(2, 'Jane', NULL, 'Smith'),
(3, 'Mike', 'B', 'Lee');

INSERT INTO Enrollments VALUES
(1, 1, 85),
(1, 2, 90),
(2, 1, 78),
(3, 3, 88);
