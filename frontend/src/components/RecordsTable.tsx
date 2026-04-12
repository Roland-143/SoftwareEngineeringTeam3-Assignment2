import type { Student } from "../types/Student";

type RecordsTableProps = {
  students: Student[];
  onDeleteEnrollment: (student: Student) => void;
  deletingRowKey: string | null;
};

function RecordsTable({
  students,
  onDeleteEnrollment,
  deletingRowKey,
}: RecordsTableProps) {
  return (
    <section className="table-section">
      <table className="records-table">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>First Name</th>
            <th>Middle Name</th>
            <th>Last Name</th>
            <th>Course</th>
            <th>Score</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => {
            const rowKey = `${student.studentId}-${student.courseId}`;
            const isDeleting = deletingRowKey === rowKey;

            return (
              <tr key={rowKey}>
                <td>{student.studentId}</td>
                <td>{student.firstName}</td>
                <td>{student.middleName || "-"}</td>
                <td>{student.lastName}</td>
                <td>{student.courseName}</td>
                <td>{student.score.toFixed(2)}</td>
                <td>
                  <button
                    type="button"
                    className="ellipsis-button"
                    title="Remove this record"
                    aria-label={`Remove record for ${student.firstName} ${student.lastName} in ${student.courseName}`}
                    onClick={() => onDeleteEnrollment(student)}
                    disabled={isDeleting}
                  >
                    ...
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}

export default RecordsTable;
