import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import StudentEntryPage from "./pages/StudentEntryPage";
import ViewRecordsPage from "./pages/ViewRecordsPage";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/students/new" element={<StudentEntryPage />} />
          <Route path="/students" element={<ViewRecordsPage />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;