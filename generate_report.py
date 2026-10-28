import subprocess
from collections import defaultdict
import datetime
import io
import os
import sys
import html
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# CONFIGURATION: Institution & Department Details
# -------------------------------------------------------------
COLLEGE_NAME = "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
DEPARTMENT_NAME = "Department of Computer Science & Engineering"
# -------------------------------------------------------------

def get_repo_info():
    """Extracts the repository name and current branch."""
    repo_name = "Devops-2026-CS-F-17"
    branch_name = "main"

    try:
        remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8').strip()
        extracted = remote_url.rstrip('/').split('/')[-1].replace('.git', '')
        if extracted:
            repo_name = extracted
    except Exception:
        try:
            root_path = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], encoding='utf-8').strip()
            repo_name = os.path.basename(root_path)
        except Exception:
            repo_name = os.path.basename(os.getcwd())

    try:
        branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()
    except Exception:
        pass

    return repo_name, branch_name

def normalize_author(author):
    """Normalize collaborator usernames to clear student identities."""
    if not author:
        return "Unknown"
    norm = author.strip()
    if norm.lower() in ["utkarsh16-tech", "utkarsh hinger", "utkarshhinger"]:
        return "Utkarsh Hinger"
    if norm.lower() in ["vanshitagr", "vanshita agrawal", "vanshita"]:
        return "vanshitagr"
    return norm

def get_git_metrics(interval="weekly", target_date=None, start_date=None, end_date=None, custom_scope=None):
    """
    Parses Git commit logs and aggregates metrics.
    Supported intervals: 'weekly', 'monthly', 'final', 'sprint'
    """
    git_args = ['git', 'log', '--pretty=format:COMMIT|||%h|||%an|||%ad|||%s', '--date=short', '--numstat']
    
    if start_date and end_date:
        scope_title = custom_scope or f"Milestone Window: {start_date} to {end_date}"
        filter_start = start_date
        filter_end = end_date
    elif interval == "weekly":
        if target_date is None:
            today = datetime.date.today()
        elif isinstance(target_date, str):
            today = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            today = target_date
        filter_start = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        filter_end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        scope_title = f"Sprint Window ({filter_start} to {today.strftime('%Y-%m-%d')})"
    elif interval == "monthly":
        if target_date is None:
            today = datetime.date.today()
        elif isinstance(target_date, str):
            today = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
        else:
            today = target_date
        filter_start = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        filter_end = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        scope_title = f"Sprint Month ({filter_start} to {today.strftime('%Y-%m-%d')})"
    else:
        filter_start = None
        filter_end = None
        scope_title = "Complete Project Lifecycle (All Commits)"

    try:
        raw_output = subprocess.check_output(git_args, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError:
        print("[ERROR] Git command failed. Please ensure you are inside a Git repository.")
        return None, None, None, scope_title

    students = defaultdict(lambda: {"commits": 0, "added": 0, "deleted": 0, "active_days": set()})
    timeline_activity = defaultdict(lambda: defaultdict(int))
    student_logs = defaultdict(list)

    current_author = None
    current_date_str = None
    in_scope = False

    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('COMMIT|||'):
            parts = line.split('|||')
            if len(parts) >= 5:
                sha = parts[1].strip()
                raw_author = parts[2].strip()
                date_str = parts[3].strip()
                msg = parts[4].strip()
            else:
                continue
            
            # Exclude bot commits from metric calculations
            if "bot" in raw_author.lower() or "github-actions" in raw_author.lower():
                current_author = None
                in_scope = False
                continue
            
            # Filter by date range if applicable
            if filter_start and filter_end:
                if not (filter_start <= date_str <= filter_end):
                    current_author = None
                    in_scope = False
                    continue

            in_scope = True
            author = normalize_author(raw_author)
            current_author = author
            current_date_str = date_str
            
            students[current_author]["commits"] += 1
            students[current_author]["active_days"].add(current_date_str)
            student_logs[current_author].append((date_str, sha, msg))
            
            try:
                dt = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
                if interval == "weekly" or interval == "sprint":
                    period_key = dt.strftime("%b %d")
                elif interval == "monthly":
                    period_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                else:
                    period_key = dt.strftime("%Y-%m")
                timeline_activity[period_key][current_author] += 1
            except Exception:
                pass

        elif in_scope and current_author and not line.startswith('COMMIT|||'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                students[current_author]["added"] += int(parts[0])
                students[current_author]["deleted"] += int(parts[1])

    return students, timeline_activity, student_logs, scope_title

def create_charts(students, timeline_activity, interval, save_assets=False):
    """Generates workload distribution and timeline comparison charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.8))
    authors = sorted(list(students.keys()))
    periods = sorted(timeline_activity.keys())

    # 1. Timeline Chart
    if periods and authors:
        for author in authors:
            counts = [timeline_activity[p].get(author, 0) for p in periods]
            ax1.plot(periods, counts, marker='o', linewidth=2, label=author)
        ax1.set_title(f"Commit Timeline ({interval.capitalize()})", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Commits")
        ax1.tick_params(axis='x', rotation=30)
        ax1.grid(True, linestyle='--', alpha=0.5)
        ax1.legend(fontsize=8)
    else:
        ax1.text(0.5, 0.5, "No commits recorded in this interval", ha='center', va='center')

    # 2. Net LOC Chart
    if authors:
        net_loc = [students[a]["added"] - students[a]["deleted"] for a in authors]
        colors_list = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F', '#EDC948', '#B07AA1']
        ax2.bar(authors, net_loc, color=colors_list[:len(authors)], width=0.45)
        ax2.set_title("Net Lines of Code Written", fontsize=10, fontweight='bold')
        ax2.set_ylabel("LOC (Added - Deleted)")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)
        ax2.tick_params(axis='x', rotation=15)
    else:
        ax2.text(0.5, 0.5, "No LOC changes recorded in this interval", ha='center', va='center')

    plt.tight_layout()

    if save_assets:
        os.makedirs("assets", exist_ok=True)
        plt.savefig("assets/evaluation_trends.png", dpi=200, bbox_inches='tight')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=200)
    plt.close()
    img_buffer.seek(0)
    return Image(img_buffer, width=500, height=170)

def generate_pdf(interval="weekly", target_date=None, start_date=None, end_date=None, custom_scope=None, custom_filename=None, output_dir=None):
    repo_name, branch_name = get_repo_info()
    students, timeline_activity, student_logs, scope_title = get_git_metrics(
        interval=interval,
        target_date=target_date,
        start_date=start_date,
        end_date=end_date,
        custom_scope=custom_scope
    )

    if students is None:
        return

    if custom_filename:
        doc_filename = custom_filename
    elif target_date:
        date_stamp = target_date if isinstance(target_date, str) else target_date.strftime("%Y-%m-%d")
        doc_filename = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"
    elif interval == "final":
        date_stamp = datetime.date.today().strftime("%Y-%m-%d")
        doc_filename = f"{repo_name}_Final_Report_{date_stamp}.pdf"
    else:
        date_stamp = datetime.date.today().strftime("%Y-%m-%d")
        doc_filename = f"{repo_name}_Weekly_Progress_Report_Form-3_{date_stamp}.pdf"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        full_path = os.path.join(output_dir, doc_filename)
    else:
        full_path = doc_filename

    doc = SimpleDocTemplate(
        full_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    college_style = ParagraphStyle(
        'CollegeStyle', parent=styles['Heading1'],
        fontSize=13.5, leading=17, textColor=colors.HexColor("#0F172A"), alignment=1, spaceAfter=2
    )
    dept_style = ParagraphStyle(
        'DeptStyle', parent=styles['Normal'],
        fontSize=9.5, leading=13, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=6
    )
    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Heading2'],
        fontSize=13, leading=17, textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=5
    )
    repo_style = ParagraphStyle(
        'RepoStyle', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=8
    )
    section_style = ParagraphStyle(
        'SectionStyle', parent=styles['Heading2'],
        fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"), spaceBefore=7, spaceAfter=4
    )
    sub_section_style = ParagraphStyle(
        'SubSectionStyle', parent=styles['Heading3'],
        fontSize=9, leading=12, textColor=colors.HexColor("#2563EB"), spaceBefore=5, spaceAfter=2
    )
    msg_style = ParagraphStyle(
        'MsgStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#1E293B")
    )
    meta_cell_style = ParagraphStyle(
        'MetaCellStyle', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=colors.HexColor("#475569"), alignment=1
    )

    story = []

    # 1. Header
    report_title = "Final Project Evaluation Report" if interval == "final" else "Weekly Progress Report (Form-3)"
    story.append(Paragraph(f"<b>{html.escape(COLLEGE_NAME)}</b>", college_style))
    story.append(Paragraph(f"<b>{html.escape(DEPARTMENT_NAME)}</b>", dept_style))
    story.append(Paragraph(f"<u><b>{report_title}</b></u>", title_style))
    story.append(Spacer(1, 3))

    # 2. Metadata
    story.append(Paragraph(f"<b>Project Repository:</b> <font color='#2563EB'><b>{html.escape(repo_name)}</b></font> &nbsp;|&nbsp; <b>Branch:</b> <code>{html.escape(branch_name)}</code>", repo_style))
    story.append(Paragraph(f"<b>Evaluation Window:</b> {scope_title} &nbsp;|&nbsp; <b>Generated On:</b> {datetime.date.today().strftime('%B %d, %Y')}", meta_style))

    # 3. Individual Summary Table
    story.append(Paragraph("1. Individual Contribution Breakdown", section_style))
    total_commits = sum(data["commits"] for data in students.values())
    table_data = [["Student Name", "Commits (%)", "Lines Added", "Lines Deleted", "Net LOC", "Active Days"]]
    
    if students:
        for name in sorted(students.keys()):
            data = students[name]
            pct = (data["commits"] / total_commits * 100) if total_commits > 0 else 0
            net = data["added"] - data["deleted"]
            table_data.append([
                html.escape(name),
                f"{data['commits']} ({pct:.1f}%)",
                f"+{data['added']:,}",
                f"-{data['deleted']:,}",
                f"{net:,}",
                f"{len(data['active_days'])} days"
            ])
    else:
        table_data.append(["No commits recorded in this period. Run with 'final' to see all commits.", "-", "-", "-", "-", "-"])

    table = Table(table_data, colWidths=[120, 80, 80, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))

    # 4. Visual Charts
    story.append(Paragraph("2. Visual Trends & Volume", section_style))
    chart_image = create_charts(students, timeline_activity, interval, save_assets=(interval == "final"))
    story.append(chart_image)
    story.append(Spacer(1, 6))

    # 5. Detailed Commit Logs per Student
    story.append(Paragraph(f"3. Detailed Commit Logs ({interval.capitalize()})", section_style))
    if not student_logs:
        story.append(Paragraph("<i>No commit logs found for this timeframe.</i>", styles['Normal']))
    else:
        for student_name in sorted(student_logs.keys()):
            logs = student_logs[student_name]
            student_section = []
            student_section.append(Paragraph(f"<b>Student:</b> {html.escape(student_name)} — <i>{len(logs)} commit(s)</i>", sub_section_style))
            
            log_table_data = [["Date", "Hash", "Commit Message"]]
            for date_val, sha_val, msg_val in logs:
                safe_msg = html.escape(msg_val) if msg_val else "(No commit message)"
                log_table_data.append([
                    Paragraph(date_val, meta_cell_style),
                    Paragraph(f"<code>{sha_val}</code>", meta_cell_style),
                    Paragraph(safe_msg, msg_style)
                ])
            
            log_table = Table(log_table_data, colWidths=[70, 60, 410])
            t_style = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#475569")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
                ('TOPPADDING', (0, 0), (-1, -1), 2.5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]
            
            log_table.setStyle(TableStyle(t_style))
            student_section.append(log_table)
            student_section.append(Spacer(1, 5))
            story.append(KeepTogether(student_section))

    doc.build(story)
    print(f"[SUCCESS] Generated: {full_path} ({len(students)} contributor(s), {total_commits} commits)")
    return full_path

def generate_all_milestone_reports():
    """Generates milestone-based Form-3 progress reports across the active project development lifecycle."""
    milestones = [
        ("Devops-2026-CS-F-17_Sprint_1_Progress_Report_Form-3.pdf", "2026-07-25", "2026-08-15", "Sprint 1: Architecture, Schemas & UI Foundation (2026-07-25 to 2026-08-15)"),
        ("Devops-2026-CS-F-17_Sprint_2_Progress_Report_Form-3.pdf", "2026-08-16", "2026-08-22", "Sprint 2: Authentication, Security & Middleware (2026-08-16 to 2026-08-22)"),
        ("Devops-2026-CS-F-17_Sprint_3_Progress_Report_Form-3.pdf", "2026-08-23", "2026-09-05", "Sprint 3: Database Resilience, Gigs & Bids Workflows (2026-08-23 to 2026-09-05)"),
        ("Devops-2026-CS-F-17_Sprint_4_Progress_Report_Form-3.pdf", "2026-09-06", "2026-10-20", "Sprint 4: Full Stack Integration & Quality Assurance (2026-09-06 to 2026-10-20)"),
        ("Devops-2026-CS-F-17_Sprint_5_Progress_Report_Form-3.pdf", "2026-10-21", "2026-10-29", "Sprint 5: DevOps, Docker, Monitoring & CI/CD Pipeline (2026-10-21 to 2026-10-29)")
    ]
    output_directory = "weekly_reports"
    print(f"\n[INFO] Generating {len(milestones)} Milestone Sprint Form-3 Reports into '{output_directory}'...")
    for filename, start, end, scope in milestones:
        generate_pdf(
            interval="sprint",
            start_date=start,
            end_date=end,
            custom_scope=scope,
            custom_filename=filename,
            output_dir=output_directory
        )

if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "final"
    if mode == "all-sprints" or mode == "all-weekly":
        generate_all_milestone_reports()
    elif mode == "final":
        generate_pdf("final")
    else:
        generate_pdf(mode)
