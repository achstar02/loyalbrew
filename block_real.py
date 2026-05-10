import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
ml = JS.find('const MERCHANT_LANGS')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\block_real.txt', 'w', encoding='utf-8') as f:
    f.write(f'MERCHANT_LANGS at: {ml}\n')

    # Find all 4 block starts using regex
    en_m = re.search(r'en\s*:\s*\{', JS[ml:ml+50000])
    zh_m = re.search(r'zh\s*:\s*\{', JS[ml:ml+50000])
    ms_m = re.search(r'ms\s*:\s*\{', JS[ml:ml+50000])
    ta_m = re.search(r'ta\s*:\s*\{', JS[ml:ml+50000])

    if en_m:
        en_abs = ml + en_m.start() + 5  # skip 'en: {'
        f.write(f'en block starts at: {en_abs}\n')
    if zh_m:
        zh_abs = ml + zh_m.start() + 5
        f.write(f'zh block starts at: {zh_abs}\n')
    if ms_m:
        ms_abs = ml + ms_m.start() + 5
        f.write(f'ms block starts at: {ms_abs}\n')
    if ta_m:
        ta_abs = ml + ta_m.start() + 5
        f.write(f'ta block starts at: {ta_abs}\n')

    # Find block ends using quote-aware brace matching
    def find_block_end(start):
        depth = 0
        started = False
        for i in range(start, len(JS)):
            ch = JS[i]
            if ch == '{':
                depth += 1
                started = True
            elif ch == '}':
                depth -= 1
            if started and depth == 0:
                return i + 1
        return -1

    if en_m:
        en_end = find_block_end(en_abs)
        f.write(f'en block ends at: {en_end}\n')
        en_size = en_end - en_abs
        f.write(f'en block size: {en_size}\n')
    if zh_m:
        zh_abs = ml + zh_m.start() + 5
        zh_end = find_block_end(zh_abs)
        f.write(f'zh block ends at: {zh_end}, size: {zh_end-zh_abs}\n')
    if ms_m:
        ms_abs = ml + ms_m.start() + 5
        ms_end = find_block_end(ms_abs)
        f.write(f'ms block ends at: {ms_end}, size: {ms_end-ms_abs}\n')
    if ta_m:
        ta_abs = ml + ta_m.start() + 5
        ta_end = find_block_end(ta_abs)
        f.write(f'ta block ends at: {ta_end}, size: {ta_end-ta_abs}\n')

    # Now check which keys exist in which blocks
    keys = ['mNiLaunch','mNiEnds','mNiDeactivate','mNiDelete','mNiNoEndDate',
            'mNiSpecial','mNiWas','mChooseAnItem','mSelectMenuItem',
            'promoEngineTitle','promoEngineDesc','enablePromo','busyThreshold',
            'promoHideHint','shopInfo']

    f.write('\n=== Key existence check ===\n')
    for k in keys:
        en_exists = k in JS[en_abs:en_end] if en_m else False
        zh_exists = k in JS[zh_abs:zh_end] if zh_m else False
        ms_exists = k in JS[ms_abs:ms_end] if ms_m else False
        ta_exists = k in JS[ta_abs:ta_end] if ta_m else False
        f.write(f'{k}: en={"Y" if en_exists else "N"} zh={"Y" if zh_exists else "N"} ms={"Y" if ms_exists else "N"} ta={"Y" if ta_exists else "N"}\n')
