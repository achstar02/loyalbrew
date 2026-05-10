import re

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

keys = ['leaveEmptyBanner', 'smallTextHint', 'bigTitleHint', 'bannerImageUrl', 'saveShopInfo', 'pointsSettings', 'pointsPerRM', 'shopSettings']

print(f"File size: {len(js)} chars")
print()

for k in keys:
    # Find in en block (first occurrence after LANGS)
    en_m = re.search(rf"{k}\s*:\s*'([^']*)'", js)
    # Find in zh block
    zh_match = re.search(rf"zh:\s*\{{[^}}]*{k}\s*:\s*'([^']*)'", js, re.DOTALL)
    ms_match = re.search(rf"ms:\s*\{{[^}}]*{k}\s*:\s*'([^']*)'", js, re.DOTALL)
    
    en_val = en_m.group(1) if en_m else 'MISSING'
    zh_val = zh_match.group(1) if zh_match else 'MISSING'
    ms_val = ms_match.group(1) if ms_match else 'MISSING'
    
    status = 'OK' if en_val != 'MISSING' and zh_val != 'MISSING' and ms_val != 'MISSING' else 'NEEDS FIX'
    print(f"[{status}] {k:25s} EN={en_val:30s} ZH={zh_val:30s} MS={ms_val}")
