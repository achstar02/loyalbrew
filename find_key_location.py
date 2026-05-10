import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找 mRulePerOrderOpt 的上下文
key = 'mRulePerOrderOpt'
pos = js.find(key)
print(f"=== {key} at {pos} ===")
# Show 500 chars of context
start = max(0, pos - 300)
end = min(len(js), pos + 200)
ctx = js[start:end]
print(ctx)
print()

# 也检查这个位置是否在 LANGS 内
langs_start = js.index('const LANGS = {')
print(f"LANGS starts at: {langs_start}")
print(f"Key position {pos} is {'inside' if pos > langs_start else 'outside'} LANGS area (roughly)")

# 找 LANGS 结束位置
# 数括号
depth = 0
p = langs_start + len('const LANGS = {') - 1
while p < len(js):
    if js[p] == '{': depth += 1
    elif js[p] == '}': 
        depth -= 1
        if depth == 0:
            break
    p += 1
print(f"LANGS ends at: {p}")
print(f"Key at {pos} is {'INSIDE' if langs_start <= pos <= p else 'OUTSIDE'} LANGS object")
