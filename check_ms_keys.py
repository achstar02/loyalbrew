import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找 ms: 块
ms_start = js.index('ms:', js.index('zh:')) + 3
ms_start = js.index('{', ms_start) + 1
depth = 1; p = ms_start
while depth > 0:
    if js[p] == '{': depth += 1
    elif js[p] == '}': depth -= 1
    p += 1
ms_block = js[ms_start:p-1]

keys = re.findall(r"(\w[\w-]*)\s*:\s*'", ms_block)
print(f'MS block has {len(keys)} keys:')
for k in keys:
    print(f'  {k}')
