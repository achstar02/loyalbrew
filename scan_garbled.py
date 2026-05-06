import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    content = fh.read()

lines = content.split('\n')
issues = []
for i, line in enumerate(lines, 1):
    qcount = line.count('?')
    if qcount >= 3 and ('???' in line or '\ufffd' in line or '\xef\xbf\xbd' in line.encode('utf-8', errors='replace').decode('utf-8')):
        stripped = line.strip()
        if len(stripped) > 5:
            issues.append((i, stripped[:150], qcount))

print(f'Found {len(issues)} lines with damaged text:')
for num, text, qc in issues[:80]:
    print(f'  L{num} ({qc}?): {text}')
