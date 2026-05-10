import re
BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\index.html','r',encoding='utf-8') as f:
    html = f.read()
out_lines = []
for key in ['promoEngineTitle','promoEngineDesc','enablePromo','busyThreshold','promoHideHint','shopInfo']:
    idx = html.find(key)
    if idx >= 0:
        start = max(0,idx-50)
        end = min(len(html),idx+len(key)+30)
        context = html[start:end].replace('\n','\\n')
        out_lines.append(f'{key} at {idx}: ...{context}...')
    else:
        out_lines.append(f'{key}: NOT FOUND')
result = '\n'.join(out_lines)
with open(BASE + r'\promo_find.txt','w',encoding='utf-8') as f:
    f.write(result)
print(result)
