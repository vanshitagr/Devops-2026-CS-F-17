import mongoose from "mongoose";

const gigSchema = new mongoose.Schema(
  {
    title: { type: String, required: true, trim: true },
    description: { type: String, required: true },
    category: {
      type: String,
      required: true,
      enum: [
        "Moving & Shifting Help",
        "Design & Poster Making",
        "Notes & Assignment Help",
        "Tech & Coding Help",
        "Event Volunteering",
        "Tutoring",
        "Photography/Videography",
        "Errands & Delivery",
        "Other",
      ],
    },
    budget: { type: Number, required: true, min: 0 },
    location: {
      type: String,
      required: true,
      enum: [
        "SKIT Campus, Jagatpura",
        "Jagatpura",
        "Malviya Nagar",
        "Pratap Nagar",
        "Sanganer",
        "Vaishali Nagar",
        "C-Scheme",
        "Mansarovar",
        "Tonk Road",
        "Other (Jaipur)",
      ],
    },
    deadline: { type: Date, required: true },
    status: {
      type: String,
      enum: ["open", "assigned", "completed", "cancelled"],
      default: "open",
    },
    postedBy: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
    assignedTo: { type: mongoose.Schema.Types.ObjectId, ref: "User", default: null },
  },
  { timestamps: true }
);

export default mongoose.model("Gig", gigSchema);
