import re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()

# Strategy: find lines with corrupted i18n values
# The pattern is: the Chinese/translation text got replaced with garbage or truncated

# Let's look at what's around line 7303 more carefully - it's inside an i18n object
print('=== Lines 7280-7320 (full context) ===')
for i in range(7279, min(7320, len(lines))):
    line = lines[i].rstrip()
    print(f'  L{i+1}: {line}')

# Also check if there's a pattern of corruption - maybe whole sections are damaged
print('\n=== Scanning for lines containing ", e); pattern ===')
for i, line in enumerate(lines, 1):
    if "', e);" in line or '", e);' in line:
        print(f'  L{i}: {line.rstrip()[:150]}')

print('\n=== Scanning for lines starting with showToast( or alert( with short/truncated content ===')
for i, line in enumerate(lines, 1):
    s = line.strip()
    if (s.startswith('showToast(') or s.startswith('alert(')) and len(s) < 40:
        print(f'  L{i}: {s[:150]}')
