import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('C:/Users/Administrator/CodeBuddy/20260416214625/nav_search.txt', 'w', encoding='utf-8') as out:
    for pattern in [r'catNewItems', r'mTabNewItems', r'mNiLaunch|new.?item.*tab|\u2728']:
        matches = [(m.start(), js[max(0,m.start()-60):m.end()+80]) for m in re.finditer(pattern, js, re.IGNORECASE)]
        if matches:
            out.write(f'=== {pattern} ({len(matches)} matches) ===\n')
            for pos, ctx in matches[:5]:
                out.write(f'  @{pos}: {repr(ctx)}\n')
            out.write('\n')
    
    # Also search for Tamil text that might be hardcoded
    out.write('=== Searching for Tamil in nav generation ===\n')
    for pattern in [r'\u0ba4\u0bbf\u0baf\u0bae\u0bcd', r'\u0baa\u0bc1\u0ba4\u0bbf\u0baf']:
        matches = [(m.start(), js[max(0,m.start()-40):m.end()+40]) for m in re.finditer(pattern, js)]
        if matches:
            out.write(f'  Found {len(matches)} matches\n')
            for pos, ctx in matches[:3]:
                out.write(f'  @{pos}: {repr(ctx)}\n')

print('Done - see nav_search.txt')
