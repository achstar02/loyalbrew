import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找所有 ms: 出现的位置
for m in re.finditer(r'\bms\s*:', js):
    pos = m.start()
    ctx = js[pos:pos+100]
    print(f"ms: at {pos}: ...{ctx}...")
