import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

# Search for .type access that might fail on null
results = []
for m in re.finditer(r'\.type\b', JS):
    pos = m.start()
    context = JS[max(0,pos-80):pos+80]
    # Skip comments and strings
    line_start = JS.rfind('\n', 0, pos)
    line = JS[line_start+1:JS.find('\n', pos)]
    if '//' in line[:line.find(m.group())] or re.match(r'\s', JS[pos-1]):
        continue
    results.append((pos, context))

print(f'Total .type accesses: {len(results)}')
for pos, ctx in results[:10]:
    with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\type_search.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n=== {pos} ===\n{ctx}\n')

# Also check loadPromoSettings for null access issues
p = JS.find('function loadPromoSettings')
with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\promo_full.txt', 'w', encoding='utf-8') as f:
    f.write(JS[p:p+2000])
