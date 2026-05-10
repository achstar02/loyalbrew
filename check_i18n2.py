import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\app.js", "r", encoding="utf-8") as f:
    content = f.read()

start = content.index("const LANGS = {")
snippet = content[start:start+150000]

# 更好的方法：直接找每个 key:value 对
def extract_all_keys(text):
    keys = {}
    # 匹配 key: 'value' 格式，value 可以包含转义字符
    for m in re.finditer(r"""(\w[\w]*)(?:\s*:\s*['"]([^'"]*(?:\\.[^'"]*)*)['"])""", text):
        k = m.group(1)
        v = m.group(2)
        # 过滤掉太短或明显不是翻译键的
        if len(k) >= 3 and len(v) >= 1 and not k.startswith('//'):
            keys[k] = v
    return keys

print("=== Trying broader extraction ===")
all_keys = extract_all_keys(snippet)
print(f"Total key-value pairs found: {len(all_keys)}")

# 看看前50个
for i, k in enumerate(sorted(all_keys.keys())):
    if i < 80:
        print(f"  {k} = '{all_keys[k][:60]}'")
