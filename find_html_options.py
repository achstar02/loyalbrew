import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Search for stamp rule options in HTML
print('=== Searching index.html for stamp dropdown options ===')
patterns = [
    r'Every purchase',
    r'per_order',
    r'mRulePerOrder',
    r'free_item',
    mRewardFreeItem,
    r'stamp.*rule',
    r'per_amount',
    r'1 stamp',
]
for pat in patterns:
    matches = list(re.finditer(pat, html, re.IGNORECASE))
    if matches:
        print(f'\n"{pat}": {len(matches)} matches')
        for m in matches[:3]:
            start = max(0, m.start()-50)
            end = min(len(html), m.end()+80)
            print(f'  ...{html[start:end]}...')
    else:
        print(f'"{pat}": NOT FOUND')

# Also search for the Chinese text we see
print('\n=== Searching for Chinese text ===')
cn_patterns = [r'每消费', r'1印章', r'免费菜单']
for pat in cn_patterns:
    matches = list(re.finditer(pat, html))
    if matches:
        print(f'\n"{pat}": {len(matches)} matches')
        for m in matches[:2]:
            start = max(0, m.start()-40)
            end = min(len(html), m.end()+60)
            print(f'  ...{html[start:end]}...')
