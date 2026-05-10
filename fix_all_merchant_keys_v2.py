"""
COMPLETE FIX v2: Add all missing merchant HTML keys to MERCHANT_LANGS
- Properly escapes all special characters in translation values
- Validates syntax before saving
- Uses UTF-8 output
"""
import re, subprocess, tempfile, os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
HTML = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\index.html'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# Backup
with open(JS + '.bak_fix2', 'w', encoding='utf-8') as f:
    f.write(js)
print(f'Backup saved ({len(js)} chars)')

# ====== Step 1: Get all data-i18n keys from HTML ======
html_keys = sorted(set(re.findall(r'data-i18n="([^"]+)"', html)))
print(f'HTML data-i18n keys: {len(html_keys)}')

# ====== Step 2: Get existing MERCHANT_LANGS blocks =====+
ml_pos = js.find('const MERCHANT_LANGS')

def get_ml_block(lang_name):
    pattern = rf'^(\s+)({lang_name})\s*:\s*\{{'
    match = re.search(pattern, js[ml_pos:], re.MULTILINE)
    if not match:
        return None, None, {}, 0
    block_start_ml = ml_pos + match.end()
    indent = match.group(1)
    depth = 1
    pos = block_start_ml
    while depth > 0 and pos < len(js):
        if js[pos] == '{': depth += 1
        elif js[pos] == '}': depth -= 1
        pos += 1
    block_end = pos - 1
    block_content = js[block_start_ml:block_end]
    keys = {}
    for m in re.finditer(r"([\w]+)\s*:\s*'([^']*)'", block_content):
        keys[m.group(1)] = m.group(2)
    return ml_pos + match.start(), block_end, keys, len(indent)

en_start, en_end, en_keys, en_indent = get_ml_block('en')
zh_start, zh_end, zh_keys, zh_indent = get_ml_block('zh')
ms_start, ms_end, ms_keys, ms_indent = get_ml_block('ms')
ta_start, ta_end, ta_keys, ta_indent = get_ml_block('ta')
print(f'MERCHANT_LANGS: en={len(en_keys)} zh={len(zh_keys)} ms={len(ms_keys)} ta={len(ta_keys)}')

# ====== Step 3: Get customer LANGS translations =====+
langs_pos = js.find('const LANGS')

def get_cust_lang(lang_name):
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

cust_en = get_cust_lang('en')
cust_zh = get_cust_lang('zh')
cust_ms = get_cust_lang('ms')
cust_ta = get_cust_lang('ta')
print(f'Customer LANGS: en={len(cust_en)} zh={len(cust_zh)} ms={len(cust_ms)} ta={len(cust_ta)}')

# ====== Step 4: Build translations for missing keys ======
missing_keys = [k for k in html_keys if k not in en_keys]
print(f'Missing from MERCHANT_LANGS: {len(missing_keys)}')

def safe_js_str(s):
    """Escape string for safe inclusion in JS single-quoted string"""
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    # Remove any other control chars
    s = ''.join(c for c in s if ord(c) >= 32 or c in '\t\n\r')
    return s

translations = {}
for k in missing_keys:
    translations[k] = {
        'en': safe_js_str(cust_en.get(k, k)),
        'zh': safe_js_str(cust_zh.get(k, cust_en.get(k, k))),
        'ms': safe_js_str(cust_ms.get(k, cust_en.get(k, k))),
        'ta': safe_js_str(cust_ta.get(k, cust_en.get(k, k))),
    }

# ====== Step 5: Inject into each block =====+
def inject_keys(block_start, block_end, existing_keys, new_translations, lang_name, indent_str):
    original = js[block_start:block_end]
    
    new_entries = []
    for k in missing_keys:
        if k not in existing_keys:
            val = new_translations[k][lang_name]
            new_entries.append(f"{indent_str}  {k}: '{val}',")
    
    if not new_entries:
        return original, 0
    
    # Insert before the closing of the block
    # Find last entry line
    new_content = original.rstrip().rstrip(',') + ',\n' + '\n'.join(new_entries) + '\n'
    return new_content, len(new_entries)

new_en, n_en = inject_keys(en_start, en_end, en_keys, translations, 'en', ' ' * en_indent)
new_zh, n_zh = inject_keys(zh_start, zh_end, zh_keys, translations, 'zh', ' ' * zh_indent)
new_ms, n_ms = inject_keys(ms_start, ms_end, ms_keys, translations, 'ms', ' ' * ms_indent)
new_ta, n_ta = inject_keys(ta_start, ta_end, ta_keys, translations, 'ta', ' ' * ta_indent)

print(f'Injected: en+{n_en} zh+{n_zh} ms+{n_ms} ta+{n_ta}')

# ====== Step 6: Rebuild file =====+
new_js = (
    js[:en_start] + new_en + js[en_end:zh_start] +
    new_zh + js[zh_end:ms_start] +
    new_ms + js[ms_end:ta_start] +
    new_ta + js[ta_end:]
)

print(f'Size: {len(js)} -> {len(new_js)} (+{len(new_js)-len(js)})')

# ====== Step 7: Validate syntax =====+
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
tmp.write(new_js)
tmp.close()

result = subprocess.run(
    ['node', '-e', 
     f'try {{ new Function(require("fs").readFileSync("{tmp.name.replace(os.sep, \"/\")}", "utf-8")); console.log("SYNTAX_OK") }} catch(e) {{ console.log("SYNTAX_ERR:", e.message) }}'],
    capture_output=True, text=True)
status = result.stdout.strip()
print(f'Syntax: {status}')

if 'SYNTAX_OK' in status:
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(new_js)
    print(f'SAVED! All {len(missing_keys)} keys added to MERCHANT_LANGS.')
else:
    print('NOT SAVED - syntax error')
    # Try to find the error location
    result2 = subprocess.run(
        ['node', '--check', tmp.name],
        capture_output=True, text=True)
    if result2.stderr:
        err = result2.stderr.strip()[:500]
        print(f'Node check error: {err}')
    os.unlink(tmp.name)
