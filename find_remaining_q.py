import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Find remaining visible ? patterns in text content (not in comments/JS)
lines = c.split('\n')
for i, line in enumerate(lines, 1):
    s = line.strip()
    # Look for visible text with ?? that users would see
    # Skip HTML comments, skip script/style tags
    if ('??' in s or '?'*3 in s) and not s.startswith('<!--') and '<script' not in s and '<style' not in s:
        # Only show lines that look like user-visible content
        if any(tag in s for tag in ['<button', '<span', '<div', '<label', '<p>', '<h', '<small', '<title']):
            print(f'L{i}: {s[:160]}')
