with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS
ml_pos = js.find('const MERCHANT_LANGS')
print(f'MERCHANT_LANGS at: {ml_pos}')

# Within MERCHANT_LANGS area, find en:, zh:, ms:, ta:
en_pos = js.find('en:', ml_pos)
zh_pos = js.find('zh:', ml_pos)
ms_pos = js.find('ms:', ml_pos)
ta_pos = js.find('ta:', ml_pos)
print(f'  en: at {en_pos}')
print(f'  zh: at {zh_pos}')
print(f'  ms: at {ms_pos}')
print(f'  ta: at {ta_pos}')

# zh block ends at ms: or ta:
if zh_pos > en_pos:
    zh_end = min(p for p in [ms_pos, ta_pos] if p > zh_pos)
else:
    zh_end = ml_pos + 200000

print(f'zh block: {zh_pos} to {zh_end}')
zh_area = js[zh_pos:zh_end]
print(f'zh block size: {len(zh_area)} chars')

# Check keys
for key in ['overview', 'menuMgmt2', 'viewOrders2', 'shopSettings2', 'kitchenDisplay2', 'quickActions', 'add_points_manually', 'mTabOverview', 'mStatMembers', 'mAddPointsManually', 'mTitleQuickActions', 'mBtnViewOrders2']:
    found = key in zh_area
    print(f'  zh has "{key}": {found}')

print()
en_end = zh_pos
en_area = js[en_pos:en_end]
print(f'en block size: {len(en_area)} chars')
for key in ['overview', 'menuMgmt2', 'viewOrders2', 'mTabOverview']:
    found = key in en_area
    print(f'  en has "{key}": {found}')
