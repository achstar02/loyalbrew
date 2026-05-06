import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find all CSS for member-card, app-header, btn-topup, etc.
all_css = ''
for m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
    all_css += m.group(1) + '\n'

targets = ['member-card', 'app-header', 'btn-topup', 'btn-stamp', 'btn-outline', 'customer-header', '.tier-', 'section-card']
print("=== Relevant CSS ===")
for line in all_css.split('\n'):
    line = line.strip()
    if any(t in line.lower() for t in targets):
        print(line)
