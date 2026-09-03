import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent

OUTPUT = ROOT / "Devops-2026-CS-F-16_Final_Project_Evaluation_Report.pdf"

CHART_DIR = ROOT / ".report_charts"
CHART_DIR.mkdir(exist_ok=True)


# ============================================================
# RUN GIT COMMAND
# ============================================================

def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


# ============================================================
# GET COMMIT HISTORY
# ============================================================

def get_commits():

    fmt = "%H%x1f%an%x1f%ad%x1f%s%x1e"

    raw = git(
        "log",
        "--all",
        f"--format={fmt}",
        "--date=iso-strict",
    )

    commits = []

    for record in raw.strip("\x1e\n").split("\x1e"):

        if not record.strip():
            continue

        parts = record.strip().split("\x1f")

        if len(parts) != 4:
            continue

        commit_hash, author, date_text, subject = parts

        try:
            date = datetime.fromisoformat(date_text)
        except ValueError:
            continue

        commits.append(
            {
                "hash": commit_hash[:7],
                "author": author,
                "date": date,
                "subject": subject,
            }
        )

    return commits


# ============================================================
# GET LINES ADDED / DELETED
# ============================================================

def get_numstat():

    raw = git(
        "log",
        "--all",
        "--format=%H%x1f%an%x1e",
        "--numstat",
    )

    totals = defaultdict(lambda: [0, 0])

    current_author = None

    for line in raw.splitlines():

        if "\x1e" in line:

            header, author = line.split("\x1e", 1)

            current_author = author

            continue

        if current_author and line.count("\t") == 2:

            added, deleted, filename = line.split("\t", 2)

            if added.isdigit() and deleted.isdigit():

                totals[current_author][0] += int(added)

                totals[current_author][1] += int(deleted)

    return totals


# ============================================================
# CREATE CHARTS
# ============================================================

def create_charts(commits, stats):

    authors = sorted(
        set(commit["author"] for commit in commits)
    )

    # --------------------------------------------------------
    # COMMIT TIMELINE
    # --------------------------------------------------------

    commits_by_day = defaultdict(lambda: defaultdict(int))

    for commit in commits:

        day = commit["date"].date()

        author = commit["author"]

        commits_by_day[day][author] += 1

    days = sorted(commits_by_day.keys())

    timeline_file = CHART_DIR / "commit_timeline.png"

    plt.figure(figsize=(6.4, 3.3))

    for author in authors:

        values = [
            commits_by_day[day].get(author, 0)
            for day in days
        ]

        plt.plot(
            days,
            values,
            marker="o",
            label=author,
        )

    plt.xlabel("Date")

    plt.ylabel("Commits")

    plt.title("Commit Timeline")

    plt.xticks(
        rotation=35,
        ha="right",
    )

    plt.grid(
        True,
        alpha=0.25,
    )

    plt.legend(
        fontsize=7,
    )

    plt.tight_layout()

    plt.savefig(
        timeline_file,
        dpi=180,
    )

    plt.close()


    # --------------------------------------------------------
    # NET LOC
    # --------------------------------------------------------

    loc_file = CHART_DIR / "net_loc.png"

    values = []

    for author in authors:

        added = stats.get(author, [0, 0])[0]

        deleted = stats.get(author, [0, 0])[1]

        values.append(
            added - deleted
        )

    plt.figure(figsize=(6.4, 3.3))

    plt.bar(
        authors,
        values,
    )

    plt.xlabel("Student")

    plt.ylabel("LOC (Added - Deleted)")

    plt.title("Net Lines of Code Written")

    plt.xticks(
        rotation=20,
        ha="right",
    )

    plt.tight_layout()

    plt.savefig(
        loc_file,
        dpi=180,
    )

    plt.close()


    return timeline_file, loc_file


# ============================================================
# BUILD PDF
# ============================================================

def build_pdf(commits):

    stats = get_numstat()

    authors = sorted(
        set(commit["author"] for commit in commits)
    )

    total_commits = len(commits)

    timeline_file, loc_file = create_charts(
        commits,
        stats,
    )


    # --------------------------------------------------------
    # PDF DOCUMENT
    # --------------------------------------------------------

    document = SimpleDocTemplate(

        str(OUTPUT),

        pagesize=A4,

        rightMargin=12 * mm,

        leftMargin=12 * mm,

        topMargin=10 * mm,

        bottomMargin=10 * mm,

        title="Final Project Evaluation Report",
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=17,

        leading=20,

        spaceAfter=4,
    )


    college_style = ParagraphStyle(

        "College",

        parent=title_style,

        fontSize=12,

        leading=14,
    )


    department_style = ParagraphStyle(

        "Department",

        parent=styles["BodyText"],

        alignment=TA_CENTER,

        fontSize=9,

        leading=11,
    )


    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        fontSize=11,

        leading=14,

        spaceBefore=5,

        spaceAfter=5,
    )


    small_style = ParagraphStyle(

        "Small",

        parent=styles["BodyText"],

        fontSize=8,

        leading=10,
    )


    tiny_style = ParagraphStyle(

        "Tiny",

        parent=styles["BodyText"],

        fontSize=7.2,

        leading=8.5,
    )


    dark = colors.HexColor(
        "#263548"
    )


    story = []


    # ========================================================
    # HEADER
    # ========================================================

    story.append(

        Paragraph(

            "Swami Keshvanand Institute of Technology, "
            "Management & Gramothan, Jaipur",

            college_style,
        )
    )


    story.append(

        Paragraph(

            "Department of Computer Science & Engineering",

            department_style,
        )
    )


    story.append(
        Spacer(
            1,
            3 * mm,
        )
    )


    story.append(

        Paragraph(

            "Final Project Evaluation Report",

            title_style,
        )
    )


    story.append(

        Paragraph(

            "<b>Project Repository:</b> "
            "Devops-2026-CS-F-16 "
            "&nbsp; | &nbsp; "
            "<b>Branch:</b> main",

            small_style,
        )
    )


    story.append(

        Paragraph(

            "<b>Evaluation Window:</b> "
            "Complete Project Lifecycle (All Commits)"
            "&nbsp; | &nbsp; "
            "<b>Generated On:</b> "
            + datetime.now().strftime("%B %d, %Y"),

            small_style,
        )
    )


    story.append(
        Spacer(
            1,
            3 * mm,
        )
    )


    # ========================================================
    # CONTRIBUTION TABLE
    # ========================================================

    story.append(

        Paragraph(

            "1. Individual Contribution Breakdown",

            heading_style,
        )
    )


    contribution_rows = [

        [
            "Student Name",
            "Commits (%)",
            "Lines Added",
            "Lines Deleted",
            "Net LOC",
            "Active Days",
        ]

    ]


    for author in authors:

        author_commits = [

            commit
            for commit in commits
            if commit["author"] == author

        ]

        count = len(author_commits)

        percentage = (

            count / total_commits * 100

            if total_commits

            else 0

        )

        added, deleted = stats.get(
            author,
            [0, 0]
        )

        active_days = len(
            set(
                commit["date"].date()
                for commit in author_commits
            )
        )


        contribution_rows.append(

            [
                author,

                f"{count} ({percentage:.1f}%)",

                f"+{added:,}",

                f"-{deleted:,}",

                f"{added - deleted:,}",

                str(active_days),
            ]
        )


    contribution_table = Table(

        contribution_rows,

        colWidths=[
            38 * mm,
            25 * mm,
            24 * mm,
            24 * mm,
            24 * mm,
            23 * mm,
        ],
    )


    contribution_table.setStyle(

        TableStyle(

            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    dark,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7.5,
                ),

                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.lightgrey,
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#f4f7fa"),
                    ],
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )


    story.append(
        contribution_table
    )


    # ========================================================
    # CHARTS
    # ========================================================

    story.append(

        Paragraph(

            "2. Visual Trends & Volume",

            heading_style,
        )
    )


    chart_table = Table(

        [

            [

                Image(
                    str(timeline_file),
                    width=88 * mm,
                    height=45 * mm,
                ),

                Image(
                    str(loc_file),
                    width=88 * mm,
                    height=45 * mm,
                ),

            ]

        ],

        colWidths=[
            91 * mm,
            91 * mm,
        ],
    )


    chart_table.setStyle(

        TableStyle(

            [

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),

            ]
        )
    )


    story.append(
        chart_table
    )


    # ========================================================
    # DETAILED COMMITS
    # ========================================================

    story.append(

        Paragraph(

            "3. Detailed Commit Logs (Final)",

            heading_style,
        )
    )


    for author in authors:

        author_commits = [

            commit
            for commit in commits
            if commit["author"] == author

        ]


        story.append(

            Paragraph(

                f"<b><font color='#2459a6'>"
                f"Student: {author} — "
                f"{len(author_commits)} commit(s)"
                f"</font></b>",

                small_style,
            )
        )


        rows = [

            [
                "Date",
                "Hash",
                "Commit Message",
            ]

        ]


        sorted_commits = sorted(

            author_commits,

            key=lambda x: x["date"],

            reverse=True,
        )


        for commit in sorted_commits:

            rows.append(

                [

                    commit["date"].strftime(
                        "%Y-%m-%d"
                    ),

                    commit["hash"],

                    Paragraph(
                        commit["subject"],
                        tiny_style,
                    ),

                ]
            )


        commit_table = Table(

            rows,

            colWidths=[
                28 * mm,
                22 * mm,
                132 * mm,
            ],

            repeatRows=1,
        )


        commit_table.setStyle(

            TableStyle(

                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        dark,
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7.2,
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.3,
                        colors.lightgrey,
                    ),

                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#f4f7fa"),
                        ],
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        3,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        3,
                    ),

                ]
            )
        )


        story.append(
            commit_table
        )

        story.append(
            Spacer(
                1,
                2 * mm,
            )
        )


    # ========================================================
    # BUILD
    # ========================================================

    document.build(
        story
    )


    return OUTPUT


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        commits = get_commits()

        if not commits:

            raise SystemExit(
                "No Git commits found. "
                "Make sure generate_report.py "
                "is inside your Git repository."
            )


        output = build_pdf(
            commits
        )


        print()
        print("=" * 60)
        print("REPORT GENERATED SUCCESSFULLY")
        print("=" * 60)
        print()
        print(f"File: {output}")
        print(f"Commits analysed: {len(commits)}")
        print()


    except subprocess.CalledProcessError:

        raise SystemExit(

            "Git command failed. "
            "Make sure Git is installed and "
            "the script is inside the repository."
        )