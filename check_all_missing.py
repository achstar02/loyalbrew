import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
ml = JS.find('const MERCHANT_LANGS')

# Find block positions using quote-aware parsing
# Find en: { block start and end
en_start = JS.find('en:', ml) + 3
depth = 0
for i, ch in enumerate(JS[en_start:], en_start):
    if ch == '{': depth += 1
    elif ch == '}': depth -= 1
    if depth == 0 and i > en_start:
        en_end = i + 1
        break

ms_start = JS.find('ms:', en_end) + 3
depth = 0
for i, ch in enumerate(JS[ms_start:], ms_start):
    if ch == '{': depth += 1
    elif ch == '}': depth -= 1
    if depth == 0 and i > ms_start:
        ms_end = i + 1
        break

zh_start = JS.find('zh:', ms_end) + 3
depth = 0
for i, ch in enumerate(JS[zh_start:], zh_start):
    if ch == '{': depth += 1
    elif ch == '}': depth -= 1
    if depth == 0 and i > zh_start:
        zh_end = i + 1
        break

ta_start = JS.find('ta:', zh_end) + 3
depth = 0
for i, ch in enumerate(JS[ta_start:], ta_start):
    if ch == '{': depth += 1
    elif ch == '}': depth -= 1
    if depth == 0 and i > ta_start:
        ta_end = i + 1
        break

print(f'en: {en_start}-{en_end}')
print(f'ms: {ms_start}-{ms_end}')
print(f'zh: {zh_start}-{zh_end}')
print(f'ta: {ta_start}-{ta_end}')

# Check if keys exist
keys_to_check = ['mNiLaunch', 'mNiEnds', 'mNiDeactivate', 'mNiDelete', 'mNiNoEndDate',
                 'mNiSpecial', 'mNiWas', 'mChooseAnItem', 'mSelectMenuItem',
                 'promoEngineTitle', 'promoEngineDesc', 'enablePromo', 'busyThreshold',
                 'promoHideHint', 'shopInfo']

translations = {
    'mNiLaunch': {'en': 'Launch:', 'zh': '发布日期：', 'ms': 'Lancar:', 'ta': 'வெளியீடு:'},
    'mNiEnds': {'en': 'Ends:', 'zh': '截止：', 'ms': 'Tamat:', 'ta': 'முடிவு:'},
    'mNiDeactivate': {'en': 'Deactivate', 'zh': '下架', 'ms': 'Nyahaktif', 'ta': 'நிறுத்து'},
    'mNiDelete': {'en': 'Delete', 'zh': '删除', 'ms': 'Padam', 'ta': 'நீக்கு'},
    'mNiNoEndDate': {'en': 'No end date', 'zh': '无截止日期', 'ms': 'Tiada tarikh tamat', 'ta': 'முடிவு தேதி இல்லை'},
    'mNiSpecial': {'en': 'Special: RM', 'zh': '特价：RM', 'ms': 'Istimewa: RM', 'ta': 'சிறப்பு: RM'},
    'mNiWas': {'en': 'was RM', 'zh': '原价 RM', 'ms': 'asal RM', 'ta': 'முன்பு RM'},
    'mChooseAnItem': {'en': '-- Choose an item --', 'zh': '-- 选择商品 --', 'ms': '-- Pilih item --', 'ta': '-- பொருளைத் தேர்வுசெய்க --'},
    'mSelectMenuItem': {'en': 'Select Menu Item', 'zh': '选择菜单商品', 'ms': 'Pilih Item Menu', 'ta': 'மெனு பொருளைத் தேர்வுசெய்க'},
    'promoEngineTitle': {'en': 'Promo Engine', 'zh': '促销引擎', 'ms': 'Enjin Promo', 'ta': 'இனம்முறை'},
    'promoEngineDesc': {'en': 'Off-peak pricing to attract more orders', 'zh': '非高峰时段特价，吸引更多订单', 'ms': 'Harga bukan puncak untuk attracts pesanan', 'ta': 'இல்லாத நேரம் விலைக்கும் உத்தேச வாங்குபவர்களை ஈர்க்க'},
    'enablePromo': {'en': 'Enable Promo', 'zh': '启用促销', 'ms': 'Aktifkan Promo', 'ta': 'இனம்மை செயல்படுத்து'},
    'busyThreshold': {'en': 'Busy threshold (orders)', 'zh': '繁忙阈值（订单）', 'ms': 'Ambang sibuk (pesanan)', 'ta': 'நெரிசல் அளவு (ஆர்டர்)'},
    'promoHideHint': {'en': 'Leave empty to always show promo price', 'zh': '留空则一直显示促销价', 'ms': 'Biarkan kosong untuk sentiasa tunjuk harga promo', 'ta': 'காலியாக விட்டால் எப்போதும் இனம்மு விலை காட்டும்'},
    'shopInfo': {'en': 'Shop Info', 'zh': '店铺信息', 'ms': 'Info Kedai', 'ta': 'கடை தகவல்'},
}

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\add_all_missing.txt', 'w', encoding='utf-8') as f:
    for key in keys_to_check:
        en_exists = key in JS[en_start:en_end]
        zh_exists = key in JS[zh_start:zh_end]
        ms_exists = key in JS[ms_start:ms_end]
        ta_exists = key in JS[ta_start:ta_end]
        f.write(f'{key}: en={"Y" if en_exists else "N"} zh={"Y" if zh_exists else "N"} ms={"Y" if ms_exists else "N"} ta={"Y" if ta_exists else "N"}\n')
