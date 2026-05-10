import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 看 LANGS 最后 3000 字符
langs_start = js.index('const LANGS = {')
depth = 0
p = langs_start + len('const LANGS = {') - 1
while p < len(js):
    if js[p] == '{': depth += 1
    elif js[p] == '}': 
        depth -= 1
        if depth == 0: break
    p += 1
langs_end = p + 1

print(f'LANGS ends at {langs_end}')
print(f'Total size: {langs_end - langs_start} chars')
print()
print('=== Last 2000 chars of LANGS ===')
print(js[langs_end-2000:langs_end])
