import Navbar from "../components/Navbar";
import SummaryCards from "../components/SummaryCards";
import RecordsTable from "../components/RecordsTable";
import EmptyState from "../components/EmptyState";
import { mockStudents } from "../data/mockStudents";

function ViewRecordsPage() {
  const sortedStudents = [...mockStudents].sort(
    (a, b) => a.studentId - b.studentId
  );

  const totalStudents = sortedStudents.length;

  const averageScore =
    totalStudents > 0
      ? (
          sortedStudents.reduce((sum, student) => sum + student.score, 0) /
          totalStudents
        ).toFixed(2)
      : "0.00";

  return (
    <>
      <Navbar />
      <main className="page-container">
        <section className="page-header">
          <h1>View Student Records</h1>
          <p>Student records displayed in ascending order by Student ID.</p>
        </section>

        <SummaryCards
          totalStudents={totalStudents}
          averageScore={averageScore}
        />

        {totalStudents > 0 ? (
          <RecordsTable students={sortedStudents} />
        ) : (
          <EmptyState message="No student records available." />
        )}
      </main>
      <footer className="page-footer">
        <p>Course Management System Framework designed and developed by Group 3</p>
      </footer>
    </>
  );
}

export default ViewRecordsPage;