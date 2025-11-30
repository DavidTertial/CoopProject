// Import React and necessary hooks
import React, { useState } from "react";
// Import useNavigate for programmatic navigation after login
import { useNavigate } from "react-router-dom";
// Import the Axios instance preconfigured with baseURL and JWT handling
import api from "../services/api";

export default function Login() {
  // State to store the user's email input
  const [email, setEmail] = useState("");

  // State to store the user's password input
  const [password, setPassword] = useState("");

  // State to store any error messages (e.g., wrong credentials)
  const [err, setErr] = useState("");

  // Initialize the navigate function to redirect user after login
  const nav = useNavigate();

  // Function to handle form submission
  async function submit(e) {
    e.preventDefault(); // Prevent default form submission (page reload)
    setErr(""); // Clear any previous error messages

    try {
      // Send POST request to backend /auth/login with email and password
      const { data } = await api.post("/auth/login", { email, password });

      // Save the JWT token returned from backend into localStorage
      localStorage.setItem("token", data.token);

      // Redirect the user to the files page after successful login
      nav("/files");
    } catch (e) {
      // If login fails, display the error message from backend or a default one
      setErr(e.response?.data?.message || "Login failed");
    }
  }

  return (
    // Form element that triggers submit() on submit
    <form onSubmit={submit} style={{ display: "grid", gap: 8 }}>
      <h3>Login</h3>

      {/* Display error message if login fails */}
      {err && <div style={{ color: "red" }}>{err}</div>}

      {/* Input for email */}
      <input
        placeholder="Email" // Placeholder text
        value={email} // Controlled input value from state
        onChange={(e) => setEmail(e.target.value)} // Update state on change
      />

      {/* Input for password */}
      <input
        placeholder="Password" // Placeholder text
        type="password" // Mask input for privacy
        value={password} // Controlled input value from state
        onChange={(e) => setPassword(e.target.value)} // Update state on change
      />

      {/* Submit button */}
      <button>Login</button>
    </form>
  );
}
