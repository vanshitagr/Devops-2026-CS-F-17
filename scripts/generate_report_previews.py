"""
Generate PNG preview images for all Form-3 weekly/sprint reports.
These render directly on GitHub README instead of unrenderable PDFs.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

os.makedirs('assets/report_previews', exist_ok=True)

COLLEGE = "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur (SKIT)"
DEPT    = "Department of Computer Science & Engineering"
SUBJECT = "DevOps – CSE (2026) | Team: CS-F-17"
MEMBERS = "vanshitagr  &  Utkarsh Hinger"

BG      = "#0d1117"
CARD    = "#161b22"
BORDER  = "#30363d"
GREEN   = "#3fb950"
BLUE    = "#58a6ff"
ORANGE  = "#f0883e"
WHITE   = "#e6edf3"
MUTED   = "#8b949e"
RED     = "#f85149"
PURPLE  = "#bc8cff"
YELLOW  = "#d29922"

SPRINT_DATA = [
    {
        "title": "Sprint 1 – Architecture & Foundation",
        "window": "Aug 24, 2026  →  Sep 05, 2026",
        "focus": "Project setup, MongoDB schemas (User, Gig, Bid),\nReact UI foundation, Auth flows & routing",
        "commits_v": 6, "commits_u": 6, "total": 12,
        "days": 9,
        "vanshita_work": ["Project scaffold & folder structure", "React Router v6 setup", "Frontend Auth pages (Login/Register)", "MongoDB Atlas connection", "Initial Mongoose User schema"],
        "utkarsh_work":  ["Gig & Bid schema design", "Express route stubs", "bcrypt password hashing", "JWT token generation", "Postman API testing"],
        "status": "COMPLETED",
    },
    {
        "title": "Sprint 2 – Auth, Security & Middleware",
        "window": "Sep 06, 2026  →  Sep 19, 2026",
        "focus": "JWT authentication, request validation, rate limiting,\ncustom error handling & middleware chain",
        "commits_v": 10, "commits_u": 8, "total": 18,
        "days": 7,
        "vanshita_work": ["Axios interceptors with token refresh", "Protected route HOC", "JWT decode & storage", "Frontend form validation (Yup)", "Responsive CSS modules"],
        "utkarsh_work":  ["Rate limiter middleware (express-rate-limit)", "Request ID middleware", "Request logger middleware", "validateRequest schema guard", "Global error handler"],
        "status": "COMPLETED",
    },
    {
        "title": "Sprint 3 – Backend APIs & DB Resilience",
        "window": "Sep 20, 2026  →  Oct 05, 2026",
        "focus": "Gig CRUD, Bid workflows, Health check APIs,\ndatabase error recovery & edge case handling",
        "commits_v": 9, "commits_u": 14, "total": 23,
        "days": 6,
        "vanshita_work": ["Gig listing page with filters", "Bid submission UI flow", "Profile page & bid history", "Frontend error boundaries", "Loading state skeletons"],
        "utkarsh_work":  ["GET /gigs, POST /gigs endpoints", "POST /bids, GET /bids/:gigId", "GET /health, GET /api-info", "Mongoose retry logic on disconnect", "Unit test scaffolding (Jest)"],
        "status": "COMPLETED",
    },
    {
        "title": "Sprint 4 – Full-Stack Integration & Testing",
        "window": "Oct 06, 2026  →  Oct 20, 2026",
        "focus": "End-to-end integration, test coverage,\nedge cases & production hardening",
        "commits_v": 3, "commits_u": 0, "total": 3,
        "days": 3,
        "vanshita_work": ["API base URL configuration", "E2E flow: post gig → receive bid", "Nginx config for SPA routing"],
        "utkarsh_work":  ["Code review & PR merge", "—", "—"],
        "status": "COMPLETED",
    },
    {
        "title": "Sprint 5 – DevOps, CI/CD & Monitoring",
        "window": "Oct 21, 2026  →  Oct 29, 2026",
        "focus": "Docker Compose, Prometheus/Grafana integration,\nJenkins CI/CD pipeline & alerting rules",
        "commits_v": 5, "commits_u": 1, "total": 6,
        "days": 4,
        "vanshita_work": ["Docker multi-stage Dockerfile (frontend)", "docker-compose.yml (all 4 services)", "Grafana auto-provisioning dashboard JSON", "Jenkins pipeline (Jenkinsfile)", "Prometheus alerting_rules.yml"],
        "utkarsh_work":  ["prom-client metrics endpoint (/metrics)", "22 backend Jest tests", "—", "—", "—"],
        "status": "COMPLETED",
    },
]

WEEKLY_DATA = [
    {"week": "Week 1",  "date": "August 31, 2026",   "window": "Aug 24 – Aug 31", "commits_v": 3, "commits_u": 2, "total": 5,  "days": 4,
     "activities": ["GitHub repository initialized", "README scaffold & branch strategy defined", "MongoDB Atlas cluster provisioned", "Basic Express server created", "React Vite project bootstrapped"]},
    {"week": "Week 2",  "date": "September 05, 2026","window": "Sep 01 – Sep 05", "commits_v": 3, "commits_u": 4, "total": 7,  "days": 5,
     "activities": ["Mongoose User, Gig, Bid schemas finalized", "JWT auth routes (POST /login, POST /register)", "React Auth context & token storage", "bcrypt integration for password hashing", "Postman collection created & tested"]},
    {"week": "Week 3",  "date": "September 12, 2026","window": "Sep 06 – Sep 12", "commits_v": 5, "commits_u": 4, "total": 9,  "days": 5,
     "activities": ["Rate limiter middleware added", "Request ID & logger middleware integrated", "validateRequest middleware (Joi/Zod)", "Frontend protected routes via HOC", "Axios interceptors with 401 handling"]},
    {"week": "Week 4",  "date": "September 19, 2026","window": "Sep 13 – Sep 19", "commits_v": 5, "commits_u": 4, "total": 9,  "days": 4,
     "activities": ["Global error handler finalized", "GET /gigs & POST /gigs API endpoints", "POST /bids & GET /bids/:gigId implemented", "React Gig listing page with search filters", "Bid submission modal UI completed"]},
    {"week": "Week 5",  "date": "September 26, 2026","window": "Sep 20 – Sep 26", "commits_v": 4, "commits_u": 7, "total": 11, "days": 5,
     "activities": ["MongoDB reconnect retry logic implemented", "GET /health & GET /api-info endpoints", "Frontend profile page & bid history view", "Loading skeleton components added", "Frontend unit test stubs created"]},
    {"week": "Week 6",  "date": "September 27, 2026","window": "Sep 27", "commits_v": 1, "commits_u": 1, "total": 2,  "days": 1,
     "activities": ["Hotfix: CORS origin whitelist updated", "Hotfix: JWT expiry env variable corrected"]},
    {"week": "Week 7",  "date": "October 03, 2026",  "window": "Sep 28 – Oct 03", "commits_v": 3, "commits_u": 4, "total": 7,  "days": 4,
     "activities": ["End-to-end flow: post gig → receive bid → accept", "Frontend error boundary components", "Backend input sanitization", "Pagination added to GET /gigs", "PR review & merge of feature branches"]},
    {"week": "Week 8",  "date": "October 10, 2026",  "window": "Oct 04 – Oct 10", "commits_v": 2, "commits_u": 3, "total": 5,  "days": 3,
     "activities": ["Jest test suite: User auth tests (4 tests)", "Jest test suite: Gig API tests (5 tests)", "Jest test suite: Bid API tests (4 tests)", "Frontend Vitest: constants & format tests", "CI test run validated locally"]},
    {"week": "Week 9",  "date": "October 17, 2026",  "window": "Oct 11 – Oct 17", "commits_v": 3, "commits_u": 2, "total": 5,  "days": 3,
     "activities": ["Nginx SPA routing config finalized", "API base URL env config for Docker", "Remaining edge case test coverage", "Code cleanup & ESLint fixes", "Dev branch merged into main"]},
    {"week": "Week 10", "date": "October 24, 2026",  "window": "Oct 18 – Oct 24", "commits_v": 3, "commits_u": 0, "total": 3,  "days": 3,
     "activities": ["Docker multi-stage Dockerfile (frontend: Vite+Nginx)", "Backend Dockerfile (Node 20 Alpine)", "docker-compose.yml: backend, frontend, prometheus, grafana", ".dockerignore files added", "Docker Compose network: fsd-shared-network"]},
    {"week": "Week 11", "date": "October 28, 2026",  "window": "Oct 25 – Oct 28", "commits_v": 2, "commits_u": 1, "total": 3,  "days": 3,
     "activities": ["Prometheus scrape config (5s interval, /metrics)", "prom-client collectDefaultMetrics in backend", "Grafana auto-provisioned NodeJS dashboard JSON", "Prometheus alerting_rules.yml (4 alert rules)", "Jenkins CI/CD pipeline (Jenkinsfile) finalized"]},
]


def draw_form3_sprint(data, filename):
    fig = plt.figure(figsize=(16, 11), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_facecolor(BG)

    # Header band
    ax.add_patch(FancyBboxPatch((0.3, 9.7), 15.4, 1.1, boxstyle="round,pad=0.05",
                                 fc="#0d2137", ec=BLUE, lw=2))
    ax.text(8, 10.55, COLLEGE, ha='center', va='center', color=BLUE, fontsize=9, fontweight='bold')
    ax.text(8, 10.22, f"{DEPT}  |  {SUBJECT}", ha='center', va='center', color=MUTED, fontsize=8)
    ax.text(8, 9.88, "FORM-3: Progress Evaluation Report", ha='center', va='center',
            color=WHITE, fontsize=11, fontweight='bold')

    # Sprint title card
    ax.add_patch(FancyBboxPatch((0.3, 8.9), 15.4, 0.65, boxstyle="round,pad=0.04",
                                 fc="#1c2e1c", ec=GREEN, lw=1.5))
    ax.text(8, 9.35, data["title"], ha='center', va='center', color=GREEN, fontsize=13, fontweight='bold')
    ax.text(8, 9.05, f"Period: {data['window']}  |  Active Days: {data['days']}  |  Status: {data['status']}",
            ha='center', va='center', color=WHITE, fontsize=9)

    # Members
    ax.add_patch(FancyBboxPatch((0.3, 8.25), 15.4, 0.5, boxstyle="round,pad=0.04",
                                 fc=CARD, ec=BORDER, lw=1))
    ax.text(0.8, 8.5, "👥 Team Members:", color=MUTED, fontsize=9, va='center')
    ax.text(3.5, 8.5, "vanshitagr", color=ORANGE, fontsize=10, fontweight='bold', va='center')
    ax.text(5.5, 8.5, "&", color=MUTED, fontsize=9, va='center')
    ax.text(6.0, 8.5, "Utkarsh Hinger", color=PURPLE, fontsize=10, fontweight='bold', va='center')
    ax.text(10.0, 8.5, f"Total Commits This Sprint: ", color=MUTED, fontsize=9, va='center')
    ax.text(13.1, 8.5, str(data['total']), color=GREEN, fontsize=14, fontweight='bold', va='center')

    # Focus area
    ax.add_patch(FancyBboxPatch((0.3, 7.55), 15.4, 0.58, boxstyle="round,pad=0.04",
                                 fc="#1a1a2e", ec=PURPLE, lw=1))
    ax.text(0.7, 8.12, "📌 Sprint Focus:", color=MUTED, fontsize=9, va='center')
    ax.text(0.7, 7.78, data["focus"], color=WHITE, fontsize=9, va='center')

    # Commit bar chart (inline)
    ax_bar = fig.add_axes([0.03, 0.44, 0.28, 0.18], facecolor=CARD)
    bars = ax_bar.bar(['vanshitagr', 'Utkarsh\nHinger'], [data['commits_v'], data['commits_u']],
                       color=[ORANGE, PURPLE], zorder=3, width=0.5)
    ax_bar.set_facecolor(CARD)
    ax_bar.set_title("Commits", color=WHITE, fontsize=8, pad=4)
    ax_bar.tick_params(colors=MUTED, labelsize=7)
    ax_bar.spines[:].set_color(BORDER)
    ax_bar.yaxis.label.set_color(MUTED)
    ax_bar.set_ylim(0, max(data['commits_v'], data['commits_u'], 1) + 3)
    ax_bar.grid(axis='y', color=BORDER, alpha=0.5)
    for b in bars:
        ax_bar.text(b.get_x()+b.get_width()/2, b.get_height()+0.2, str(int(b.get_height())),
                    ha='center', color=WHITE, fontsize=9, fontweight='bold')

    # Contribution rings (pie)
    ax_pie = fig.add_axes([0.34, 0.44, 0.15, 0.18], facecolor=BG)
    total = data['commits_v'] + data['commits_u']
    if total > 0:
        ax_pie.pie([data['commits_v'], data['commits_u']], colors=[ORANGE, PURPLE],
                   startangle=90, wedgeprops=dict(width=0.5, edgecolor=BG))
    ax_pie.set_title(f"Share\n{data['commits_v']} vs {data['commits_u']}", color=WHITE, fontsize=7.5, pad=2)

    # Work breakdown - vanshitagr
    ax.add_patch(FancyBboxPatch((0.3, 2.2), 7.5, 4.95, boxstyle="round,pad=0.06",
                                 fc=CARD, ec=ORANGE, lw=1.5))
    ax.text(4.05, 6.95, "🔶 vanshitagr — Contributions", ha='center', color=ORANGE,
            fontsize=10, fontweight='bold')
    for i, item in enumerate(data['vanshita_work']):
        ax.text(0.65, 6.55 - i*0.72, f"✔  {item}", color=WHITE, fontsize=8.5, va='center')

    # Work breakdown - utkarsh
    ax.add_patch(FancyBboxPatch((8.2, 2.2), 7.5, 4.95, boxstyle="round,pad=0.06",
                                 fc=CARD, ec=PURPLE, lw=1.5))
    ax.text(11.95, 6.95, "🔷 Utkarsh Hinger — Contributions", ha='center', color=PURPLE,
            fontsize=10, fontweight='bold')
    for i, item in enumerate(data['utkarsh_work']):
        ax.text(8.5, 6.55 - i*0.72, f"✔  {item}", color=WHITE, fontsize=8.5, va='center')

    # Stats row
    ax.add_patch(FancyBboxPatch((0.3, 0.9), 15.4, 1.15, boxstyle="round,pad=0.05",
                                 fc="#0d1f2d", ec=BLUE, lw=1.5))
    stats = [
        ("Total Commits", str(data['total']), GREEN),
        ("vanshitagr", str(data['commits_v']), ORANGE),
        ("Utkarsh Hinger", str(data['commits_u']), PURPLE),
        ("Active Days", str(data['days']), BLUE),
        ("Status", data['status'], GREEN),
    ]
    for i, (label, val, col) in enumerate(stats):
        x0 = 0.8 + i * 3.1
        ax.text(x0+1.1, 1.73, val, ha='center', color=col, fontsize=16, fontweight='bold', va='center')
        ax.text(x0+1.1, 1.12, label, ha='center', color=MUTED, fontsize=8, va='center')

    # Footer
    ax.text(8, 0.5, f"DevOps-2026-CS-F-17  |  SKIT Jaipur  |  Generated: October 29, 2026",
            ha='center', color=MUTED, fontsize=7.5)

    plt.savefig(filename, dpi=130, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"Saved: {filename}")


def draw_form3_weekly(data, filename):
    fig = plt.figure(figsize=(16, 10), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(BG)

    # Header
    ax.add_patch(FancyBboxPatch((0.3, 8.8), 15.4, 1.0, boxstyle="round,pad=0.05",
                                 fc="#0d2137", ec=BLUE, lw=2))
    ax.text(8, 9.55, COLLEGE, ha='center', va='center', color=BLUE, fontsize=9, fontweight='bold')
    ax.text(8, 9.22, f"{DEPT}  |  {SUBJECT}", ha='center', va='center', color=MUTED, fontsize=8)
    ax.text(8, 8.92, "FORM-3: Weekly Progress Report", ha='center', va='center',
            color=WHITE, fontsize=11, fontweight='bold')

    # Week title
    ax.add_patch(FancyBboxPatch((0.3, 8.0), 15.4, 0.65, boxstyle="round,pad=0.04",
                                 fc="#1c2e1c", ec=GREEN, lw=1.5))
    ax.text(8, 8.45, f"{data['week']}  –  Milestone Date: {data['date']}", ha='center',
            color=GREEN, fontsize=13, fontweight='bold', va='center')
    ax.text(8, 8.12, f"Reporting Window: {data['window']}  |  Active Days: {data['days']}",
            ha='center', color=WHITE, fontsize=9, va='center')

    # Members row
    ax.add_patch(FancyBboxPatch((0.3, 7.38), 15.4, 0.48, boxstyle="round,pad=0.04",
                                 fc=CARD, ec=BORDER, lw=1))
    ax.text(0.8, 7.62, "👥 Team:", color=MUTED, fontsize=9, va='center')
    ax.text(2.2, 7.62, "vanshitagr", color=ORANGE, fontsize=10, fontweight='bold', va='center')
    ax.text(4.1, 7.62, "&  Utkarsh Hinger", color=PURPLE, fontsize=10, fontweight='bold', va='center')
    ax.text(9.5, 7.62, "Total Commits This Week:", color=MUTED, fontsize=9, va='center')
    ax.text(13.0, 7.62, str(data['total']), color=GREEN, fontsize=14, fontweight='bold', va='center')
    ax.text(13.7, 7.62, f"({data['commits_v']}+{data['commits_u']})", color=MUTED, fontsize=8, va='center')

    # Activities list
    ax.add_patch(FancyBboxPatch((0.3, 2.1), 15.4, 5.1, boxstyle="round,pad=0.06",
                                 fc=CARD, ec=BLUE, lw=1.5))
    ax.text(8, 6.98, "📋 Weekly Activities & Deliverables", ha='center', color=BLUE,
            fontsize=11, fontweight='bold')

    for i, act in enumerate(data['activities']):
        y = 6.45 - i * 0.8
        # bullet circle
        circ = plt.Circle((0.85, y), 0.13, color=GREEN, zorder=3)
        ax.add_patch(circ)
        ax.text(0.85, y, str(i+1), ha='center', va='center', color=BG, fontsize=7, fontweight='bold', zorder=4)
        ax.text(1.15, y, act, color=WHITE, fontsize=10, va='center')

    # Stats bar
    ax.add_patch(FancyBboxPatch((0.3, 0.85), 15.4, 1.1, boxstyle="round,pad=0.05",
                                 fc="#0d1f2d", ec=BLUE, lw=1.5))

    # Mini commit bar inside stats
    v_pct = int((data['commits_v'] / max(data['total'],1)) * 100)
    u_pct = 100 - v_pct

    stats = [
        ("Week", data['week'].split()[1], BLUE),
        ("vanshitagr Commits", str(data['commits_v']), ORANGE),
        ("Utkarsh Commits", str(data['commits_u']), PURPLE),
        ("Total Commits", str(data['total']), GREEN),
        ("Active Days", str(data['days']), YELLOW),
    ]
    for i, (label, val, col) in enumerate(stats):
        x0 = 0.8 + i * 3.1
        ax.text(x0+1.1, 1.6, val, ha='center', color=col, fontsize=15, fontweight='bold', va='center')
        ax.text(x0+1.1, 1.05, label, ha='center', color=MUTED, fontsize=8, va='center')

    # Footer
    ax.text(8, 0.45, f"DevOps-2026-CS-F-17  |  SKIT Jaipur  |  Generated: October 29, 2026",
            ha='center', color=MUTED, fontsize=7.5)

    plt.savefig(filename, dpi=130, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f"Saved: {filename}")


# Generate all sprint reports
for d in SPRINT_DATA:
    n = d['title'].split()[1]
    fname = f"assets/report_previews/Sprint_{n}_Form3.png"
    draw_form3_sprint(d, fname)

# Generate all weekly reports
date_map = {
    "Week 1":  "2026-08-31", "Week 2":  "2026-09-05", "Week 3":  "2026-09-12",
    "Week 4":  "2026-09-19", "Week 5":  "2026-09-26", "Week 6":  "2026-09-27",
    "Week 7":  "2026-10-03", "Week 8":  "2026-10-10", "Week 9":  "2026-10-17",
    "Week 10": "2026-10-24", "Week 11": "2026-10-28",
}
for d in WEEKLY_DATA:
    wdate = date_map[d['week']]
    fname = f"assets/report_previews/Weekly_{wdate}_Form3.png"
    draw_form3_weekly(d, fname)

print("\nAll report preview PNGs generated!")
files = os.listdir('assets/report_previews')
print(f"Total files: {len(files)}")
for f in sorted(files):
    size = os.path.getsize(f"assets/report_previews/{f}")
    print(f"  {f}: {size} bytes")
