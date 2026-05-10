import re

with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

ms_pos = js.find('ms:', 311000)
ta_pos = js.find('ta:', 319000)
print(f'ms: {ms_pos}, ta: {ta_pos}')

region = js[ms_pos:ta_pos]
aliases = []
for m in re.finditer(r"\n\s*([a-z][a-zA-Z_0-9]*)\s*:\s*'([^']*)'", region):
    key = m.group(1)
    if not key.startswith('m') and len(key) > 2:
        aliases.append((key, m.group(1)))

print(f'Found {len(aliases)} unprefixed alias keys in MS region:')
for k, v in aliases[:40]:
    print(f'  {k}: {v}')
