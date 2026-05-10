import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
js = open(JS, 'r', encoding='utf-8').read()

# New translations for the 5 missing keys
new_keys = {
    'mTitleQuickActions': {
        'en': "Quick Actions",
        'zh': "\u5feb\u6377\u64cd\u4f5c",
        'ms': "Tindakan Pantas",
        'ta': "\u0b9a\u0bc1\u0b9f\u0bcd\u0b9f \u0b9a\u0bc6\u0baf\u0bb2\u0bcd\u0b95\u0bb3\u0bcd",
    },
    'mBtnViewOrders2': {
        'en': "View Orders",
        'zh': "\u67e5\u770b\u8ba2\u5355",
        'ms': "Lihat Pesanan",
        'ta': "\u0b86\u0baf\u0bcd\u0b9f\u0bb0\u0bcd\u0b95\u0bb3\u0bcd \u0baaa\u0bbe\u0bb0\u0bcd",
    },
    'mBtnMenuMgmt2': {
        'en': "Menu Management",
        'zh': "\u83dc\u5355\u7ba1\u7406",
        'ms': "Urusan Menu",
        'ta': "\u0baae\u0bc6\u0ba9\u0bc1 \u0baa\u0bb0\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5",
    },
    'mBtnShopSettings2': {
        'en': "Shop Settings",
        'zh': "\u5e97\u94fa\u8bbe\u7f6e",
        'ms': "Tetapan Kedai",
        'ta': "\u0b95\u0b9f\u0bc8 \u0b85\u0bae\u0bc8\u0baa\u0bcd\u0baa\u0bc1\u0b9f\u0bc1\u0ba4\u0bcd\u0ba4\u0bc1\u0b95\u0bb3\u0bcd",
    },
    'mBtnKitchenDisplay2': {
        'en': "Kitchen Display",
        'zh': "\u53a8\u623f\u663e\u793a",
        'ms': "Paparan Dapur",
        'ta': "\u0b9a\u0bae\u0bc8\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f \u0b95\u0bbe\u0b9f\u0bcd\u0b9a\u0bbf",
    },
}

# Find MERCHANT_LANGS and each language block
ml_start = js.find('const MERCHANT_LANGS')
en_pos = js.find('en:', ml_start)
# Find actual block starts by looking for patterns
# We need to insert after the first key in each block

count = 0
for lang_code in ['en', 'zh', 'ms', 'ta']:
    # Find this language block within MERCHANT_LANGS
    lang_pos = js.find(lang_code + ':', ml_start)
    if lang_pos == -1 or lang_pos > ml_start + 100000:
        print(f'{lang_code}: NOT FOUND in MLANGS range')
        continue
    
    # Find first key-value pair after "lang_code:"
    # Look for pattern like: key: 'value',
    block_content_start = js.find('{', lang_pos) + 1
    
    # Insert all new keys at the start of this block
    inserts = ""
    for key_name, translations in new_keys.items():
        val = translations[lang_code]
        inserts += f"    {key_name}: '{val}',\n"
    
    # Insert after the opening brace
    insert_pos = block_content_start
    js = js[:insert_pos] + inserts + js[insert_pos:]
    count += len(new_keys)
    # Adjust ml_start for subsequent searches since we added text
    ml_start += len(inserts)

open(JS, 'w', encoding='utf-8').write(js)
print(f'Done! Added {count} keys total (5 keys x {len(new_keys)} languages)')
