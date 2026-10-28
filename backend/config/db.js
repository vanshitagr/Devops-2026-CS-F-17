import mongoose from "mongoose";

const connectDB = async () => {
  if (process.env.NODE_ENV === "test") {
    return;
  }
  const uri = process.env.MONGO_URI || process.env.ATLAS_DB_URL;
  if (!uri) {
    console.warn("[WARN] MongoDB URI not provided. Running without database connection.");
    return;
  }
  try {
    const conn = await mongoose.connect(uri);
    console.log(`MongoDB connected: ${conn.connection.host}`);
  } catch (err) {
    console.error(`MongoDB connection error: ${err.message}`);
    if (process.env.NODE_ENV === "production") {
      process.exit(1);
    }
  }
};

export default connectDB;
