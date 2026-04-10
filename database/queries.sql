SELECT 
    s.student_id,
    s.first_name,
    s.last_name,
    c.course_name,
    e.score
FROM Enrollments e
JOIN Students s ON e.student_id = s.student_id
JOIN Courses c ON e.course_id = c.course_id
ORDER BY e.score ASC;

SELECT AVG(score) AS average_score
FROM Enrollments;
