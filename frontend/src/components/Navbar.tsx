function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Course Management System</div>

      <div className="navbar-links">
        <a href="#" className="nav-link">
          Student Entry
        </a>
        <a href="#" className="nav-link active">
          View Records
        </a>
      </div>
    </nav>
  );
}

export default Navbar;