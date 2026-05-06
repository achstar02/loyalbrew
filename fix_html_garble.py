import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Fix all ï¿½ garbled chars - these were originally · (middle dot) or similar
replacements = {
    'ï¿½': '·',           # Main replacement: middle dot
    'LoyalBrew ï¿½ Loyalty': 'LoyalBrew · Loyalty',
    'ï¿½ LoyalBrew': '© LoyalBrew',
    'Bank: ï¿½ &nbsp;|&nbsp; Acc: ï¿½': 'Bank: — | Acc: —',
    "Name: ï¿½": 'Name: —',
    "I've Paid ï¿½ Notify Kitchen": "I've Paid · Notify Kitchen",
    '(optional ï¿½ for off-': '(optional · for off-',
    '5% ï¿½ <span credited_to_referrer_s_wal': '5% · <span credited_to_referrer_s_wal',
    'Landing Page ï¿½ Welcome Text / ???': 'Landing Page · Welcome Text',
    'Landing Page ï¿½ Main Title / ???': 'Landing Page · Main Title',
    '750ï¿½300px': '750×300px',
    'done ï¿½ no waiting around': 'done · no waiting around',
}

count = 0
for old, new in replacements.items():
    if old in c:
        c = c.replace(old, new)
        count += 1
        print(f'  Fixed: {old[:40]} -> {new[:40]}')

# Also fix data-i18n text content with ??
c = c.replace('Enter your phone &amp; tap ?? to earn points', 'Enter your phone &amp; tap + to earn points')
c = c.replace('Save Shop Info / ??????', 'Save Shop Info')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f'\nTotal fixes applied: {count}')
print(f'File size: {len(c):,} bytes')
