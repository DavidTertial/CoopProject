// Import React core library
import React from "react";

// Import ReactDOM's createRoot function to render our app
import { createRoot } from "react-dom/client";

// Import BrowserRouter and routing components from React Router
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

// Import main App layout component
import App from "./App.jsx";

// Import individual page components
import Login from "./pages/Login.jsx";
import Register from "./pages/Register.jsx";
import Upload from "./pages/Upload.jsx";
import Files from "./pages/Files.jsx";
import FileDetail from "./pages/FileDetail.jsx";
import Jobs from "./pages/Jobs.jsx";

// -----------------------------
// ROOT RENDERING
// -----------------------------

// Find the root HTML element where the React app will be mounted
const rootElement = document.getElementById("root");

// Create a root using React 18's createRoot API
const root = createRoot(rootElement);

// Render the application inside the root element
root.render(
  // BrowserRouter wraps the app and enables client-side routing
  <BrowserRouter>
    {/* Routes component contains all route definitions */}
    <Routes>
      {/* The main layout route */}
      <Route path="/" element={<App />}>
        {/* Default route: if user visits "/", redirect to "/files" */}
        <Route index element={<Navigate to="/files" />} />
        {/* Public routes */}
        <Route path="/login" element={<Login />} /> {/* Login page */}
        <Route path="/register" element={<Register />} />{" "}
        {/* Registration page */}
        {/* Protected or authenticated routes */}
        <Route path="/upload" element={<Upload />} /> {/* File upload page */}
        <Route path="/files" element={<Files />} /> {/* List of all files */}
        <Route path="/files/:id" element={<FileDetail />} />
        {/* File detail page with dynamic ID */}
        <Route path="/jobs" element={<Jobs />} />{" "}
        {/* Jobs page to view processing jobs */}
      </Route>
    </Routes>
  </BrowserRouter>
);
