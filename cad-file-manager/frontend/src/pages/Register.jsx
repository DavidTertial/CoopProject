// Import React and necessary hooks
import React, { useState } from "react";
// Import Axios instance for API requests
import api from "../services/api";
// Import useNavigate for programmatic navigation after registration
import { useNavigate } from "react-router-dom";

export default function Register() {
  // State to store the user's username input
  const [username, setUsername] = useState("");

  // State to store the user's email input
  const [email, setEmail] = useState("");

  // State to store the user's password input
  const [password, setPassword] = useState("");

  // State to store messages for the user (e.g., success message)
  const [msg, setMsg] = useState("");

  // Initialize the navigate function to redirect user after registration
  const nav = useNavigate();

  // Function to handle form submission
  async function submit(e) {
    e.preventDefault(); // Prevent default form submission (page reload)

    try {
      // Send POST request to backend /auth/register with username, email, and password
      await api.post("/auth/register", { username, email, password });

      // Update state to show success message
      setMsg("Registered! Redirecting to login...");

      // Redirect to login page after a short delay (800ms)
      setTimeout(() => nav("/login"), 800);
    } catch (err) {
      // Handle error response from backend
      setMsg(err.response?.data?.message || "Registration failed");
      console.error("Registration error:", err);
    }
  }

  return (
    // Form element that triggers submit() on submit
    <form onSubmit={submit} style={{ display: "grid", gap: 8 }}>
      <h3>Register</h3>

      {/* Display message (success or error) if present */}
      {msg && (
        <div style={{ color: msg.includes("Registered") ? "green" : "red" }}>
          {msg}
        </div>
      )}

      {/* Input for username */}
      <input
        placeholder="Username" // Placeholder text
        value={username} // Controlled input value from state
        onChange={(e) => setUsername(e.target.value)} // Update state on change
      />

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
      <button>Create Account</button>
    </form>
  );
}
