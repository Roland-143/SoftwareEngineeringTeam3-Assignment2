"""Health-check route to verify the backend is running."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Return a simple JSON proving the backend is alive."""
    return jsonify({"status": "ok", "service": "backend"}), 200
