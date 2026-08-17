# GigBoard — Campus Micro-Gig Board

A full-stack MERN application built as a summer internship project. GigBoard is a
mini "Fiverr for college" where students can post small paid tasks (gigs) —
help shifting a hostel room, poster design, assignment help, tutoring, etc. —
and other students can bid on them. The poster reviews bids and picks one
person to do the work.
testing
Themed and seeded with sample data for **SKIT, Jagatpura, Jaipur**, but the
category/location lists in `frontend/src/constants.js` can be edited for any
college or city in five minutes.

---

## 1. Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | React 18 (Vite), React Router, Axios, plain CSS |
| Backend   | Node.js, Express |
| Database  | MongoDB (Mongoose) |
| Auth      | JWT (JSON Web Tokens) + bcrypt password hashing |
| Deploy    | Frontend → Vercel/Netlify · Backend → Render/Railway · DB → MongoDB Atlas |

## 2. Core Features

- Register/login with JWT auth (role is implicit: anyone can post gigs **and**
  bid on others' gigs — this is what makes it "multi-role" without needing a
  separate admin panel).
- Post a gig: title, description, category, budget (₹), Jaipur-area location,
  deadline.
- Browse/search/filter open gigs by category, location, keyword.
- Place a bid with an amount + message (one bid per user per gig).
- Poster views all bids on their gig and **selects a winner** → gig status
  becomes `assigned`, other bids auto-rejected.
- Poster marks the gig `completed` and rates the worker (1–5 stars) → feeds
  into the worker's profile rating.
- "My Gigs" (posted / working on) and "My Bids" dashboards.
- Editable profile with skills, bio, course, year, rating, gigs completed.

## 3. Project Structure

```
gigboard/
├── backend/
│   ├── config/db.js          MongoDB connection
│   ├── models/                User.js, Gig.js, Bid.js (Mongoose schemas)
│   ├── middleware/auth.js     JWT verification middleware
│   ├── routes/                auth.js, gigs.js, bids.js
│   ├── seed.js                 Sample SKIT/Jaipur data loader
│   ├── server.js               Express app entry point
│   └── package.json
└── frontend/
    ├── src/
    │   ├── pages/              Home, Login, Register, PostGig, GigDetail,
    │   │                       MyGigs, MyBids, Profile
    │   ├── components/         Navbar, GigCard, ProtectedRoute
    │   ├── context/AuthContext.jsx
    │   ├── api.js               Axios instance with JWT interceptor
    │   ├── constants.js         Categories & Jaipur locations (edit here)
    │   └── styles.css
    └── package.json
```

## 4. Running Locally

### Prerequisites
- Node.js 18+ installed
- A MongoDB connection string — easiest is a **free MongoDB Atlas cluster**
  (see step 6 below), or a local MongoDB install.

### Backend
```bash
cd backend
npm install
cp .env.example .env
# edit .env and paste your MONGO_URI + a random JWT_SECRET
npm run seed     # optional: loads sample SKIT/Jaipur gigs + demo users
npm run dev      # starts on http://localhost:5000
```

Demo login after seeding: `aarav.sharma@skit.ac.in` / `password123`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# VITE_API_URL should point to your backend, e.g. http://localhost:5000/api
npm run dev       # starts on http://localhost:5173
```

Open `http://localhost:5173` in your browser.

## 5. Environment Variables

**backend/.env**
```
PORT=5000
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/gigboard
JWT_SECRET=some_long_random_string
CLIENT_URL=http://localhost:5173
```

**frontend/.env**
```
VITE_API_URL=http://localhost:5000/api
```

## 6. Deployment (all free-tier friendly)

### Step A — Database: MongoDB Atlas
1. Go to mongodb.com/atlas and create a free account.
2. Create a free M0 cluster (any region, AWS Mumbai `ap-south-1` is closest
   to Jaipur if given a choice).
3. Under **Database Access**, create a user + password.
4. Under **Network Access**, add IP `0.0.0.0/0` (allow from anywhere — fine
   for a college project).
5. Click **Connect → Drivers**, copy the connection string, and replace
   `<password>` with your DB user's password. This is your `MONGO_URI`.

### Step B — Backend: Render
1. Push this project to a GitHub repo.
2. Go to render.com → New → Web Service → connect your repo.
3. Root directory: `backend`
4. Build command: `npm install`
5. Start command: `npm start`
6. Add environment variables: `MONGO_URI`, `JWT_SECRET`, `CLIENT_URL`
   (set `CLIENT_URL` after you deploy the frontend and know its URL).
7. Deploy. Note the live URL, e.g. `https://gigboard-api.onrender.com`.
8. Optionally run the seed script once from Render's Shell tab: `npm run seed`.

*(Railway.app works the same way if you prefer it over Render.)*

### Step C — Frontend: Vercel
1. Go to vercel.com → New Project → import the same GitHub repo.
2. Root directory: `frontend`
3. Framework preset: Vite (auto-detected)
4. Add environment variable: `VITE_API_URL` = `https://gigboard-api.onrender.com/api`
5. Deploy. You'll get a URL like `https://gigboard-skit.vercel.app`.
6. Go back to Render, set `CLIENT_URL` to this Vercel URL, and redeploy the
   backend so CORS allows it.

*(Netlify works the same way if you prefer it over Vercel.)*

### Step D — Verify
Visit your Vercel URL, register a new account, post a gig, and confirm it
appears. Check Render logs and Atlas's "Collections" tab if anything looks off.

## 7. Ideas for Extending (good for viva/Q&A questions)

- Add image upload for gigs (e.g. Cloudinary) so posters can attach photos.
- Real-time notifications (Socket.io) when a bid is placed or selected.
- In-app chat between poster and assigned worker.
- Payment integration (Razorpay test mode) to simulate escrow.
- Admin panel to moderate flagged gigs.
- Email/SMS deadline reminders.

## 8. Presenting This Project

Suggested narrative for your college presentation:
1. **Problem**: students informally ask for help on WhatsApp groups with no
   structure, no way to compare offers, no accountability.
2. **Solution**: a lightweight, localized micro-gig marketplace.
3. **Architecture**: React SPA ↔ REST API (Express) ↔ MongoDB, JWT auth.
4. **Live demo flow**: register → post a gig → (second account) bid on it →
   select a bid → mark complete → rating shows on profile.
5. **What you learned**: REST API design, JWT auth flow, MongoDB schema
   design (referencing collections with `ObjectId`), React state/context,
   protected routing, deployment pipeline.
