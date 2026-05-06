import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find app-header class definition in <style> block
import re
# Search style blocks
for m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.DOTALL):
    style_content = m.group(1)
    if 'app-header' in style_content or 'customer-header' in style_content:
        print("=== STYLE BLOCK with header ===")
        for line in style_content.split('\n'):
            if 'header' in line.lower() or 'app-header' in line or 'customer-header' in line:
                print(line.strip())

# Also find the actual HTML of the orange header bar shown in screenshot
print("\n=== First app-header occurrence ===")
idx = c.find('app-header')
if idx >= 0:
    # Go back to find the tag start
    start = c.rfind('<', 0, idx)
    print(c[start:start+300])

# The screenshot shows orange top bar - let's look at what's around "DATA-I18N" 
print("\n=== DATA-I18N LOYALBREW_BRAND area ===")
idx = c.find('LOYALBREW_BRAND')
if idx >= 0:
    print(c[max(0,idx-200):idx+200])
