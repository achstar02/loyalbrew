import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# The orange header must be styled via CSS class .app-header
# Let's find ALL style content
import re
all_styles = ''
for m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
    all_styles += m.group(1) + '\n'

print("=== All CSS with 'header' ===")
for line in all_styles.split('\n'):
    line = line.strip()
    if line and ('header' in line.lower() or 'app-' in line.lower()):
        print(line)

# Also check for the member card (orange card with Bronze badge)
print("\n=== Searching for member profile card ===")
for term in ['rounded-2xl bg-gradient', 'member-info', 'profile-card', 'user-card']:
    if term in c:
        idx = c.find(term)
        print(f"\n'{term}' at {idx}:")
        print(c[idx:idx+300])
