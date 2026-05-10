import re, sys
sys.stdout.reconfigure(encoding='utf-8')

JS = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'

# Restore from clean backup
with open(JS + '.bak7', 'r', encoding='utf-8') as f:
    js = f.read()
print(f'Restored from backup: {len(js)} chars')

# Define the missing keys with translations for each language
missing_keys = {
    'en': {
        'mRulePerOrderOpt': 'Every purchase = 1 stamp',
        'mRulePerAmountOpt': 'Every RM X spent = 1 stamp',
        'mRulePerItemOpt': 'Purchase specific item = 1 stamp',
        'mRewardFreeItemOpt': 'Free Menu Item',
        'mRewardFlatDiscountOpt': 'Flat Discount (RM)',
        'mRewardBonusPointsOpt': 'Bonus Points',
    },
    'zh': {
        'mRulePerOrderOpt': '每消费1次=1印章',
        'mRulePerAmountOpt': '每消费RM X=1印章',
        'mRulePerItemOpt': '购买指定商品=1印章',
        'mRewardFreeItemOpt': '免费菜单商品',
        'mRewardFlatDiscountOpt': '固定折扣 (RM)',
        'mRewardBonusPointsOpt': '额外积分',
    },
    'ms': {
        'mRulePerOrderOpt': 'Setiap pembelian = 1 setem',
        'mRulePerAmountOpt': 'Setiap RM X dibelanjakan = 1 setem',
        'mRulePerItemOpt': 'Beli item tertentu = 1 setem',
        'mRewardFreeItemOpt': 'Item Menu Percuma',
        'mRewardFlatDiscountOpt': 'Diskaun Tetap (RM)',
        'mRewardBonusPointsOpt': 'Mata Bonus',
    },
    'ta': {
        'mRulePerOrderOpt': 'ஒவ்வொரு கொள்முதலுக்கும் = 1 முத்திரை',
        'mRulePerAmountOpt': 'ஒவ்வொரு RM X செலவிற்கும் = 1 முத்திரை',
        'mRulePerItemOpt': 'குறிப்பிட்ட பொருள் வாங்க = 1 முத்திரை',
        'mRewardFreeItemOpt': 'இலவச மெனு பொருள்',
        'mRewardFlatDiscountOpt': 'நிலையான தள்ளுபடி (RM)',
        'mRewardBonusPointsOpt': 'போனஸ் புள்ளிகள்',
    },
}

# Strategy: find the last key-value pair in each lang block and add after it
# We'll search for the pattern:  },\n  },\n  <next_lang>:
# And insert our keys before the },\n that closes each lang block

ml_start = js.find('const MERCHANT_LANGS')
ml_end = js.find('\n};', ml_start) + 2  # End of MERCHANT_LANGS
ml_block = js[ml_start:ml_end]

# Find each lang block by tracking braces
def find_lang_blocks(text, start_offset=0):
    """Find {en, zh, ms, ta} block positions in MERCHANT_LANGS"""
    blocks = {}
    for lang in ['en', 'zh', 'ms', 'ta']:
        pat = re.compile(rf'\b{lang}\s*:\s*\{{')
        match = pat.search(text)
        if not match:
            continue
        # Find matching closing brace
        depth = 0
        block_start = match.end() - 1  # position of opening {
        for i in range(block_start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    blocks[lang] = (start_offset + block_start, start_offset + i)
                    break
    return blocks

blocks = find_lang_blocks(ml_block, ml_start)
print(f'Found blocks: {[(k, v[0], v[1]) for k, v in blocks.items()]}')

# For each lang block, insert keys before the closing }
# We need to work from LAST to FIRST to avoid position shifts
for lang in ['ta', 'ms', 'zh', 'en']:  # reverse order
    if lang not in blocks:
        print(f'WARNING: {lang} block not found, skipping')
        continue
    
    block_start, block_end = blocks[lang]
    block_content = js[block_start:block_end+1]
    
    # Find the last key-value pair (before the closing })
    # Pattern: look for the last 'key: value' before }
    # We want to insert after the last comma/value
    
    # Find the position just before the closing }
    close_pos = block_end
    
    # Check if the character before } is a comma, newline, or value
    before_close = js[close_pos-80:close_pos].rstrip()
    
    # Build the insertion text
    keys_list = []
    for k, v in missing_keys[lang].items():
        keys_list.append(f"    {k}: '{v}'")
    insertion = ',\n' + ',\n'.join(keys_list)
    
    # Insert before the closing }
    js = js[:close_pos] + insertion + js[close_pos:]
    
    print(f'{lang}: Inserted {len(missing_keys[lang])} keys at pos {close_pos}')

# Verify
for key in missing_keys['en']:
    count = js.count(key)
    print(f'{key}: found {count} times')

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nSaved! New size: {len(js)} chars')
