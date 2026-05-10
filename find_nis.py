JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

# Find populateNewItemSelect
p = JS.find('function populateNewItemSelect')
print(f'populateNewItemSelect at: {p}')
if p > 0:
    with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\nis_out.txt', 'w', encoding='utf-8') as f:
        f.write(f'Position: {p}\n')
        f.write(JS[p:p+3000])

# Also find what calls loadShopPointsSettings in switchMerchantTab
p2 = JS.find('function switchMerchantTab')
if p2 > 0:
    with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\switch_out.txt', 'w', encoding='utf-8') as f:
        f.write(JS[p2:p2+1000])

# Find the actual error - look for .type access on potentially null
for pattern in ['.type', '.status', 'null]', 'undefined]']:
    positions = [m.start() for m in __import__('re').finditer(pattern, JS)]
    for pos in positions[:3]:
        context = JS[max(0,pos-50):pos+50]
        with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\error_search.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n=== {pattern} at {pos} ===\n')
            f.write(context + '\n')
