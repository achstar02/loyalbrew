import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.index('filterComplaints')
rest = html[idx:]
old = " all>All</button>"
new = ' all data-i18n="filterAllC">All</button>'
fixed = rest.replace(old, new, 1)
new_html = html[:idx] + fixed

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'Done! filterAllC count: {new_html.count("filterAllC")}')
