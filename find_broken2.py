import re

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

# Find ALL lines that look like broken i18n value strings
# Pattern: they end with '); which suggests a function call leaked into a string
lines = content.split('\n')
broken = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    # Look for:   key: '...');  or   key: "...");
    # This is a broken object property where the string value is corrupted
    if re.match(r"^\s*[\w]+:\s*'[^']*\);\s*$", s) or re.match(r'^\s*[\w]+:\s*"[^"]*");\s*$', s):
        # Exclude valid patterns
        if not s.startswith('//') and not s.startswith('*'):
            broken.append((i, s))

print(f'Found {len(broken)} broken lines:')
for num, text in broken:
    print(f'  Line {num}: {text[:120]}')

# Now let's also find the specific area around line 7303
print('\n--- Lines 7295-7315 ---')
for i in range(7294, min(7315, len(lines))):
    marker = ' >>> BROKEN <<<' if (i+1) in [b[0] for b in broken] else ''
    print(f'  {i+1}: {lines[i][:120]}{marker}')
