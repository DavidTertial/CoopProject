import mongoose from "mongoose";

// -----------------------------
// Define the schema for processing jobs
// -----------------------------
const jobSchema = new mongoose.Schema(
  {
    // Reference to the file this job is processing
    fileId: {
      type: mongoose.Schema.Types.ObjectId, // MongoDB ObjectId
      ref: "File", // References the "File" collection
      required: true,
    },

    // Reference to the user who created the job
    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User", // References the "User" collection
      required: true,
    },

    // Current state of the job
    state: {
      type: String,
      enum: ["queued", "running", "succeeded"], // Allowed job states
      default: "queued", // Newly created jobs start in "queued"
    },

    // Result of the processing job (e.g., simulated MTO JSON)
    result: {
      type: Object,
      default: null, // Initially null, populated once job succeeds
    },
  },
  {
    timestamps: true, // Automatically adds createdAt & updatedAt fields
    versionKey: false, // Disable __v field (Mongoose versioning)
  }
);

// Export the Mongoose model for use in routes/controllers
export default mongoose.model("Job", jobSchema);
