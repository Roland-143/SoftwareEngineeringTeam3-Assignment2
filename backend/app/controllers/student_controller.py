"""Student controller - handles HTTP request/response logic."""

import logging

from flask import jsonify, request
from mysql.connector import errorcode
from mysql.connector.errors import DataError, IntegrityError
from werkzeug.exceptions import BadRequest

from app.services.student_service import (
    CourseNotFoundError,
    DuplicateEnrollmentError,
    StudentNotFoundError,
    create_enrollment,
    compute_average_score,
    fetch_all_students_sorted,
    insert_student,
)
from app.validators import validate_enrollment_payload, validate_student_payload

logger = logging.getLogger(__name__)

_DUPLICATE_ENTRY_ERRNO = getattr(errorcode, "ER_DUP_ENTRY", 1062)
_DB_CONSTRAINT_ERRNOS = {
    getattr(errorcode, "ER_BAD_NULL_ERROR", 1048),
    getattr(errorcode, "ER_WARN_DATA_OUT_OF_RANGE", 1264),
    getattr(errorcode, "ER_TRUNCATED_WRONG_VALUE_FOR_FIELD", 1366),
    getattr(errorcode, "ER_DATA_TOO_LONG", 1406),
    getattr(errorcode, "ER_CHECK_CONSTRAINT_VIOLATED", 3819),
}


def _map_insert_db_error(exc):
    """Map expected MySQL insert failures to client-facing API responses."""
    errno = getattr(exc, "errno", None)

    if errno == _DUPLICATE_ENTRY_ERRNO:
        return jsonify({"error": "studentId already exists."}), 409

    if isinstance(exc, (IntegrityError, DataError)) or errno in _DB_CONSTRAINT_ERRNOS:
        return jsonify({"error": "Student data violates database constraints."}), 400

    return None


def _parse_json_object_request():
    """Return parsed JSON dict or a Flask response tuple for invalid request bodies."""
    if not request.is_json:
        return None, (jsonify({"error": "Request body must be JSON."}), 400)

    try:
        data = request.get_json(silent=False)
    except BadRequest:
        return None, (jsonify({"error": "Request body contains malformed JSON."}), 400)

    if not isinstance(data, dict):
        return None, (jsonify({"error": "Request body must be a JSON object."}), 400)

    return data, None


def get_students():
    """GET /api/students - Return student-course enrollment records."""
    try:
        students = fetch_all_students_sorted()
        return jsonify(students), 200
    except Exception:
        logger.exception("Failed to fetch students")
        return jsonify({"error": "An internal error occurred"}), 500


def get_average_score():
    """GET /api/students/average - Return per-course average scores."""
    try:
        result = compute_average_score()
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to compute average score")
        return jsonify({"error": "An internal error occurred"}), 500


def create_student():
    """POST /api/students - Validate and insert a new student record."""
    data, error_response = _parse_json_object_request()
    if error_response is not None:
        return error_response

    errors, cleaned = validate_student_payload(data)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 400

    try:
        student = insert_student(cleaned)
        return jsonify(student), 201
    except CourseNotFoundError:
        return jsonify({"error": "courseId does not exist."}), 400
    except Exception as exc:
        mapped_response = _map_insert_db_error(exc)
        if mapped_response is not None:
            logger.warning("Rejected student insert due to database constraint: %s", exc)
            return mapped_response

        logger.exception("Failed to insert student")
        return jsonify({"error": "An internal error occurred"}), 500


def create_student_enrollment(student_id):
    """POST /api/students/<student_id>/enrollments - Enroll an existing student."""
    data, error_response = _parse_json_object_request()
    if error_response is not None:
        return error_response

    errors, cleaned = validate_enrollment_payload(data)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 400

    try:
        enrollment = create_enrollment(student_id, cleaned)
        return jsonify(enrollment), 201
    except StudentNotFoundError:
        return jsonify({"error": "studentId does not exist."}), 404
    except CourseNotFoundError:
        return jsonify({"error": "courseId does not exist."}), 404
    except DuplicateEnrollmentError:
        return jsonify({"error": "Student is already enrolled in this course."}), 409
    except Exception as exc:
        mapped_response = _map_insert_db_error(exc)
        if mapped_response is not None:
            logger.warning(
                "Rejected enrollment insert due to database constraint: %s", exc
            )
            if mapped_response[1] == 409:
                return (
                    jsonify({"error": "Student is already enrolled in this course."}),
                    409,
                )
            return mapped_response

        logger.exception("Failed to create enrollment")
        return jsonify({"error": "An internal error occurred"}), 500
