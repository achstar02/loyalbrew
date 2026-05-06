import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# The screenshot shows an ORANGE header bar + orange member card
# Let's find the app-header / header styling
print("=== Searching for orange header ===")
for t in ['app-header', 'bg-gradient-to-r from-[#FF', 'from-[#ff8c00]', 'from-[#F97316]', 'orange-500', 'orange-600']:
    cnt = c.count(t)
    if cnt:
        print(f"  {t}: {cnt}x")

# Find the actual CSS or inline style for headers
print("\n=== app-header in style/css ===")
# Check if there's a .app-header style
import re
for m in re.finditer(r'\.app-header[^{]*\{[^}]+\}', c):
    print(m.group()[:200])
    
for m in re.finditer(r'\.customer-header[^{]*\{[^}]+\}', c):
    print(m.group()[:200])

# Find the orange top bar - it might be in a <style> block
print("\n=== Looking for #ff8c00 / F97316 / orange gradient ===")
for t in ['#ff8c00', '#F97316', '#f97316', '#FF6B00', '#ff6b00']:
    if t.lower() in c.lower():
        idx = c.lower().find(t.lower())
        print(f"  Found '{t}' at {idx}: ...{c[max(0,idx-40):idx+60]}...")
