import re, sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')

# Show lines 7295-7310
print('=== Lines 7295-7310 ===')
for i in range(7294, min(7310, len(lines))):
    line = lines[i]
    # Check for non-ascii
    has_non_ascii = any(ord(c) > 126 for c in line)
    marker = ' [NON-ASCII]' if has_non_ascii else ''
    print(f'  L{i+1}: {line[:140]}{marker}')

# Now run node --check to get exact error
print('\nDone. Use node --check for exact error.')
