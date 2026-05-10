import sys, re
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# 精确找各块
langs_start = js.index('const LANGS = {')

en_m = re.search(r'\ben\s*:\s*\{', js[langs_start:])
en_open = langs_start + en_m.end()
depth = 1; p = en_open
while depth > 0:
    if js[p] == '{': depth += 1
    elif js[p] == '}': depth -= 1
    p += 1

zh_m = re.search(r'\bzh\s*:\s*\{', js[p:])
zh_open = p + zh_m.end()
depth = 1; p2 = zh_open
while depth > 0:
    if js[p2] == '{': depth += 1
    elif js[p2] == '}': depth -= 1
    p2 += 1

ms_m = re.search(r'\bms\s*:\s*\{', js[p2:])
ms_open = p2 + ms_m.end()
depth = 1; p3 = ms_open
while depth > 0:
    if js[p3] == '{': depth += 1
    elif js[p3] == '}': depth -= 1
    p3 += 1

print(f'ZH block: {zh_open}-{p2-1} ({p2-1-zh_open} chars)')
print(f'MS block: {ms_open}-{p3-1} ({p3-1-ms_open} chars)')

keys_to_check = [
    'mRulePerOrderOpt', 'mRewardFreeItemOpt', 'catNewItems', 'filterAll',
    'placeOrder', 'newItemsTitle', 'referralProgramTitle', 'kitchenDisplayLbl',
    'getNotifiedWhenReady', 'myShopLink', 'stampCard', 'everyPurchase1Stamp',
    'freeMenuItem', 'redeemReward', 'myAccount', 'stamp_rule',
    'reward_type', 'mLoginHint', 'complaintOpenBtn', 'tngName'
]

passed = 0
failed = 0

for key in keys_to_check:
    zh_match = re.search(re.escape(key) + r"\s*:\s*'([^']*)'", js[zh_open:p2])
    ms_match = re.search(re.escape(key) + r"\s*:\s*'([^']*)'", js[ms_open:p3])
    
    zh_val = zh_match.group(1) if zh_match else 'NOT FOUND'
    ms_val = ms_match.group(1) if ms_match else 'NOT FOUND'
    
    # Check ZH has Chinese chars
    zh_has_cn = any('\u4e00' <= c <= '\u9fff' for c in zh_val)
    # MS is Malay (not Tamil, not Chinese)
    ms_is_ms = (len(ms_val) > 0 and ms_val != 'NOT FOUND' and '\u0b80' not in ms_val 
                and not any('\u4e00' <= c <= '\u9fff' for c in ms_val[:5]))
    
    zh_ok = zh_has_cn and zh_val != 'NOT FOUND'
    ms_ok = ms_is_ms and ms_val != 'NOT FOUND'
    
    if zh_ok and ms_ok:
        print(f"✅ {key}")
        passed += 1
    else:
        print(f"❌ {key}")
        print(f"   ZH: {zh_val[:70]}")
        print(f"   MS: {ms_val[:70]}")
        failed += 1

print(f"\n=== RESULT: {passed} passed, {failed} failed ===")
