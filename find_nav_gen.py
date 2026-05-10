import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('C:/Users/Administrator/CodeBuddy/20260416214625/nav_gen_search.txt', 'w', encoding='utf-8') as out:
    # Find where merchant nav tabs are generated - look for the function that renders tabs
    for pattern in [r'mTabNewItems', r'new_items.*tab', r'tab.*new.*item', r'nav.*tab.*html']:
        matches = [(m.start(), js[max(0,m.start()-100):m.end()+100]) for m in re.finditer(pattern, js, re.IGNORECASE)]
        if matches:
            out.write(f'=== {pattern} ({len(matches)} matches) ===\n')
            for pos, ctx in matches[:8]:
                out.write(f'  @{pos}:\n{ctx}\n')
                out.write('---\n')
            out.write('\n')

    # Find the nav tab rendering function - look for tab HTML generation
    # Search for where mTabNewItems is used in a template string
    idx = js.find('mTabNewItems')
    if idx > 0:
        # Look in a wider range around each occurrence
        start = max(0, idx - 200)
        end = min(len(js), idx + 200)
        out.write(f'=== Context around first mTabNewItems ===\n')
        out.write(js[start:end])
        out.write('\n\n')

    # Also find where catNewItems is used in merchant dashboard (not customer LANGS)
    out.write('=== Looking for nav tab HTML generation with mt() or data-mi18n ===\n')
    # Find the function that generates the top navigation bar
    for pattern in [r'mt\([\'"]mTabNewItems[\'"]\)', r'mt\([\'"]tabNewItems[\'"]\)', r'data-mi18n.*New.*Item']:
        matches = [(m.start(), js[max(0,m.start()-60):m.end()+60]) for m in re.finditer(pattern, js)]
        if matches:
            out.write(f'  {pattern}: {len(matches)} matches\n')
            for pos, ctx in matches[:5]:
                out.write(f'    @{pos}: {repr(ctx)}\n')

print('Done')
