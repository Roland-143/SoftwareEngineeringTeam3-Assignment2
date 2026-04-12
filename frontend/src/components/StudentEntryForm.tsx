import { useCallback, useEffect, useState } from "react";
import { createStudent, fetchStudents } from "../api/students";
import type { CourseOption, CreateStudentPayload } from "../types/Student";

type FormData = {
    firstName: string;
    middleName: string;
    lastName: string;
    studentId: string;
    courseId: string;
    courseScore: string;
};

type FormErrors = {
    firstName?: string;
    lastName?: string;
    studentId?: string;
    courseId?: string;
    courseScore?: string;
};

const initialFormData: FormData = {
    firstName: "",
    middleName: "",
    lastName: "",
    studentId: "",
    courseId: "",
    courseScore: "",
};

export default function StudentEntryForm() {
    const [formData, setFormData] = useState<FormData>(initialFormData);
    const [errors, setErrors] = useState<FormErrors>({});
    const [topError, setTopError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [courseOptions, setCourseOptions] = useState<CourseOption[]>([]);
    const [isLoadingCourses, setIsLoadingCourses] = useState(true);

    const loadCourseOptions = useCallback(async () => {
        setIsLoadingCourses(true);
        setTopError("");

        try {
            const records = await fetchStudents();
            const courseMap = new Map<number, string>();

            for (const record of records) {
                if (!courseMap.has(record.courseId)) {
                    courseMap.set(record.courseId, record.courseName);
                }
            }

            const options = Array.from(courseMap.entries())
                .map(([courseId, courseName]) => ({ courseId, courseName }))
                .sort((a, b) => a.courseId - b.courseId);

            setCourseOptions(options);

            if (options.length === 0) {
                setTopError(
                    "No courses are currently available from the database. Please seed courses first.",
                );
                setFormData((prev) => ({ ...prev, courseId: "" }));
            } else {
                setFormData((prev) => ({
                    ...prev,
                    courseId:
                        prev.courseId && options.some((opt) => String(opt.courseId) === prev.courseId)
                            ? prev.courseId
                            : String(options[0].courseId),
                }));
            }
        } catch (error) {
            setCourseOptions([]);
            setFormData((prev) => ({ ...prev, courseId: "" }));
            setTopError(
                error instanceof Error
                    ? `Failed to load courses: ${error.message}`
                    : "Failed to load courses from the backend.",
            );
        } finally {
            setIsLoadingCourses(false);
        }
    }, []);

    useEffect(() => {
        void loadCourseOptions();
    }, [loadCourseOptions]);

    function handleChange(event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
        const { name, value } = event.target;

        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));

        setErrors((prev) => ({
            ...prev,
            [name]: "",
        }));

        setTopError("");
        setSuccessMessage("");
    }

    function validateForm() {
        const newErrors: FormErrors = {};

        if (!formData.firstName.trim()) {
            newErrors.firstName = "First Name is required.";
        }

        if (!formData.lastName.trim()) {
            newErrors.lastName = "Last Name is required.";
        }

        if (!formData.studentId.trim()) {
            newErrors.studentId = "Student ID is required.";
        } else {
            const studentId = Number(formData.studentId);

            if (!Number.isInteger(studentId) || studentId < 1 || studentId > 10) {
                newErrors.studentId = "Student ID must be an integer from 1 to 10.";
            }
        }

        if (!formData.courseScore.trim()) {
            newErrors.courseScore = "Course Score is required.";
        } else {
            const courseScore = Number(formData.courseScore);

            if (Number.isNaN(courseScore) || courseScore < 0 || courseScore > 100) {
                newErrors.courseScore = "Course Score must be a number from 0 to 100.";
            }
        }

        if (formData.courseId.trim()) {
            const courseId = Number(formData.courseId);

            if (!Number.isInteger(courseId) || courseId < 1) {
                newErrors.courseId = "Course ID must be a positive integer.";
            } else if (!courseOptions.some((course) => course.courseId === courseId)) {
                newErrors.courseId = "Please select a valid course from the list.";
            }
        } else {
            newErrors.courseId = "Course selection is required.";
        }

        return newErrors;
    }

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const validationErrors = validateForm();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            setTopError("Please correct the highlighted fields before submitting.");
            setSuccessMessage("");
            return;
        }

        if (isLoadingCourses) {
            setTopError("Course options are still loading. Please wait and try again.");
            return;
        }

        if (courseOptions.length === 0) {
            setTopError("No course options are available for submission.");
            return;
        }

        setIsSubmitting(true);

        try {
            const payload: CreateStudentPayload = {
                studentId: Number(formData.studentId),
                firstName: formData.firstName.trim(),
                middleName: formData.middleName.trim() || null,
                lastName: formData.lastName.trim(),
                score: Number(formData.courseScore),
                courseId: Number(formData.courseId),
            };

            await createStudent(payload);

            setErrors({});
            setTopError("");
            setSuccessMessage("Student submitted successfully and saved to the database.");
            setFormData((prev) => ({
                ...initialFormData,
                courseId: prev.courseId,
            }));
        } catch (error) {
            setSuccessMessage("");
            setTopError(
                error instanceof Error
                    ? error.message
                    : "Failed to submit student. Please try again.",
            );
        } finally {
            setIsSubmitting(false);
        }
    }

    function handleReset() {
        setFormData((prev) => ({
            ...initialFormData,
            courseId: prev.courseId,
        }));
        setErrors({});
        setTopError("");
        setSuccessMessage("");
    }

    return (
        <div className="form-card">
            <form className="student-form" onSubmit={handleSubmit}>
                {topError && <div className="form-message error">{topError}</div>}
                {successMessage && (
                    <div className="form-message success">{successMessage}</div>
                )}

                <div className="form-grid">
                    <div className="form-group">
                        <label htmlFor="studentId">Student ID</label>
                        <input
                            id="studentId"
                            name="studentId"
                            type="number"
                            value={formData.studentId}
                            onChange={handleChange}
                            placeholder="Enter student ID"
                            className={errors.studentId ? "input-error" : ""}
                        />
                        {errors.studentId && (
                            <p className="field-error">{errors.studentId}</p>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="courseScore">Course Score</label>
                        <input
                            id="courseScore"
                            name="courseScore"
                            type="number"
                            value={formData.courseScore}
                            onChange={handleChange}
                            placeholder="Enter course score"
                            className={errors.courseScore ? "input-error" : ""}
                        />
                        {errors.courseScore && (
                            <p className="field-error">{errors.courseScore}</p>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="courseId">Course</label>
                        <select
                            id="courseId"
                            name="courseId"
                            value={formData.courseId}
                            onChange={handleChange}
                            disabled={isLoadingCourses || courseOptions.length === 0}
                            className={errors.courseId ? "input-error" : ""}
                        >
                            <option value="">
                                {isLoadingCourses
                                    ? "Loading courses..."
                                    : "Select a course"}
                            </option>
                            {courseOptions.map((course) => (
                                <option
                                    key={course.courseId}
                                    value={String(course.courseId)}
                                >
                                    {course.courseName} (ID: {course.courseId})
                                </option>
                            ))}
                        </select>
                        {errors.courseId && (
                            <p className="field-error">{errors.courseId}</p>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="firstName">First Name</label>
                        <input
                            id="firstName"
                            name="firstName"
                            type="text"
                            value={formData.firstName}
                            onChange={handleChange}
                            placeholder="Enter first name"
                            className={errors.firstName ? "input-error" : ""}
                        />
                        {errors.firstName && (
                            <p className="field-error">{errors.firstName}</p>
                        )}
                    </div>

                    <div className="form-group">
                        <label htmlFor="middleName">Middle Name</label>
                        <input
                            id="middleName"
                            name="middleName"
                            type="text"
                            value={formData.middleName}
                            onChange={handleChange}
                            placeholder="Enter middle name (optional)"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="lastName">Last Name</label>
                        <input
                            id="lastName"
                            name="lastName"
                            type="text"
                            value={formData.lastName}
                            onChange={handleChange}
                            placeholder="Enter last name"
                            className={errors.lastName ? "input-error" : ""}
                        />
                        {errors.lastName && (
                            <p className="field-error">{errors.lastName}</p>
                        )}
                    </div>
                </div>

                <div className="form-actions">
                    <button
                        type="submit"
                        className="primary-button"
                        disabled={isSubmitting || isLoadingCourses || courseOptions.length === 0}
                    >
                        {isSubmitting ? "Submitting..." : "Submit"}
                    </button>
                    <button
                        type="button"
                        className="secondary-button"
                        onClick={handleReset}
                        disabled={isSubmitting}
                    >
                        Reset
                    </button>
                </div>
            </form>
        </div>
    );
}
