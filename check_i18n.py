import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\app.js", "r", encoding="utf-8") as f:
    content = f.read()

start = content.index("const LANGS = {")
snippet = content[start:start+150000]

# 改进版：用更精确的方式提取每个语言块
def extract_lang_block(lang_name, text):
    pattern = rf"^\s*{lang_name}\s*:\s*\{{"
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        print(f"  WARNING: {lang_name} block not found!")
        return {}, ""
    block_start = m.end()
    depth = 1
    i = block_start
    while i < len(text) and depth > 0:
        if text[i] == "{": depth += 1
        elif text[i] == "}": depth -= 1
        i += 1
    block = text[block_start:i-1]
    
    keys = {}
    # 匹配 key: 'value' 或 key: "value"
    for m2 in re.finditer(r"""['"]([^'"]+)['"]\s*:\s*['"](.*?)(?:['"]\s*,|['"]\s*\})""", block):
        keys[m2.group(1)] = m2.group(2)
    
    return keys, block

print("Extracting language blocks...")
en_keys, en_block = extract_lang_block("en", snippet)
zh_keys, zh_block = extract_lang_block("zh", snippet)
ms_keys, ms_block = extract_lang_block("ms", snippet)

print(f"EN keys: {len(en_keys)}")
print(f"ZH keys: {len(zh_keys)}")
print(f"MS keys: {len(ms_keys)}")

missing_zh = sorted(set(en_keys.keys()) - set(zh_keys.keys()))
missing_ms = sorted(set(en_keys.keys()) - set(ms_keys.keys()))

print(f"\n=== MISSING IN ZH ({len(missing_zh)}) ===")
for k in missing_zh:
    v = en_keys.get(k, "?")
    print(f"  {k} = '{v}'")

print(f"\n=== MISSING IN MS ({len(missing_ms)}) ===")
for k in missing_ms[:30]:
    v = en_keys.get(k, "?")
    print(f"  {k} = '{v}'")
if len(missing_ms) > 30:
    print(f"  ... and {len(missing_ms)-30} more")

# Also find hardcoded English in index.html that should have data-i18n
print("\n\n=== HARDCODED ENGLISH IN index.html (no data-i18n) ===")
with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find visible English text not inside data-i18n attributes or scripts
# Look for >English text< patterns outside of <script> and where no data-i18n nearby
lines = html.split('\n')
in_script = False
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if '<script' in stripped and '</script>' not in stripped:
        in_script = True
    if '</script>' in stripped:
        in_script = False
        continue
    if in_script:
        continue
    
    # Skip lines with data-i18n (they're already translated)
    if 'data-i18n' in line:
        continue
    
    # Look for common English UI patterns between HTML tags
    english_patterns = re.findall(r'>([A-Z][a-zA-Z\s&;=]{3,50})<', line)
    for ep in english_patterns:
        # Filter out URLs, CSS, class names etc
        if any(skip in ep.lower() for skip in ['http', 'class=', 'style=', 'div ', 'span ', 'doctype', 'meta ', 'link ']):
            continue
        if ep.strip():
            print(f"  Line {i}: '{ep.strip()}'")
