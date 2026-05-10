import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 提取 EN 块的所有键值对
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

langs_content = js[langs_start:langs_end]

# 提取 en 块
en_match = re.search(r'en\s*:\s*\{', langs_content)
bdepth = 0
bp = en_match.end() - 1
while bp < len(langs_content):
    if langs_content[bp] == '{': bdepth += 1
    elif langs_content[bp] == '}':
        bdepth -= 1
        if bdepth == 0: break
    bp += 1
en_block = langs_content[en_match.start():bp+1]

# 提取所有 key: 'value' 对
pairs = re.findall(r"(\w[\w.]*)\s*:\s*'([^']*)'", en_block)
print(f'Total EN keys: {len(pairs)}')
print()

# 分类：哪些看起来像需要翻译的用户可见文本
merchant_keys = []  # m前缀 - 商家端
customer_keys = []  # 无m前缀 - 顾客端
special_keys = []   # 特殊格式

for k, v in pairs:
    if k.startswith('m'):
        merchant_keys.append((k, v))
    elif '.' in k or k.startswith("'") or 'saved' in k.lower():
        special_keys.append((k, v))
    else:
        customer_keys.append((k, v))

print(f'=== Customer-facing keys (no m prefix): {len(customer_keys)} ===')
for k, v in sorted(customer_keys):
    print(f'  {k}: {v}')

print(f'\n=== Merchant keys (m prefix): {len(merchant_keys)} ===')
for k, v in sorted(merchant_keys):
    print(f'  {k}: {v}')

print(f'\n=== Special keys: {len(special_keys)} ===')
for k, v in special_keys:
    print(f'  {k}: {v}')
