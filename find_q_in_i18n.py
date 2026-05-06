import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# The screenshot shows the page is in Tamil language (title is in Tamil script)
# So we need to find the ta (Tamil) translations that have ??? or are missing
# Let's find ALL translation sections and check for ? values

# Find lines with ? in translation values - any single ? is suspicious in a translation
lines = c.split('\n')
q_lines = []
for i, line in enumerate(lines, 1):
    if '?' in line and "'" in line and ':' in line:
        s = line.strip()
        m = re.match(r"^[\w]+:\s*'([^']*)',?\s*$", s)
        if m and '?' in m.group(1):
            q_lines.append((i, m.group(1)))

print(f'Found {len(q_lines)} translation values containing "?":')
for num, val in q_lines[:50]:
    print(f'  L{num}: "{val}"')
