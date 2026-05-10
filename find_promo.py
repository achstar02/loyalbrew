BASE = r'C:\Users\Administrator\CodeBuddy\20260416214625'
with open(BASE + r'\deploy\app.js','r',encoding='utf-8') as f:
    js = f.read()
# Find loadPromoSettings function
idx = js.find('function loadPromoSettings')
if idx >= 0:
    # Find the end of the function (simple approach: find next function)
    next_func = js.find('function ', idx + 10)
    func_body = js[idx:next_func] if next_func > 0 else js[idx:idx+1000]
    with open(BASE + r'\load_promo.txt','w',encoding='utf-8') as f:
        f.write(func_body[:1500])
    print('Found at', idx)
else:
    print('NOT FOUND')
