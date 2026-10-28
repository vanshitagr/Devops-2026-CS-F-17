import express from "express";
import mongoose from "mongoose";

const router = express.Router();

router.get("/database", (req, res) => {
  const states = {
    0: "disconnected",
    1: "connected",
    2: "connecting",
    3: "disconnecting",
  };

  const state = states[mongoose.connection.readyState] || "unknown";

  res.status(state === "connected" ? 200 : 503).json({
    success: state === "connected",
    database: state,
  });
});

export default router;