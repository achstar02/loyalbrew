import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找 LANGS 中的 ms 块
langs_start = js.index('const LANGS = {')

en_m = re.search(r'\ben\s*:\s*\{', js[langs_start:])
ep = langs_start + en_m.end()
depth = 1; p = ep
while depth > 0:
    if js[p] == '{': depth += 1
    elif js[p] == '}': depth -= 1
    p += 1

zh_m = re.search(r'\bzh\s*:\s*\{', js[p:])
zp = p + zh_m.end()
depth = 1; p2 = zp
while depth > 0:
    if js[p2] == '{': depth += 1
    elif js[p2] == '}': depth -= 1
    p2 += 1

ms_m = re.search(r'\bms\s*:\s*\{', js[p2:])
msp = p2 + ms_m.end()
depth = 1; p3 = msp
while depth > 0:
    if js[p3] == '{': depth += 1
    elif js[p3] == '}': depth -= 1
    p3 += 1

ms_block = js[msp:p3-1]
print(f'MS block ({len(ms_block)} chars):')
print(ms_block[:3000])
print('...')
print(ms_block[-1000:] if len(ms_block) > 1000 else '')
