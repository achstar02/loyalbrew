import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find MERCHANT_LANGS
m = re.search(r'const MERCHANT_LANGS\s*=\s*\{', js)
if m:
    print(f'MERCHANT_LANGS at position {m.start()}')
    print(js[m.start():m.start()+1200])
else:
    print('MERCHANT_LANGS NOT FOUND')

# Find all language blocks in MERCHANT_LANGS
print('\n--- Looking for en/zh/ms/ta blocks near MERCHANT_LANGS ---')
if m:
    start = m.start()
    # Search for language keys within next 50000 chars
    chunk = js[start:start+50000]
    for lang in ['en', 'zh', 'ms', 'ta']:
        # Look for lang: { or lang: null
        matches = list(re.finditer(rf'\b{lang}\s*:\s*(null|\{{)', chunk))
        for match in matches:
            pos = start + match.start()
            print(f'{lang}: at position {pos} -> {match.group()[:50]}')
            # Show context
            ctx_start = max(0, match.start()-20)
            ctx_end = min(len(chunk), match.end()+100)
            print(f'  context: ...{chunk[ctx_start:ctx_end]}...')
