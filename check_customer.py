import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find page-customer section
idx = c.find('id="page-customer"')
if idx >= 0:
    snippet = c[idx:idx+2000]
    print("=== page-customer (first 2000 chars) ===")
    print(snippet)
else:
    print("page-customer NOT found")

# Also find the member card area (orange card showing Bronze/points)
print("\n\n=== Looking for orange member card ===")
for term in ['from-[#ff', 'to-orange', 'bg-orange', '#FF6B00', 'orange-500', 'orange-400']:
    count = c.count(term)
    if count > 0:
        print(f"  {term}: {count}x")
