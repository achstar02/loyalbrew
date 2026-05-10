import re

bak = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js.bak'
out = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(bak, 'r', encoding='utf-8') as f:
    content = f.read()

# Find MERCHANT_LANGS boundaries
ml_start = content.index('const MERCHANT_LANGS = {')
# Find the ORIGINAL premature }; that closes MERCHANT_LANGS too early
# It should close AFTER ta block, not after ms block
# Pattern: after ms block content ends, there's "  },\r\n  zh: {" 
# But there's a "};  " closing MERCHANT_LANGS right after ms!

# Find the ms block closing
ms_start = content.index('ms: {', ml_start)
# Count depth to find where ms: {} ends
depth = 0
ms_end = -1
in_ms = False
for i in range(ms_start, len(content)):
    if content[i] == '{':
        depth += 1
        in_ms = True
    elif content[i] == '}':
        depth -= 1
        if in_ms and depth == 0:
            ms_end = i
            break

print(f"ms block: {ms_start} - {ms_end}")
print(f"ms content: {repr(content[ms_end-30:ms_end+30])}")

# Now find zh: { after ms block
zh_pattern = re.search(r'\},\s*\r?\n\s+zh:\s*\{', content[ms_end:])
if zh_pattern:
    zh_abs = ms_end + zh_pattern.start()
    print(f"zh block starts at: {zh_abs}")
    print(f"Content: {repr(content[zh_abs-20:zh_abs+50])}")

# Find ta: { after zh
ta_pattern = re.search(r'\},\s*\r?\n\s+ta:\s*\{', content[zh_abs+1:])
if ta_pattern:
    ta_abs = zh_abs + 1 + ta_pattern.start()
    print(f"ta block starts at: {ta_abs}")
    print(f"Content: {repr(content[ta_abs-20:ta_abs+50])}")

# Find the premature }; closing MERCHANT_LANGS after ms
# It appears as "  },\r\n};\r\n\r\nzh:" or similar
# We need to find where this is
premature_close_match = re.search(r'(\}),\s*\r?\n\};(\s*\r?\n\r?\n)(\s+zh:)', content[ms_end:zh_abs+100])
if premature_close_match:
    print(f"\nFound premature close: {repr(premature_close_match.group(0))}")
    print(f"Start: {ms_end + premature_close_match.start()}")
