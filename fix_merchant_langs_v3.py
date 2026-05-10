import re, sys
sys.stdout.reconfigure(encoding='utf-8')

JS = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'

# Restore from clean backup
with open(JS + '.bak7', 'r', encoding='utf-8') as f:
    js = f.read()
print(f'Restored from backup: {len(js)} chars')

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

ml_start = js.find('const MERCHANT_LANGS')
ml_end = js.find('\n};', ml_start) + 2
ml_block = js[ml_start:ml_end]

def find_lang_blocks(text, start_offset=0):
    blocks = {}
    for lang in ['en', 'zh', 'ms', 'ta']:
        pat = re.compile(rf'\b{lang}\s*:\s*\{{')
        match = pat.search(text)
        if not match:
            continue
        depth = 0
        block_start = match.end() - 1
        for i in range(block_start, len(text)):
            if text[i] == '{': depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    blocks[lang] = (start_offset + block_start, start_offset + i)
                    break
    return blocks

blocks = find_lang_blocks(ml_block, ml_start)

# For each lang block, find the closing } and insert keys before it
# The closing } might be preceded by whitespace/newlines
# We need to find the actual last key-value and add after it
for lang in ['ta', 'ms', 'zh', 'en']:
    if lang not in blocks:
        continue
    
    block_start, block_end = blocks[lang]
    
    # Find the closing } of this lang block
    close_pos = block_end
    
    # Look at the text just before the }
    # We want to insert our keys before the }
    # The last character before } should be a newline
    # We insert: ,\n    key: 'value',\n    key: 'value'\n
    
    keys_list = []
    for k, v in missing_keys[lang].items():
        keys_list.append(f"    {k}: '{v}'")
    
    # Check if there's already a trailing comma
    # The block content before }
    before_close = js[block_start:close_pos]
    
    # Find last non-whitespace char
    stripped = before_close.rstrip()
    last_char = stripped[-1] if stripped else ''
    
    if last_char == ',':
        # Already has trailing comma, just add new keys
        insertion = '\n' + ',\n'.join(keys_list)
    else:
        # Need to add comma before first new key
        insertion = ',\n' + ',\n'.join(keys_list)
    
    js = js[:close_pos] + insertion + js[close_pos:]
    print(f'{lang}: Inserted at pos {close_pos}, last_char was "{last_char}"')

# Verify
for key in missing_keys['en']:
    count = js.count(key)
    print(f'{key}: found {count} times')

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nSaved! New size: {len(js)} chars')
