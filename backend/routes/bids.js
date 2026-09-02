import express from "express";
import Bid from "../models/Bid.js";
import { protect } from "../middleware/auth.js";

const router = express.Router();

// @route GET /api/bids/mine  (all bids the logged-in user has placed)
router.get("/mine", protect, async (req, res) => {
  try {
    const bids = await Bid.find({ bidder: req.user._id })
      .populate({
        path: "gig",
        select: "title status budget location deadline postedBy",
      })
      .sort({ createdAt: -1 });
    res.json(bids);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;
