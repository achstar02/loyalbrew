import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

targets = ['member-card', 'app-header', 'btn-topup', 'btn-stamp', 'btn-outline', '.tier-', 'section-card']
print("=== Relevant CSS in style.css ===")
for line in c.split('\n'):
    line = line.strip()
    if any(t in line.lower() for t in targets):
        print(line)
