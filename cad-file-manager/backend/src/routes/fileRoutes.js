// -----------------------------
// Imports
// -----------------------------
import { Router } from "express"; // Router to define route endpoints
import multer from "multer"; // Middleware for handling multipart/form-data (file uploads)
import fs from "fs"; // Node.js file system module to create directories
import path from "path"; // Node.js module to handle file paths
import auth from "../middleware/auth.js"; // Authentication middleware to protect routes
import FileModel from "../models/File.js"; // Mongoose model for storing file metadata

// Create a new router instance
const router = Router();

// -----------------------------
// Multer configuration for file uploads
// -----------------------------
const storage = multer.diskStorage({
  // Set destination folder for uploaded files
  destination: (req, file, cb) => {
    const dir = path.join("uploads", req.user.id); // Each user has their own folder
    fs.mkdirSync(dir, { recursive: true }); // Create folder if it doesn't exist
    cb(null, dir); // Callback with directory
  },
  // Set filename format
  filename: (req, file, cb) => cb(null, Date.now() + "-" + file.originalname),
});

// Initialize multer middleware
const upload = multer({
  storage, // Use custom storage config
  limits: { fileSize: 25 * 1024 * 1024 }, // Limit file size to 25MB
  fileFilter: (req, file, cb) => {
    // Accept any file; optionally filter by mimetype
    cb(null, true);
  },
});

// -----------------------------
// POST /files/upload → Upload a file
// -----------------------------
router.post("/upload", auth, upload.single("file"), async (req, res) => {
  try {
    const { type } = req.body; // Get file type from request body

    // Validate file type
    if (!["pnid", "isometric", "idsv"].includes(type))
      return res.status(400).json({ message: "Invalid type" });

    // Save file metadata to MongoDB
    const saved = await FileModel.create({
      name: req.file.originalname, // Original filename
      type, // File type (pnid, isometric, idsv)
      size: req.file.size, // File size in bytes
      owner: req.user.id, // ID of the authenticated user
      path: req.file.path, // File path on the server
    });

    res.status(201).json(saved); // Respond with saved file metadata
  } catch (e) {
    res.status(500).json({ message: "Upload error" }); // Handle upload errors
  }
});

// -----------------------------
// GET /files → List and search files with pagination
// -----------------------------
router.get("/", auth, async (req, res) => {
  const { type, q, page = 1, pageSize = 10 } = req.query; // Extract query params

  // Build query: only files owned by user and not deleted
  const query = { owner: req.user.id, deletedAt: null };
  if (type) query.type = type; // Filter by file type if provided
  if (q) query.name = { $regex: q, $options: "i" }; // Case-insensitive search by name

  // Fetch files and total count concurrently
  const [items, total] = await Promise.all([
    FileModel.find(query)
      .sort({ createdAt: -1 }) // Most recent files first
      .skip((Number(page) - 1) * Number(pageSize)) // Pagination skip
      .limit(Number(pageSize)), // Pagination limit
    FileModel.countDocuments(query), // Total number of matching files
  ]);

  // Respond with paginated results
  res.json({ items, total, page: Number(page), pageSize: Number(pageSize) });
});

// -----------------------------
// GET /files/:id → Get file metadata by ID
// -----------------------------
router.get("/:id", auth, async (req, res) => {
  const doc = await FileModel.findOne({
    _id: req.params.id, // File ID from URL
    owner: req.user.id, // Ensure file belongs to authenticated user
  });

  if (!doc) return res.status(404).json({ message: "Not found" }); // File not found
  res.json(doc); // Return file metadata
});

// -----------------------------
// DELETE /files/:id → Soft delete a file
// -----------------------------
router.delete("/:id", auth, async (req, res) => {
  // Find the file and update the deletedAt timestamp
  const doc = await FileModel.findOneAndUpdate(
    { _id: req.params.id, owner: req.user.id }, // Only user's own file
    { deletedAt: new Date() }, // Soft delete by marking deletedAt
    { new: true } // Return the updated document
  );

  if (!doc) return res.status(404).json({ message: "Not found" }); // File not found
  res.json({ message: "Deleted", id: doc._id }); // Respond with confirmation
});

// Export the router to be used in the main server file
export default router;
