"""Fix assets: convert grafana JPG to proper PNG, verify prometheus PNG."""
import shutil, os
from PIL import Image

grafana_jpg = r'C:\Users\LENOVO\.gemini\antigravity\brain\73fc6ae9-a033-40ec-bf7c-a136729a8dff\.user_uploaded\media_1793209468861_91f06208.jpg'
prometheus_png = r'C:\Users\LENOVO\.gemini\antigravity\brain\73fc6ae9-a033-40ec-bf7c-a136729a8dff\.user_uploaded\media_1793209484109_f01d7233.png'

os.makedirs('assets', exist_ok=True)

# Convert grafana JPG to proper PNG
img = Image.open(grafana_jpg)
img.save('assets/grafana_dashboard.png', 'PNG')
size = os.path.getsize('assets/grafana_dashboard.png')
print(f'Grafana saved as PNG: {size} bytes')

# Copy prometheus PNG (already valid)
shutil.copy2(prometheus_png, 'assets/prometheus_targets.png')
size2 = os.path.getsize('assets/prometheus_targets.png')
print(f'Prometheus PNG copied: {size2} bytes')

# Verify magic bytes
for f in ['assets/grafana_dashboard.png', 'assets/prometheus_targets.png', 'assets/evaluation_trends.png']:
    with open(f, 'rb') as fh:
        magic = fh.read(8).hex()
    valid = magic.startswith('89504e47')
    print(f'{f}: magic={magic} valid_png={valid}')
