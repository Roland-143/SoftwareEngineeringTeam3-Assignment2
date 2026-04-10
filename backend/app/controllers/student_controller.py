"""Student controller – handles HTTP request/response logic."""

from flask import jsonify

from app.services.student_service import (
    fetch_all_students_sorted,
    compute_average_score,
)


def get_students():
    """GET /api/students – Return all student records sorted by studentId ASC."""
    try:
        students = fetch_all_students_sorted()
        return jsonify(students), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


def get_average_score():
    """GET /api/students/average – Return the average course score."""
    try:
        average = compute_average_score()
        return jsonify({"averageScore": average}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
