// Import React and necessary hooks/components from react-router-dom
import React from "react";
import { Outlet, Link, useNavigate } from "react-router-dom";

// Define the main App component, which serves as a layout for all pages
export default function App() {
  // useNavigate hook allows programmatic navigation
  const nav = useNavigate();

  // Retrieve JWT token from localStorage to check if the user is logged in
  const token = localStorage.getItem("token");

  // Function to log the user out
  function logout() {
    // Remove token from localStorage, effectively logging the user out
    localStorage.removeItem("token");

    // Navigate user to the login page
    nav("/login");
  }

  return (
    // Main container for the app
    <div
      style={{
        fontFamily: "sans-serif", // Set font for the app
        maxWidth: 960, // Limit maximum width of content
        margin: "0 auto", // Center the app horizontally
        padding: 16, // Add some padding inside the container
      }}
    >
      {/* Header section */}
      <header
        style={{
          display: "flex", // Use flexbox to arrange items horizontally
          gap: 12, // Space between header items
          alignItems: "center", // Vertically center items
          marginBottom: 16, // Space below the header
        }}
      >
        {/* App title, pushed to the left using marginRight: 'auto' */}
        <h2 style={{ marginRight: "auto" }}>CAD Mini</h2>

        {/* Navigation links */}
        <Link to="/files">Files</Link>
        <Link to="/upload">Upload</Link>
        <Link to="/jobs">Jobs</Link>

        {/* Conditional rendering based on whether the user is logged in */}
        {!token ? (
          // If no token (not logged in), show Login and Register links
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        ) : (
          // If token exists (logged in), show Logout button
          <button onClick={logout}>Logout</button>
        )}
      </header>

      {/* Outlet is where the nested routes/pages will be rendered */}
      <Outlet />
    </div>
  );
}
