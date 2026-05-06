import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()
for pattern in ["setLang('zh')", "setLang('ta')", 'mlang-zh', 'mlang-ta']:
    idx = c.find(pattern)
    if idx >= 0:
        start = c.find('>', idx) + 1
        end = c.find('<', start)
        text = c[start:end]
        print(f'{pattern}: "{text}"')
    else:
        print(f'{pattern}: NOT FOUND')
