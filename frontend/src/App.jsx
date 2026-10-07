import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Analyze from "./pages/Analyze";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#F7F8FC] text-[#111827]">
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;