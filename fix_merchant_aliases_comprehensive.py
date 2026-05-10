"""
Comprehensive fix for MERCHANT_LANGS:
Add unprefixed alias keys to ZH, TA, and EN blocks (MS already has them).
This ensures mt('overview') works in ALL languages.
"""
import re

JS_PATH = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    js = f.read()

print(f'Original size: {len(js)}')

# Find MERCHANT_LANGS
ml_start = js.find('const MERCHANT_LANGS')
if ml_start < 0:
    print('ERROR: MERCHANT_LANGS not found!')
    exit(1)

# Find each language block
blocks = {}
for lang in ['en', 'zh', 'ms', 'ta']:
    # Find lang: after ml_start
    search_from = ml_start
    pos = js.find(lang + ':', search_from)
    if pos < 0:
        print(f'{lang}: NOT FOUND')
        continue
    
    # Check if it's a block (not a string like ms: 'xxx')
    # Look for { after lang:
    after_lang = js[pos + len(lang) + 1:].lstrip()
    if after_lang.startswith('{'):
        # Find the matching closing }
        start = pos + len(lang) + 1 + after_lang.index('{')
        depth = 1
        i = 1
        while depth > 0 and i < len(after_lang):
            if after_lang[i] == '{':
                depth += 1
            elif after_lang[i] == '}':
                depth -= 1
            i += 1
        end = start + i
        blocks[lang] = (start, end)
        print(f'{lang}: block at {start}-{end} ({end-start} chars)')
    else:
        print(f'{lang}: not a block at {pos}')

# Extract MS block to get the list of unprefixed keys
ms_start, ms_end = blocks['ms']
ms_block = js[ms_start:ms_end]

# Find all unprefixed keys in MS block (keys without 'm' prefix, excluding common words)
unprefixed_keys = set()
# Match key patterns like:   keyname: 'value'
# But skip keys starting with 'm' (those are the prefixed ones)
for m in re.finditer(r"\n\s*([a-z][a-zA-Z_0-9]*)\s*:", ms_block):
    key = m.group(1)
    if not key.startswith('m') and len(key) > 2:
        unprefixed_keys.add(key)

# Also find keys that look like aliases (shorter, meaningful)
alias_keys = sorted([k for k in unprefixed_keys if k not in ('if', 'in', 'or', 'as', 'is', 'to', 'do', 'it', 'at', 'on', 'of', 'no', 'up', 'go')])
print(f'\nFound {len(alias_keys)} unprefixed alias keys in MS block:')
print(alias_keys[:20], '...' if len(alias_keys) > 20 else '')

# For each language that needs aliases (ZH, TA, EN), add missing keys
for lang in ['zh', 'ta', 'en']:
    if lang not in blocks:
        continue
    start, end = blocks[lang]
    block = js[start:end]
    
    # Check which alias keys are already present
    existing = set()
    for key in alias_keys:
        if "'" + key + "'" in block or '"' + key + '"' in block:
            existing.add(key)
    
    missing = [k for k in alias_keys if k not in existing]
    
    if not missing:
        print(f'{lang}: All alias keys already present')
        continue
    
    print(f'{lang}: Adding {len(missing)} missing alias keys...')
    
    # Get values from MS block as reference
    ms_values = {}
    for key in missing:
        # Find this key's value in MS block
        pattern = r"\b" + re.escape(key) + r"\s*:\s*'([^']*)'"
        match = re.search(pattern, ms_block)
        if match:
            ms_values[key] = match.group(1)
        else:
            ms_values[key] = key  # fallback
    
    # Build insertion text - add before the closing }
    insert_lines = []
    for key in missing:
        val = ms_values[key]
        insert_lines.append(f"    {key}: '{val}',")
    
    insert_text = '\n'.join(insert_lines) + '\n  '
    
    # Insert before closing brace
    close_brace = block.rfind('}')
    if close_brace > 0:
        new_block = block[:close_brace] + insert_text + block[close_brace:]
        js = js[:start] + new_block + js[end:]
        
        # Update positions of subsequent blocks
        shift = len(new_block) - len(block)
        for l2 in blocks:
            if blocks[l2][0] > start:
                blocks[l2] = (blocks[l2][0] + shift, blocks[l2][1] + shift)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nNew size: {len(js)}')
print('Done! All alias keys added to ZH/TA/EN blocks.')
