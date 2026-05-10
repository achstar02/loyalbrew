import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Find loadMerchantDashboard full function
fn_pos = js.find('function loadMerchantDashboard')
print(f'loadMerchantDashboard: {fn_pos}')

# Show first 2000 chars of the function
print('=== Function body (first 2000 chars) ===')
print(js[fn_pos:fn_pos+2000])