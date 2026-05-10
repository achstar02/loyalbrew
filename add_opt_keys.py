import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# The 6 missing keys with translations for all 4 languages
missing = {
    'mRulePerOrderOpt': {
        'en': "Every purchase = 1 stamp",
        'zh': "每消费1次=1印章",
        'ms': "Setiap pembelian = 1 setem",
        'ta': "ஒவ்வொரு கொள்முதலும் = 1 முத்திரை",
    },
    'mRulePerAmountOpt': {
        'en': "Every RM X spent = 1 stamp",
        'zh': "每消费RM X=1印章",
        'ms': "Setiap RM X dibelanjakan = 1 setem",
        'ta': "ஒவ்வொரு RM X செலவிட்டால் = 1 முத்திரை",
    },
    'mRulePerItemOpt': {
        'en': "Buy specific item = 1 stamp",
        'zh': "购买指定商品=1印章",
        'ms': "Beli item tertentu = 1 setem",
        'ta': "குறிப்பிட்ட பொருள் வாங்க = 1 முத்திரை",
    },
    'mRewardFreeItemOpt': {
        'en': "Free Menu Item",
        'zh': "免费菜单商品",
        'ms': "Item Menu Percuma",
        'ta': "இலவச மெனு பொருள்",
    },
    'mRewardFlatDiscountOpt': {
        'en': "Flat Discount (RM)",
        'zh': "固定折扣 (RM)",
        'ms': "Diskaun Tetap (RM)",
        'ta': "நிலையான தள்ளுபடி (RM)",
    },
    'mRewardBonusPointsOpt': {
        'en': "Bonus Points",
        'zh': "奖励积分",
        'ms': "Mata Bonus",
        'ta': "போனஸ் புள்ளிகள்",
    },
}

ml_start = js.find('const MERCHANT_LANGS')
print(f'MERCHANT_LANGS at: {ml_start}')

# Find each language block's closing brace position
# We need to insert keys before the } of each block
added = {lang: 0 for lang in ['en','zh','ms','ta']}

for key, translations in missing.items():
    for lang, value in translations.items():
        # Find this language block in MERCHANT_LANGS
        # Search for the pattern: lang: { ... }
        # We need to find where to insert - before the last } of each block
        
        # Find lang marker after ml_start
        search_from = ml_start
        while True:
            pos = js.find(lang + ':', search_from)
            if pos == -1 or pos > ml_start + 200000:
                break
            # Check if it looks like a language block (followed by {)
            after = js[pos+len(lang)+1:pos+len(lang)+3].strip()
            if after.startswith('{'):
                # This is our language block - find its closing by counting braces
                block_start = js.find('{', pos)
                depth = 0
                i = block_start
                while i < len(js):
                    if js[i] == '{':
                        depth += 1
                    elif js[i] == '}':
                        depth -= 1
                        if depth == 0:
                            # Found the end of this block - insert before this }
                            insert_pos = i
                            # Check if key already exists in this block
                            block_content = js[block_start:i]
                            if key not in block_content:
                                # Insert the key before the closing }
                                new_line = f"\n    {key}: '{value}',"
                                js = js[:insert_pos] + new_line + js[insert_pos:]
                                added[lang] += 1
                                # Adjust positions for subsequent searches
                                ml_start = js.find('const MERCHANT_LANGS')
                            break
                    i += 1
                break
            search_from = pos + 1

print(f'Added keys: en={added["en"]} zh={added["zh"]} ms={added["ms"]} ta={added["ta"]}')

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print('Saved!')
