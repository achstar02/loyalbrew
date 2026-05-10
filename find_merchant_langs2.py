import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS
m = re.search(r'const MERCHANT_LANGS\s*=\s*\{', js)
start = m.start()
chunk = js[start:start+50000]

print('=== MERCHANT_LANGS language blocks ===')
for lang in ['en', 'zh', 'ms', 'ta']:
    matches = list(re.finditer(rf'\b{lang}\s*:\s*(null|\{{)', chunk))
    for match in matches:
        pos = start + match.start()
        print(f'\n{lang}: at position {pos}')
        # Show 200 chars after
        ctx_end = min(len(chunk), match.end()+300)
        snippet = chunk[match.start():ctx_end]
        # Truncate for display
        if len(snippet) > 250:
            snippet = snippet[:250] + '...'
        print(snippet)

# Check the problematic keys: mRulePerOrderOpt, mRewardFreeItemOpt etc.
print('\n=== Checking stamp card dropdown keys ===')
keys_to_check = [
    'mRulePerOrderOpt', 'mRulePerAmountOpt', 'mRulePerItemOpt',
    'mRewardFreeItemOpt', 'mRewardFlatDiscountOpt', 'mRewardBonusPointsOpt',
    'mFreeItemLabel', 'mFreePrefix',
    'stamp_rule', 'reward_type'
]
for key in keys_to_check:
    # Find in en block (first occurrence after MERCHANT_LANGS)
    pat = re.escape(key) + r"\s*:\s*'([^']*)'"
    matches = list(re.finditer(pat, chunk))
    if matches:
        for i, match in enumerate(matches[:4]):  # max 4 occurrences (one per lang)
            val = match.group(1)
            # Find which lang block this is in by counting { } before it
            prefix = chunk[:match.start()]
            opens = prefix.count('{')
            closes = prefix.count('}')
            print(f'{key} [{i}] = "{val}" (depth approx {opens-closes})')
    else:
        print(f'{key} = NOT FOUND in MERCHANT_LANGS area')
