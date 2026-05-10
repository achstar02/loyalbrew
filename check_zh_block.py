import re

# Check what's actually in zh block
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

ml_pos = js.find('const MERCHANT_LANGS')
zh_pos = js.find('zh:', ml_pos)
ta_pos = js.find('ta:', ml_pos)
zh_block = js[zh_pos:ta_pos]
print(f'zh block: {zh_pos}-{ta_pos}, size={len(zh_block)}')

# Find all keys in zh block
keys = re.findall(r"    (\w+):", zh_block)
print(f'All zh keys ({len(keys)}):')
print(keys[:50])
print()
print(keys[50:])
