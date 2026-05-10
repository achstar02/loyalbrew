with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find customer LANGS
lgs_pos = js.find('const LANGS = {')
en_start = js.find('en: {', lgs_pos)
zh_start = js.find('zh: {', lgs_pos)
ms_start = js.find('ms: {', lgs_pos)
ta_start = js.find('ta: {', lgs_pos)

blocks = {}
blocks['en'] = js[en_start:zh_start]
blocks['zh'] = js[zh_start:ms_start]
blocks['ms'] = js[ms_start:ta_start]
blocks['ta'] = js[ta_start:ta_start+50000]

check_keys = ['welcomeBack', 'drinkToday', 'firebaseNote', 'myAccount', 'orderNow', 'myStampCard', 'topUp', 'loyalbrew_brand', 'noMembersYet', 'noTransactionsYet']

with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\cust_langs_check.txt', 'w', encoding='utf-8') as out:
    for lang in ['en', 'zh', 'ms', 'ta']:
        out.write('--- %s ---\n' % lang)
        for k in check_keys:
            found = ('"%s":' % k) in blocks[lang] or ("'%s':" % k) in blocks[lang]
            out.write('  %s: %s\n' % (k, 'FOUND' if found else 'MISSING'))
    
    # Also check if the landing page content is dynamically generated or uses data-i18n
    # Look for the specific pattern in app.js
    out.write('\n--- Looking for landing page HTML generation ---\n')
    # Search for welcomeBack usage
    pos = 0
    count = 0
    while True:
        pos = js.find('welcomeBack', pos)
        if pos < 0 or count > 5:
            break
        out.write('  welcomeBack at %d: %s\n' % (pos, js[pos-50:pos+80]))
        out.write('\n')
        pos += 1
        count += 1
