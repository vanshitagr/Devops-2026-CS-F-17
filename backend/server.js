import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import connectDB from "./config/db.js";
import authRoutes from "./routes/auth.js";
import gigRoutes from "./routes/gigs.js";
import bidRoutes from "./routes/bids.js";
import errorHandler from "./middleware/errorHandler.js";
import requestLogger from "./middleware/requestLogger.js";
import apiInfoRoutes from "./routes/apiInfo.js";
import requestId from "./middleware/requestId.js";
import { validateEnvironment } from "./config/env.js";

dotenv.config();
validateEnvironment();
connectDB();

const app = express();

// Middleware
// Restrict cross-origin requests to the deployed frontend URL in production;
// falls back to allowing all origins during local development.
app.use(cors({ origin: process.env.CLIENT_URL || "*" }));
app.use(express.json());
app.use(requestLogger);

// Root API route
app.get("/", (req, res) => {
  res.json({
    message: "GigBoard API is running - SKIT Jagatpura, Jaipur",
  });
});

// API health-check endpoint
app.get("/api/health", (req, res) => {
  res.status(200).json({
    status: "ok",
    service: "GigBoard API",
    timestamp: new Date().toISOString(),
  });
});

// API routes
app.use("/api/auth", authRoutes);
app.use("/api/gigs", gigRoutes);
app.use("/api/bids", bidRoutes);
app.use("/api/info", apiInfoRoutes);
app.use(requestId);


// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: "API route not found",
    path: req.originalUrl,
    method: req.method,
  });
});

// Centralized error handler
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});