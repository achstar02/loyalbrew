import re
js = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
ml = js.find('const MERCHANT_LANGS')
keys = ['mTitleQuickActions','mBtnViewOrders2','mBtnMenuMgmt2','mBtnShopSettings2','mBtnKitchenDisplay2']
for k in keys:
    pat = re.escape(k) + r":\s*'([^']*)'"
    full = re.search(pat, js)
    if full:
        print(f'{k}: FOUND = {full.group(1)}')
    else:
        # check LANGS too
        lang_match = re.search(pat, js[:js.find('const MERCHANT_LANGS')])
        print(f'{k}: NOT FOUND in MERCHANT_LANGS | In LANGS: {lang_match.group(1) if lang_match else "NO"}')
