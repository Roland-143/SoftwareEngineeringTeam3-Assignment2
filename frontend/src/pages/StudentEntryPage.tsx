import Navbar from "../components/Navbar";
import StudentEntryForm from "../components/StudentEntryForm";

export default function StudentEntryPage() {
    return (
        <>
            <Navbar />

            <main className="page-container">
                <header className="page-header">
                    <h1>Student Entry</h1>
                    <p>
                        Enter student information below. Required fields must be completed
                        before submission.
                    </p>
                </header>

                <section className="form-section">
                    <StudentEntryForm />
                </section>
            </main>

            <footer className="page-footer">
                <p>Course Management System Framework designed and developed by Group 3</p>
            </footer>
        </>
    );
}