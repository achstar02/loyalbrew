import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找 ms: 附近的内容
ms_pos = js.index('ms:', js.index('zh:'))
print(f'ms: at position {ms_pos}')
print(f'Context (500 chars around ms:):')
print(repr(js[ms_pos-20:ms_pos+500]))
