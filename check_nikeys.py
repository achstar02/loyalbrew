import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

ml = JS.find('const MERCHANT_LANGS')
print(f'MERCHANT_LANGS at: {ml}')

keys = ['mNiLaunch','mNiEnds','mNiDeactivate','mNiDelete','mNiNoEndDate','mNiSpecial','mNiWas',
        'mChooseAnItem','mSelectMenuItem']

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\check_nikeys.txt', 'w', encoding='utf-8') as f:
    area = JS[ml:ml+50000]
    for k in keys:
        p = area.find(k)
        if p > 0:
            end = area.find("',", p+len(k)+3)
            val = area[p+len(k)+3:end]
            f.write(f'{k}: {val[:60]}\n')
        else:
            f.write(f'{k}: NOT FOUND\n')

    # Also check: what about new item management form labels?
    # Check promoEngine related
    promo_keys = ['promoEngineTitle', 'promoEngineDesc', 'enablePromo', 'startTime', 'endTime',
                  'activeDays', 'busyThreshold', 'promoHideHint', 'shopInfo']
    f.write('\n=== promoEngine keys ===\n')
    for k in promo_keys:
        p = area.find(k)
        if p > 0:
            end = area.find("',", p+len(k)+3)
            val = area[p+len(k)+3:end]
            f.write(f'{k}: {val[:60]}\n')
        else:
            f.write(f'{k}: NOT FOUND\n')
