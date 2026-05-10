import re, sys
sys.stdout.reconfigure(encoding='utf-8')

JS = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Backup
with open(JS + '.bak7', 'w', encoding='utf-8') as f:
    f.write(js)
print(f'Backup saved: {len(js)} chars')

# Strategy: Add the missing *Opt keys to each language block in MERCHANT_LANGS
# We need to find each lang block in MERCHANT_LANGS and add keys after the existing ones

ml_start = js.find('const MERCHANT_LANGS')
if ml_start == -1:
    print('ERROR: MERCHANT_LANGS not found!')
    sys.exit(1)

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

# Find each language block end in MERCHANT_LANGS
# We need to insert keys before the closing } of each lang block
ml_chunk = js[ml_start:]

for lang in ['en', 'zh', 'ms', 'ta']:
    # Find the lang block start
    lang_pat = re.compile(rf'\b{lang}\s*:\s*\{{')
    lang_match = lang_pat.search(ml_chunk)
    if not lang_match:
        print(f'WARNING: {lang} block not found in MERCHANT_LANGS!')
        continue
    
    # Find the matching closing brace
    depth = 0
    pos = lang_match.end() - 1  # start from the opening {
    for i in range(pos, min(pos + 20000, len(ml_chunk))):
        if ml_chunk[i] == '{':
            depth += 1
        elif ml_chunk[i] == '}':
            depth -= 1
            if depth == 0:
                # Found the closing }
                # Check if there's a comma before the }
                # We want to insert before the closing }
                insert_pos = ml_start + i
                
                # Check what's before the }
                before_close = js[insert_pos-100:insert_pos].rstrip()
                
                # Build the key-value string
                keys_str = ', '.join(f"{k}: '{v}'" for k, v in missing_keys[lang].items())
                
                # Insert before the closing }
                # The line before } typically ends with a comma or is a key-value
                # We need to add comma + newline + our keys
                js = js[:insert_pos] + keys_str + js[insert_pos:]
                
                print(f'{lang}: Added 6 keys before closing brace at pos {insert_pos}')
                break

# Verify - check that the keys now exist
for key in missing_keys['en']:
    count = js.count(key)
    print(f'{key}: found {count} times')

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nSaved! New size: {len(js)} chars')
