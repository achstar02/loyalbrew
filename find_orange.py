import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the member card / dashboard area (after login)
# Look for "Bronze" or member card display
idx = c.find('customer-dashboard')
if idx < 0:
    idx = c.find('member-card')
if idx < 0:
    idx = c.find('Bronze')
    
# Search for the orange gradient card that shows user info
terms = ['from-[#f97316]', 'from-orange-', 'to-[#ea580c]', '#FF6B00', 'bg-gradient-to-br from-[#ff']
for t in terms:
    positions = []
    start = 0
    while True:
        pos = c.find(t, start)
        if pos < 0:
            break
        positions.append(pos)
        start = pos + 1
    if positions:
        print(f"  '{t}' found at {len(positions)} positions: {positions}")
        for p in positions[:2]:
            print(f"    context: ...{c[max(0,p-30):p+60]}...")

# Also search for the header bar (orange strip at top)
print("\n=== customer-header ===")
idx2 = c.find('customer-header')
if idx2 >= 0:
    print(c[idx2:idx2+200])
