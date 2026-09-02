import express from "express";
import Gig from "../models/Gig.js";
import Bid from "../models/Bid.js";
import User from "../models/User.js";
import { protect } from "../middleware/auth.js";

const router = express.Router();

// @route GET /api/gigs  (browse/filter, public)
router.get("/", async (req, res) => {
  try {
    const { category, location, status, search } = req.query;
    const filter = {};
    if (category) filter.category = category;
    if (location) filter.location = location;
    filter.status = status || "open";
    if (search) {
      filter.$or = [
        { title: { $regex: search, $options: "i" } },
        { description: { $regex: search, $options: "i" } },
      ];
    }

    const gigs = await Gig.find(filter)
      .populate("postedBy", "name college rating")
      .sort({ createdAt: -1 });

    res.json(gigs);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route GET /api/gigs/mine/posted
router.get("/mine/posted", protect, async (req, res) => {
  const gigs = await Gig.find({ postedBy: req.user._id })
    .populate("assignedTo", "name")
    .sort({ createdAt: -1 });
  res.json(gigs);
});

// @route GET /api/gigs/mine/working
router.get("/mine/working", protect, async (req, res) => {
  const gigs = await Gig.find({ assignedTo: req.user._id })
    .populate("postedBy", "name")
    .sort({ createdAt: -1 });
  res.json(gigs);
});

// @route GET /api/gigs/:id
router.get("/:id", async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id).populate(
      "postedBy",
      "name college rating ratingCount"
    );
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    res.json(gig);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route POST /api/gigs  (create)
router.post("/", protect, async (req, res) => {
  try {
    const { title, description, category, budget, location, deadline } = req.body;
    if (!title || !description || !category || !budget || !location || !deadline) {
      return res.status(400).json({ message: "All fields are required" });
    }
    const gig = await Gig.create({
      title,
      description,
      category,
      budget,
      location,
      deadline,
      postedBy: req.user._id,
    });
    res.status(201).json(gig);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route POST /api/gigs/:id/bids  (place a bid)
router.post("/:id/bids", protect, async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id);
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    if (gig.status !== "open") return res.status(400).json({ message: "Gig is not open for bids" });
    if (gig.postedBy.toString() === req.user._id.toString()) {
      return res.status(400).json({ message: "You cannot bid on your own gig" });
    }

    const { amount, message } = req.body;
    if (!amount || !message) {
      return res.status(400).json({ message: "Amount and message are required" });
    }

    const bid = await Bid.create({
      gig: gig._id,
      bidder: req.user._id,
      amount,
      message,
    });
    const populated = await bid.populate("bidder", "name rating college");
    res.status(201).json(populated);
  } catch (err) {
    if (err.code === 11000) {
      return res.status(400).json({ message: "You already placed a bid on this gig" });
    }
    res.status(500).json({ message: err.message });
  }
});

// @route GET /api/gigs/:id/bids  (poster views bids on their gig)
router.get("/:id/bids", protect, async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id);
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    if (gig.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: "Only the gig owner can view bids" });
    }
    const bids = await Bid.find({ gig: gig._id })
      .populate("bidder", "name rating ratingCount college gigsCompleted")
      .sort({ amount: 1 });
    res.json(bids);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route PUT /api/gigs/:id/select/:bidId  (poster picks a bidder)
router.put("/:id/select/:bidId", protect, async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id);
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    if (gig.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: "Only the gig owner can select a bid" });
    }
    if (gig.status !== "open") {
      return res.status(400).json({ message: "Gig is already assigned or closed" });
    }

    const bid = await Bid.findById(req.params.bidId);
    if (!bid || bid.gig.toString() !== gig._id.toString()) {
      return res.status(404).json({ message: "Bid not found for this gig" });
    }

    gig.status = "assigned";
    gig.assignedTo = bid.bidder;
    await gig.save();

    bid.status = "accepted";
    await bid.save();
    await Bid.updateMany(
      { gig: gig._id, _id: { $ne: bid._id } },
      { status: "rejected" }
    );

    res.json(gig);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route PUT /api/gigs/:id/complete  (poster marks gig completed + rates worker)
router.put("/:id/complete", protect, async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id);
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    if (gig.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: "Only the gig owner can complete this gig" });
    }
    if (gig.status !== "assigned") {
      return res.status(400).json({ message: "Gig must be assigned before completion" });
    }

    gig.status = "completed";
    await gig.save();

    const { rating } = req.body; // optional 1-5
    if (gig.assignedTo && rating) {
      const worker = await User.findById(gig.assignedTo);
      const totalPoints = worker.rating * worker.ratingCount + Number(rating);
      worker.ratingCount += 1;
      worker.rating = Number((totalPoints / worker.ratingCount).toFixed(2));
      worker.gigsCompleted += 1;
      await worker.save();
    }

    res.json(gig);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// @route DELETE /api/gigs/:id  (poster cancels an open gig)
router.delete("/:id", protect, async (req, res) => {
  try {
    const gig = await Gig.findById(req.params.id);
    if (!gig) return res.status(404).json({ message: "Gig not found" });
    if (gig.postedBy.toString() !== req.user._id.toString()) {
      return res.status(403).json({ message: "Only the gig owner can cancel this gig" });
    }
    gig.status = "cancelled";
    await gig.save();
    res.json({ message: "Gig cancelled" });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

export default router;
