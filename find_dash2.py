import re
with open('app.js','r',encoding='utf-8') as f:
    js = f.read()
# Find loadMerchantDashboard function - get full content
m = re.search(r'function loadMerchantDashboard\(\)', js)
if m:
    pos = m.start()
    # Print first 3000 chars of the function
    print(js[pos:pos+5000])
