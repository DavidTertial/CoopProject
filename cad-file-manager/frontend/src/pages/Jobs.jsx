// Import React and necessary hooks
import React, { useEffect, useState } from "react";
// Import the Axios instance preconfigured with baseURL and JWT handling
import api from "../services/api";

export default function Jobs() {
  // State to store the list of jobs fetched from the backend
  const [jobs, setJobs] = useState([]);

  // State to indicate whether the data is currently being loaded
  const [loading, setLoading] = useState(true);

  // State to store any error message if fetching fails
  const [error, setError] = useState("");

  // useEffect hook to fetch jobs when the component mounts
  useEffect(() => {
    // Define an async function to fetch jobs
    async function fetchJobs() {
      try {
        // Retrieve JWT token from localStorage
        const token = localStorage.getItem("token");
        if (!token) throw new Error("Not authenticated"); // Abort if no token

        // Make GET request to /jobs endpoint with Authorization header
        const res = await api.get("/jobs", {
          headers: { Authorization: `Bearer ${token}` },
        });

        // Set the jobs state with the data returned from backend
        // Use empty array if res.data is null/undefined
        setJobs(res.data || []);
      } catch (err) {
        // Log error to console for debugging
        console.error(err);
        // Update error state to display message to user
        setError("Failed to fetch jobs.");
      } finally {
        // Set loading to false after request completes (success or failure)
        setLoading(false);
      }
    }

    // Call the async function to fetch jobs
    fetchJobs();
  }, []); // Empty dependency array → runs only once when component mounts

  // Conditional rendering while loading data
  if (loading) return <p>Loading jobs...</p>;

  // Conditional rendering if there was an error fetching data
  if (error) return <p>{error}</p>;

  // Conditional rendering if there are no jobs yet
  if (jobs.length === 0)
    return <p>Trigger a job from a file detail page to see live status.</p>;

  // Main return: render the list of jobs
  return (
    <div>
      <h2>Jobs</h2>

      {/* Map through jobs array and display each job in a card */}
      {jobs.map((job) => (
        <div
          key={job._id} // Unique key for each element in a list
          style={{ border: "1px solid #ccc", margin: 10, padding: 10 }} // Simple card styling
        >
          {/* Display the associated File ID */}
          <p>
            <strong>File ID:</strong> {job.fileId}
          </p>

          {/* Display the current state of the job */}
          <p>
            <strong>Status:</strong> {job.state}
          </p>

          {/* Display the result JSON if the job has finished and result exists */}
          {job.result && (
            <pre style={{ background: "#f9f9f9", padding: 10 }}>
              {JSON.stringify(job.result, null, 2)} {/* Pretty-print JSON */}
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}
