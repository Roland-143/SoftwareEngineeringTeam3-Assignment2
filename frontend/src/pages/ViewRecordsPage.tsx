import { useCallback, useEffect, useState } from "react";
import { deleteStudentEnrollment, fetchStudents } from "../api/students";
import Navbar from "../components/Navbar";
import SummaryCards from "../components/SummaryCards";
import RecordsTable from "../components/RecordsTable";
import EmptyState from "../components/EmptyState";
import type { CourseOption, Student } from "../types/Student";

function calculateAverageFromStudents(students: Student[]): string {
  if (students.length === 0) {
    return "0.00";
  }

  const totalScore = students.reduce((sum, student) => sum + student.score, 0);
  return (totalScore / students.length).toFixed(2);
}

function ViewRecordsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<string>("all");
  const [deletingRowKey, setDeletingRowKey] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const loadStudentData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const records = await fetchStudents();
      const sortedRecords = [...records].sort((a, b) => {
        if (a.studentId !== b.studentId) {
          return a.studentId - b.studentId;
        }
        return a.courseId - b.courseId;
      });

      setStudents(sortedRecords);
    } catch (error) {
      setStudents([]);
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Failed to load student records.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadStudentData();
  }, [loadStudentData]);

  const courseOptions: CourseOption[] = Array.from(
    new Map(
      students.map((student) => [
        student.courseId,
        { courseId: student.courseId, courseName: student.courseName },
      ]),
    ).values(),
  ).sort((a, b) => a.courseId - b.courseId);

  useEffect(() => {
    if (selectedCourseId === "all") {
      return;
    }

    const selectedCourseIdNumber = Number(selectedCourseId);
    const isValidSelection = courseOptions.some(
      (course) => course.courseId === selectedCourseIdNumber,
    );

    if (!isValidSelection) {
      setSelectedCourseId("all");
    }
  }, [courseOptions, selectedCourseId]);

  const filteredStudents =
    selectedCourseId === "all"
      ? students
      : students.filter((student) => student.courseId === Number(selectedCourseId));

  const totalStudents = new Set(filteredStudents.map((student) => student.studentId))
    .size;
  const averageScore = calculateAverageFromStudents(filteredStudents);

  const handleDeleteEnrollment = useCallback(
    async (student: Student) => {
      const rowKey = `${student.studentId}-${student.courseId}`;
      const shouldDelete = window.confirm(
        `Remove ${student.firstName} ${student.lastName} from ${student.courseName}?`,
      );

      if (!shouldDelete) {
        return;
      }

      setDeletingRowKey(rowKey);
      setErrorMessage("");

      try {
        await deleteStudentEnrollment(student.studentId, student.courseId);
        await loadStudentData();
      } catch (error) {
        setErrorMessage(
          error instanceof Error
            ? error.message
            : "Failed to delete enrollment record.",
        );
      } finally {
        setDeletingRowKey(null);
      }
    },
    [loadStudentData],
  );

  return (
    <>
      <Navbar />
      <main className="page-container">
        <section className="page-header">
          <h1>View Student Records</h1>
          <p>
            Student records loaded from the backend API and displayed in ascending
            order by Student ID.
          </p>
          <div className="records-controls">
            <div className="records-filter-group">
              <label htmlFor="course-filter">Course</label>
              <select
                id="course-filter"
                value={selectedCourseId}
                onChange={(event) => setSelectedCourseId(event.target.value)}
                disabled={isLoading || courseOptions.length === 0}
              >
                <option value="all">All Classes</option>
                {courseOptions.map((course) => (
                  <option key={course.courseId} value={String(course.courseId)}>
                    {course.courseName} (ID: {course.courseId})
                  </option>
                ))}
              </select>
            </div>
            <button
              type="button"
              className="secondary-button"
              onClick={() => void loadStudentData()}
              disabled={isLoading}
            >
              {isLoading ? "Loading..." : "Refresh Data"}
            </button>
          </div>
        </section>

        <SummaryCards
          totalStudents={totalStudents}
          averageScore={averageScore}
        />

        {errorMessage ? (
          <div className="form-message error">{errorMessage}</div>
        ) : null}

        {isLoading ? (
          <EmptyState message="Loading student records..." />
        ) : filteredStudents.length > 0 ? (
          <RecordsTable
            students={filteredStudents}
            onDeleteEnrollment={handleDeleteEnrollment}
            deletingRowKey={deletingRowKey}
          />
        ) : (
          <EmptyState message="No records match the selected course filter." />
        )}
      </main>
      <footer className="page-footer">
        <p>Course Management System Framework designed and developed by Group 3</p>
      </footer>
    </>
  );
}

export default ViewRecordsPage;
