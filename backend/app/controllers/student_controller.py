"""Student controller – handles HTTP request/response logic."""

import logging

from flask import jsonify

from app.services.student_service import (
    fetch_all_students_sorted,
    compute_average_score,
)

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
    """GET /api/students/average – Return the average course score."""
    try:
        average = compute_average_score()
        return jsonify({"averageScore": average}), 200
    except Exception:
        logger.exception("Failed to compute average score")
        return jsonify({"error": "An internal error occurred"}), 500
