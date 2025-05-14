import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./page/Home";
import "./App.css";
import AppRoutes from "./Routes/AppRoutes";
import Admin from "./admin/Admin";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
function App() {
  return (
    <Router>
      <AppRoutes />
      <ToastContainer autoClose={10000} /> {/* 10 seconds */}
    </Router>
  );
}

export default App;
