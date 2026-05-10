import re

html_path = 'C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the merchant dashboard area
idx = html.find('Merchant Nav Tabs')
if idx == 0:
    print('ERROR: Merchant Nav Tabs not found!')
    exit(1)

# Find end of merchant area (end of file or start of customer area)
# We'll process a large section from nav tabs to end
merchant_section_start = idx
merchant_section_end = len(html)

# Replace ALL remaining data-i18n with data-mi18n in the merchant area
section = html[merchant_section_start:merchant_section_end]

count = 0
def replacer(match):
    global count
    count += 1
    key = match.group(1)
    return f'data-mi18n="{key}"'

new_section, n = re.subn(r'data-i18n="([^"]+)"', replacer, section)
html = html[:merchant_section_start] + new_section + html[merchant_section_end:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Replaced {n} more data-i18n -> data-mi18n in merchant area')

# Verify no data-i18n remains in merchant area
remaining = re.findall(r'data-i18n="([^"]+)"', html[merchant_section_start:])
print(f'Remaining data-i18n: {len(remaining)}')
for r in remaining[:10]:
    print(f'  - {r}')

mi18n_total = re.findall(r'data-mi18n="([^"]+)"', html)
print(f'\nTotal data-mi18n in file: {len(mi18n_total)}')
print('Done!')
