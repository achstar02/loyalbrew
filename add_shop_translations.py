import re, subprocess

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# New translations to add (EN/ZH/MS) - only simple keys
translations = [
    ('leaveEmptyBanner', 'Leave empty to hide banner', '留空隐藏横幅', 'Kosongkan untuk sembunyi banner'),
    ('smallTextHint', 'Small text (e.g. "Welcome back")', '小字（例如"欢迎回来"）', 'Teks kecil (cth: "Selamat kembali")'),
    ('bigTitleHint', 'Big title (e.g. "What\'s new today?")', '大标题（例如"今天想喝什么？"）', 'Tajuk besar (cth: "Apa yang baharu hari ini?")'),
    ('bannerImageUrl', 'Banner Image URL', '横幅图片链接', 'URL Gambar Banner'),
    ('saveShopInfo', 'Save Shop Info', '保存店铺信息', 'Simpan Maklumat Kedai'),
    ('pointsSettings', 'Points Settings', '积分设置', 'Tetapan Mata'),
    ('pointsPerRM', 'Points per RM', '每 RM 积分', 'Mata setiap RM'),
    ('shopSettings', 'Shop Settings', '店铺设置', 'Tetapan Kedai'),
]

def find_block_end(text, start):
    """Find the } that closes the object starting at or after `start`"""
    i = start
    while i < len(text) and text[i] != '{':
        i += 1
    depth = 1
    i += 1
    while i < len(text) and depth > 0:
        c = text[i]
        if c == '{': depth += 1
        elif c == '}': depth -= 1
        i += 1
    return i - 1  # position of closing }

def insert_at_block_end(text, block_label, entries):
    """Insert key:value pairs before the closing } of a language block"""
    pos = text.find(block_label)
    if pos == -1:
        print(f"WARNING: Cannot find {block_label}")
        return text
    end_pos = find_block_end(text, pos)
    insert_str = ',\n    ' + ',\n    '.join(entries)
    new_text = text[:end_pos] + insert_str + text[end_pos:]
    return new_text

en_entries = [f"{k}: '{en}'" for k, en, zh, ms in translations]
zh_entries = [f"{k}: '{zh}'" for k, en, zh, ms in translations]
ms_entries = [f"{k}: '{ms}'" for k, en, zh, ms in translations]

js = insert_at_block_end(js, 'en:', en_entries)
js = insert_at_block_end(js, 'zh:', zh_entries)
js = insert_at_block_end(js, 'ms:', ms_entries)

with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f"Done! Size: {len(js)} chars")

# Verify syntax
result = subprocess.run(['node', '-e',
    "try{new Function(require('fs').readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js','utf-8'));console.log('SYNTAX OK')}catch(e){console.log('ERROR:',e.message)}"],
    capture_output=True, text=True)
print(result.stdout.strip())
if result.stderr:
    print("STDERR:", result.stderr[:200])
