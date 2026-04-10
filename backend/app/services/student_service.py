"""Student service – business logic for student data."""

from app.db import get_connection


def fetch_all_students_sorted():
    """Return all students ordered by student_id ascending.

    Maps database column names to the camelCase field names the
    frontend expects::

        studentId, firstName, middleName, lastName, score
    """
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT student_id, first_name, middle_name, last_name, course_score "
            "FROM students ORDER BY student_id ASC"
        )
        rows = cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    return [
        {
            "studentId": row["student_id"],
            "firstName": row["first_name"],
            "middleName": row["middle_name"],
            "lastName": row["last_name"],
            "score": float(row["course_score"]),
        }
        for row in rows
    ]


def compute_average_score():
    """Return the average course_score across all students."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT AVG(course_score) AS avg_score FROM students")
        result = cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    avg = result["avg_score"]
    return round(float(avg), 2) if avg is not None else 0.0
