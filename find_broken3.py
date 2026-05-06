import re

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')
broken = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    # Pattern: key: '...');  - broken string ending with function call syntax
    m = re.match(r"^(\s*[\w]+:\s*)'[^']*'\);\s*$", s)
    if m:
        broken.append((i, s, m.group(1)))

print('Found', len(broken), 'broken lines:')
for num, text, prefix in broken:
    print(f'  Line {num}: {text[:120]}')

# Show context around known error
print('\n--- Context around line 7303 ---')
for i in range(7294, min(7310, len(lines))):
    marker = ''
    for bnum, _, _ in broken:
        if i+1 == bnum:
            marker = '  <<< BROKEN'
            break
    print(f'  {i+1}: {lines[i][:130]}{marker}')
