"""
COMPLETE I18N DIAGNOSTIC for LoyalBrew
Checks both LANGS (customer) and MERCHANT_LANGS (merchant) objects
for missing/corrupted translations across all 4 languages.
"""
import re, json

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

print(f'File size: {len(js)} chars')
print()

# ====== 1. Find LANGS object (customer) ======
langs_pos = js.find('const LANGS')
if langs_pos == -1:
    print('ERROR: LANGS not found!')
else:
    print(f'=== CUSTOMER LANGS (at {langs_pos}) ===')
    # Find en/zh/ms/ta blocks within LANGS
    # Look for the first occurrence of each after langs_pos
    en_match = re.search(r'\ben\s*:\s*\{', js[langs_pos:])
    zh_match = re.search(r'\bzh\s*:\s*\{', js[langs_pos:])
    ms_match = re.search(r'\bms\s*:\s*(null|\{)', js[langs_pos:])
    ta_match = re.search(r'\bta\s*:\s*\{', js[langs_pos:])
    
    if en_match:
        print(f'  en: at offset {en_match.start()}')
    if zh_match:
        print(f'  zh: at offset {zh_match.start()}')
    else:
        print('  zh: NOT FOUND!')
    if ms_match:
        print(f'  ms: at offset {ms_match.start()} ({js[langs_pos+ms_match.start():langs_pos+ms_match.start()+20]})')
    if ta_match:
        print(f'  ta: at offset {ta_match.start()}')

# ====== 2. Find MERCHANT_LANGS object ======
ml_pos = js.find('const MERCHANT_LANGS')
if ml_pos == -1:
    print('\nERROR: MERCHANT_LANGS not found!')
else:
    print(f'\n=== MERCHANT_LANGS (at {ml_pos}) ===')
    # Find all language blocks
    for lang_name in ['en', 'zh', 'ms', 'ta']:
        pattern = rf'^\s+{lang_name}\s*:\s*\{{'
        match = re.search(pattern, js[ml_pos:], re.MULTILINE)
        if match:
            start = ml_pos + match.start()
            # Count keys in this block
            block_start = match.end() + ml_pos
            # Find matching closing brace
            depth = 1
            pos = block_start
            while depth > 0 and pos < len(js):
                if js[pos] == '{': depth += 1
                elif js[pos] == '}': depth -= 1
                pos += 1
            block_content = js[block_start:pos-1]
            key_count = len(re.findall(r"[\w]+:", block_content))
            print(f'  {lang_name}: at {start}, {key_count} keys, block size={pos-block_start}')
        else:
            print(f'  {lang_name}: NOT FOUND!')

# ====== 3. Check mt() function ======
mt_pos = js.find('function mt(')
if mt_pos != -1:
    print(f'\n=== mt() function (at {mt_pos}) ===')
    print(js[mt_pos:mt_pos+500])
else:
    print('\n=== mt() function: NOT FOUND! ===')

# ====== 4. Check applyMerchantLang function =====+
aml_pos = js.find('function applyMerchantLang')
if aml_pos != -1:
    print(f'\n=== applyMerchantLang (at {aml_pos}) ===')
    print(js[aml_pos:aml_pos+800])
else:
    print('\napplyMerchantLang: NOT FOUND!')

# ====== 5. Check data-mi18n usage in index.html ======
HTML = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html'
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

mi18n_count = len(re.findall(r'data-mi18n=', html))
i18n_count = len(re.findall(r'data-i18n=', html))
print(f'\n=== index.html attributes ===')
print(f'  data-mi18n: {mi18n_count} occurrences')
print(f'  data-i18n: {i18n_count} occurrences')

# Sample some data-mi18n keys
mi18n_keys = re.findall(r'data-mi18n="([^"]+)"', html)
unique_keys = sorted(set(mi18n_keys))
print(f'  Unique data-mi18n keys: {len(unique_keys)}')
for k in unique_keys[:30]:
    count = mi18n_keys.count(k)
    print(f'    {k} ({count}x)')
if len(unique_keys) > 30:
    print(f'    ... and {len(unique_keys)-30} more')
