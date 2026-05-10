import re

JS = open(r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js', 'r', encoding='utf-8').read()

# Search for promoEngine in the file - find all instances
promo_positions = [m.start() for m in re.finditer(r'promoEngineTitle|promoEngineDesc|promoHideHint|shopInfo', JS)]
print(f'Total promoEngineTitle keys found: {len(promo_positions)}')
for p in promo_positions:
    context = JS[p:p+80]
    print(f'\nAt {p}: {context}')

# Check for the error source - search for null.type or similar
null_type = JS.find('null')
print(f'\nFirst null: {null_type} -> {JS[null_type:null_type+30]}')

# Find the actual null.type pattern
for m in re.finditer(r'null\.type|null\[', JS):
    pos = m.start()
    print(f'\nAt {pos}: {JS[max(0,pos-50):pos+50]}')
    if pos > 1000:
        break

# Check around app.js:14:2595  -- find line 14 in minified JS
lines = JS.split('\n')
print(f'\nTotal lines: {len(lines)}')
if len(lines) >= 14:
    line14 = lines[13]
    print(f'Line 14 length: {len(line14)}')
    if len(line14) > 2595:
        print(f'Line 14[2590:2610]: {line14[2590:2610]}')
    # Print lines around the error
    for i in range(10, 17):
        if i < len(lines):
            print(f'L{i+1}: {lines[i][:200]}')
