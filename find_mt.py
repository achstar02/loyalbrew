import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Step 1: Fix mt() fallback order — try unprefixed FIRST, then m-prefixed
# Find and replace the mt() function
mt_match = re.search(r'function mt\(key\)\s*\{', js)
if mt_match:
    mt_pos = mt_match.start()
    # Show current implementation
    ctx = js[mt_pos:mt_pos+500]
    safe = ctx.encode('ascii', errors='replace').decode()
    print(f'mt() at {mt_pos}:')
    print(safe[:400])
    print()
else:
    print('mt() not found')

# Also find applyMerchantLang
am_match = re.search(r'function applyMerchantLang\(\)', js)
if am_match:
    print(f'applyMerchantLang() at {am_match.start()}')
