import re

# Check zh block structure - it has DUPLICATES (customer LANGS zh mixed in)
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

ml_pos = js.find('const MERCHANT_LANGS')
zh_pos = js.find('zh:', ml_pos)
ta_pos = js.find('ta:', ml_pos)
zh_block = js[zh_pos:ta_pos]

# Show first and last parts
print('=== ZH BLOCK START (first 500 chars) ===')
print(zh_block[:500].encode('ascii', errors='replace').decode())
print()
print('=== ZH BLOCK around "ms" key ===')
ms_key_pos = zh_block.find("    ms:")
print(f"ms key at zh_block[{ms_key_pos}]")
print(zh_block[ms_key_pos-100:ms_key_pos+200].encode('ascii', errors='replace').decode())
print()
print('=== ZH BLOCK END (last 500 chars) ===')
print(zh_block[-500:].encode('ascii', errors='replace').decode())

# Find all keys
keys = re.findall(r"    (\w+):", zh_block)
unique_keys = []
seen = set()
for k in keys:
    if k not in seen:
        unique_keys.append(k)
        seen.add(k)

print(f'\nTotal keys: {len(keys)}, Unique: {len(unique_keys)}')
print('First 60 unique keys:', unique_keys[:60])
print()
print('Last 20 unique keys:', unique_keys[-20:])
