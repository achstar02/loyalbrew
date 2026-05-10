import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 看 LANGS 结束后 1000 字符
langs_start = js.index('const LANGS = {')
depth = 0
p = langs_start + len('const LANGS = {') - 1
while p < len(js):
    if js[p] == '{': depth += 1
    elif js[p] == '}': 
        depth -= 1
        if depth == 0: break
    p += 1

print(f"LANGS ends at {p}")
print(f"\n=== After LANGS (1500 chars) ===")
print(js[p:p+1500])
