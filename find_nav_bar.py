import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('C:/Users/Administrator/CodeBuddy/20260416214625/nav_bar_html.txt', 'w', encoding='utf-8') as out:
    # Find mnav class (merchant nav buttons)
    for pattern in [r'mnav.*onclick.*tab', r'class="mnav"', r"class='mnav'", r'mnav\b']:
        matches = [(m.start(), js[max(0,m.start()-200):m.end()+200]) for m in re.finditer(pattern, js)]
        if matches:
            out.write(f'=== {pattern} ({len(matches)} matches) ===\n')
            for pos, ctx in matches[:3]:
                out.write(f'  @{pos}:\n{ctx}\n')
                out.write('=== END ===\n\n')

    # Find where merchant nav tabs HTML is built - look for tab-overview button
    idx = js.find('tab-overview')
    if idx > 0:
        out.write(f'=== Context around "tab-overview" (@{idx}) ===\n')
        out.write(js[max(0,idx-800):idx+200])
        out.write('\n')

print('Done')
