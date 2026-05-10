import re
with open('deploy/index.html','r',encoding='utf-8') as f:
    html = f.read()
# Find ALL data-mi18n attributes
keys = re.findall(r'data-mi18n="([^"]+)"', html)
unique_keys = sorted(set(keys))
print(f'Total data-mi18n attrs: {len(keys)}')
print(f'Unique keys: {len(unique_keys)}')
for k in unique_keys:
    print(f'  {k}')
