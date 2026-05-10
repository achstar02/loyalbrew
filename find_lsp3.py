import re, codecs

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

positions = [m.start() for m in re.finditer(r'loadShopSettings', JS)]
for p in positions[:3]:
    # Show context around each occurrence
    with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\find_lsp_out.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n=== Position {p} ===\n')
        f.write(JS[p:p+600] + '\n')

# Search for promoEngine in the file
promo_pos = [m.start() for m in re.finditer(r'promoEngine|PromoEngine', JS)]
for p in promo_pos[:5]:
    with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\find_lsp_out.txt', 'a', encoding='utf-8') as f:
        f.write(f'\nPromo at {p}: {JS[p:p+100]}\n')
