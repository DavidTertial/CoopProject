// Import React and necessary hooks
import React, { useEffect, useState } from "react";
// Link component to navigate to file details without refreshing the page
import { Link } from "react-router-dom";
// Axios instance with baseURL and JWT handling for API requests
import api from "../services/api";

export default function Files() {
  // State to store the list of files fetched from the backend
  const [items, setItems] = useState([]);

  // State to store the search query input by the user
  const [q, setQ] = useState("");

  // State to store the selected file type filter
  const [type, setType] = useState("");

  // Function to load files from backend based on current search & filter
  async function load() {
    try {
      // GET request with query parameters q (search) and type (filter)
      const { data } = await api.get("/files", { params: { q, type } });

      // Store the fetched file items into state
      // data.items assumes the backend returns { items: [...] }
      setItems(data.items);
    } catch (err) {
      // Log error if API call fails
      console.error("Failed to load files:", err);
    }
  }

  // useEffect to load files when the component mounts
  useEffect(() => {
    load(); // Initial fetch when the page loads
  }, []); // Empty dependency array → runs only once on mount

  return (
    <div>
      {/* Page heading */}
      <h3>My Files</h3>

      {/* Search and filter section */}
      <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
        {/* Text input to search by file name */}
        <input
          placeholder="Search by name"
          value={q} // Controlled input tied to state
          onChange={(e) => setQ(e.target.value)} // Update state on change
        />

        {/* Dropdown to filter by file type */}
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="">All types</option> {/* No filter */}
          <option value="pnid">PNID</option>
          <option value="isometric">Isometric</option>
          <option value="idsv">IDSV</option>
        </select>

        {/* Button to trigger loading files based on current search/filter */}
        <button onClick={load}>Search</button>
      </div>

      {/* Table to display the list of files */}
      <table
        width="100%"
        border="1"
        cellPadding="6"
        style={{ borderCollapse: "collapse" }} // Merge table borders
      >
        <thead>
          <tr>
            <th>Name</th> {/* File name */}
            <th>Type</th> {/* File type */}
            <th>Size</th> {/* File size in KB */}
            <th>Created</th> {/* File creation date */}
            <th>Action</th> {/* Action column (e.g., Open link) */}
          </tr>
        </thead>

        <tbody>
          {/* Loop through the items array and render a row for each file */}
          {items?.map((f) => (
            <tr key={f._id}>
              {/* File name with link to its detail page */}
              <td>
                <Link to={`/files/${f._id}`}>{f.name}</Link>
              </td>

              {/* File type */}
              <td>{f.type}</td>

              {/* File size in KB (rounded) */}
              <td>{Math.round((f.size || 0) / 1024)} KB</td>

              {/* Formatted creation date */}
              <td>{new Date(f.createdAt).toLocaleString()}</td>

              {/* Action column with a link to open file details */}
              <td>
                <Link to={`/files/${f._id}`}>Open</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
