BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()
# Find where page-merchant-settings loads
idx = js.find('page-merchant-settings')
if idx >= 0:
    start = max(0, idx - 200)
    end = min(len(js), idx + 300)
    with open(BASE + r'\settings_page.txt','w',encoding='utf-8') as f:
        f.write(js[start:end])
    print('Found at', idx)
else:
    print('NOT FOUND')
