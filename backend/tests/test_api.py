import os
import sys
import unittest
from unittest.mock import patch


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.services.student_service import (  # noqa: E402
    CourseNotFoundError,
    DuplicateEnrollmentError,
    StudentNotFoundError,
)


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health_endpoint_returns_expected_json(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok", "service": "backend"})

    @patch("app.controllers.student_controller.fetch_all_students_sorted")
    def test_get_students_returns_expected_json_array_shape(self, mock_fetch_students):
        mock_fetch_students.return_value = [
            {
                "studentId": 1,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "courseId": 1,
                "courseName": "Course Management",
                "score": 86.5,
            },
            {
                "studentId": 1,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "courseId": 2,
                "courseName": "Database Systems",
                "score": 91.0,
            }
        ]

        response = self.client.get("/api/students")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 2)
        self.assertEqual(
            set(payload[0].keys()),
            {
                "studentId",
                "firstName",
                "middleName",
                "lastName",
                "courseId",
                "courseName",
                "score",
            },
        )
        self.assertEqual(payload[0]["studentId"], 1)
        self.assertEqual(payload[1]["courseId"], 2)

    @patch("app.controllers.student_controller.insert_student")
    def test_post_student_valid_payload_returns_201_with_default_course(self, mock_insert_student):
        mock_insert_student.return_value = {
            "studentId": 6,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "courseId": 1,
            "courseName": "Course Management",
            "score": 86.5,
        }

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["studentId"], 6)
        self.assertEqual(payload["courseId"], 1)
        self.assertEqual(payload["courseName"], "Course Management")

    @patch("app.controllers.student_controller.insert_student")
    def test_post_student_accepts_optional_course_id(self, mock_insert_student):
        mock_insert_student.return_value = {
            "studentId": 6,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "courseId": 2,
            "courseName": "Database Systems",
            "score": 86.5,
        }

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "courseId": 2,
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["courseId"], 2)
        self.assertEqual(mock_insert_student.call_args[0][0]["courseId"], 2)

    def test_post_student_non_json_body_returns_400(self):
        response = self.client.post(
            "/api/students",
            data="studentId=6&firstName=Alex",
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Request body must be JSON."})

    def test_post_student_malformed_json_returns_400(self):
        response = self.client.post(
            "/api/students",
            data='{"studentId":',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Request body contains malformed JSON."},
        )

    def test_post_student_non_object_json_bodies_return_400(self):
        for body in ("[]", '"text"', "42", "null"):
            with self.subTest(body=body):
                response = self.client.post(
                    "/api/students",
                    data=body,
                    content_type="application/json",
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {"error": "Request body must be a JSON object."},
                )

    def test_post_student_id_outside_allowed_range_returns_400(self):
        response = self.client.post(
            "/api/students",
            json={
                "studentId": 11,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn(
            "studentId must be between 1 and 10.",
            response.get_json()["details"],
        )

    def test_post_student_boolean_student_id_returns_400(self):
        response = self.client.post(
            "/api/students",
            json={
                "studentId": True,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn("studentId must be an integer.", response.get_json()["details"])

    def test_post_student_boolean_course_id_returns_400(self):
        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "courseId": True,
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn("courseId must be an integer.", response.get_json()["details"])

    def test_post_student_boolean_score_returns_400(self):
        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": True,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn("score must be a number.", response.get_json()["details"])

    def test_post_score_outside_allowed_range_returns_400(self):
        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 101,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn(
            "score must be between 0 and 100.",
            response.get_json()["details"],
        )

    @patch("app.controllers.student_controller.insert_student")
    def test_duplicate_student_id_maps_to_409(self, mock_insert_student):
        duplicate_error = Exception("duplicate key")
        duplicate_error.errno = 1062
        mock_insert_student.side_effect = duplicate_error

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 1,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json(), {"error": "studentId already exists."})

    @patch("app.controllers.student_controller.insert_student")
    def test_non_duplicate_db_integrity_failure_maps_to_400(self, mock_insert_student):
        constraint_error = Exception("check constraint")
        constraint_error.errno = 3819
        mock_insert_student.side_effect = constraint_error

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Student data violates database constraints."},
        )

    @patch("app.controllers.student_controller.insert_student")
    def test_post_student_unknown_course_id_returns_400(self, mock_insert_student):
        mock_insert_student.side_effect = CourseNotFoundError("courseId does not exist.")

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "courseId": 99,
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "courseId does not exist."})

    @patch("app.controllers.student_controller.compute_average_score")
    def test_get_average_returns_expected_json_shape(self, mock_compute_average_score):
        mock_compute_average_score.return_value = {
            "courseAverages": [
                {
                    "courseId": 1,
                    "courseName": "Course Management",
                    "averageScore": 86.5,
                    "enrollmentCount": 5,
                }
            ]
        }

        response = self.client.get("/api/students/average")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(set(payload.keys()), {"courseAverages"})
        self.assertEqual(len(payload["courseAverages"]), 1)
        self.assertEqual(
            set(payload["courseAverages"][0].keys()),
            {"courseId", "courseName", "averageScore", "enrollmentCount"},
        )
        self.assertEqual(payload["courseAverages"][0]["enrollmentCount"], 5)

    @patch("app.controllers.student_controller.insert_student")
    def test_unexpected_insert_failure_returns_500(self, mock_insert_student):
        mock_insert_student.side_effect = RuntimeError("unexpected failure")

        response = self.client.post(
            "/api/students",
            json={
                "studentId": 6,
                "firstName": "Alex",
                "middleName": None,
                "lastName": "Carter",
                "score": 86.5,
            },
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "An internal error occurred"})

    @patch("app.controllers.student_controller.create_enrollment")
    def test_post_student_enrollment_returns_201(self, mock_create_enrollment):
        mock_create_enrollment.return_value = {
            "studentId": 1,
            "firstName": "Alex",
            "middleName": None,
            "lastName": "Carter",
            "courseId": 2,
            "courseName": "Database Systems",
            "score": 91.0,
        }

        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": 2, "score": 91.0},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["courseId"], 2)
        self.assertEqual(mock_create_enrollment.call_args[0], (1, {"courseId": 2, "score": 91.0}))

    @patch("app.controllers.student_controller.create_enrollment")
    def test_post_student_enrollment_duplicate_maps_to_409(self, mock_create_enrollment):
        mock_create_enrollment.side_effect = DuplicateEnrollmentError(
            "Student is already enrolled in this course."
        )

        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": 1, "score": 91.0},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(),
            {"error": "Student is already enrolled in this course."},
        )

    @patch("app.controllers.student_controller.create_enrollment")
    def test_post_student_enrollment_missing_student_returns_404(
        self, mock_create_enrollment
    ):
        mock_create_enrollment.side_effect = StudentNotFoundError("studentId does not exist.")

        response = self.client.post(
            "/api/students/9/enrollments",
            json={"courseId": 2, "score": 91.0},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "studentId does not exist."})

    @patch("app.controllers.student_controller.create_enrollment")
    def test_post_student_enrollment_missing_course_returns_404(
        self, mock_create_enrollment
    ):
        mock_create_enrollment.side_effect = CourseNotFoundError("courseId does not exist.")

        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": 99, "score": 91.0},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "courseId does not exist."})

    def test_post_student_enrollment_boolean_course_id_returns_400(self):
        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": True, "score": 91.0},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn("courseId must be an integer.", response.get_json()["details"])

    def test_post_student_enrollment_boolean_score_returns_400(self):
        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": 1, "score": True},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Validation failed.")
        self.assertIn("score must be a number.", response.get_json()["details"])

    @patch("app.controllers.student_controller.create_enrollment")
    def test_post_student_enrollment_unexpected_failure_returns_500(
        self, mock_create_enrollment
    ):
        mock_create_enrollment.side_effect = RuntimeError("unexpected failure")

        response = self.client.post(
            "/api/students/1/enrollments",
            json={"courseId": 2, "score": 91.0},
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "An internal error occurred"})


if __name__ == "__main__":
    unittest.main()
