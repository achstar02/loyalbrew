import re

with open('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

with open('C:/Users/Administrator/CodeBuddy/20260416214625/nav_html_search.txt', 'w', encoding='utf-8') as out:
    # Find where tab-new-items or the nav bar HTML is generated
    for pattern in [r'tab-new-items', r'tab-overview', r'tab-orders', r'tab-menu-mgmt']:
        matches = [(m.start(), js[max(0,m.start()-150):m.end()+150]) for m in re.finditer(pattern, js)]
        if matches:
            out.write(f'=== {pattern} ({len(matches)} matches) ===\n')
            for pos, ctx in matches[:3]:
                out.write(f'  @{pos}:\n{ctx}\n')
                out.write('=== END ===\n\n')

    # Find the function that renders merchant dashboard with nav tabs
    # Look for the HTML that contains the tab buttons
    idx = js.find("tab-new-items")
    if idx > 0:
        out.write(f'=== Wide context around "tab-new-items" (@{idx}) ===\n')
        out.write(js[max(0,idx-500):idx+500])
        out.write('\n')

print('Done')
