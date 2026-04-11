"""Student service - business logic for student data."""

import logging

from app.db import get_connection

logger = logging.getLogger(__name__)

_DEFAULT_COURSE_ID = 1


class StudentNotFoundError(Exception):
    """Raised when a referenced student does not exist."""


class CourseNotFoundError(Exception):
    """Raised when a referenced course does not exist."""


class DuplicateEnrollmentError(Exception):
    """Raised when a student is already enrolled in the target course."""


class EnrollmentNotFoundError(Exception):
    """Raised when a requested enrollment record does not exist."""


def _get_course_record(cursor, course_id):
    cursor.execute(
        "SELECT course_id, course_name FROM Courses WHERE course_id = %s",
        (course_id,),
    )
    return cursor.fetchone()


def _get_student_record(cursor, student_id):
    cursor.execute(
        "SELECT student_id, first_name, middle_name, last_name "
        "FROM Students WHERE student_id = %s",
        (student_id,),
    )
    return cursor.fetchone()


def _enrollment_exists(cursor, student_id, course_id):
    cursor.execute(
        "SELECT 1 FROM Enrollments WHERE student_id = %s AND course_id = %s",
        (student_id, course_id),
    )
    return cursor.fetchone() is not None


def _build_enrollment_record(student_row, course_row, score):
    return {
        "studentId": student_row["student_id"],
        "firstName": student_row["first_name"],
        "middleName": student_row["middle_name"],
        "lastName": student_row["last_name"],
        "courseId": course_row["course_id"],
        "courseName": course_row["course_name"],
        "score": float(score),
    }


def fetch_all_students_sorted():
    """Return student-course enrollment records ordered by student_id ascending."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT "
            "Students.student_id AS student_id, "
            "Students.first_name AS first_name, "
            "Students.middle_name AS middle_name, "
            "Students.last_name AS last_name, "
            "Courses.course_id AS course_id, "
            "Courses.course_name AS course_name, "
            "Enrollments.score AS course_score "
            "FROM Students "
            "INNER JOIN Enrollments ON Enrollments.student_id = Students.student_id "
            "INNER JOIN Courses ON Courses.course_id = Enrollments.course_id "
            "ORDER BY Students.student_id ASC, Courses.course_id ASC"
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
            "courseId": row["course_id"],
            "courseName": row["course_name"],
            "score": float(row["course_score"]),
        }
        for row in rows
    ]


def compute_average_score():
    """Return average scores grouped by course."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT "
            "Courses.course_id AS course_id, "
            "Courses.course_name AS course_name, "
            "AVG(Enrollments.score) AS avg_score, "
            "COUNT(*) AS enrollment_count "
            "FROM Courses "
            "INNER JOIN Enrollments ON Enrollments.course_id = Courses.course_id "
            "GROUP BY Courses.course_id, Courses.course_name "
            "ORDER BY Courses.course_id ASC"
        )
        rows = cursor.fetchall()
    except Exception:
        logger.exception("DB error in compute_average_score")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    return {
        "courseAverages": [
            {
                "courseId": row["course_id"],
                "courseName": row["course_name"],
                "averageScore": round(float(row["avg_score"]), 2)
                if row["avg_score"] is not None
                else None,
                "enrollmentCount": int(row["enrollment_count"]),
            }
            for row in rows
        ]
    }


def insert_student(cleaned):
    """Insert a validated student and enroll them in a course."""
    course_id = cleaned["courseId"] or _DEFAULT_COURSE_ID
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        course_row = _get_course_record(cursor, course_id)
        if course_row is None:
            raise CourseNotFoundError("courseId does not exist.")

        cursor.execute(
            "INSERT INTO Students (student_id, first_name, middle_name, last_name) "
            "VALUES (%s, %s, %s, %s)",
            (
                cleaned["studentId"],
                cleaned["firstName"],
                cleaned["middleName"],
                cleaned["lastName"],
            ),
        )
        cursor.execute(
            "INSERT INTO Enrollments (student_id, course_id, score) VALUES (%s, %s, %s)",
            (
                cleaned["studentId"],
                course_id,
                cleaned["score"],
            ),
        )
        conn.commit()
    except CourseNotFoundError:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        logger.exception("DB error in insert_student")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    student_row = {
        "student_id": cleaned["studentId"],
        "first_name": cleaned["firstName"],
        "middle_name": cleaned["middleName"],
        "last_name": cleaned["lastName"],
    }
    return _build_enrollment_record(student_row, course_row, cleaned["score"])


def create_enrollment(student_id, cleaned):
    """Create an enrollment for an existing student and return the enrollment record."""
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        student_row = _get_student_record(cursor, student_id)
        if student_row is None:
            raise StudentNotFoundError("studentId does not exist.")

        course_row = _get_course_record(cursor, cleaned["courseId"])
        if course_row is None:
            raise CourseNotFoundError("courseId does not exist.")

        if _enrollment_exists(cursor, student_id, cleaned["courseId"]):
            raise DuplicateEnrollmentError(
                "Student is already enrolled in this course."
            )

        cursor.execute(
            "INSERT INTO Enrollments (student_id, course_id, score) VALUES (%s, %s, %s)",
            (
                student_id,
                cleaned["courseId"],
                cleaned["score"],
            ),
        )
        conn.commit()
    except (StudentNotFoundError, CourseNotFoundError, DuplicateEnrollmentError):
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        logger.exception("DB error in create_enrollment")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

    return _build_enrollment_record(student_row, course_row, cleaned["score"])


def delete_enrollment(student_id, course_id):
    """Delete one enrollment record.

    If the student has no remaining enrollments after deletion, their Students row
    is also removed to avoid orphaned records that never appear in list queries.
    """
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT 1 FROM Enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id),
        )
        if cursor.fetchone() is None:
            raise EnrollmentNotFoundError("Enrollment does not exist.")

        cursor.execute(
            "DELETE FROM Enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id),
        )

        cursor.execute(
            "SELECT COUNT(*) AS enrollment_count FROM Enrollments WHERE student_id = %s",
            (student_id,),
        )
        remaining_count = int(cursor.fetchone()["enrollment_count"])

        if remaining_count == 0:
            cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))

        conn.commit()
    except EnrollmentNotFoundError:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        logger.exception("DB error in delete_enrollment")
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()
