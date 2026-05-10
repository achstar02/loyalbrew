import re

js_path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js'
out_path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\alias_patch.txt'

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS block
mlangs_pos = js.find('MERCHANT_LANGS')
print('MERCHANT_LANGS position:', mlangs_pos)

# Get en block
en_start = js.find('en: {', mlangs_pos)
en_end = js.find('zh: {', mlangs_pos)
en_block = js[en_start:en_end]
print('en block length:', len(en_block))

# Extract all keys with their values
pattern = r'([\w]+):\s*(["\x27])(.*?)\2'
matches = re.findall(pattern, en_block)

# Build mapping: strip 'm' prefix if present
alias_map = {}
for key, quote, value in matches:
    if key.startswith('m') and len(key) > 1:
        short_key = key[1:]
        # Only add alias if short_key doesn't already exist
        existing = re.findall(r'(?<![a-zA-Z])' + re.escape(short_key) + r':\s*["\'].*?["\']', en_block)
        if not existing and short_key not in alias_map:
            alias_map[short_key] = (key, value)

print('Aliases to add:', len(alias_map))
with open(out_path, 'w', encoding='utf-8') as f:
    for short, (orig, val) in sorted(alias_map.items()):
        f.write('%s: %s  <- from %s\n' % (short, val, orig))
