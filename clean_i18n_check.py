import re, os

# Read files
HTML = open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html', 'r', encoding='utf-8').read()
JS = open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'r', encoding='utf-8').read()

print(f"HTML: {len(HTML)} chars, JS: {len(JS)} chars")

# Extract all data-i18n and data-mi18n keys from HTML
html_i18n_keys = set(re.findall(r'data-i18n="([^"]+)"', HTML))
html_mi18n_keys = set(re.findall(r'data-mi18n="([^"]+)"', HTML))

all_html_keys = html_i18n_keys | html_mi18n_keys
print(f"data-i18n keys: {len(html_i18n_keys)}, data-mi18n keys: {len(html_mi18n_keys)}, total: {len(all_html_keys)}")

# Find LANGS structure in JS
# LANGS = { en: {...}, zh: {...}, ms: {...}, ta: {...} }
langs_pos = JS.find('const LANGS =')
if langs_pos < 0:
    langs_pos = JS.find('const LANGS=')
print(f"LANGS at: {langs_pos}")

# Extract keys from each language block in LANGS
def extract_keys(js_content, lang_block_name, start_pos):
    """Extract all key:value pairs from a language block"""
    # Find the block start
    start = js_content.find(lang_block_name + ': {', start_pos)
    if start < 0:
        return set()
    # Find the closing brace (simple approach - count braces)
    depth = 1
    i = start + len(lang_block_name) + 3  # skip ": {"
    keys = set()
    while depth > 0 and i < len(js_content):
        if js_content[i] == '{':
            depth += 1
        elif js_content[i] == '}':
            depth -= 1
        elif js_content[i] == ':':
            # Find the key
            key_start = js_content.rfind(' ', start, i)
            if key_start > start:
                key = js_content[key_start+1:i].strip()
                if key and re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', key):
                    keys.add(key)
        i += 1
    return keys

# Check existing keys in LANGS
en_keys = extract_keys(JS, 'en', langs_pos)
zh_keys = extract_keys(JS, 'zh', langs_pos)
ms_keys = extract_keys(JS, 'ms', langs_pos)
ta_keys = extract_keys(JS, 'ta', langs_pos)

print(f"\nLANGS keys: en={len(en_keys)}, zh={len(zh_keys)}, ms={len(ms_keys)}, ta={len(ta_keys)}")

# Find MERCHANT_LANGS
ml_pos = JS.find('const MERCHANT_LANGS =')
if ml_pos < 0:
    ml_pos = JS.find('const MERCHANT_LANGS=')
print(f"MERCHANT_LANGS at: {ml_pos}")

# Extract merchant keys
ml_en_keys = extract_keys(JS, 'en', ml_pos)
ml_zh_keys = extract_keys(JS, 'zh', ml_pos)
ml_ms_keys = extract_keys(JS, 'ms', ml_pos)
ml_ta_keys = extract_keys(JS, 'ta', ml_pos)

print(f"MERCHANT_LANGS keys: en={len(ml_en_keys)}, zh={len(ml_zh_keys)}, ms={len(ml_ms_keys)}, ta={len(ml_ta_keys)}")

# Find MISSING keys - keys in HTML but not in LANGS
print(f"\n=== MISSING keys in LANGS ===")
missing_en = all_html_keys - en_keys
missing_zh = all_html_keys - zh_keys
missing_ms = all_html_keys - ms_keys
missing_ta = all_html_keys - ta_keys

print(f"Missing in EN: {len(missing_en)}")
print(f"Missing in ZH: {len(missing_zh)}")
print(f"Missing in MS: {len(missing_ms)}")
print(f"Missing in TA: {len(missing_ta)}")

# Show a sample of missing keys
if missing_en:
    print(f"\nFirst 20 missing EN keys: {sorted(list(missing_en))[:20]}")

# Only add keys that are missing in ALL languages (truly untranslated)
truly_missing = missing_en & missing_zh & missing_ms & missing_ta
print(f"\n=== Keys missing in ALL 4 languages: {len(truly_missing)} ===")
if truly_missing:
    print(f"Sample: {sorted(list(truly_missing))[:30]}")

# For keys missing only in some languages, note which ones
print(f"\n=== Summary ===")
print(f"Total unique HTML i18n keys: {len(all_html_keys)}")
print(f"Keys with full translation (4/4): {len(all_html_keys) - len(truly_missing)}")
print(f"Keys completely missing: {len(truly_missing)}")