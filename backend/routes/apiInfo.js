import express from "express";

const router = express.Router();

router.get("/", (req, res) => {
  res.json({
    name: "GigBoard API",
    version: "1.0.0",
    description: "Backend API for the GigBoard student freelancing platform",
    endpoints: {
      authentication: "/api/auth",
      gigs: "/api/gigs",
      bids: "/api/bids",
      health: "/api/health",
    },
  });
});

export default router;