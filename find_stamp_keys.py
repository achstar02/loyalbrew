import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Search for these keys in the ENTIRE file (not just MERCHANT_LANGS)
keys = ['mRulePerOrderOpt', 'mRulePerAmountOpt', 'mRulePerItemOpt',
        'mRewardFreeItemOpt', 'mRewardFlatDiscountOpt', 'mRewardBonusPointsOpt']

print('=== Full file search for stamp dropdown keys ===')
for key in keys:
    pat = re.escape(key) + r"\s*:\s*'([^']*)'"
    matches = list(re.finditer(pat, js))
    print(f'\n{key}: found {len(matches)} occurrences')
    for i, m in enumerate(matches):
        val = m.group(1)
        pos = m.start()
        # Find surrounding context (which lang block?)
        # Look backwards for "en:", "zh:", "ms:", "ta:"
        before = js[max(0,pos-2000):pos]
        lang_hint = '?'
        for lang in ['ta:', 'ms:', 'zh:', 'en:']:
            idx = before.rfind(lang)
            if idx != -1 and idx > len(before) - 100:
                lang_hint = lang
                break
        print(f'  [{i}] pos={pos} val="{val}" ~{lang_hint}')
