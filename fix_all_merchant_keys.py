"""
COMPLETE FIX: Add all missing merchant HTML keys to MERCHANT_LANGS
This script:
1. Extracts all data-i18n keys from index.html
2. For each missing key, adds it to MERCHANT_LANGS en/zh/ms/ta blocks
3. Uses existing LANGS (customer) translations as source where available
4. Validates syntax before saving
"""
import re, copy

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
HTML = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# Backup
with open(JS + '.bak_fix', 'w', encoding='utf-8') as f:
    f.write(js)
print(f'Backup saved: {JS}.bak_fix ({len(js)} chars)')

# ====== Step 1: Get all data-i18n keys from HTML ======
html_keys = sorted(set(re.findall(r'data-i18n="([^"]+)"', html)))
print(f'HTML data-i18n keys: {len(html_keys)}')

# ====== Step 2: Get existing MERCHANT_LANGS keys per language ======
ml_pos = js.find('const MERCHANT_LANGS')

def get_ml_block(lang_name):
    """Find a language block in MERCHANT_LANGS and return (start, end, keys_dict)"""
    pattern = rf'^(\s+)({lang_name})\s*:\s*\{{'
    match = re.search(pattern, js[ml_pos:], re.MULTILINE)
    if not match:
        return None, None, {}, 0
    block_start_ml = ml_pos + match.end()
    indent = match.group(1)
    
    # Find closing brace
    depth = 1
    pos = block_start_ml
    while depth > 0 and pos < len(js):
        if js[pos] == '{': depth += 1
        elif js[pos] == '}': depth -= 1
        pos += 1
    block_end = pos - 1
    block_content = js[block_start_ml:block_end]
    
    # Parse key:value pairs
    keys = {}
    for m in re.finditer(r"([\w]+)\s*:\s*'([^']*)'", block_content):
        keys[m.group(1)] = m.group(2)
    
    return ml_pos + match.start(), block_end, keys, len(indent)

en_start, en_end, en_keys, en_indent = get_ml_block('en')
zh_start, zh_end, zh_keys, zh_indent = get_ml_block('zh')
ms_start, ms_end, ms_keys, ms_indent = get_ml_block('ms')
ta_start, ta_end, ta_keys, ta_indent = get_ml_block('ta')

print(f'MERCHANT_LANGS keys: en={len(en_keys)}, zh={len(zh_keys)}, ms={len(ms_keys)}, ta={len(ta_keys)}')

# ====== Step 3: Get translations from customer LANGS ======
langs_pos = js.find('const LANGS')

def get_lang_block(lang_name):
    """Get all key:value pairs from customer LANGS for a language"""
    # Find the lang block - search after langs_pos
    pattern = rf'^\s+{lang_name}\s*:\s*\{{'
    match = re.search(pattern, js[langs_pos:], re.MULTILINE)
    if not match:
        return {}
    start = langs_pos + match.end()
    depth = 1
    pos = start
    while depth > 0 and pos < len(js):
        if js[pos] == '{': depth += 1
        elif js[pos] == '}': depth -= 1
        pos += 1
    content = js[start:pos-1]
    keys = {}
    for m in re.finditer(r"([\w]+)\s*:\s*'([^']*)'", content):
        keys[m.group(1)] = m.group(2)
    return keys

cust_en = get_lang_block('en')
cust_zh = get_lang_block('zh')
cust_ms = get_lang_block('ms')
cust_ta = get_lang_block('ta')
print(f'Customer LANGS keys: en={len(cust_en)}, zh={len(cust_zh)}, ms={len(cust_ms)}, ta={len(cust_ta)}')

# ====== Step 4: Build translation dictionaries for missing keys ======
missing_keys = [k for k in html_keys if k not in en_keys]
print(f'\nMissing from MERCHANT_LANGS: {len(missing_keys)} out of {len(html_keys)}')

# For each missing key, try to get translation from customer LANGS
# If not in customer LANGS either, use English value as fallback
translations = {}  # key -> {en, zh, ms, ta}

for k in missing_keys:
    t = {
        'en': cust_en.get(k, k),
        'zh': cust_zh.get(k, cust_en.get(k, k)),
        'ms': cust_ms.get(k, cust_en.get(k, k)),
        'ta': cust_ta.get(k, cust_en.get(k, k)),
    }
    translations[k] = t

# Also add keys that ARE in MERCHANT_LANGS but might be in HTML too (already covered)
# Just focus on missing ones

print(f'\nTranslation samples:')
for k in list(missing_keys)[:10]:
    t = translations[k]
    import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print(f'  {k}: en="{t["en"][:30]}" zh="{t["zh"][:30]}"')

# ====== Step 5: Inject missing keys into each MERCHANT_LANGS block ======
def inject_keys(block_start, block_end, existing_keys, new_translations, lang_name, indent):
    """Generate new block content with added keys"""
    # Read original block
    original = js[block_start:block_end]
    
    # Find the last key:value pair to know where to insert
    # Find position of last 'key': 'value' before closing
    lines = original.rstrip().rstrip(',').rstrip().split('\n')
    
    # Build new entries string
    new_entries = []
    for k in missing_keys:
        if k not in existing_keys:
            val = new_translations[k][lang_name]
            # Escape single quotes in value
            val = val.replace("'", "\\'")
            new_entries.append(f"{indent}  {k}: '{val}',")
    
    if not new_entries:
        return original, 0
    
    # Append new entries before closing
    new_content = original.rstrip().rstrip(',') + ',\n' + '\n'.join(new_entries) + '\n'
    return new_content, len(new_entries)

print('\n=== Injecting keys ===')

new_en, n_en = inject_keys(en_start, en_end, en_keys, translations, 'en', ' ' * int(en_indent))
new_zh, n_zh = inject_keys(zh_start, zh_end, zh_keys, translations, 'zh', ' ' * int(zh_indent))
new_ms, n_ms = inject_keys(ms_start, ms_end, ms_keys, translations, 'ms', ' ' * int(ms_indent))
new_ta, n_ta = inject_keys(ta_start, ta_end, ta_keys, translations, 'ta', ' ' * int(ta_indent))

print(f'  en: +{n_en} keys')
print(f'  zh: +{n_zh} keys')
print(f'  ms: +{n_ms} keys')
print(f'  ta: +{n_ta} keys')

# ====== Step 6: Rebuild file ======
new_js = (
    js[:en_start] + 
    new_en + 
    js[en_end:zh_start] +
    new_zh +
    js[zh_end:ms_start] +
    new_ms +
    js[ms_end:ta_start] +
    new_ta +
    js[ta_end:]
)

print(f'\nOriginal size: {len(js)}')
print(f'New size:      {len(new_js)}')

# ====== Step 7: Validate syntax =====+
import subprocess, tempfile
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
tmp.write(new_js)
tmp.close()

result = subprocess.run(['node', '-e', f'try {{ new Function(require("fs").readFileSync("{tmp.name.replace("\\","/")}", "utf-8")); console.log("SYNTAX OK") }} catch(e) {{ console.log("SYNTAX ERROR:", e.message) }}'], capture_output=True, text=True)
print(f'\nSyntax check: {result.stdout.strip()}')
if result.stderr:
    print(f'Stderr: {result.stderr.strip()[:200]}')

if 'SYNTAX OK' in result.stdout:
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(new_js)
    print(f'\n✅ SAVED! All {len(missing_keys)} missing keys injected into MERCHANT_LANGS.')
else:
    print('\n❌ Syntax error! File NOT saved. Check the error above.')
    # Cleanup temp file
    import os
    os.unlink(tmp.name)
