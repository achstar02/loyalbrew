import re

html_path = 'C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Merchant section: from "<!-- Merchant Nav" to "<!-- Firebase init"
merchant_start = html.find('<!-- Merchant Nav')
firebase_start = html.find('<!-- Firebase init')

if merchant_start == -1 or firebase_start == -1:
    print(f'ERROR: merchant_start={merchant_start}, firebase_start={firebase_start}')
    exit(1)

print(f'Merchant section: {merchant_start} - {firebase_start}')
print(f'Length: {firebase_start - merchant_start} chars')

# Apply fix ONLY to merchant section
merchant_html = html[merchant_start:firebase_start]
customer_html = html[firebase_start:]

def replacer(match):
    key = match.group(1)
    return f'data-mi18n="{key}"'

new_merchant, n = re.subn(r'data-i18n="([^"]+)"', replacer, merchant_html)

# Verify customer section is NOT affected
customer_i18n = re.findall(r'data-i18n="([^"]+)"', customer_html)
print(f'Customer data-i18n (should be unchanged): {len(customer_i18n)}')
if customer_i18n:
    for r in customer_i18n[:5]:
        print(f'  WARNING: {r}')

html = html[:merchant_start] + new_merchant + customer_html

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nReplaced {n} data-i18n -> data-mi18n in merchant area')

# Final verification
remaining = re.findall(r'data-i18n="([^"]+)"', html[merchant_start:])
print(f'Remaining data-i18n in merchant: {len(remaining)}')
total_mi18n = re.findall(r'data-mi18n="([^"]+)"', html)
print(f'Total data-mi18n in file: {len(total_mi18n)}')
print('Done!')
