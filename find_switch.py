BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()
# Find the switchMerchantTab function
idx = js.find('function switchMerchantTab')
if idx >= 0:
    with open(BASE + r'\switch_tab.txt','w',encoding='utf-8') as f:
        f.write(js[idx:idx+1000])
    print('Found at', idx)
else:
    print('NOT FOUND')
