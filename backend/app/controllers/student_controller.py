"""Student controller – handles HTTP request/response logic."""

import logging

from flask import jsonify, request

from app.services.student_service import (
    fetch_all_students_sorted,
    compute_average_score,
    insert_student,
)
from app.validators import validate_student_payload

logger = logging.getLogger(__name__)


def get_students():
    """GET /api/students – Return all student records sorted by studentId ASC."""
    try:
        students = fetch_all_students_sorted()
        return jsonify(students), 200
    except Exception:
        logger.exception("Failed to fetch students")
        return jsonify({"error": "An internal error occurred"}), 500


def get_average_score():
    """GET /api/students/average – Return the average course score and count."""
    try:
        result = compute_average_score()
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to compute average score")
        return jsonify({"error": "An internal error occurred"}), 500


def create_student():
    """POST /api/students – Validate and insert a new student record."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON."}), 400

    errors, cleaned = validate_student_payload(data)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 400

    try:
        student = insert_student(cleaned)
        return jsonify(student), 201
    except Exception:
        logger.exception("Failed to insert student")
        return jsonify({"error": "An internal error occurred"}), 500
