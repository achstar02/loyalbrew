import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 提取 LANGS 前 3000 字符看结构
langs_start = js.index('const LANGS = {')
print(js[langs_start:langs_start+3000])
