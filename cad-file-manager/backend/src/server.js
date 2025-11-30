// -----------------------------
// Imports
// -----------------------------
import express from "express"; // Express framework for building APIs
import mongoose from "mongoose"; // MongoDB ODM for database operations
import dotenv from "dotenv"; // Load environment variables from .env
import cors from "cors"; // Enable Cross-Origin Resource Sharing
import path from "path"; // Node.js module for handling file paths
import { fileURLToPath } from "url"; // Convert module URL to file path
import authRoutes from "./routes/authRoutes.js"; // Authentication routes
import fileRoutes from "./routes/fileRoutes.js"; // File management routes
import jobRoutes from "./routes/jobRoutes.js"; // Job processing routes
import http from "http"; // Node.js HTTP module for server creation

// -----------------------------
// Load environment variables
// -----------------------------
dotenv.config(); // Loads variables like MONGO_URI and PORT from .env

// -----------------------------
// Initialize Express app
// -----------------------------
const app = express();

// -----------------------------
// Middleware
// -----------------------------
app.use(cors()); // Enable requests from other origins (frontend)
app.use(express.json()); // Automatically parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded form data

// -----------------------------
// Serve uploaded files statically
// -----------------------------
const __filename = fileURLToPath(import.meta.url); // Get current file path
const __dirname = path.dirname(__filename); // Get current directory
app.use("/uploads", express.static(path.join(__dirname, "uploads")));
// Files in /uploads folder are accessible via /uploads/<filename>

// -----------------------------
// API Routes
// -----------------------------
app.use("/api/auth", authRoutes); // Register and login endpoints
app.use("/api/files", fileRoutes); // Upload, list, delete files
app.use("/api/jobs", jobRoutes); // Create, list, and view processing jobs

// -----------------------------
// Default route for testing
// -----------------------------
app.get("/", (req, res) => {
  res.send("CAD Mini File Management & Processing API is running");
});

// -----------------------------
// Connect to MongoDB
// -----------------------------
mongoose
  .connect(process.env.MONGO_URI) // Connect using URI from .env
  .then(() => {
    console.log("MongoDB Connected Successfully!");
  })
  .catch((err) => {
    console.error("MongoDB Connection Failed:", err.message);
    process.exit(1); // Exit process if DB connection fails
  });

// -----------------------------
// Server startup
// -----------------------------
const DEFAULT_PORT = process.env.PORT || 3000; // Default port if none in .env

function startServer(port) {
  const server = http.createServer(app); // Create HTTP server from Express app

  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });

  // Handle port errors (e.g., port already in use)
  server.on("error", (err) => {
    if (err.code === "EADDRINUSE") {
      console.log(`⚠️  Port ${port} busy, trying ${port + 1}...`);
      startServer(port + 1); // Try next port
    } else {
      console.error("Server error:", err);
    }
  });
}

// Start server with default port
startServer(DEFAULT_PORT);
