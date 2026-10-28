# GigBoard — Campus Micro-Gig Board (DevOps-2026-CS-F-17)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/tests-17%20passed-success.svg)]()
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)]()
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange.svg)]()
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800.svg)]()
[![Institution](https://img.shields.io/badge/SKIT-Jaipur-002147.svg)]()

A full-stack MERN application built as an academic internship and DevOps project for **Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur (SKIT)**. GigBoard is a localized campus micro-gig marketplace where students post tasks (room shifting, design, tutoring, assignment notes) and peer students submit bids.

---

## 1. Project Visualizations & Monitoring Dashboards

### A. Grafana — NodeJS Application Dashboard
Real-time containerized telemetry visualizing **Process CPU Usage**, **Event Loop Lag**, **Node.js Runtime Version**, **Process Restart Times**, **Memory & Heap Allocation Details**, and **Active Handlers / Requests Total**:

![Grafana NodeJS Application Dashboard](assets/grafana_dashboard.png)

* **Dashboard URL**: `http://localhost:3001` (User: `admin`, Password: `admin`)
* **Dashboard JSON Definition**: [`grafana/provisioning/dashboards/nodejs_dashboard.json`](grafana/provisioning/dashboards/nodejs_dashboard.json)
* **Automated Provisioning**: Pre-configured in Docker Compose to mount and auto-load upon container start.

---

### B. Prometheus — Scraper & Target Health
Scraping raw application metrics from the backend exporter endpoint (`/metrics`) every **5 seconds** under job `my-own-website`:

![Prometheus Target Health](assets/prometheus_targets.png)

* **Prometheus UI**: `http://localhost:9091/targets`
* **Exposition Endpoint**: `http://localhost:5000/metrics`
* **Configuration**: [`prometheus.yml`](prometheus.yml)

---

### C. Project Evaluation Trends & Volume
Visual distribution of commit activity and net code contribution generated across the project lifecycle:

![Git Commit Trends & LOC Volume](assets/evaluation_trends.png)

---

## 2. Student Contribution Breakdown

| Student Name | Commits (%) | Lines Added | Lines Deleted | Net LOC | Active Days | Role / Contributions |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **vanshitagr** | 33 (54.1%) | +25,840 | -3,420 | 22,420 | 18 days | Frontend architecture, Auth flows, CI/CD Jenkinsfile, Docker packaging, Grafana setup |
| **Utkarsh Hinger** | 28 (45.9%) | +18,920 | -2,150 | 16,770 | 14 days | Backend API endpoints, Mongoose models, Rate limiting, Request logging, Prometheus exporter |

* **Full Final Report**: [Devops-2026-CS-F-17_Final_Report_2026-10-29.pdf](Devops-2026-CS-F-17_Final_Report_2026-10-29.pdf)

---

## 3. Weekly Progress Reports Archive (Form-3)

Weekly progress reports automatically generated via ReportLab and Matplotlib, tracking week-by-week sprint deliverables:

| Week # | Report Window / Milestone Date | Status | Downloadable Form-3 PDF |
|:---:|:---:|:---:|:---:|
| **Week 1** | August 31, 2026 | Archived | [Form-3 Report (2026-08-31)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-08-31.pdf) |
| **Week 2** | September 05, 2026 | Archived | [Form-3 Report (2026-09-05)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-05.pdf) |
| **Week 3** | September 12, 2026 | Archived | [Form-3 Report (2026-09-12)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-12.pdf) |
| **Week 4** | September 19, 2026 | Archived | [Form-3 Report (2026-09-19)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-19.pdf) |
| **Week 5** | September 26, 2026 | Archived | [Form-3 Report (2026-09-26)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-26.pdf) |
| **Week 6** | September 27, 2026 | Archived | [Form-3 Report (2026-09-27)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-27.pdf) |
| **Week 7** | October 03, 2026 | Archived | [Form-3 Report (2026-10-03)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-03.pdf) |
| **Week 8** | October 10, 2026 | Archived | [Form-3 Report (2026-10-10)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-10.pdf) |
| **Week 9** | October 17, 2026 | Archived | [Form-3 Report (2026-10-17)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-17.pdf) |
| **Week 10** | October 24, 2026 | Archived | [Form-3 Report (2026-10-24)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-24.pdf) |
| **Week 11** | October 28, 2026 | Archived | [Form-3 Report (2026-10-28)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-28.pdf) |

---

## 4. Tech Stack & Architecture

| Layer | Technology |
|---|---|
| **Frontend** | React 18 (Vite), React Router v6, Axios, Custom CSS Modules |
| **Backend** | Node.js, Express, `prom-client` (Prometheus metrics) |
| **Database** | MongoDB & Mongoose ORM |
| **Authentication** | JWT (JSON Web Tokens) with bcrypt password salting |
| **Containerization** | Docker, Docker Compose, Nginx multi-stage builds |
| **Monitoring** | Prometheus v2.x, Grafana v10.x |
| **CI/CD** | Jenkins Automation Pipeline (`Jenkinsfile`), GitHub Actions |
| **Reporting** | Python 3, ReportLab, Matplotlib |

---

## 5. Running the Project

### A. Quick Start via Docker Compose (Recommended)
Spins up Backend, Frontend, Prometheus, and Grafana in a single command:
```bash
docker compose up --build -d
```
* **Frontend**: `http://localhost:3000`
* **Backend API**: `http://localhost:5000`
* **Prometheus Targets**: `http://localhost:9091/targets`
* **Grafana Dashboard**: `http://localhost:3001` (User: `admin` / Password: `admin`)

---

### B. Running Locally (Development Mode)

#### 1. Backend Setup
```bash
cd backend
npm install
cp .env.example .env
npm run seed       # loads demo users & campus gigs
npm run test:ci    # runs 12 backend unit tests with JUnit output
npm run dev        # starts backend on http://localhost:5000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run test:ci    # runs 5 frontend unit tests with JUnit output
npm run dev        # starts frontend on http://localhost:5173
```

---

### C. Regenerating PDF Progress Reports
```bash
# Generate the complete Final Evaluation Report:
python generate_report.py final

# Generate all past weekly Form-3 progress reports:
python generate_report.py all-weekly
```
Weekly reports are also automatically generated and committed via GitHub Actions on every Saturday (`.github/workflows/auto_weekly_report.yml`).
