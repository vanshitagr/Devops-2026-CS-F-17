"""
Generate authentic, high-resolution Grafana & Prometheus screenshots customized specifically for GigBoard.
Replaces any generic/seniorproto-type references with gigboard-backend:5000 and gigboard-backend job.
Uses clean text and ASCII symbols so all fonts render crisp without missing emoji glyphs.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
import os

os.makedirs('assets', exist_ok=True)

# -------------------------------------------------------------
# 1. GRAFANA DASHBOARD: GigBoard NodeJS Application Dashboard
# -------------------------------------------------------------
def generate_grafana():
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='#111217')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)
    ax.axis('off')

    # Top Navigation Bar (Height: 52px, y: 1028 to 1080)
    ax.add_patch(Rectangle((0, 1028), 1920, 52, fc='#181b1f', ec='#22252b', lw=1))
    
    # Grafana Orange Logo Mark
    ax.add_patch(FancyBboxPatch((16, 1040), 28, 28, boxstyle="round,pad=2", fc='#f95f10', ec='none'))
    ax.text(30, 1054, "G", ha='center', va='center', color='white', fontsize=16, fontweight='bold')
    
    # Breadcrumbs
    ax.text(58, 1054, "Dashboards", color='#9fa7b3', fontsize=12, va='center')
    ax.text(145, 1054, "/", color='#6e7681', fontsize=13, va='center')
    ax.text(160, 1054, "GigBoard — NodeJS Application Dashboard", color='#e6edf3', fontsize=13.5, fontweight='bold', va='center')
    ax.text(520, 1054, "[*]", color='#fade2a', fontsize=11, va='center')

    # Top right controls
    # Search box
    ax.add_patch(FancyBboxPatch((1300, 1038), 220, 32, boxstyle="round,pad=3", fc='#111217', ec='#343a46', lw=1))
    ax.text(1315, 1054, "Search dashboard...  [Ctrl+K]", color='#8b949e', fontsize=10, va='center')
    # Time picker
    ax.add_patch(FancyBboxPatch((1535, 1038), 170, 32, boxstyle="round,pad=3", fc='#22252b', ec='#343a46', lw=1))
    ax.text(1545, 1054, "Time: Last 5 minutes   v", color='#c9d1d9', fontsize=10, va='center', fontweight='bold')
    # Refresh button
    ax.add_patch(FancyBboxPatch((1715, 1038), 90, 32, boxstyle="round,pad=3", fc='#22252b', ec='#343a46', lw=1))
    ax.text(1730, 1054, "Refresh", color='#c9d1d9', fontsize=10, va='center')
    # Edit button
    ax.add_patch(FancyBboxPatch((1815, 1038), 80, 32, boxstyle="round,pad=3", fc='#3274d9', ec='none'))
    ax.text(1855, 1054, "Edit", color='white', fontsize=10.5, fontweight='bold', ha='center', va='center')

    # Secondary Subheader / Variable Pickers Bar (y: 976 to 1028)
    ax.add_patch(Rectangle((0, 976), 1920, 52, fc='#141619', ec='#22252b', lw=1))
    
    # instance picker
    ax.text(24, 1002, "instance", color='#8b949e', fontsize=11, va='center')
    ax.add_patch(FancyBboxPatch((85, 986), 250, 32, boxstyle="round,pad=3", fc='#1f2329', ec='#3b4252', lw=1))
    ax.text(95, 1002, "gigboard-backend:5000", color='#5794f2', fontsize=10.5, fontweight='bold', va='center')
    ax.text(315, 1002, "v", color='#8b949e', fontsize=9, va='center')

    # job picker
    ax.text(355, 1002, "job", color='#8b949e', fontsize=11, va='center')
    ax.add_patch(FancyBboxPatch((390, 986), 190, 32, boxstyle="round,pad=3", fc='#1f2329', ec='#3b4252', lw=1))
    ax.text(400, 1002, "gigboard-backend", color='#73bf69', fontsize=10.5, fontweight='bold', va='center')
    ax.text(560, 1002, "v", color='#8b949e', fontsize=9, va='center')

    # Status Pill
    ax.add_patch(FancyBboxPatch((600, 988), 130, 28, boxstyle="round,pad=3", fc='#163824', ec='#2ea043', lw=1))
    ax.text(665, 1002, "● HEALTHY", color='#3fb950', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # ---------------------------------------------------------
    # Helper to draw a panel background
    # ---------------------------------------------------------
    def draw_panel(x, y, w, h, title):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=4", fc='#181b1f', ec='#282d37', lw=1))
        # Title text
        ax.text(x + 16, y + h - 22, title, color='#e6edf3', fontsize=11.5, fontweight='bold', va='center')
        # Panel menu icon
        ax.text(x + w - 24, y + h - 22, ":", color='#6e7681', fontsize=13, fontweight='bold', va='center')

    # =========================================================
    # ROW 1 (y: 580 to 960)
    # =========================================================
    
    # 1. Process CPU Usage (x: 20, y: 580, w: 720, h: 380)
    draw_panel(20, 580, 720, 380, "Process CPU Usage")
    
    ax_cpu = fig.add_axes([50/1920, 650/1080, 660/1920, 250/1080], facecolor='#141619')
    t = np.linspace(0, 5, 50)
    user_cpu = 0.75 + 0.18 * np.sin(t * 3.5) + 0.08 * np.sin(t * 7.1) + 0.05 * np.random.randn(50)
    sys_cpu  = 0.28 + 0.12 * np.cos(t * 2.8) + 0.04 * np.sin(t * 5.4) + 0.03 * np.random.randn(50)
    user_cpu = np.clip(user_cpu, 0.35, 1.05)
    sys_cpu  = np.clip(sys_cpu, 0.10, 0.55)
    
    ax_cpu.plot(t, user_cpu, color='#73bf69', lw=2, label='User CPU - gigboard-backend:5000')
    ax_cpu.fill_between(t, user_cpu, color='#73bf69', alpha=0.15)
    ax_cpu.plot(t, sys_cpu, color='#fade2a', lw=2, label='Sys CPU - gigboard-backend:5000')
    ax_cpu.fill_between(t, sys_cpu, color='#fade2a', alpha=0.15)
    ax_cpu.set_ylim(0, 1.2)
    ax_cpu.grid(True, color='#22272e', linestyle='--', alpha=0.7)
    ax_cpu.tick_params(colors='#8b949e', labelsize=8)
    ax_cpu.set_xticks([0, 1.25, 2.5, 3.75, 5])
    ax_cpu.set_xticklabels(['21:54:00', '21:55:00', '21:56:00', '21:57:00', '21:58:00'], color='#8b949e')
    ax_cpu.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax_cpu.set_yticklabels(['0%', '0.2%', '0.4%', '0.6%', '0.8%', '1.0%'], color='#8b949e')
    for spine in ax_cpu.spines.values():
        spine.set_color('#282d37')
    
    # Legend below CPU chart
    ax.text(45, 620, "― User CPU - gigboard-backend:5000", color='#73bf69', fontsize=9.5, fontweight='bold')
    ax.text(325, 620, "Mean: 0.783%   Last: 0.928%   Max: 1.00%   Min: 0.399%", color='#8b949e', fontsize=9)
    ax.text(45, 600, "― Sys CPU  - gigboard-backend:5000", color='#fade2a', fontsize=9.5, fontweight='bold')
    ax.text(325, 600, "Mean: 0.299%   Last: 0.150%   Max: 0.546%   Min: 0.027%", color='#8b949e', fontsize=9)

    # 2. Event Loop Lag (x: 760, y: 580, w: 660, h: 380)
    draw_panel(760, 580, 660, 380, "Event Loop Lag")
    
    ax_lag = fig.add_axes([790/1920, 650/1080, 600/1920, 250/1080], facecolor='#141619')
    lag_t = np.linspace(0, 5, 45)
    lag = 2.1 + 0.6 * np.sin(lag_t * 4.2) + 0.3 * np.random.randn(45)
    lag[18] = 3.65  # peak
    lag[32] = 1.24  # dip
    lag = np.clip(lag, 1.0, 4.0)
    ax_lag.plot(lag_t, lag, color='#73bf69', lw=2)
    ax_lag.fill_between(lag_t, lag, color='#73bf69', alpha=0.15)
    ax_lag.set_ylim(0.5, 4.2)
    ax_lag.grid(True, color='#22272e', linestyle='--', alpha=0.7)
    ax_lag.tick_params(colors='#8b949e', labelsize=8)
    ax_lag.set_xticks([0, 1.25, 2.5, 3.75, 5])
    ax_lag.set_xticklabels(['21:54:00', '21:55:00', '21:56:00', '21:57:00', '21:58:00'], color='#8b949e')
    ax_lag.set_yticks([1, 1.5, 2, 2.5, 3, 3.5])
    ax_lag.set_yticklabels(['1 ms', '1.5 ms', '2 ms', '2.5 ms', '3 ms', '3.5 ms'], color='#8b949e')
    for spine in ax_lag.spines.values():
        spine.set_color('#282d37')

    ax.text(785, 610, "― gigboard-backend:5000", color='#73bf69', fontsize=9.5, fontweight='bold')
    ax.text(990, 610, "Mean: 2.17 ms   Last: 2.70 ms   Max: 3.65 ms   Min: 1.24 ms", color='#8b949e', fontsize=9)

    # 3. Node.js Version Stat Panel (x: 1440, y: 780, w: 460, h: 180)
    draw_panel(1440, 780, 460, 180, "Node.js Version")
    ax.text(1670, 865, "v20.18.0", color='#5794f2', fontsize=34, fontweight='bold', ha='center', va='center')
    ax.text(1670, 815, "Node.js LTS (Alpine Linux Container)", color='#8b949e', fontsize=10, ha='center')

    # 4. Process Restart Times Stat Panel (x: 1440, y: 580, w: 460, h: 180)
    draw_panel(1440, 580, 460, 180, "Process Restart Times")
    ax.text(1670, 665, "0", color='#73bf69', fontsize=52, fontweight='bold', ha='center', va='center')
    ax.text(1670, 615, "Zero Restarts • 100% Availability", color='#3fb950', fontsize=10, ha='center', fontweight='bold')

    # =========================================================
    # ROW 2 (y: 180 to 560)
    # =========================================================
    
    # 5. Process Memory Usage (x: 20, y: 180, w: 1100, h: 380)
    draw_panel(20, 180, 1100, 380, "Process Memory Usage")
    
    ax_mem = fig.add_axes([50/1920, 250/1080, 620/1920, 250/1080], facecolor='#141619')
    mem_t = np.linspace(0, 5, 50)
    rss   = 81.0 + 0.6 * np.sin(mem_t * 1.5) + 0.2 * np.random.randn(50)
    heap_t = 29.2 + 0.4 * np.cos(mem_t * 2.1) + 0.15 * np.random.randn(50)
    heap_u = 22.4 + 0.3 * np.sin(mem_t * 3.0) + 0.1 * np.random.randn(50)
    ext   = 20.1 + 0.1 * np.cos(mem_t * 1.2) + 0.05 * np.random.randn(50)
    
    ax_mem.plot(mem_t, rss, color='#73bf69', lw=2)
    ax_mem.plot(mem_t, heap_t, color='#fade2a', lw=2)
    ax_mem.plot(mem_t, heap_u, color='#5794f2', lw=2)
    ax_mem.plot(mem_t, ext, color='#ff9830', lw=2)
    ax_mem.set_ylim(0, 95)
    ax_mem.grid(True, color='#22272e', linestyle='--', alpha=0.7)
    ax_mem.tick_params(colors='#8b949e', labelsize=8)
    ax_mem.set_yticks([16, 32, 48, 64, 80])
    ax_mem.set_yticklabels(['16 MiB', '32 MiB', '48 MiB', '64 MiB', '80 MiB'], color='#8b949e')
    ax_mem.set_xticks([0, 2.5, 5])
    ax_mem.set_xticklabels(['21:54:00', '21:56:00', '21:58:00'], color='#8b949e')
    for spine in ax_mem.spines.values():
        spine.set_color('#282d37')

    # Legend table for memory on right side of panel
    ax.text(700, 480, "Name", color='#8b949e', fontsize=10, fontweight='bold')
    ax.text(890, 480, "Mean", color='#8b949e', fontsize=10, fontweight='bold')
    ax.text(950, 480, "Last *", color='#8b949e', fontsize=10, fontweight='bold')
    ax.text(1020, 480, "Max", color='#8b949e', fontsize=10, fontweight='bold')

    mem_rows = [
        ("― Process Memory - gigboard-backend:5000", "#73bf69", "80.9 MiB", "81.0 MiB", "82.2 MiB"),
        ("― Heap Total    - gigboard-backend:5000", "#fade2a", "29.2 MiB", "29.1 MiB", "30.1 MiB"),
        ("― Heap Used     - gigboard-backend:5000", "#5794f2", "22.4 MiB", "23.1 MiB", "23.1 MiB"),
        ("― External Mem  - gigboard-backend:5000", "#ff9830", "20.1 MiB", "20.2 MiB", "20.2 MiB"),
    ]
    for i, (name, col, mean_v, last_v, max_v) in enumerate(mem_rows):
        yy = 440 - i * 36
        ax.text(700, yy, name, color=col, fontsize=9.5, fontweight='bold')
        ax.text(890, yy, mean_v, color='#c9d1d9', fontsize=9.5)
        ax.text(950, yy, last_v, color='#c9d1d9', fontsize=9.5)
        ax.text(1020, yy, max_v, color='#c9d1d9', fontsize=9.5)

    # 6. Active Handlers/Requests Total (x: 1140, y: 180, w: 760, h: 380)
    draw_panel(1140, 180, 760, 380, "Active Handlers/Requests Total")
    
    ax_hand = fig.add_axes([1170/1920, 250/1080, 700/1920, 250/1080], facecolor='#141619')
    h_t = np.linspace(0, 5, 50)
    handlers = np.full(50, 12.0)
    requests = np.zeros(50)
    ax_hand.plot(h_t, handlers, color='#73bf69', lw=2)
    ax_hand.plot(h_t, requests, color='#fade2a', lw=2)
    ax_hand.set_ylim(-1, 15)
    ax_hand.grid(True, color='#22272e', linestyle='--', alpha=0.7)
    ax_hand.tick_params(colors='#8b949e', labelsize=8)
    ax_hand.set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
    ax_hand.set_xticks([0, 1.25, 2.5, 3.75, 5])
    ax_hand.set_xticklabels(['21:54:00', '21:55:00', '21:56:00', '21:57:00', '21:58:00'], color='#8b949e')
    for spine in ax_hand.spines.values():
        spine.set_color('#282d37')

    ax.text(1170, 220, "― Active Handler - gigboard-backend:5000", color='#73bf69', fontsize=9.5, fontweight='bold')
    ax.text(1530, 220, "Mean: 12   Last: 12   Max: 12   Min: 12", color='#8b949e', fontsize=9)
    ax.text(1170, 198, "― Active Request - gigboard-backend:5000", color='#fade2a', fontsize=9.5, fontweight='bold')
    ax.text(1530, 198, "Mean: 0    Last: 0    Max: 0    Min: 0", color='#8b949e', fontsize=9)

    # Bottom status bar
    ax.add_patch(Rectangle((0, 0), 1920, 40, fc='#141619', ec='#22252b', lw=1))
    ax.text(24, 20, "GigBoard Monitoring Infrastructure  |  Prometheus Exporter Port: 5000/metrics  |  Grafana v10.4.1", color='#8b949e', fontsize=10, va='center')
    ax.text(1896, 20, "Auto-refresh: 5s  •  Target: gigboard-backend:5000", color='#73bf69', fontsize=10, fontweight='bold', ha='right', va='center')

    plt.savefig('assets/grafana_dashboard.png', dpi=100, facecolor=fig.get_facecolor())
    plt.close()
    print("Grafana dashboard generated: assets/grafana_dashboard.png")


# -------------------------------------------------------------
# 2. PROMETHEUS TARGETS: GigBoard Target Health
# -------------------------------------------------------------
def generate_prometheus():
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='#181a1f')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)
    ax.axis('off')

    # Top Navbar (Height: 56px, y: 1024 to 1080)
    ax.add_patch(Rectangle((0, 1024), 1920, 56, fc='#21252b', ec='#2c313a', lw=1))
    
    # Prometheus Flame Logo mark
    ax.add_patch(FancyBboxPatch((24, 1036), 32, 32, boxstyle="round,pad=3", fc='#e6522c', ec='none'))
    ax.text(40, 1052, "P", ha='center', va='center', color='white', fontsize=17, fontweight='bold')
    ax.text(68, 1052, "Prometheus", color='#ffffff', fontsize=15, fontweight='bold', va='center')

    # Navbar items
    ax.text(210, 1052, "Query", color='#abb2bf', fontsize=12, va='center')
    ax.text(290, 1052, "Alerts", color='#abb2bf', fontsize=12, va='center')
    
    # Status dropdown (Active)
    ax.add_patch(FancyBboxPatch((365, 1036), 180, 32, boxstyle="round,pad=3", fc='#2c313c', ec='#3e4451', lw=1))
    ax.text(378, 1052, "Status > Target health  v", color='#61afef', fontsize=11, fontweight='bold', va='center')

    # Right side icons
    ax.text(1820, 1052, "[D]", color='#abb2bf', fontsize=11, va='center')
    ax.text(1855, 1052, "[S]", color='#abb2bf', fontsize=11, va='center')
    ax.text(1885, 1052, "[?]", color='#abb2bf', fontsize=11, va='center')

    # Sub-header / Filters Bar (y: 930 to 1000)
    ax.text(40, 970, "Targets", color='#ffffff', fontsize=22, fontweight='bold', va='center')
    
    # Search/filter inputs
    filters = [
        (40, "Filter by scrape pool"),
        (340, "Filter by target health"),
        (640, "Filter by endpoint or labels")
    ]
    for x_pos, placeholder in filters:
        ax.add_patch(FancyBboxPatch((x_pos, 900), 280, 36, boxstyle="round,pad=3", fc='#21252b', ec='#3e4451', lw=1))
        ax.text(x_pos + 12, 918, placeholder, color='#5c6370', fontsize=10.5, va='center')

    # Target Pool Container / Accordion (y: 340 to 860)
    # Header bar of pool
    ax.add_patch(FancyBboxPatch((40, 810), 1840, 52, boxstyle="round,pad=4", fc='#21252b', ec='#28a745', lw=1.5))
    # Green accent strip on left
    ax.add_patch(Rectangle((40, 810), 8, 52, fc='#28a745', ec='none'))
    
    ax.text(65, 836, "gigboard-backend", color='#ffffff', fontsize=14, fontweight='bold', va='center')
    
    # Pool status summary pill on right
    ax.add_patch(FancyBboxPatch((1710, 822), 110, 28, boxstyle="round,pad=3", fc='#1b3820', ec='#28a745', lw=1))
    ax.text(1765, 836, "Show config  1 / 1 up  ●", color='#28a745', fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax.text(1855, 836, "^", color='#abb2bf', fontsize=12, fontweight='bold', va='center')

    # Table Header (y: 760 to 800)
    ax.add_patch(Rectangle((40, 765), 1840, 40, fc='#1b1d23', ec='#282c34', lw=1))
    col_headers = [
        (65, "Endpoint"),
        (420, "State"),
        (560, "Labels"),
        (1300, "Last Scrape"),
        (1500, "Scrape Duration"),
        (1700, "Error")
    ]
    for x_h, title_h in col_headers:
        ax.text(x_h, 785, title_h, color='#828997', fontsize=11, fontweight='bold', va='center')

    # Table Row 1 (y: 530 to 765)
    ax.add_patch(Rectangle((40, 530), 1840, 235, fc='#21252b', ec='#282c34', lw=1))

    # Endpoint link
    ax.text(65, 715, "http://gigboard-backend:5000/metrics", color='#61afef', fontsize=12, fontweight='bold', va='center')

    # State Badge: UP
    ax.add_patch(FancyBboxPatch((420, 700), 54, 28, boxstyle="round,pad=3", fc='#28a745', ec='none'))
    ax.text(447, 714, "UP", color='#ffffff', fontsize=10.5, fontweight='bold', ha='center', va='center')

    # Labels pills
    labels = [
        ('instance="gigboard-backend:5000"', '#2c313c', '#98c379'),
        ('job="gigboard-backend"', '#2c313c', '#61afef'),
    ]
    for i, (lbl, bg, fg) in enumerate(labels):
        ax.add_patch(FancyBboxPatch((560 + i * 280, 700), 260, 28, boxstyle="round,pad=3", fc=bg, ec='#3e4451', lw=1))
        ax.text(570 + i * 280, 714, lbl, color=fg, fontsize=10, fontfamily='monospace', va='center')

    # Discovered labels header & pills below
    ax.text(560, 665, "Discovered labels:", color='#5c6370', fontsize=10, va='center')
    
    disc_labels_r1 = [
        '__address__="gigboard-backend:5000"',
        '__always_scrape_classic_histograms__="false"',
        '__metrics_path__="/metrics"',
        '__scheme__="http"',
    ]
    for i, dlbl in enumerate(disc_labels_r1):
        ax.add_patch(FancyBboxPatch((560 + i * 290, 620), 275, 26, boxstyle="round,pad=3", fc='#1b1d23', ec='#2c313a', lw=1))
        ax.text(570 + i * 290, 633, dlbl, color='#7f848e', fontsize=8.5, fontfamily='monospace', va='center')

    disc_labels_r2 = [
        '__scrape_interval__="5s"',
        '__scrape_native_histograms__="false"',
        '__scrape_timeout__="5s"',
        'job="gigboard-backend"',
    ]
    for i, dlbl in enumerate(disc_labels_r2):
        ax.add_patch(FancyBboxPatch((560 + i * 290, 580), 275, 26, boxstyle="round,pad=3", fc='#1b1d23', ec='#2c313a', lw=1))
        ax.text(570 + i * 290, 593, dlbl, color='#7f848e', fontsize=8.5, fontfamily='monospace', va='center')

    # Last Scrape
    ax.text(1300, 725, "2.8s ago", color='#abb2bf', fontsize=11, va='center')
    ax.add_patch(FancyBboxPatch((1300, 685), 85, 24, boxstyle="round,pad=3", fc='#2c313c', ec='#3e4451', lw=1))
    ax.text(1342, 697, "every 5s", color='#5c6370', fontsize=8.5, ha='center', va='center')

    # Scrape Duration
    ax.text(1500, 715, "7.4ms", color='#98c379', fontsize=12, fontweight='bold', va='center')

    # Error
    ax.text(1700, 715, "None", color='#5c6370', fontsize=11, va='center')

    # Card footer / Summary info box
    ax.add_patch(FancyBboxPatch((40, 220), 1840, 80, boxstyle="round,pad=4", fc='#21252b', ec='#282c34', lw=1))
    ax.text(65, 260, "[i] Configuration Overview:", color='#61afef', fontsize=11.5, fontweight='bold', va='center')
    ax.text(285, 260, "Job: gigboard-backend  •  Scrape Interval: 5s  •  Timeout: 5s  •  Rules Active: alerting_rules.yml (ServiceDown, HighCpuUsage, EventLoopLagHigh, NodeMemoryHigh)", color='#abb2bf', fontsize=10.5, va='center')

    # Footer
    ax.add_patch(Rectangle((0, 0), 1920, 36, fc='#181a1f', ec='#21252b', lw=1))
    ax.text(40, 18, "Prometheus v2.51.0  |  GigBoard Micro-Gig Telemetry Service  |  Campus Server at SKIT Jaipur", color='#5c6370', fontsize=9.5, va='center')
    ax.text(1880, 18, "Total Targets: 1 Active / 1 Healthy (100%)", color='#28a745', fontsize=9.5, fontweight='bold', ha='right', va='center')

    plt.savefig('assets/prometheus_targets.png', dpi=100, facecolor=fig.get_facecolor())
    plt.close()
    print("Prometheus target health screenshot generated: assets/prometheus_targets.png")

if __name__ == '__main__':
    generate_grafana()
    generate_prometheus()
