import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找 LANGS 对象的精确范围
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

print(f'LANGS object: {langs_start} to {langs_end} ({langs_end-langs_start} chars)')

# 提取完整的 LANGS 对象内容
langs_content = js[langs_start:langs_end]

# 统计每个块有多少个键
for label, pattern in [('EN', r'en\s*:\s*\{'), ('ZH', r'zh\s*:\s*\{'), ('MS', r'ms\s*:\s*\{')]:
    m = re.search(pattern, langs_content)
    if not m:
        print(f'{label}: NOT FOUND!')
        continue
    # 找这个块的结束括号
    bdepth = 0
    bp = m.end() - 1
    while bp < len(langs_content):
        if langs_content[bp] == '{': bdepth += 1
        elif langs_content[bp] == '}':
            bdepth -= 1
            if bdepth == 0: break
        bp += 1
    block = langs_content[m.start():bp+1]
    keys = re.findall(r"(\w[\w]*)\s*:\s*'[^']*'", block)
    print(f'{label}: {len(keys)} keys, block size: {len(block)} chars')
    
    # 也提取所有键名存到文件
    with open(f'{label.lower()}_keys.txt', 'w', encoding='utf-8') as out:
        for k in sorted(keys):
            out.write(k + '\n')
