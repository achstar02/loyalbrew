import re

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find ta: block start
ta_start = content.find('ta: {')
if ta_start == -1:
    print('ta: block not found')
    exit()

# Find the end of ta block by counting braces
depth = 0
i = ta_start + 4  # skip 'ta: '
while i < len(content):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            ta_end = i + 1
            break
    i += 1

ta_block = content[ta_start:ta_end]
# Count keys
keys = re.findall(r"\s+(\w[\w.]*):\s*['\"]", ta_block)
print(f'ta: block size: {len(ta_block)} chars')
print(f'ta: keys count: {len(keys)}')
print(f'First 10 keys: {keys[:10]}')

# Check if ta block is inside LANGS or standalone
# Find the const LANGS positions
langs1 = content.find('const LANGS = {')
langs2 = content.find('const LANGS = {', langs1 + 1)
print(f'\nFirst LANGS at: {langs1}')
print(f'Second LANGS at: {langs2}')
print(f'ta: block at: {ta_start}')

if langs1 < ta_start < langs2:
    print('ta: is INSIDE first LANGS')
elif ta_start > langs2:
    print('ta: is INSIDE second LANGS or standalone')
else:
    print('ta: is OUTSIDE both LANGS objects')
