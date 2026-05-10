with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

ml_start = js.find('const MERCHANT_LANGS')
print('MERCHANT_LANGS at:', ml_start)

# Show the structure around each language block
for label, offset in [('en', 297947), ('ms', 299057), ('zh', 305771), ('ta', 319732)]:
    print(f'\n=== {label} at {offset} ===')
    chunk = js[offset:offset+300]
    # Replace non-ascii for safety
    safe = chunk.encode('ascii', errors='replace').decode()
    print(safe)
