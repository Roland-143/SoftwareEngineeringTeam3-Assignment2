"""Student API routes."""

from flask import Blueprint

from app.controllers.student_controller import (
    create_student,
    create_student_enrollment,
    delete_student_enrollment,
    get_average_score,
    get_students,
)

students_bp = Blueprint("students", __name__)

students_bp.route("/students", methods=["GET"])(get_students)
students_bp.route("/students", methods=["POST"])(create_student)
students_bp.route("/students/<int:student_id>/enrollments", methods=["POST"])(
    create_student_enrollment
)
students_bp.route(
    "/students/<int:student_id>/enrollments/<int:course_id>",
    methods=["DELETE"],
)(delete_student_enrollment)
students_bp.route("/students/average", methods=["GET"])(get_average_score)
