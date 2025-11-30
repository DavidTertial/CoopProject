// Import Router from Express to define route endpoints
import { Router } from "express";

// Import authentication middleware to protect routes
import auth from "../middleware/auth.js";

// Import Mongoose models for Job and File
import Job from "../models/Job.js";
import FileModel from "../models/File.js";

// Create a new router instance
const router = Router();

// -----------------------------
// POST /jobs → Create a new job for a file
// -----------------------------
router.post("/", auth, async (req, res) => {
  const { fileId } = req.body; // Extract fileId from request body

  // Check if the file exists and belongs to the authenticated user
  const file = await FileModel.findOne({
    _id: fileId,
    owner: req.user.id,
    deletedAt: null, // Only non-deleted files
  });
  if (!file) return res.status(404).json({ message: "File not found" });

  // Create a new Job document in the database with initial state "queued"
  const job = await Job.create({ fileId, owner: req.user.id, state: "queued" });

  // Respond immediately with the created job
  res.status(201).json(job);

  // Simulate asynchronous job lifecycle:
  // queued -> running (after 2s) -> succeeded (after 3s)
  setTimeout(async () => {
    job.state = "running"; // Update job to running
    await job.save(); // Save change to DB

    setTimeout(async () => {
      job.state = "succeeded"; // Update job to succeeded
      job.result = makeFakeResult(file); // Generate fake result based on file type
      await job.save(); // Save final result
    }, 3000); // 3 seconds delay
  }, 2000); // 2 seconds delay
});

// -----------------------------
// GET /jobs → List all jobs for the authenticated user
// -----------------------------
router.get("/", auth, async (req, res) => {
  try {
    // Find all jobs owned by the user, sorted by newest first
    const jobs = await Job.find({ owner: req.user.id }).sort({ createdAt: -1 });
    res.json(jobs); // Respond with job array
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Failed to fetch jobs" });
  }
});

// -----------------------------
// GET /jobs/:id → Get details of a specific job
// -----------------------------
router.get("/:id", auth, async (req, res) => {
  // Find job by ID and ensure it belongs to the authenticated user
  const job = await Job.findOne({ _id: req.params.id, owner: req.user.id });
  if (!job) return res.status(404).json({ message: "Not found" });

  res.json(job); // Respond with job data
});

// -----------------------------
// DELETE /jobs/:id → Soft delete a file
// -----------------------------
router.delete("/:id", auth, async (req, res) => {
  try {
    // Find the file by ID and ensure it belongs to the user
    const file = await FileModel.findOne({
      _id: req.params.id,
      owner: req.user.id,
    });
    if (!file) return res.status(404).json({ message: "File not found" });

    // Soft delete by setting deletedAt timestamp
    file.deletedAt = new Date();
    await file.save();

    res.json({ message: "File deleted successfully" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Failed to delete file" });
  }
});

// -----------------------------
// Helper function: Generate fake job result based on file type
// -----------------------------
function makeFakeResult(file) {
  const base = {
    sourceFileId: String(file._id), // Store reference to original file
    generatedAt: new Date().toISOString(), // Timestamp of result generation
  };

  // Example fake result for PNID files
  if (file.type === "pnid") {
    return {
      ...base,
      summary: { equipments: 3, instruments: 5, lines: { CS: 2, SS: 1 } },
    };
  }

  // Example fake result for Isometric files
  if (file.type === "isometric") {
    return {
      ...base,
      summary: { spools: 7, welds: 12, materials: { CS: 20, SS: 6 } },
    };
  }

  // Example fake result for IDSV / 3D model files
  return { ...base, summary: { meshes: 42, vertices: 155000, materials: 6 } };
}

// Export the router to be used in main server file
export default router;
