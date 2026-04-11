import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function LandingPage() {
    return (
        <>
            <Navbar/>

            <main className="page-container">
                <header className="page-header">
                    <h1>Course Management System</h1>
                    <p>
                        Manage student records and course data efficiently. Choose an option
                        below to get started.
                    </p>
                </header>

                <section className="landing-actions">
                    <div className="landing-card">
                        <h2>Add Student</h2>
                        <p>Enter a new student into the system.</p>
                        <Link to="/students/new" className="landing-button">
                            Go to Student Entry
                        </Link>
                    </div>

                    <div className="landing-card">
                        <h2>View Records</h2>
                        <p>Browse all existing student records.</p>
                        <Link to="/students" className="landing-button secondary">
                            View Student Records
                        </Link>
                    </div>
                </section>
            </main>
            <footer className="page-footer">
                <p>Course Management System Framework designed and developed by Group 3</p>
            </footer>
        </>
    );
}

export default LandingPage;