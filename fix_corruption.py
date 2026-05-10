import sys
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
backup = src + '.bak_corrupt'
bak_src = src + '.bak7'

# Read corrupted file
with open(src, 'r', encoding='utf-8-sig') as f:
    lines = f.read().split('\n')

print(f'Original: {len(lines)} lines')

# Step 1: Fix line 16 (idx 15) - corrupted 'newIte  ms: {' -> 'newItems: null,'
lines[15] = '    newItems: null,'

# Step 2: Delete the translation pollution block: idx 16-631 (lines 17-632)
# After these deleted lines, idx 631+ continues from what was line 633
# But line 633 in original is '    menu: null' (the original menu:null that got pushed)
# So: keep 0-15, delete 16-631, and we DON'T keep idx 631 (it's the orphan menu:null)
# We want: lines 0-15 + lines[632:] (skip idx 16-631)
# BUT: idx 631 was the translation block closing `},` and idx 632 was the orphan `menu: null`
# Actually looking at original:
# idx 630: "    mPhComplaintOrderId: 'cth: ORD123456',"
# idx 631: "  },"  <-- translation block closing
# idx 632: "  "    <-- blank
# idx 633: "    menu: null"  <-- orphan from original _cache.menu
# idx 634: "  },"  <-- _cache closing
# So we keep idx 632 (blank) and idx 633+ (the rest)
# But the orphan `menu: null` at idx 633 should NOT be there - it was the original menu:null
# that got duplicated. The LANGS at line 857 already has its own menu: null values.
# The orphan at idx 633 is from the _cache object, which should only have newItems and menu.
# Since we fixed newItems at idx 15, we need to insert menu: null at idx 16,
# but we also need to remove the orphan at idx 633.

# Correct approach:
# Keep lines 0-15 (before corruption, with fixed line 16)
# Skip lines 16-632 (corruption + orphan menu:null)
# Keep lines 633+ (rest of file)
lines = lines[:16] + lines[633:]

print(f'After cleanup: {len(lines)} lines')

# Verify _cache structure
print()
print('=== _cache area ===')
for i in range(20):
    print(f'L{i+1:4d}: {lines[i]}')
