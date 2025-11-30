// Import React and necessary hooks
import React, { useEffect, useState } from "react";
// useParams allows us to read dynamic parameters from the URL (e.g., /files/:id)
import { useParams } from "react-router-dom";
// Import the Axios instance configured with baseURL and JWT handling
import api from "../services/api";

export default function FileDetail() {
  // Extract the "id" parameter from the URL (represents the file ID)
  const { id } = useParams();

  // State to hold the file metadata fetched from the backend
  const [file, setFile] = useState();

  // State to hold the processing job associated with this file
  const [job, setJob] = useState();

  // Function to load the file details from the backend
  async function load() {
    try {
      // Send GET request to fetch the file data by its ID
      const { data } = await api.get(`/files/${id}`);
      // Update state with the fetched file details
      setFile(data);
    } catch (err) {
      // Log any errors during API call
      console.error("Failed to load file:", err);
    }
  }

  // useEffect runs when the component mounts or the file ID changes
  useEffect(() => {
    load(); // Call the load function to fetch file data
  }, [id]);

  // Function to trigger a processing job for this file
  async function processFile() {
    try {
      // POST request to create a new job for this file
      const { data } = await api.post("/jobs", { fileId: id });

      // Store the initial job data in state
      setJob(data);

      // Polling: periodically check the job status every 1 second
      const interval = setInterval(async () => {
        // GET request to fetch the latest job details
        const { data: jd } = await api.get(`/jobs/${data._id}`);

        // Update the job state with the latest information
        setJob(jd);

        // Stop polling once the job has succeeded
        if (jd.state === "succeeded") clearInterval(interval);
      }, 1000);
    } catch (err) {
      console.error("Failed to start job:", err);
    }
  }

  // Function to delete the current file
  async function deleteFile() {
    // Show confirmation dialog to prevent accidental deletion
    if (!window.confirm("Are you sure you want to delete this file?")) return;

    try {
      // Retrieve the JWT token from localStorage
      const token = localStorage.getItem("token");

      // DELETE request to the backend with authorization header
      await api.delete(`/files/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Notify the user of successful deletion
      alert("File deleted successfully!");

      // Redirect user back to the main files list
      window.location.href = "/files";
    } catch (err) {
      // Handle errors during deletion
      console.error("Failed to delete file:", err);
      alert("Failed to delete file.");
    }
  }

  return (
    <div>
      {/* Main heading */}
      <h3>File Detail</h3>

      {/* Display file information only if the file is loaded */}
      {file && (
        <>
          <div>
            <b>Name:</b> {file.name} {/* File name */}
          </div>
          <div>
            <b>Type:</b> {file.type} {/* File type (pnid, isometric, idsv) */}
          </div>
          <div>
            <b>Size:</b> {Math.round((file.size || 0) / 1024)} KB{" "}
            {/* File size in KB */}
          </div>
          <div>
            <b>Created:</b> {new Date(file.createdAt).toLocaleString()}{" "}
            {/* Formatted creation date */}
          </div>

          {/* Button to trigger a processing job */}
          <button onClick={processFile}>Process File</button>

          {/* Button to delete the file */}
          <button
            onClick={deleteFile}
            style={{ marginLeft: 10, color: "red" }} // Styling: margin and color
          >
            Delete File
          </button>
        </>
      )}

      {/* Display the job information if a processing job exists */}
      {job && (
        <div style={{ marginTop: 12 }}>
          <h4>Job</h4>
          <div>
            <b>Status:</b> {job.state}{" "}
            {/* Job state: queued, running, succeeded */}
          </div>

          {/* Display JSON result if the job has finished and produced results */}
          {job.result && (
            <pre style={{ background: "#f2f2f2", padding: 8 }}>
              {JSON.stringify(job.result, null, 2)} {/* Pretty-print JSON */}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
