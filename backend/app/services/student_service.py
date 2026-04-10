"""Student service – business logic for student data."""

import logging

from app.db import get_connection

logger = logging.getLogger(__name__)


def fetch_all_students_sorted():
    """Return all students ordered by student_id ascending.

    Maps database column names to the camelCase field names the
    frontend expects::

        studentId, firstName, middleName, lastName, score

    Returns an empty list when no records exist.
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
    except Exception:
        logger.exception("DB error in fetch_all_students_sorted")
        raise
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
    """Return the average course_score and student count.

    Returns a dict::

        {"averageScore": 85.45, "count": 20}

    When the table is empty, ``averageScore`` is ``None`` and ``count`` is 0.
    """
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT AVG(course_score) AS avg_score, COUNT(*) AS total FROM students"
        )
        result = cursor.fetchone()
    except Exception:
        logger.exception("DB error in compute_average_score")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    count = int(result["total"])
    avg = result["avg_score"]
    return {
        "averageScore": round(float(avg), 2) if avg is not None else None,
        "count": count,
    }


def insert_student(cleaned):
    """Insert a validated student record and return it with its generated id.

    Args:
        cleaned: dict produced by ``validate_student_payload`` with keys
                 studentId, firstName, middleName, lastName, score.

    Returns:
        The inserted record as a camelCase dict.
    """
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (first_name, middle_name, last_name, student_id, course_score) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                cleaned["firstName"],
                cleaned["middleName"],
                cleaned["lastName"],
                cleaned["studentId"],
                cleaned["score"],
            ),
        )
        conn.commit()
    except Exception:
        logger.exception("DB error in insert_student")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    return {
        "studentId": cleaned["studentId"],
        "firstName": cleaned["firstName"],
        "middleName": cleaned["middleName"],
        "lastName": cleaned["lastName"],
        "score": cleaned["score"],
    }

