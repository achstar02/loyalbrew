import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Find all i18n values that contain ??? or are suspiciously short/garbled
# Pattern: within the translations object (en/zh/bm/ta), find values like '????'
lines = c.split('\n')
fixes_needed = []

for i, line in enumerate(lines, 1):
    s = line.strip()
    # Match translation value:   key: 'value',
    m = re.match(r"^(\s*)([\w]+):\s*'([^']*)',?\s*$", s)
    if m:
        indent, key, val = m.group(1), m.group(2), m.group(3)
        # Check if value is mostly ? marks
        if len(val) >= 2 and val.count('?') >= len(val) * 0.6:
            fixes_needed.append((i, key, val))

print(f'Found {len(fixes_needed)} translation values that are mostly "?" garbage:')
for num, key, val in fixes_needed[:50]:
    print(f'  L{num}: {key} = "{val}"')
