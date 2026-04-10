"""Student API routes."""

from flask import Blueprint

from app.controllers.student_controller import get_students, get_average_score

students_bp = Blueprint("students", __name__)

students_bp.route("/students", methods=["GET"])(get_students)
students_bp.route("/students/average", methods=["GET"])(get_average_score)
