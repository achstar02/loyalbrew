JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
ml = JS.find('const MERCHANT_LANGS')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\block_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f'File length: {len(JS)}\n')
    f.write(f'MERCHANT_LANGS at: {ml}\n\n')

    # Find en: using regex
    import re
    en_matches = [m for m in re.finditer(r'en\s*:\s*\{', JS[ml:ml+50000])]
    ms_matches = [m for m in re.finditer(r'ms\s*:\s*\{', JS[ml:ml+50000])]
    zh_matches = [m for m in re.finditer(r'zh\s*:\s*\{', JS[ml:ml+50000])]
    ta_matches = [m for m in re.finditer(r'zh\s*:\s*\{', JS[ml:ml+50000])]

    for name, matches in [('en', en_matches), ('ms', ms_matches), ('zh', zh_matches), ('ta', ta_matches)]:
        f.write(f'{name} matches:\n')
        for m in matches:
            abs_pos = ml + m.start()
            f.write(f'  at {abs_pos}: ...{JS[abs_pos:abs_pos+50]}...\n')

    # Show content around positions
    positions = [ml, 297950, 305962, 307157]
    for pos in positions:
        if 0 <= pos < len(JS):
            snippet = JS[pos-5:pos+50].replace('\n', '\\n')
            f.write(f'\nPosition {pos}: {snippet}\n')

    # Show the actual structure
    f.write('\n=== First 2000 chars after MERCHANT_LANGS ===\n')
    f.write(JS[ml:ml+2000] + '\n')
