import re
BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()

# Find switchMerchantTab function and add applyMerchantLang() call
old_code = "if (tabId === 'tab-settings')   { loadPromoSettings(); loadShopSettings(); loadPointsSettings(); }"
new_code = "if (tabId === 'tab-settings')   { loadPromoSettings(); loadShopSettings(); loadPointsSettings(); applyMerchantLang(); }"

if old_code in js:
    js = js.replace(old_code, new_code)
    with open(BASE + r'\deploy\app.js','w',encoding='utf-8') as f:
        f.write(js)
    print('Fixed: added applyMerchantLang() to tab-settings switch')
else:
    print('Pattern not found')
