import re

js_path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js'
html_path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\index.html'
out_path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\mi18n_missing.txt'

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# HTML data-mi18n keys
mi18n_keys = set(re.findall(r'data-mi18n=["\']([^"\']+)["\']', html))

# MERCHANT_LANGS en block
mlangs_pos = js.find('MERCHANT_LANGS')
en_start = js.find('en: {', mlangs_pos)
en_end = js.find('zh: {', mlangs_pos)
en_block = js[en_start:en_end]
ml_keys = set(re.findall(r'(m\w+):\s*["\']', en_block))

missing = sorted([k for k in mi18n_keys if k not in ml_keys])

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('HTML mi18n keys count: %d\n' % len(mi18n_keys))
    f.write('MERCHANT_LANGS en keys count: %d\n' % len(ml_keys))
    f.write('Missing keys (%d):\n' % len(missing))
    for k in missing:
        f.write('  ' + k + '\n')

    # Customer LANGS check
    lgs_start = js.find('const LANGS = {')
    lgs_en_start = js.find('en: {', lgs_start)
    lgs_en_end = js.find('zh: {', lgs_start)
    lgs_en_block = js[lgs_en_start:lgs_en_end]
    lgs_keys = set(re.findall(r'(m?\w+):\s*["\']', lgs_en_block))

    cust_keys = ['welcomeBack', 'drinkToday', 'firebaseNote', 'myAccount', 'orderNow', 'myStampCard', 'topUp', 'loyalbrew_brand']
    f.write('\nCustomer LANGS check:\n')
    for k in cust_keys:
        status = 'FOUND' if k in lgs_keys else 'MISSING'
        f.write('  ' + k + ': ' + status + '\n')
