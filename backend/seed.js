// Run with: npm run seed
// Populates the database with sample SKIT Jagatpura / Jaipur themed data.
import dotenv from "dotenv";
import connectDB from "./config/db.js";
import User from "./models/User.js";
import Gig from "./models/Gig.js";
import Bid from "./models/Bid.js";

dotenv.config();

const sampleUsers = [
  {
    name: "Aarav Sharma",
    email: "aarav.sharma@skit.ac.in",
    password: "password123",
    course: "B.Tech CSE",
    year: "3rd Year",
    phone: "9829000001",
    bio: "Frontend dev, into React and UI design.",
    skills: ["React", "Figma", "Tailwind"],
  },
  {
    name: "Priya Meena",
    email: "priya.meena@skit.ac.in",
    password: "password123",
    course: "B.Tech IT",
    year: "2nd Year",
    phone: "9829000002",
    bio: "Good with Canva/Photoshop, posters and event banners.",
    skills: ["Poster Design", "Canva", "Photoshop"],
  },
  {
    name: "Rohit Choudhary",
    email: "rohit.choudhary@skit.ac.in",
    password: "password123",
    course: "B.Tech ECE",
    year: "4th Year",
    phone: "9829000003",
    bio: "Have a bike, happy to help with campus errands and moving stuff.",
    skills: ["Delivery", "Logistics"],
  },
  {
    name: "Simran Kanwar",
    email: "simran.kanwar@skit.ac.in",
    password: "password123",
    course: "B.Tech CSE",
    year: "3rd Year",
    phone: "9829000004",
    bio: "DSA and coding assignment help, competitive programming.",
    skills: ["DSA", "C++", "Python"],
  },
];

const seed = async () => {
  await connectDB();
  console.log("Clearing existing data...");
  await User.deleteMany();
  await Gig.deleteMany();
  await Bid.deleteMany();

  console.log("Creating users...");
  const users = [];
  for (const u of sampleUsers) {
    const created = await User.create(u);
    users.push(created);
  }

  const [aarav, priya, rohit, simran] = users;

  console.log("Creating gigs...");
  const gigs = await Gig.insertMany([
    {
      title: "Help shifting hostel room - 2nd to 4th floor",
      description:
        "Need 2 people to help carry boxes, a study table and a mattress from Boys Hostel Block B to Block D at SKIT campus. Should take under 2 hours.",
      category: "Moving & Shifting Help",
      budget: 300,
      location: "SKIT Campus, Jagatpura",
      deadline: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
      postedBy: aarav._id,
    },
    {
      title: "Design a poster for Tech Fest 'Innovate 2026'",
      description:
        "Need an A2 size poster for our department tech fest. Theme: futuristic/AI. Should include SKIT logo and event details (will share).",
      category: "Design & Poster Making",
      budget: 500,
      location: "SKIT Campus, Jagatpura",
      deadline: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
      postedBy: rohit._id,
    },
    {
      title: "DSA assignment help - Trees & Graphs",
      description:
        "Need help solving 10 problems on trees and graphs (C++), with explanations so I can understand for viva, not just copy-paste.",
      category: "Notes & Assignment Help",
      budget: 250,
      location: "Jagatpura",
      deadline: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
      postedBy: priya._id,
    },
    {
      title: "Fix bugs in my React mini-project before submission",
      description:
        "My React app has routing issues and a form validation bug. Need someone to debug and fix before Friday submission.",
      category: "Tech & Coding Help",
      budget: 400,
      location: "SKIT Campus, Jagatpura",
      deadline: new Date(Date.now() + 4 * 24 * 60 * 60 * 1000),
      postedBy: simran._id,
    },
    {
      title: "Volunteers needed for college cultural fest registration desk",
      description:
        "Need 3 volunteers for the registration desk on fest day, 9am - 5pm. Food and fest T-shirt provided.",
      category: "Event Volunteering",
      budget: 200,
      location: "SKIT Campus, Jagatpura",
      deadline: new Date(Date.now() + 6 * 24 * 60 * 60 * 1000),
      postedBy: aarav._id,
    },
    {
      title: "Pick up parcel from Malviya Nagar and drop at Jagatpura hostel",
      description:
        "A courier is stuck at a Malviya Nagar pickup point, need someone with a bike to collect and drop it at my hostel by evening.",
      category: "Errands & Delivery",
      budget: 150,
      location: "Malviya Nagar",
      deadline: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000),
      postedBy: priya._id,
    },
    {
      title: "Photography for pre-wedding style farewell shoot",
      description:
        "Need someone with a decent DSLR/phone camera skills to shoot photos for our farewell party at a Vaishali Nagar banquet hall.",
      category: "Photography/Videography",
      budget: 800,
      location: "Vaishali Nagar",
      deadline: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000),
      postedBy: rohit._id,
    },
    {
      title: "1-on-1 tutoring for Engineering Maths 2 before exam",
      description:
        "Need 3 sessions of Laplace transforms and Fourier series explained, exam is next week.",
      category: "Tutoring",
      budget: 600,
      location: "Pratap Nagar",
      deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      postedBy: simran._id,
    },
  ]);

  console.log("Creating a couple of sample bids...");
  await Bid.create([
    {
      gig: gigs[0]._id,
      bidder: simran._id,
      amount: 280,
      message: "I stay in Block D itself, can help right away this evening.",
    },
    {
      gig: gigs[2]._id,
      bidder: aarav._id,
      amount: 250,
      message: "I've done trees & graphs recently, can explain with diagrams.",
    },
  ]);

  console.log("Seed complete!");
  console.log("Sample login -> email: aarav.sharma@skit.ac.in | password: password123");
  process.exit();
};

seed().catch((err) => {
  console.error(err);
  process.exit(1);
});
