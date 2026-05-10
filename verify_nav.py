import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('Merchant Nav Tabs')
if idx > 0:
    section = html[idx:idx+15000]
    remaining = re.findall(r'data-i18n="([^"]+)"', section)
    print(f'Remaining data-i18n in merchant area: {len(remaining)}')
    for r in remaining:
        print(f'  - {r}')

mi18n = re.findall(r'data-mi18n="([^"]+)"', html)
print(f'\nTotal data-mi18n in file: {len(mi18n)}')

# Also verify the nav section looks correct
nav_start = html.find('merchant-nav')
if nav_start > 0:
    nav_html = html[nav_start:nav_start+1500]
    with open('nav_verify.txt', 'w', encoding='utf-8') as out:
        out.write(nav_html)
    print('\nNav section saved to nav_verify.txt')
