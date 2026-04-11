import { useState } from "react";

type FormData = {
    firstName: string;
    middleName: string;
    lastName: string;
    studentId: string;
    courseScore: string;
};

type FormErrors = {
    firstName?: string;
    lastName?: string;
    studentId?: string;
    courseScore?: string;
};

const initialFormData: FormData = {
    firstName: "",
    middleName: "",
    lastName: "",
    studentId: "",
    courseScore: "",
};

export default function StudentEntryForm() {
    const [formData, setFormData] = useState<FormData>(initialFormData);
    const [errors, setErrors] = useState<FormErrors>({});
    const [topError, setTopError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
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

        return newErrors;
    }

    function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const validationErrors = validateForm();

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            setTopError("Please correct the highlighted fields before submitting.");
            setSuccessMessage("");
            return;
        }

        setErrors({});
        setTopError("");
        setSuccessMessage("Student submitted successfully.");
        setFormData(initialFormData);
    }

    function handleReset() {
        setFormData(initialFormData);
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

                    <div className="form-group form-group-full">
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
                    <button type="submit" className="primary-button">
                        Submit
                    </button>
                    <button
                        type="button"
                        className="secondary-button"
                        onClick={handleReset}
                    >
                        Reset
                    </button>
                </div>
            </form>
        </div>
    );
}