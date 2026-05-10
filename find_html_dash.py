import re
with open('deploy/index.html','r',encoding='utf-8') as f:
    html = f.read()
# Search for nav tabs, stat cards, quick actions in HTML
for pattern in [r'mnav.*overview', r'stat-members', r'viewOrders2', r'quickActions', r'mtab.*overview', r'class="mnav"']:
    m = re.search(pattern, html)
    if m:
        pos = m.start()
        print(f'=== {pattern} at {pos} ===')
        print(html[max(0,pos-100):pos+200])
        print('---')
