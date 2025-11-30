// -----------------------------
// Imports
// -----------------------------
import { Router } from "express"; // Router to define endpoints
import jwt from "jsonwebtoken"; // JSON Web Token library for authentication
import User from "../models/User.js"; // Mongoose model for user

// Create a new router instance
const router = Router();

// -----------------------------
// POST /auth/register → Register a new user
// -----------------------------
router.post("/register", async (req, res) => {
  try {
    const { username, email, password } = req.body; // Extract fields from request body

    // Validate that all required fields are provided
    if (!username || !email || !password)
      return res.status(400).json({ message: "Missing fields" });

    // Check if a user already exists with the same email or username
    const exists = await User.findOne({ $or: [{ email }, { username }] });
    if (exists) return res.status(409).json({ message: "User exists" });

    // Create a new user document in MongoDB
    const user = await User.create({ username, email, password });

    // Respond with user info (excluding password)
    res
      .status(201)
      .json({ id: user._id, username: user.username, email: user.email });
  } catch (e) {
    // Handle server errors
    res.status(500).json({ message: "Server error" });
  }
});

// -----------------------------
// POST /auth/login → Authenticate user and issue JWT
// -----------------------------
router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body; // Extract credentials from request body

    // Find user by email
    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ message: "Invalid credentials" });

    // Verify password using a method defined in User model
    const ok = await user.comparePassword(password);
    if (!ok) return res.status(401).json({ message: "Invalid credentials" });

    // Sign a JWT token containing the user's ID
    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, {
      expiresIn: "1d", // Token expires in 1 day
    });

    // Respond with the JWT token
    res.json({ token });
  } catch (e) {
    // Handle server errors
    res.status(500).json({ message: "Server error" });
  }
});

// Export the router to be used in main server file
export default router;
