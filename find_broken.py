f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()

print('File has', len(lines), 'lines')
print('\nSearching for syntax-damaged lines...')

# Find lines that look like broken string assignments
# Pattern: key: '<garbage>');
# These are i18n strings where the value got corrupted
issues = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Look for patterns indicating broken JS strings
    if (stripped.endswith("');") or stripped.endswith("\");")) and ':' in stripped:
        # Check if the line looks like a broken property
        import re
        # Match:  key: 'something');
        m = re.match(r"^(\s*\w[\w]*:\s*')[^']*('\);$)", stripped)
        if m:
            issues.append((i, stripped))

print(f'Found {len(lines)} potentially broken string lines:')
for num, text in issues[:30]:
    print(f'  Line {num}: {text[:100]}')

# Also use Node.js to find ALL syntax errors
print('\n--- Running Node.js syntax check for exact error location ---')
