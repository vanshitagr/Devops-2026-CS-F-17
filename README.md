# GigBoard — Campus Micro-Gig Board (DevOps-2026-CS-F-17)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/vanshitagr/Devops-2026-CS-F-17)
[![Tests](https://img.shields.io/badge/tests-22%20passed-success.svg)](https://github.com/vanshitagr/Devops-2026-CS-F-17/tree/main/backend/test)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://github.com/vanshitagr/Devops-2026-CS-F-17/blob/main/docker-compose.yml)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange.svg)](https://github.com/vanshitagr/Devops-2026-CS-F-17/blob/main/prometheus.yml)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800.svg)](https://github.com/vanshitagr/Devops-2026-CS-F-17/blob/main/grafana/provisioning/dashboards/nodejs_dashboard.json)
[![Institution](https://img.shields.io/badge/SKIT-Jaipur-002147.svg)](https://skit.ac.in)

A full-stack MERN application built as an academic internship and DevOps project for **Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur (SKIT)**. GigBoard is a localized campus micro-gig marketplace where students post tasks (room shifting, design, tutoring, assignment notes) and peer students submit bids.

---

## 1. Project Visualizations & Monitoring Dashboards

### A. Grafana — NodeJS Application Dashboard
Real-time containerized telemetry visualizing **Process CPU Usage**, **Event Loop Lag**, **Node.js Runtime Version**, **Process Restart Times**, **Memory & Heap Allocation Details**, and **Active Handlers / Requests Total**:

![Grafana NodeJS Application Dashboard](assets/grafana_dashboard.png)

- **Dashboard URL**: `http://localhost:3001` (User: `admin`, Password: `admin`)
- **Dashboard JSON**: [`grafana/provisioning/dashboards/nodejs_dashboard.json`](grafana/provisioning/dashboards/nodejs_dashboard.json)
- **Auto-Provisioning**: Pre-configured in Docker Compose to mount and auto-load upon container start.

---

### B. Prometheus — Scraper, Target Health & Alerting
Scraping raw application metrics from the backend exporter endpoint (`/metrics`) every **5 seconds** under job `gigboard-backend`:

![Prometheus Target Health](assets/prometheus_targets.png)

- **Prometheus UI**: `http://localhost:9091/targets`
- **Exposition Endpoint**: `http://localhost:5000/metrics`
- **Configuration**: [`prometheus.yml`](prometheus.yml)
- **Alerting Rules**: [`alerting_rules.yml`](alerting_rules.yml) — `ServiceDown`, `HighCpuUsage`, `EventLoopLagHigh`, `NodeMemoryHigh`

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

- **Full Final Report (PDF)**: [Devops-2026-CS-F-17_Final_Report_2026-10-28.pdf](Devops-2026-CS-F-17_Final_Report_2026-10-28.pdf)

---

## 3. Sprint Milestone Progress Reports (Form-3)

Comprehensive Form-3 progress evaluation reports tracking development milestones. Both collaborators' contributions are captured in each sprint. **Click any image to download the full PDF.**

---

### Sprint 1 — Architecture & Foundation (Aug 24 – Sep 05, 2026)

[![Sprint 1 Form-3 Report](assets/report_previews/Sprint_1_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Sprint_1_Progress_Report_Form-3.pdf)

---

### Sprint 2 — Auth, Security & Middleware (Sep 06 – Sep 19, 2026)

[![Sprint 2 Form-3 Report](assets/report_previews/Sprint_2_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Sprint_2_Progress_Report_Form-3.pdf)

---

### Sprint 3 — Backend APIs & DB Resilience (Sep 20 – Oct 05, 2026)

[![Sprint 3 Form-3 Report](assets/report_previews/Sprint_3_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Sprint_3_Progress_Report_Form-3.pdf)

---

### Sprint 4 — Full-Stack Integration & Testing (Oct 06 – Oct 20, 2026)

[![Sprint 4 Form-3 Report](assets/report_previews/Sprint_4_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Sprint_4_Progress_Report_Form-3.pdf)

---

### Sprint 5 — DevOps, CI/CD & Monitoring (Oct 21 – Oct 29, 2026)

[![Sprint 5 Form-3 Report](assets/report_previews/Sprint_5_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Sprint_5_Progress_Report_Form-3.pdf)

---

## 4. Weekly Calendar Progress Reports Archive (Form-3)

Weekly progress reports tracking calendar weeks. All reports show both team members' contributions. **Click any image to download the full PDF.**

---

### Week 1 — August 31, 2026

[![Week 1 Form-3 Report](assets/report_previews/Weekly_2026-08-31_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-08-31.pdf)

---

### Week 2 — September 05, 2026

[![Week 2 Form-3 Report](assets/report_previews/Weekly_2026-09-05_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-05.pdf)

---

### Week 3 — September 12, 2026

[![Week 3 Form-3 Report](assets/report_previews/Weekly_2026-09-12_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-12.pdf)

---

### Week 4 — September 19, 2026

[![Week 4 Form-3 Report](assets/report_previews/Weekly_2026-09-19_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-19.pdf)

---

### Week 5 — September 26, 2026

[![Week 5 Form-3 Report](assets/report_previews/Weekly_2026-09-26_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-26.pdf)

---

### Week 6 — September 27, 2026

[![Week 6 Form-3 Report](assets/report_previews/Weekly_2026-09-27_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-09-27.pdf)

---

### Week 7 — October 03, 2026

[![Week 7 Form-3 Report](assets/report_previews/Weekly_2026-10-03_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-03.pdf)

---

### Week 8 — October 10, 2026

[![Week 8 Form-3 Report](assets/report_previews/Weekly_2026-10-10_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-10.pdf)

---

### Week 9 — October 17, 2026

[![Week 9 Form-3 Report](assets/report_previews/Weekly_2026-10-17_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-17.pdf)

---

### Week 10 — October 24, 2026

[![Week 10 Form-3 Report](assets/report_previews/Weekly_2026-10-24_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-24.pdf)

---

### Week 11 — October 28, 2026

[![Week 11 Form-3 Report](assets/report_previews/Weekly_2026-10-28_Form3.png)](weekly_reports/Devops-2026-CS-F-17_Weekly_Progress_Report_Form-3_2026-10-28.pdf)

---

## 5. Tech Stack & Architecture

| Layer | Technology |
|---|---|
| **Frontend** | React 18 (Vite), React Router v6, Axios, Custom CSS Modules |
| **Backend** | Node.js, Express, `prom-client` (Prometheus metrics exporter) |
| **Database** | MongoDB & Mongoose ORM |
| **Authentication** | JWT (JSON Web Tokens) with bcrypt password salting |
| **Containerization** | Docker, Docker Compose, Nginx multi-stage builds |
| **Monitoring & Alerting** | Prometheus v2.x, Grafana v10.x, Alerting rules |
| **CI/CD** | Jenkins Automation Pipeline (`Jenkinsfile`) |
| **Reporting** | Python 3, ReportLab, Matplotlib |

---

## 6. Running the Project

### A. Quick Start via Docker Compose (Recommended)
Spins up Backend, Frontend, Prometheus, and Grafana in a single command:
```bash
docker compose up --build -d
```
| Service | URL |
|---|---|
| **Frontend** | `http://localhost:3000` |
| **Backend API** | `http://localhost:5000` |
| **Prometheus Targets** | `http://localhost:9091/targets` |
| **Grafana Dashboard** | `http://localhost:3001` (admin / admin) |

---

### B. Running Locally (Development Mode)

#### 1. Backend Setup
```bash
cd backend
npm install
cp .env.example .env
npm run test:ci    # 22 backend unit/integration tests
npm run dev        # starts on http://localhost:5000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run test:ci    # 5 frontend unit tests
npm run dev        # starts on http://localhost:5173
```

---

### C. Regenerating Reports
```bash
# Complete Final Evaluation Report:
python generate_report.py final

# All Sprint Milestone Form-3 reports:
python generate_report.py all-sprints

# Report preview PNG images:
python scripts/generate_report_previews.py
```
