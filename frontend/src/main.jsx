import React from "react";
import ReactDOM from "react-dom";
import App from "./App.jsx";
import "./index.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { AuthContextProvider } from "./context/authContext.jsx";

ReactDOM.render(
  <>
    <ToastContainer />
    <AuthContextProvider>
      <App />
    </AuthContextProvider>
  </>,
  document.getElementById("root")
);
