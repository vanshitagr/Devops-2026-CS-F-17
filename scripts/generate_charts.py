"""Generate professional evaluation trends chart for the README."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('assets', exist_ok=True)

# Sprint data
sprints = ['Sprint 1\n(Aug 24–Sep 05)', 'Sprint 2\n(Sep 06–Sep 19)', 'Sprint 3\n(Sep 20–Oct 05)', 
           'Sprint 4\n(Oct 06–Oct 20)', 'Sprint 5\n(Oct 21–Oct 29)']
vanshita_commits = [6, 10, 9, 3, 5]
utkarsh_commits  = [6, 8, 14, 0, 1]

x = np.arange(len(sprints))
width = 0.35

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#1a1a2e')

# --- Chart 1: Sprint Commits Bar Chart ---
ax1 = axes[0]
ax1.set_facecolor('#16213e')
bars1 = ax1.bar(x - width/2, vanshita_commits, width, label='vanshitagr', color='#e94560', zorder=3)
bars2 = ax1.bar(x + width/2, utkarsh_commits,  width, label='Utkarsh Hinger', color='#0f3460', zorder=3)

ax1.set_xlabel('Sprint / Milestone', color='#eaeaea', fontsize=11)
ax1.set_ylabel('Number of Commits', color='#eaeaea', fontsize=11)
ax1.set_title('Commit Activity per Sprint (CS-F-17)', color='white', fontsize=13, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(sprints, color='#cccccc', fontsize=8.5)
ax1.tick_params(colors='#cccccc')
ax1.spines['bottom'].set_color('#444')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#444')
ax1.yaxis.label.set_color('#eaeaea')
ax1.grid(axis='y', color='#333', linestyle='--', alpha=0.5, zorder=0)
ax1.set_ylim(0, 20)

for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3, 
             str(int(bar.get_height())), ha='center', va='bottom', color='#e94560', fontsize=9, fontweight='bold')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
             str(int(bar.get_height())), ha='center', va='bottom', color='#4fc3f7', fontsize=9, fontweight='bold')

ax1.legend(facecolor='#1a1a2e', edgecolor='#444', labelcolor='white', fontsize=10)

# --- Chart 2: Cumulative LOC Line Chart ---
ax2 = axes[1]
ax2.set_facecolor('#16213e')

weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11']
vanshita_loc = [800, 2100, 4200, 7500, 10200, 12800, 15600, 18900, 21400, 24200, 25840]
utkarsh_loc  = [600, 1800, 3900, 6800,  9400, 11700, 14200, 16800, 18000, 18700, 18920]

ax2.plot(weeks, vanshita_loc, color='#e94560', linewidth=2.5, marker='o', markersize=6, label='vanshitagr', zorder=3)
ax2.plot(weeks, utkarsh_loc,  color='#4fc3f7', linewidth=2.5, marker='s', markersize=6, label='Utkarsh Hinger', zorder=3)
ax2.fill_between(weeks, vanshita_loc, alpha=0.15, color='#e94560')
ax2.fill_between(weeks, utkarsh_loc,  alpha=0.15, color='#4fc3f7')

ax2.set_xlabel('Weekly Milestone', color='#eaeaea', fontsize=11)
ax2.set_ylabel('Cumulative Lines Added', color='#eaeaea', fontsize=11)
ax2.set_title('Cumulative LOC Contribution by Week', color='white', fontsize=13, fontweight='bold', pad=12)
ax2.set_xticklabels(weeks, rotation=35, ha='right', color='#cccccc', fontsize=8.5)
ax2.tick_params(colors='#cccccc')
ax2.spines['bottom'].set_color('#444')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#444')
ax2.grid(color='#333', linestyle='--', alpha=0.5, zorder=0)
ax2.legend(facecolor='#1a1a2e', edgecolor='#444', labelcolor='white', fontsize=10)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, _: f'{int(val):,}'))

# Annotations
ax2.annotate('25,840 LOC', xy=(weeks[-1], 25840), xytext=(weeks[-2], 24000),
             color='#e94560', fontsize=8, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#e94560', lw=1.5))
ax2.annotate('18,920 LOC', xy=(weeks[-1], 18920), xytext=(weeks[-2], 17200),
             color='#4fc3f7', fontsize=8, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#4fc3f7', lw=1.5))

# Footer
fig.text(0.5, 0.01, 'DevOps-2026-CS-F-17 | Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur (SKIT)',
         ha='center', color='#888888', fontsize=8)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('assets/evaluation_trends.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('evaluation_trends.png generated successfully')

import os
size = os.path.getsize('assets/evaluation_trends.png')
print(f'File size: {size} bytes')
