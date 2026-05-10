"""Quote-aware block parser for minified JS"""
import re, os

DEPLOY_DIR = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy'
JS_PATH = os.path.join(DEPLOY_DIR, 'app.js')

with open(JS_PATH, 'r', encoding='utf-8-sig') as f:
    js = f.read()

def find_block_end_robust(content, block_name, start_pos):
    """Find the closing } of a language block, ignoring } inside strings."""
    # Find the block start
    colon = content.find(block_name + ': {', start_pos)
    if colon < 0:
        colon = content.find(block_name + ':{', start_pos)
    if colon < 0:
        return -1, -1
    
    i = colon + len(block_name) + 2  # skip ": {"
    depth = 0
    in_string = False
    string_char = None
    
    while i < len(content):
        c = content[i]
        
        # Handle string state
        if in_string:
            if c == '\\':
                i += 2  # Skip escaped character
                continue
            elif c == string_char:
                in_string = False
                string_char = None
            i += 1
            continue
        
        # Handle code state
        if c in ('"', "'", '`'):
            in_string = True
            string_char = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i, colon
        i += 1
    
    return -1, colon

def extract_keys_robust(content, block_name, start_pos):
    """Extract keys from a block using quote-aware parsing."""
    end_pos, block_start = find_block_end_robust(content, block_name, start_pos)
    if end_pos < 0:
        return set(), end_pos, block_start
    
    existing = set()
    depth = 0
    in_string = False
    string_char = None
    i = block_start + len(block_name) + 2
    
    while i < end_pos:
        c = content[i]
        
        if in_string:
            if c == '\\':
                i += 2
                continue
            elif c == string_char:
                in_string = False
                string_char = None
            i += 1
            continue
        
        if c in ('"', "'", '`'):
            in_string = True
            string_char = c
        elif c == ':':
            # Check if we're at depth 1 (direct child of the block object)
            # Look back to find the key
            key_start = content.rfind(' ', block_start, i)
            if key_start > block_start:
                key = content[key_start+1:i].strip()
                if re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', key):
                    existing.add(key)
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        i += 1
    
    return existing, end_pos, block_start

# Check LANGS blocks
langs_pos = js.find('const LANGS')
ml_pos = js.find('const MERCHANT_LANGS')
print(f"LANGS at {langs_pos}, MERCHANT_LANGS at {ml_pos}")
print(f"File size: {len(js)}")

for label, start in [('LANGS', langs_pos), ('MERCHANT_LANGS', ml_pos)]:
    print(f"\n=== {label} ===")
    for lang in ['en', 'zh', 'ms', 'ta']:
        keys, end_pos, block_start = extract_keys_robust(js, lang, start)
        if end_pos < 0:
            print(f"  {lang}: NOT FOUND")
            continue
        print(f"  {lang}: {len(keys)} keys, spans {block_start}-{end_pos} ({end_pos - block_start} chars)")
        if keys:
            sorted_keys = sorted(keys)
            print(f"    First 5: {sorted_keys[:5]}")
            print(f"    Last 5: {sorted_keys[-5:]}")

# Check if there's content AFTER the LANGS blocks and BEFORE MERCHANT_LANGS
if ml_pos > langs_pos:
    # Find the end of the LAST LANGS block (ta)
    ta_keys, ta_end, ta_start = extract_keys_robust(js, 'ta', langs_pos)
    if ta_end > 0:
        between = js[ta_end+1:ml_pos].strip()
        print(f"\nContent between LANGS end ({ta_end}) and MERCHANT_LANGS ({ml_pos}):")
        print(f"  {len(between)} chars: {repr(between[:200])}")