import mongoose from "mongoose";

const bidSchema = new mongoose.Schema(
  {
    gig: { type: mongoose.Schema.Types.ObjectId, ref: "Gig", required: true },
    bidder: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    amount: { type: Number, required: true, min: 0 },
    message: { type: String, required: true },
    status: {
      type: String,
      enum: ["pending", "accepted", "rejected"],
      default: "pending",
    },
  },
  { timestamps: true }
);

// A user can only bid once per gig
bidSchema.index({ gig: 1, bidder: 1 }, { unique: true });

export default mongoose.model("Bid", bidSchema);
