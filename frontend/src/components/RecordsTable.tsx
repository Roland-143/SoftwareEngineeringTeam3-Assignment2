import type { Student } from "../types/Student";

type RecordsTableProps = {
  students: Student[];
};

function RecordsTable({ students }: RecordsTableProps) {
  return (
    <section className="table-section">
      <table className="records-table">
        <thead>
          <tr>
            <th>Student ID</th>
            <th>First Name</th>
            <th>Middle Name</th>
            <th>Last Name</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.studentId}>
              <td>{student.studentId}</td>
              <td>{student.firstName}</td>
              <td>{student.middleName}</td>
              <td>{student.lastName}</td>
              <td>{student.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default RecordsTable;