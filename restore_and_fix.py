import shutil, os, re

# Step 1: Restore from clean backup
bak = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js.bak'
dst = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
shutil.copy(bak, dst)
print(f'Restored. Size: {os.path.getsize(dst)}')

with open(dst, 'r', encoding='utf-8') as f:
    js = f.read()

# Step 2: Find MERCHANT_LANGS and add missing promo keys
ml_start = js.find('const MERCHANT_LANGS')
if ml_start < 0:
    print('ERROR: MERCHANT_LANGS not found')
    exit(1)

print(f'MERCHANT_LANGS at: {ml_start}')

# New keys to add (6 keys x 4 languages = 24 translations)
new_keys = {
    'promoEngineTitle': {
        'en': "Promo Engine",
        'zh': "促销引擎",
        'ms': "Enjin Promo",
        'ta': "ப்ரோமோ இயந்திரம்"
    },
    'promoEngineDesc': {
        'en': "Auto-apply promotions based on time/day",
        'zh': "根据时间/天自动应用促销",
        'ms': "Guna promosi auto berdasarkan masa/hari",
        'ta': "நேரம்/நாள் அடிப்படையில் தானாக விளம்பரங்களைபயன்படுத்து"
    },
    'enablePromo': {
        'en': "Enable Promo",
        'zh': "启用促销",
        'ms': "Aktifkan Promo",
        'ta': "விளம்பரங்களை இயக்கு"
    },
    'busyThreshold': {
        'en': "Busy Threshold",
        'zh': "繁忙阈值",
        'ms': "Ambang Sibuk",
        'ta': "சிக்கல் வரம்பு"
    },
    'promoHideHint': {
        'en': "(hidden when off)",
        'zh': "（关闭时隐藏）",
        'ms': "(tersembunyi bila tutup)",
        'ta': "(அணையில் மறைக்கப்பட்டது)"
    },
    'shopInfo': {
        'en': "Shop Info",
        'zh': "店铺信息",
        'ms': "Maklumat Kedai",
        'ta': "கடை தகவல்"
    }
}

# For each language block, find its end and insert missing keys before the closing brace
for lang_code in ['en', 'zh', 'ms', 'ta']:
    # Find this language block's opening position within MERCHANT_LANGS
    # Pattern: 2 spaces + lang_code + ': {'
    pattern = f'  {lang_code}: {{'
    block_start = js.find(pattern, ml_start)
    if block_start < 0:
        print(f'WARNING: {lang_code} block not found in MERCHANT_LANGS')
        continue
    
    # Use brace matching to find end of this block
    depth = 0
    i = js.find('{', block_start)  # first { after label
    if i < 0:
        print(f'WARNING: no opening brace for {lang_code}')
        continue
    
    # Start counting from the first {
    depth = 1
    in_string = False
    string_char = None
    end_pos = -1
    
    while i < len(js) - 1:
        i += 1
        c = js[i]
        
        # Handle string literals (skip braces inside strings)
        if c == '"' or c == "'":
            if not in_string:
                in_string = True
                string_char = c
            elif c == string_char and js[i-1] != '\\':
                in_string = False
        
        if not in_string:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end_pos = i
                    break
    
    if end_pos < 0:
        print(f'WARNING: could not find end of {lang_code} block')
        continue
    
    # Check which keys are already present
    block_content = js[block_start:end_pos]
    keys_to_add = {}
    for key, translations in new_keys.items():
        if key + ':' not in block_content:
            keys_to_add[key] = translations[lang_code]
    
    if not keys_to_add:
        print(f'{lang_code}: all keys already present')
        continue
    
    # Insert new keys before the closing } of this block
    insert_text = ''
    for key, value in keys_to_add.items():
        insert_text += f"    {key}: '{value}',\n"
    
    insertion_point = end_pos  # right before the closing }
    js = js[:insertion_point] + '\n' + insert_text + js[insertion_point:]
    print(f'{lang_code}: added {len(keys_to_add)} keys at pos {insertion_point}')

# Write fixed file
with open(dst, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'Written. New size: {os.path.getsize(dst)}')
