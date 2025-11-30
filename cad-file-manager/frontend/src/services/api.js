// Import the Axios library, which is used for making HTTP requests
import axios from "axios";

// Create a new Axios instance with a base URL
// This base URL will be prefixed to all HTTP requests made using this instance
// Example: api.get("/files") will actually call "http://localhost:50001/api/files"
const api = axios.create({ baseURL: "http://localhost:50001/api" });

// Add a request interceptor to this Axios instance
// Interceptors let you modify requests before they are sent
api.interceptors.request.use((config) => {
  // Get the JWT token stored in localStorage (from login)
  const token = localStorage.getItem("token");

  // If a token exists, attach it to the request headers as a Bearer token
  // This ensures that all protected backend routes receive authentication
  if (token) config.headers.Authorization = `Bearer ${token}`;

  // Return the updated config object so the request proceeds
  return config;
});

// Export the configured Axios instance so it can be imported and used in React components
// Example usage in a component: const { data } = await api.get("/files");
export default api;
