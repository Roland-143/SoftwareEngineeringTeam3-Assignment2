"""Input validation helpers for student data."""

import re

STUDENT_ID_MIN = 1
STUDENT_ID_MAX = 10

SCORE_MIN = 0
SCORE_MAX = 100

# Allows letters, spaces, hyphens, and apostrophes (e.g. O'Brien, Mary-Jane)
_NAME_RE = re.compile(r"^[A-Za-z\s\-']+$")
_NAME_MAX_LEN = 50


def _validate_positive_int(value, field_label):
    """Return ``(error, cleaned_int)`` for a positive integer field."""
    if isinstance(value, bool):
        return f"{field_label} must be an integer.", None

    try:
        cleaned_value = int(value)
        if cleaned_value != value and not isinstance(value, int):
            raise ValueError
    except (ValueError, TypeError):
        return f"{field_label} must be an integer.", None

    if cleaned_value < 1:
        return f"{field_label} must be a positive integer.", None

    return None, cleaned_value


def _validate_name(value, field_label, required=True):
    """Return an error string if ``value`` is not a valid name, else None."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        if required:
            return f"{field_label} is required."
        return None

    if not isinstance(value, str):
        return f"{field_label} must be a string."

    value = value.strip()

    if len(value) > _NAME_MAX_LEN:
        return f"{field_label} must be {_NAME_MAX_LEN} characters or fewer."

    if not _NAME_RE.match(value):
        return f"{field_label} may only contain letters, spaces, hyphens, and apostrophes."

    return None


def validate_student_payload(data):
    """Validate a student creation payload.

    Args:
        data: Parsed JSON dict from the request body.

    Returns:
        A tuple ``(errors, cleaned)`` where:
        - ``errors`` is a list of human-readable error strings (empty if valid).
        - ``cleaned`` is the normalised payload dict (``None`` when errors exist).

    Expected payload shape::

        {
            "studentId": 1,
            "firstName": "Alex",
            "middleName": null,   # optional
            "lastName": "Carter",
            "score": 86.5
        }
    """
    errors = []

    # --- firstName ---
    err = _validate_name(data.get("firstName"), "firstName", required=True)
    if err:
        errors.append(err)

    # --- middleName (optional) ---
    middle_raw = data.get("middleName")
    err = _validate_name(middle_raw, "middleName", required=False)
    if err:
        errors.append(err)

    # --- lastName ---
    err = _validate_name(data.get("lastName"), "lastName", required=True)
    if err:
        errors.append(err)

    # --- studentId ---
    student_id_raw = data.get("studentId")
    if student_id_raw is None:
        errors.append("studentId is required.")
    elif isinstance(student_id_raw, bool):
        errors.append("studentId must be an integer.")
    else:
        try:
            student_id = int(student_id_raw)
            if student_id != student_id_raw and not isinstance(student_id_raw, int):
                raise ValueError
        except (ValueError, TypeError):
            errors.append("studentId must be an integer.")
            student_id = None
        else:
            if not (STUDENT_ID_MIN <= student_id <= STUDENT_ID_MAX):
                errors.append(
                    f"studentId must be between {STUDENT_ID_MIN} and {STUDENT_ID_MAX}."
                )

    # --- score ---
    score_raw = data.get("score")
    if score_raw is None:
        errors.append("score is required.")
    elif isinstance(score_raw, bool):
        errors.append("score must be a number.")
    else:
        try:
            score = float(score_raw)
        except (ValueError, TypeError):
            errors.append("score must be a number.")
            score = None
        else:
            if not (SCORE_MIN <= score <= SCORE_MAX):
                errors.append(
                    f"score must be between {SCORE_MIN} and {SCORE_MAX}."
                )

    # --- courseId (optional) ---
    course_id = None
    if "courseId" in data:
        course_id_raw = data.get("courseId")
        err, course_id = _validate_positive_int(course_id_raw, "courseId")
        if err:
            errors.append(err)

    if errors:
        return errors, None

    cleaned = {
        "studentId": int(data["studentId"]),
        "firstName": data["firstName"].strip(),
        "middleName": data["middleName"].strip() if data.get("middleName") else None,
        "lastName": data["lastName"].strip(),
        "score": float(data["score"]),
        "courseId": course_id,
    }
    return [], cleaned


def validate_enrollment_payload(data):
    """Validate an enrollment creation payload.

    Expected payload shape::

        {
            "courseId": 2,
            "score": 91.0
        }
    """
    errors = []

    course_id_raw = data.get("courseId")
    if course_id_raw is None:
        errors.append("courseId is required.")
        course_id = None
    else:
        err, course_id = _validate_positive_int(course_id_raw, "courseId")
        if err:
            errors.append(err)

    score_raw = data.get("score")
    if score_raw is None:
        errors.append("score is required.")
    elif isinstance(score_raw, bool):
        errors.append("score must be a number.")
    else:
        try:
            score = float(score_raw)
        except (ValueError, TypeError):
            errors.append("score must be a number.")
            score = None
        else:
            if not (SCORE_MIN <= score <= SCORE_MAX):
                errors.append(
                    f"score must be between {SCORE_MIN} and {SCORE_MAX}."
                )

    if errors:
        return errors, None

    return [], {"courseId": course_id, "score": float(data["score"])}
