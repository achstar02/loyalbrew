import re

HTML = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html', 'r', encoding='utf-8').read()

# Find data-i18n
di = re.findall(r'data-i18n="([^"]+)"', HTML)
print(f'data-i18n count: {len(di)}')
print('First 30:', di[:30])

# Look for overview tab HTML
for term in ['tab-overview', 'overview-panel', 'id="stat-members"', 'overview', 'merchantDashboard', 'merchantAdminHTML']:
    pos = HTML.find(term)
    if pos >= 0:
        print(f'\nFound "{term}" at {pos}:')
        print(HTML[pos-50:pos+300])
        print()

# Check if merchant HTML is in app.js instead
JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
for term in ['tab-overview', 'stat-members', 'merchant-header', 'loadMerchantDashboard']:
    pos = JS.find(term)
    if pos >= 0:
        print(f'In app.js, "{term}" at {pos}:')
        print(JS[pos-100:pos+200])
        print()