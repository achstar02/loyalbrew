import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Check for garbled text in HTML
fffd_count = content.count('\ufffd')
print(f'U+FFFD in index.html: {fffd_count}')

# Find lines with ï¿½ or similar garbles
lines = content.split('\n')
issues = []
for i, line in enumerate(lines, 1):
    if '\ufffd' in line or 'ï¿½' in line:
        issues.append((i, line.strip()[:150]))

print(f'\nFound {len(issues)} lines with garbled chars in HTML:')
for num, text in issues[:30]:
    print(f'  L{num}: {text}')

# Also find data-i18n attributes with garbled content
print('\n--- data-i18n attributes ---')
for i, line in enumerate(lines, 1):
    if 'data-i18n=' in line and ('?' in line or '\ufffd' in line or 'ï¿½' in line):
        print(f'  L{i}: {line.strip()[:150]}')
