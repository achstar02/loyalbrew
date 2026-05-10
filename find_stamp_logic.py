import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find the function that populates stamp card dropdowns
print('=== Searching for stamp card option population ===')
patterns = [
    r'sc-rule',
    r'mRulePerOrder',
    r'Every purchase',
    r'stampPerOrder',
    r'stampPerPurchase',
    r'1 stamp',
    r'onRewardTypeChange',
]
for pat in patterns:
    matches = list(re.finditer(pat, js))
    if matches:
        print(f'\n"{pat}": {len(matches)} matches')
        for m in matches[:3]:
            start = max(0, m.start()-60)
            end = min(len(js), m.end()+100)
            print(f'  ...{js[start:end]}...')

# Find MERCHANT_LANGS zh block and check what stamp-related keys it has
print('\n=== Checking MERCHANT_LANGS zh block for stamp keys ===')
ml_start = js.find('const MERCHANT_LANGS')
ml_chunk = js[ml_start:ml_start+20000]
zh_match = re.search(r'zh:\s*\{', ml_chunk)
if zh_match:
    zh_start = zh_match.start()
    # Find closing bracket
    depth = 0
    zh_end = zh_start
    for i in range(zh_start, len(ml_chunk)):
        if ml_chunk[i] == '{': depth += 1
        elif ml_chunk[i] == '}':
            depth -= 1
            if depth == 0:
                zh_end = i
                break
    zh_block = ml_chunk[zh_start:zh_end]
    print(f'ZH block size: {len(zh_block)} chars')
    # Find stamp-related keys
    for key in ['mRulePer', 'mReward', 'mFreeItem', 'stamp', 'Stamp', 'Purchase', 'purchase', 'Free Menu', 'free_menu']:
        m2 = re.search(re.escape(key) + r"[^']*'([^']*)'", zh_block)
        if m2:
            print(f'  Found: {m2.group()[:80]}')
