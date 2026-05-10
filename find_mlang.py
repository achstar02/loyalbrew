import re
with open('app.js','r',encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS object
m = re.search(r'const MERCHANT_LANGS\s*=\s*\{', js)
if m:
    pos = m.start()
    print(f'MERCHANT_LANGS at {pos}')
    # Print first 2000 chars
    print(js[pos:pos+3000])
