import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

# Search for loadShopPointsSettings or similar
for k in ['loadShopPointsSettings', 'loadShopSettings', 'ShopPointsSettings', 'shopPointsSettings']:
    positions = [m.start() for m in re.finditer(k, JS)]
    print(f'{k}: {positions}')

# Check around the error location
print('\nLine 14 context (first 10000 chars):')
lines = JS[:10000].split('\n')
for i, line in enumerate(lines[:20], 1):
    print(f'L{i}: {line[:100]}')

# Check for promoEngine in the file
for m in re.finditer(r'promoEngine|PromoEngine|shopPointsSettings', JS):
    print(f'\nFound at {m.start()}: {JS[m.start():m.start()+100]}')
