import os
import sys
import unittest
from unittest.mock import MagicMock, patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.student_service import (  # noqa: E402
    CourseNotFoundError,
    DuplicateEnrollmentError,
    create_enrollment,
    compute_average_score,
    fetch_all_students_sorted,
    insert_student,
)


class StudentServiceTestCase(unittest.TestCase):
    @patch("app.services.student_service.get_connection")
    def test_fetch_all_students_sorted_uses_order_by_and_preserves_db_order(
        self, mock_get_connection
    ):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "student_id": 1,
                "first_name": "Alex",
                "middle_name": None,
                "last_name": "Carter",
                "course_id": 1,
                "course_name": "Course Management",
                "course_score": 86.5,
            },
            {
                "student_id": 1,
                "first_name": "Alex",
                "middle_name": None,
                "last_name": "Carter",
                "course_id": 2,
                "course_name": "Database Systems",
                "course_score": 91.0,
            },
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        result = fetch_all_students_sorted()

        executed_sql = mock_cursor.execute.call_args[0][0]
        self.assertIn("FROM Students", executed_sql)
        self.assertIn("JOIN Enrollments", executed_sql)
        self.assertIn("JOIN Courses", executed_sql)
        self.assertIn("ORDER BY Students.student_id ASC", executed_sql)
        self.assertIn("Courses.course_id ASC", executed_sql)
        self.assertEqual([student["studentId"] for student in result], [1, 1])
        self.assertEqual([student["courseId"] for student in result], [1, 2])
        self.assertEqual(result[0]["firstName"], "Alex")
        self.assertEqual(result[0]["courseName"], "Course Management")
        self.assertEqual(result[1]["courseName"], "Database Systems")
        self.assertEqual(result[1]["firstName"], "Alex")
        mock_connection.cursor.assert_called_once_with(dictionary=True)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("app.services.student_service.get_connection")
    def test_compute_average_score_groups_results_by_course(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "course_id": 1,
                "course_name": "Course Management",
                "avg_score": 87.75,
                "enrollment_count": 4,
            },
            {
                "course_id": 2,
                "course_name": "Database Systems",
                "avg_score": 91.25,
                "enrollment_count": 2,
            },
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        result = compute_average_score()

        executed_sql = mock_cursor.execute.call_args[0][0]
        self.assertIn("FROM Courses", executed_sql)
        self.assertIn("JOIN Enrollments", executed_sql)
        self.assertIn("GROUP BY Courses.course_id, Courses.course_name", executed_sql)
        self.assertIn("ORDER BY Courses.course_id ASC", executed_sql)
        self.assertEqual(
            result,
            {
                "courseAverages": [
                    {
                        "courseId": 1,
                        "courseName": "Course Management",
                        "averageScore": 87.75,
                        "enrollmentCount": 4,
                    },
                    {
                        "courseId": 2,
                        "courseName": "Database Systems",
                        "averageScore": 91.25,
                        "enrollmentCount": 2,
                    },
                ]
            },
        )
        mock_connection.cursor.assert_called_once_with(dictionary=True)
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("app.services.student_service.get_connection")
    def test_insert_student_writes_students_and_enrollments_with_default_course(
        self, mock_get_connection
    ):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            "course_id": 1,
            "course_name": "Course Management",
        }
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        cleaned = {
            "studentId": 6,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "score": 86.5,
            "courseId": None,
        }

        result = insert_student(cleaned)

        self.assertEqual(mock_cursor.execute.call_count, 3)
        first_sql, first_params = mock_cursor.execute.call_args_list[0][0]
        second_sql, second_params = mock_cursor.execute.call_args_list[1][0]
        third_sql, third_params = mock_cursor.execute.call_args_list[2][0]
        self.assertIn("SELECT course_id, course_name FROM Courses", first_sql)
        self.assertEqual(first_params, (1,))
        self.assertIn("INSERT INTO Students", second_sql)
        self.assertEqual(second_params, (6, "Alex", None, "Carter"))
        self.assertIn("INSERT INTO Enrollments", third_sql)
        self.assertEqual(third_params, (6, 1, 86.5))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
        self.assertEqual(result["courseId"], 1)
        self.assertEqual(result["courseName"], "Course Management")

    @patch("app.services.student_service.get_connection")
    def test_insert_student_uses_requested_course_id(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {
            "course_id": 2,
            "course_name": "Database Systems",
        }
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        cleaned = {
            "studentId": 6,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "score": 86.5,
            "courseId": 2,
        }

        result = insert_student(cleaned)

        insert_enrollment_sql, insert_enrollment_params = mock_cursor.execute.call_args_list[2][0]
        self.assertIn("INSERT INTO Enrollments", insert_enrollment_sql)
        self.assertEqual(insert_enrollment_params, (6, 2, 86.5))
        self.assertEqual(result["courseId"], 2)
        self.assertEqual(result["courseName"], "Database Systems")

    @patch("app.services.student_service.get_connection")
    def test_insert_student_raises_when_course_does_not_exist(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        cleaned = {
            "studentId": 6,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "score": 86.5,
            "courseId": 99,
        }

        with self.assertRaises(CourseNotFoundError):
            insert_student(cleaned)

    @patch("app.services.student_service.get_connection")
    def test_create_enrollment_writes_for_existing_student(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            {
                "student_id": 1,
                "first_name": "Alex",
                "middle_name": None,
                "last_name": "Carter",
            },
            {
                "course_id": 2,
                "course_name": "Database Systems",
            },
            None,
        ]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        result = create_enrollment(1, {"courseId": 2, "score": 91.0})

        self.assertEqual(mock_cursor.execute.call_count, 4)
        insert_sql, insert_params = mock_cursor.execute.call_args_list[3][0]
        self.assertIn("INSERT INTO Enrollments", insert_sql)
        self.assertEqual(insert_params, (1, 2, 91.0))
        self.assertEqual(result["studentId"], 1)
        self.assertEqual(result["courseId"], 2)
        self.assertEqual(result["courseName"], "Database Systems")

    @patch("app.services.student_service.get_connection")
    def test_create_enrollment_rejects_duplicate_enrollment(self, mock_get_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.side_effect = [
            {
                "student_id": 1,
                "first_name": "Alex",
                "middle_name": None,
                "last_name": "Carter",
            },
            {
                "course_id": 1,
                "course_name": "Course Management",
            },
            {"1": 1},
        ]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection

        with self.assertRaises(DuplicateEnrollmentError):
            create_enrollment(1, {"courseId": 1, "score": 86.5})


if __name__ == "__main__":
    unittest.main()
