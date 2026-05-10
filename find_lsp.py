JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()
p = JS.find('function loadShopPointsSettings')
if p < 0:
    p = JS.find('loadShopPointsSettings')
print(f'Position: {p}')
if p > 0:
    print(JS[p:p+800])
else:
    # Search broader
    import re
    for m in re.finditer(r'loadShopPointsSettings', JS):
        print(f'Found at {m.start()}')
        print(JS[m.start():m.start()+400])
        print('---')
