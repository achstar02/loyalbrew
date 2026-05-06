import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Search for the actual garbled patterns visible in screenshot
# 1. Find lines with replacement character U+FFFD
fffd_count = content.count('\ufffd')
print(f'U+FFFD (replacement char) count: {fffd_count}')

# 2. Find lines with latin-1 garbled text like ï¿½
garbled_patterns = ['ï¿½', '\xc3\xaf\xc2\xbf\xc2\xbd']
for p in garbled_patterns:
    c = content.count(p)
    if c > 0:
        print(f'Pattern {repr(p)}: {c} occurrences')

# 3. Find all i18n label keys and check which have ??? values
# Look for patterns like:   key: '???',
lines = content.split('\n')
q_lines = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    # Match:  someKey: 'some value with ????',
    m = re.match(r"^(\w[\w]*:\s*)'([^']*)',?\s*$", s)
    if m:
        key, val = m.group(1), m.group(2)
        qcount = val.count('?')
        total = len(val)
        # If more than half the chars are ?, it's likely damaged
        if qcount >= 3 and total > 0 and qcount / total > 0.4:
            q_lines.append((i, key, val[:80], qcount, total))

print(f'\nFound {len(q_lines)} i18n values that are mostly "?" garbage:')
for num, key, val, qc, total in q_lines:
    print(f'  L{num}: {key} -> "{val}" ({qc}/{total} are ?)')
