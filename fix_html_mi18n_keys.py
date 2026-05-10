"""
Fix merchant dashboard i18n by renaming data-mi18n attributes to match 
actual keys in MERCHANT_LANGS object.

Strategy: For each data-mi18n attribute in the HTML, check if the key exists in 
MERCHANT_LANGS.en. If not, try to find the correct m-prefixed key and rename it.
"""
import re

HTML_PATH = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html'
JS_PATH = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all keys from MERCHANT_LANGS.en block
ml_start = js.find('const MERCHANT_LANGS')
en_start = js.find('en:', ml_start)
depth = 0
i = en_start + 2
while i < len(js) and depth >= 0:
    if js[i] == '{': depth += 1
    elif js[i] == '}': 
        depth -= 1
        if depth == 0: break
    i += 1
en_block = js[en_start+2:i]

# Extract all m-prefixed keys from EN block
merchant_keys = set()
for m in re.finditer(r"(m[A-Za-z_0-9]+)\s*:", en_block):
    merchant_keys.add(m.group(1))

print(f'Found {len(merchant_keys)} keys in MERCHANT_LANGS.en')
print('Sample:', list(merchant_keys)[:10])

# Build a mapping: unprefixed -> m-prefixed (for common nav/label keys)
key_map = {}
for mk in merchant_keys:
    # Try removing common prefixes
    for prefix in ['mTab', 'mStat', 'mBtn', 'mTitle', 'mLabel', 'm', 'mPh']:
        if mk.startswith(prefix) and len(mk) > len(prefix):
            unprefixed = mk[len(prefix):].lower() if prefix == 'm' else mk[len(prefix):]
            key_map[unprefixed] = mk
            break

print(f'\nKey map ({len(key_map)} entries):')
for k, v in sorted(key_map.items())[:30]:
    print(f'  {k} -> {v}')

# Now find all data-mi18n attributes in HTML and check which need fixing
mi18n_attrs = re.findall(r'data-mi18n="([^"]*)"', html)
print(f'\nTotal data-mi18n attrs in HTML: {len(mi18n_attrs)}')

needs_fix = []
already_ok = []
for key in mi18n_attrs:
    if key in merchant_keys:
        already_ok.append(key)
    elif key in key_map:
        needs_fix.append((key, key_map[key]))
    else:
        # Check if it's already an m-prefixed key that just doesn't exist
        print(f'  UNKNOWN KEY: "{key}"')

print(f'\nAlready OK (in MERCHANT_LANGS): {len(already_ok)}')
print(f'Needs fix (remap): {len(needs_fix)}')
for old_key, new_key in needs_fix[:30]:
    print(f'  {old_key} -> {new_key}')

# Apply fixes to HTML
fix_count = 0
for old_key, new_key in needs_fix:
    html = html.replace(f'data-mi18n="{old_key}"', f'data-mi18n="{new_key}"')
    fix_count += 1

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nFixed {fix_count} attributes in HTML!')
print('Done.')
