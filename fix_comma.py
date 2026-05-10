import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix: remove double comma pattern - the last entry before } has a trailing comma
# Pattern: 'value'},  ->  just fix by removing comma before }
js = js.replace("Tetapan Kedai'},", "Tetapan Kedai'\n  },")

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f"Fixed. Size: {len(js)}")

import subprocess
r = subprocess.run(['node', '-e',
    "try{new Function(require('fs').readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js','utf-8'));console.log('SYNTAX OK')}catch(e){console.log('ERROR:',e.message)}"],
    capture_output=True, text=True)
print(r.stdout.strip())
if r.stderr:
    print('STDERR:', r.stderr[:200])
