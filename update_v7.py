import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()
c = c.replace('app.js?v=6', 'app.js?v=7')
with open(f,'w',encoding='utf-8') as fh: fh.write(c)
print('Updated to v7')
