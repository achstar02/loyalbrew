# -*- coding: utf-8 -*-
content = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js.bak', encoding='utf-8').read()
f = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\structure_analysis.txt', 'w', encoding='utf-8')

def safe_print(msg):
    try:
        msg.encode('cp1252')
        print(msg)
    except:
        # Write to file instead
        f.write(msg + '\n')

f.write(f'Total file size: {len(content)}\n\n')

# MLANGS analysis
ml_start = content.index('const MERCHANT_LANGS = {')
f.write(f'MERCHANT_LANGS starts at: {ml_start}\n')

# Find where en block ends (depth 0 after entering en)
depth = 0; en_end = -1; in_en = False
for i in range(ml_start + 25, len(content)):
    c = content[i]
    if c == '{': depth += 1; in_en = True
    elif c == '}':
        depth -= 1
        if in_en and depth == 0: en_end = i; break
f.write(f'MERCHANT_LANGS en block ends at: {en_end}\n')
f.write(f'Content after en block: {repr(content[en_end:en_end+100])}\n')

# Find what language block comes after en
for name, marker in [('zh', 'zh:'), ('ms', 'ms:'), ('ta', 'ta:')]:
    pos = content.find(marker, en_end+1, en_end+50000)
    if pos > 0:
        indent = len(marker) + len(content[en_end+1:pos])
        # Count leading spaces
        sp = len(content) - len(content.lstrip(' ', 1))
        # Find actual indent
        j = pos - 1
        while j >= 0 and content[j] in ' \t\r\n':
            j -= 1
        j += 1
        indent = pos - j
        f.write(f'{name}: at {pos}, indent={indent}, snippet: {repr(content[pos:pos+50])}\n')
    else:
        f.write(f'{name}: NOT FOUND\n')

f.write('\n')

# Find the end of the entire MERCHANT_LANGS object
depth = 0; ml_end = -1
for i in range(ml_start + 25, len(content)):
    c = content[i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0: ml_end = i; break
f.write(f'MERCHANT_LANGS ends at: {ml_end}\n')
f.write(f'Content around end: {repr(content[ml_end-30:ml_end+20])}\n')

f.close()
print('Analysis written to structure_analysis.txt')
