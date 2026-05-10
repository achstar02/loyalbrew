with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS object
ml_start = js.find('const MERCHANT_LANGS')
print('MERCHANT_LANGS at:', ml_start)

# Find each language block within MERCHANT_LANGS
search_from = ml_start
en_in_ml = js.find('en:', search_from)
zh_in_ml = js.find('zh:', search_from)
ms_in_ml = js.find('ms:', search_from)
ta_in_ml = js.find('ta:', search_from)

print(f'en: {en_in_ml}, zh: {zh_in_ml}, ms: {ms_in_ml}, ta: {ta_in_ml}')

# Check ZH section for 'overview' key (without m prefix)
if zh_in_ml > 0 and ms_in_ml > 0:
    zh_section = js[zh_in_ml:ms_in_ml]
    # Look for specific keys
    for key in ['overview', 'orders', 'menu', 'members', 'new_items']:
        found = key in zh_section or "'" + key + "'" in zh_section
        print(f'  ZH has "{key}": {found}')
    
    # Show first 800 chars of ZH
    print()
    print('ZH section (first 800):')
    print(zh_section[:800])
