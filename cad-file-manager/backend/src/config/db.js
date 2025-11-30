import mongoose from "mongoose";

// -----------------------------
// Function to connect to MongoDB using Mongoose
// -----------------------------
export default async function connectDB(uri) {
  try {
    // Attempt to connect to MongoDB using the provided URI
    // mongoose.connect() returns a promise, so we await it
    await mongoose.connect(uri);

    // If connection succeeds, log a success message
    console.log("MongoDB connected");
  } catch (err) {
    // If connection fails, log the error message
    console.error("MongoDB connection error:", err.message);

    // Exit the Node.js process with failure code
    // This is important in production so the app doesn't run without a DB
    process.exit(1);
  }
}
