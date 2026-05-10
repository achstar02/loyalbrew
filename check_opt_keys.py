import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

ml_start = js.find('const MERCHANT_LANGS')
print(f'MERCHANT_LANGS at: {ml_start}')

keys = ['mRulePerOrderOpt','mRulePerAmountOpt','mRulePerItemOpt',
        'mRewardFreeItemOpt','mRewardFlatDiscountOpt','mRewardBonusPointsOpt']

for key in keys:
    # Search each language block for the key
    found = {}
    for lang in ['en', 'zh', 'ms', 'ta']:
        # Find lang block start
        block_start = js.find(lang + ':', ml_start)
        if block_start == -1 or block_start > ml_start + 200000:
            found[lang] = 'BLOCK NOT FOUND'
            continue
        # Search for key within reasonable range (next 50000 chars)
        search_area = js[block_start:block_start+50000]
        m = re.search(re.escape(key) + r"\s*:\s*'([^']*)'", search_area)
        found[lang] = m.group(1) if m else 'NOT FOUND'
    
    print(f'{key}:')
    print(f'  EN={found["en"]}  ZH={found["zh"]}  MS={found["ms"]}  TA={found["ta"]}')
