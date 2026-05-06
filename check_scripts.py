import re

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>', content)
print('Scripts found:')
for s in scripts:
    print(f'  {s}')

# Check for showPage inline calls
inline = [(m.start(), content[max(0,m.start()-20):m.end()+30]) for m in re.finditer(r'showPage\s*\(', content)]
print(f'\nInline showPage calls: {len(inline)}')
for pos, ctx in inline[:5]:
    print(f'  Pos {pos}: ...{ctx}...')
