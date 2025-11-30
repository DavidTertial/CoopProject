// Import React and useState hook
import React, { useState } from "react";
// Import Axios instance for making API requests
import api from "../services/api";

export default function Upload() {
  // State to store the selected file object
  const [file, setFile] = useState();

  // State to store the selected file type (pnid, isometric, idsv)
  const [type, setType] = useState("pnid");

  // State to store feedback messages (e.g., upload success)
  const [msg, setMsg] = useState("");

  // Function to handle form submission
  async function submit(e) {
    e.preventDefault(); // Prevent page reload on form submit

    // Create a FormData object to send file + type in a multipart/form-data request
    const form = new FormData();
    form.append("file", file); // Append the selected file
    form.append("type", type); // Append the selected file type

    try {
      // POST request to backend /files/upload endpoint
      const { data } = await api.post("/files/upload", form);

      // Update message state to show upload success
      setMsg(`Uploaded ${data.name}`);
    } catch (err) {
      // Log and display error if upload fails
      console.error("Upload failed:", err);
      setMsg("Upload failed. Please try again.");
    }
  }

  return (
    // Form element to handle file upload
    <form onSubmit={submit} style={{ display: "grid", gap: 8 }}>
      <h3>Upload File</h3>

      {/* Display success or error message */}
      {msg && <div style={{ color: "green" }}>{msg}</div>}

      {/* Dropdown to select file type */}
      <select value={type} onChange={(e) => setType(e.target.value)}>
        <option value="pnid">PNID</option>
        <option value="isometric">Isometric</option>
        <option value="idsv">IDSV</option>
      </select>

      {/* File input to select a file */}
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])} // Store first selected file in state
      />

      {/* Upload button disabled if no file is selected */}
      <button disabled={!file}>Upload</button>
    </form>
  );
}
