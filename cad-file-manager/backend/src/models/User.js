import mongoose from "mongoose";
import bcrypt from "bcrypt";

// -----------------------------
// Define the schema for users
// -----------------------------
const userSchema = new mongoose.Schema(
  {
    // Unique username for login/display
    username: {
      type: String,
      required: true, // Must be provided
      unique: true, // No two users can have the same username
    },

    // Unique email for login/notifications
    email: {
      type: String,
      required: true,
      unique: true,
    },

    // Hashed password (stored securely)
    password: {
      type: String,
      required: true,
    },
  },
  {
    timestamps: true, // Automatically add createdAt & updatedAt fields
  }
);

// -----------------------------
// Middleware to hash password before saving
// -----------------------------
userSchema.pre("save", async function (next) {
  // Only hash the password if it has been modified (or new user)
  if (!this.isModified("password")) return next();

  // Hash the password using bcrypt with a salt round of 10
  this.password = await bcrypt.hash(this.password, 10);

  // Proceed with save
  next();
});

// -----------------------------
// Instance method to compare a plain password with the hashed password
// -----------------------------
userSchema.methods.comparePassword = function (plain) {
  // Returns a promise resolving to true if passwords match, false otherwise
  return bcrypt.compare(plain, this.password);
};

// Export the User model for use in controllers/routes
export default mongoose.model("User", userSchema);
