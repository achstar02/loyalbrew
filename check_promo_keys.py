import re
BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()

ml_start = js.find('const MERCHANT_LANGS')
en_start = js.find('en:', ml_start)
zh_start = js.find('zh:', ml_start)
ms_start = js.find('ms:', ml_start)
ta_start = js.find('ta:', ml_start)

result = [f'MERCHANT_LANGS at: {ml_start}', f'en: {en_start}, zh: {zh_start}, ms: {ms_start}, ta: {ta_start}', '']

for key in ['promoEngineTitle','promoEngineDesc','enablePromo','busyThreshold','promoHideHint','shopInfo']:
    result.append(f'=== {key} ===')
    for block, name, start in [('en','EN',en_start),('zh','ZH',zh_start),('ms','MS',ms_start),('ta','TA',ta_start)]:
        pattern = rf"{key}\s*:\s*'([^']*)'"
        match = re.search(pattern, js[start:start+20000])
        if match:
            result.append(f'  {name}: {match.group(1)[:40]}')
        else:
            result.append(f'  {name}: NOT FOUND')

with open(BASE + r'\promo_keys_check.txt','w',encoding='utf-8') as f:
    f.write('\n'.join(result))
print('Done')
