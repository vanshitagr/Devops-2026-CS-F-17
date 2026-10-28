# GigBoard — Campus Micro-Gig Board

A full-stack MERN application built as a summer internship and DevOps project. GigBoard is a mini "Fiverr for college" where students can post small paid tasks (gigs) — help shifting a hostel room, poster design, assignment help, tutoring, etc. — and other students can bid on them. The poster reviews bids and picks one person to do the work.

Themed and seeded with sample data for **SKIT, Jagatpura, Jaipur**, but the category/location lists in `frontend/src/constants.js` can be edited for any college or city in five minutes.

---

## 1. Tech Stack

| Layer     | Technology |
|-----------|------------|
| Frontend  | React 18 (Vite), React Router, Axios, plain CSS |
| Backend   | Node.js, Express, prom-client |
| Database  | MongoDB (Mongoose) |
| Auth      | JWT (JSON Web Tokens) + bcrypt password hashing |
| DevOps    | Docker & Docker Compose, Prometheus, Grafana, Jenkins CI/CD, GitHub Actions |
| Reports   | Python (ReportLab & Matplotlib) automated Form-3 and Final PDF Evaluation |

---

## 2. Core Features

- Register/login with JWT auth.
- Post a gig: title, description, category, budget (₹), Jaipur-area location, deadline.
- Browse/search/filter open gigs by category, location, keyword.
- Place a bid with an amount + message.
- Poster reviews bids and selects a winner → status becomes `assigned`.
- Poster marks gig `completed` and rates worker (1–5 stars) → updates worker profile.
- Real-time Prometheus metrics exporter at `/metrics` and Grafana NodeJS Application Dashboard.
- Automated Git evaluation reports (Weekly Form-3 and Final Project Evaluation Report).

---

## 3. DevOps, Monitoring & Containerization

### A. Prometheus & Grafana Monitoring
- **Prometheus Scraper**: Exposes Node.js runtime and application metrics on `/metrics` using `prom-client`.
- **Target Configuration**: Configured in `prometheus.yml` under job name `my-own-website` with 5s scrape interval.
- **Grafana Dashboard**: Visualizes Process CPU Usage, Event Loop Lag, Memory & Heap details, and Active Handlers.
- **Accessing Monitoring Services**:
  - Prometheus Web UI: `http://localhost:9091`
  - Grafana Dashboard: `http://localhost:3001` (User: `admin`, Password: `admin`)
  - Backend Metrics: `http://localhost:5000/metrics`

### B. Docker Compose Stack
To spin up the entire multi-container environment (Backend, Frontend, Prometheus, Grafana):
```bash
docker compose up --build -d
```

### C. Automated Git Evaluation & Weekly Progress Reports
Generate professional evaluation reports with student contribution breakdowns, commit timelines, and Net LOC charts:
```bash
# Generate Final Project Evaluation Report:
python generate_report.py final

# Generate Weekly Progress Report (Form-3):
python generate_report.py weekly
```
Weekly reports are also auto-generated and archived every Saturday via GitHub Actions workflow (`.github/workflows/auto_weekly_report.yml`).

### D. Jenkins CI/CD Pipeline
- Structured declarative pipeline (`Jenkinsfile`) with stages:
  1. `Checkout`: Pulls latest branch code.
  2. `Check Feedback Commit`: Prevents recursive feedback loop commits.
  3. `Install Dependencies`: Installs packages for backend & frontend.
  4. `Run Tests`: Executes unit tests with JUnit XML export (`backend/test-results.xml`, `frontend/test-results.xml`).
  5. `Build Frontend`: Compiles Vite production bundle.
  6. `Docker Compose Validation`: Verifies container configuration.
  7. `Generate Feedback`: Outputs `feedback.txt` and updates feedback record.
  8. `Push Feedback to Main`: Automated feedback commit to repository.

---

## 4. Running Locally

### Backend
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your MONGO_URI and JWT_SECRET
npm run seed     # optional: loads demo SKIT users & gigs
npm run test     # runs unit test suite
npm run dev      # starts server on http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run test     # runs frontend unit tests
npm run dev      # starts on http://localhost:5173
```
