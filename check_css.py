import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Extract the <style> section to examine lb-glass and lb-card-shine
start = c.find('<style>')
end = c.find('</style>')
if start >= 0 and end > start:
    style_content = c[start:end+7]
    # Find lb-glass and lb-card-shine definitions
    import re
    for cls in ['lb-glass', 'lb-card-shine', 'lb-animate-in', '.lb-d6']:
        pattern = rf'{cls}[^{{]*\{{[^}}]+\}}'
        matches = re.findall(pattern, style_content, re.DOTALL)
        if matches:
            print(f'\n=== {cls} ===')
            for m in matches:
                print(m[:500])
                print('---')
        else:
            # Try broader search
            idx = style_content.find(cls)
            if idx >= 0:
                print(f'\n=== {cls} (context) ===')
                print(style_content[max(0,idx-20):idx+300])
            else:
                print(f'\n{cls}: NOT FOUND in <style>')
