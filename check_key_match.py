"""
Check: which data-i18n keys in merchant HTML are NOT in MERCHANT_LANGS
and which data-mi18n keys ARE in MERCHANT_LANGS
"""
import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
HTML = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# Get all MERCHANT_LANGS keys (all 4 languages)
ml_pos = js.find('const MERCHANT_LANGS')
ml_en_keys = set(re.findall(r"(\w+):\s*'", js[ml_pos:ml_pos+8000]))
# Remove non-key matches
ml_en_keys = {k for k in ml_en_keys if not k.startswith('_') and len(k) > 2 and k != 'var' and k != 'function' and k != 'return'}

print(f'MERCHANT_LANGS.en has {len(ml_en_keys)} keys')
print(f'Sample: {sorted(ml_en_keys)[:20]}')

# Get all data-i18n keys from HTML
i18n_keys = re.findall(r'data-i18n="([^"]+)"', html)
unique_i18n = sorted(set(i18n_keys))
print(f'\nHTML data-i18n: {len(i18n_keys)} total, {len(unique_i18n)} unique')

# Categorize
in_merchant = []
not_in_merchant = []
for k in unique_i18n:
    if k in ml_en_keys:
        in_merchant.append(k)
    else:
        not_in_merchant.append(k)

print(f'\n=== Keys IN MERCHANT_LANGS ({len(in_merchant)}) ===')
for k in in_merchant[:30]:
    print(f'  OK: {k}')
if len(in_merchant) > 30:
    print(f'  ... and {len(in_merchant)-30} more')

print(f'\n=== Keys NOT in MERCHANT_LANGS ({len(not_in_merchant)}) ===')
for k in not_in_merchant:
    print(f'  MISSING: {k}')

# Also check data-mi18n
mi18n_keys = re.findall(r'data-mi18n="([^"]+)"', html)
print(f'\n=== HTML data-mi18n ({len(mi18n_keys)}) ===')
for k in mi18n_keys:
    in_ml = k in ml_en_keys
    print(f'  {"OK" if in_ml else "MISS"}: {k}')
