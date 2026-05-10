import re
with open('app.js','r',encoding='utf-8') as f:
    js = f.read()
for pattern in [r'function\s+loadMerchantDashboard', r'function\s+renderOverview', r'function\s+renderMerchantDash', r'overview.*innerHTML', r'quickActions.*innerHTML']:
    m = re.search(pattern, js)
    if m:
        pos = m.start()
        print(f'{pattern} found at {pos}')
        print(js[pos:pos+300])
        print('---')
