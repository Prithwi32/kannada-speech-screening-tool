// config/database.js
const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    const mongoURI =
      process.env.MONGODB_URI || "mongodb://localhost:27017/kannada_speech_db";

    // Note: useNewUrlParser and useUnifiedTopology are deprecated in MongoDB driver v4+
    await mongoose.connect(mongoURI);

    console.log("✅ MongoDB connected successfully");
  } catch (error) {
    console.error("❌ MongoDB connection error:", error.message);
    console.warn("⚠️  Using JSON fallback mode");
    // Don't exit - allow server to continue with JSON fallback
  }
};

module.exports = connectDB;
