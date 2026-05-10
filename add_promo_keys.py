import re, shutil

BAK = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js.bak'
SRC = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

shutil.copy(SRC, SRC + '.bak_fix2')
JS = open(SRC, 'r', encoding='utf-8').read()

ml = JS.find('const MERCHANT_LANGS')

# Find real block positions using regex + quote-aware brace matching
def find_block_abs(js, ml, name):
    pattern = re.compile(name + r'\s*:\s*\{')
    m = pattern.search(js[ml:ml+50000])
    if not m:
        return None, None
    start = ml + m.start() + len(name) + 3  # skip 'name: {'
    # Find block end
    depth = 0
    for i in range(start, len(js)):
        ch = js[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth <= 0:
                return start, i + 1
    return start, None

en_start, en_end = find_block_abs(JS, ml, 'en')
zh_start, zh_end = find_block_abs(JS, ml, 'zh')
ms_start, ms_end = find_block_abs(JS, ml, 'ms')
ta_start, ta_end = find_block_abs(JS, ml, 'ta')

print(f'en: {en_start}-{en_end}')
print(f'zh: {zh_start}-{zh_end}')
print(f'ms: {ms_start}-{ms_end}')
print(f'ta: {ta_start}-{ta_end}')

# Build new key blocks to add
# promoEngineTitle, promoEngineDesc, enablePromo, busyThreshold, promoHideHint
# shopInfo (ta already has it)

translations = {
    'promoEngineTitle': {
        'en': 'Promo Engine',
        'zh': '促销引擎',
        'ms': 'Enjin Promo',
        'ta': 'இனம்முறை'
    },
    'promoEngineDesc': {
        'en': 'Off-peak pricing to attract more orders',
        'zh': '非高峰时段特价，吸引更多订单',
        'ms': 'Harga bukan puncak untuk menarik pesanan lebih',
        'ta': 'இல்லாத நேரம் விலை போன்றவற்றை ஈர்க்க'
    },
    'enablePromo': {
        'en': 'Enable Promo',
        'zh': '启用促销',
        'ms': 'Aktifkan Promo',
        'ta': 'இனம்மை செயல்படுத்து'
    },
    'busyThreshold': {
        'en': 'Busy threshold (orders)',
        'zh': '繁忙阈值（订单）',
        'ms': 'Ambang sibuk (pesanan)',
        'ta': 'நெரிசல் அளவு (ஆர்டர்)'
    },
    'promoHideHint': {
        'en': 'Leave empty to always show promo price',
        'zh': '留空则一直显示促销价',
        'ms': 'Biarkan kosong untuk sentiasa tunjuk harga promo',
        'ta': 'காலியாக விட்டால் எப்போதும் இனம்மு விலை'
    },
    'shopInfo': {
        'en': 'Shop Info',
        'zh': '店铺信息',
        'ms': 'Info Kedai',
        # ta already has shopInfo
    }
}

# Build new key strings for each language block
en_additions = []
zh_additions = []
ms_additions = []
ta_additions = []

for key, langs in translations.items():
    en_additions.append(f"    {key}: '{langs['en']}',")
    zh_additions.append(f"    {key}: '{langs['zh']}',")
    ms_additions.append(f"    {key}: '{langs['ms']}',")
    if 'ta' in langs:
        ta_additions.append(f"    {key}: '{langs['ta']}',")

en_insert = '\n    ' + '\n    '.join(en_additions) + '\n'
zh_insert = '\n    ' + '\n    '.join(zh_additions) + '\n'
ms_insert = '\n    ' + '\n    '.join(ms_additions) + '\n'
ta_insert = '\n    ' + '\n    '.join(ta_additions) + '\n'

# Insert before the closing '}' of each block
# For en: insert just before the final '  },' before '  zh:'
zh_marker_abs = JS.find('  zh:', ml)
en_close_marker = JS.rfind('  },', en_start, zh_marker_abs)
print(f'\nen close marker at: {en_close_marker}')
print(f'Context: {JS[en_close_marker-20:en_close_marker+10]}')

new_JS = JS[:en_close_marker] + en_insert + JS[en_close_marker:]
# Adjust positions for zh insertion
zh_abs_adj = en_close_marker + len(en_insert)
zh_marker_adj = zh_abs_adj + (zh_marker_abs - en_close_marker)

# For zh: insert just before the '  ms:' marker
ms_marker_abs = JS.find('  ms:', ml)
zh_close_marker = JS.rfind('  },', zh_start, ms_marker_abs)
print(f'\nzh close marker at: {zh_close_marker}')
print(f'Context: {JS[zh_close_marker-20:zh_close_marker+10]}')

# Rebase from new_JS
new_JS2 = new_JS[:zh_close_marker] + zh_insert + new_JS[zh_close_marker:]
# Find ms marker in new_JS2
ms_abs2 = new_JS.find('  ms:', ml)
zh_close_marker2 = new_JS.rfind('  },', zh_start, ms_abs2)
if zh_close_marker2 < 0:
    # Search after zh_start in new_JS2
    zh_section = new_JS2[zh_start:zh_start+20000]
    zh_close_marker2 = zh_start + zh_section.rfind('  },')

print(f'\nzh close marker2 at: {zh_close_marker2}')

new_JS3 = new_JS2[:zh_close_marker2] + zh_insert + new_JS2[zh_close_marker2:]
ms_abs3 = new_JS3.find('  ms:', ml)
ms_section = new_JS3[ms_abs3:ms_abs3+20000]
ms_close_marker = ms_abs3 + ms_section.rfind('  },')

print(f'ms close marker at: {ms_close_marker}')
new_JS4 = new_JS3[:ms_close_marker] + ms_insert + new_JS3[ms_close_marker:]
ta_abs4 = new_JS4.find('  ta:', ml)
ta_section = new_JS4[ta_abs4:ta_abs4+20000]
ta_close_marker = ta_abs4 + ta_section.rfind('  },')

print(f'ta close marker at: {ta_close_marker}')
new_JS5 = new_JS4[:ta_close_marker] + ta_insert + new_JS4[ta_close_marker:]

open(SRC, 'w', encoding='utf-8').write(new_JS5)
print(f'\nSaved! New size: {len(new_JS5)} (old: {len(JS)})')

# Validate syntax
import subprocess
result = subprocess.run(['node', '-e', 'try{new Function(require("fs").readFileSync("' + SRC.replace('\\', '/') + '","utf-8"));console.log("OK")}catch(e){console.log("ERROR:",e.message)}'],
                       capture_output=True, text=True, timeout=10, cwd=r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy')
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr[:500])
