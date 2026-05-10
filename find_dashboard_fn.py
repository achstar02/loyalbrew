import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Find loadMerchantDashboard
pos = js.find('function loadMerchantDashboard')
print(f'loadMerchantDashboard at: {pos}')
print(js[pos:pos+1000])