import mongoose from "mongoose";

// -----------------------------
// Define the schema for files
// -----------------------------
const fileSchema = new mongoose.Schema(
  {
    // Name of the uploaded file (e.g., "diagram.pnid")
    name: String,

    // File type: must be one of "pnid", "isometric", or "idsv"
    type: {
      type: String,
      enum: ["pnid", "isometric", "idsv"], // restrict values
      required: true, // type is mandatory
    },

    // Size of the file in bytes
    size: Number,

    // Reference to the user who owns the file
    owner: {
      type: mongoose.Schema.Types.ObjectId, // MongoDB ObjectId
      ref: "User", // References the "User" collection
    },

    // Path where the file is stored on the server
    path: String,

    // Timestamp of when the file was created/uploaded
    createdAt: {
      type: Date,
      default: Date.now, // Automatically set to current date
    },

    // Timestamp for soft deletion; null means the file is active
    deletedAt: {
      type: Date,
      default: null, // Not deleted initially
    },
  },
  {
    versionKey: false, // Disable __v field (Mongoose versioning)
  }
);

// Export the Mongoose model for use in routes/controllers
export default mongoose.model("File", fileSchema);
