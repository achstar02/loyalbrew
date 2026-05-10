import re
BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()

ml_start = js.find('const MERCHANT_LANGS')
zh_start = js.find('zh: {', ml_start)

# Find end of zh block (next }, pattern after zh_start)
zh_end = -1
brace_count = 0
in_string = False
string_char = None
i = zh_start + 5  # Skip "zh: {"
while i < len(js):
    c = js[i]
    if not in_string:
        if c in ('"', "'"):
            in_string = True
            string_char = c
        elif c == '{':
            brace_count += 1
        elif c == '}':
            if brace_count == 0:
                zh_end = i
                break
            brace_count -= 1
    else:
        if c == string_char and js[i-1] != '\\':
            in_string = False
    i += 1

if zh_start > 0 and zh_end > 0:
    zh_block = js[zh_start:zh_end+1]
    keys = ['promoEngineTitle', 'promoEngineDesc', 'enablePromo', 'busyThreshold', 'promoHideHint', 'shopInfo']
    result = f'zh block: {zh_start} to {zh_end} ({zh_end - zh_start} chars)\n\n'
    for key in keys:
        pattern = key + r":\s*'([^']*)'"
        match = re.search(pattern, zh_block)
        if match:
            result += f'{key}: {match.group(1)}\n'
        else:
            result += f'{key}: NOT FOUND\n'
    with open(BASE + r'\zh_keys_check.txt','w',encoding='utf-8') as f:
        f.write(result)
    print('Written to zh_keys_check.txt')
else:
    print(f'zh_start={zh_start}, zh_end={zh_end}')
