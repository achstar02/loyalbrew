import re, sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')

# Find all lines that look like broken JS (string values corrupted)
# Pattern 1: key: '...');  - string value contains '); 
# Pattern 2: functionCall('...  - argument is truncated/empty
# Pattern 3: any line with orphaned '); or ', 
issues = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    # Skip comments and empty lines
    if not s or s.startswith('//') or s.startswith('*') or s.startswith('/*'):
        continue
    # Detect broken property:   key: 'something');  
    if re.match(r"^[\w]+:\s*'[^']*\)\s*;\s*$", s):
        issues.append((i, 'BROKEN_PROP', s))
    # Detect broken function call arg:   func(', or   func('');
    if re.search(r"\(\s*['\"]\s*,\s*e\s*\)\s*;?\s*$", s) and ('showToast' in s or 'console' in s or 'alert' in s):
        issues.append((i, 'BROKEN_CALL', s))
    # Detect truncated string at end of line
    if re.search(r"['\"][\s,;]*$", s) and len(s) < 50 and '=' in s:
        issues.append((i, 'TRUNCATED', s))

print(f'Found {len(issues)} suspicious lines:')
for num, typ, text in issues[:50]:
    print(f'  L{num} [{typ}]: {text[:150]}')

# Also check a wider range around the known errors for context
print('\n=== Full damage scan: lines with "); pattern ===')
for i, line in enumerate(lines, 1):
    # Look for lines where "); appears but it's NOT inside a proper function call
    if "');" in line or '");' in line:
        # Check if this looks like a broken object property
        if ':' in line and not line.strip().startswith(('if', 'else', 'for', 'while', 'return', 'const', 'let', 'var', 'function')):
            if not re.search(r'\w+\([^)]+\)\s*;', line):  # not a complete function call
                print(f'  L{i}: {line[:150]}')
