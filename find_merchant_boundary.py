import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for marker in ['<!-- Merchant Nav', 'Merchant Nav', 'merchant-nav', '<!-- Customer', '<!-- App Init', '<!-- Firebase', '<!-- Navigation']:
    pos = html.find(marker)
    print(f'{marker}: {pos}')
