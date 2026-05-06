import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js','r',encoding='utf-8') as f:
    content = f.read()

# Find all Firestore collection references
paths = list(re.finditer(r"fb\.collection\(fb\.db,\s*['\"]([^'\"]+)['\"]", content))
for m in paths:
    line = content[:m.start()].count('\n') + 1
    print(f'Line {line}: collection("{m.group(1)}")')

print("\n--- Doc refs ---")
# Find doc refs that are NOT inside _col()
docs = list(re.finditer(r"fb\.doc\(fb\.db,\s*['\"]([^'\"]+)['\"]", content))
for m in docs:
    line = content[:m.start()].count('\n') + 1
    print(f'Line {line}: doc("{m.group(1)}")')
