import { NavLink } from "react-router-dom";

function Navbar() {
    return (
        <nav className="navbar">
            <NavLink to="/" className="navbar-brand">
                Course Management System
            </NavLink>


            <div className="navbar-links">
                <NavLink
                    to="/students/new"
                    // @ts-ignore
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    Student Entry
                </NavLink>
                <NavLink
                    to="/students"
                    end
                    // @ts-ignore
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    View Records
                </NavLink>
            </div>
        </nav>
    );
}

export default Navbar;