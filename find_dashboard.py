import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the customer dashboard (logged-in view) - has the orange member card
idx = c.find('id="customer-dashboard"')
if idx >= 0:
    print("=== customer-dashboard (first 3000 chars) ===")
    print(c[idx:idx+3000])
else:
    # Try finding where the orange card renders
    print("customer-dashboard not found, searching for dashboard...")
    for t in ['customer-info', 'user-profile', 'dashboard-content', 'profile-view']:
        idx = c.find(t)
        if idx >= 0:
            print(f"Found '{t}' at {idx}:")
            print(c[idx:idx+500])
            break
