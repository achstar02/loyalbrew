import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Find feat1/feat2/feat3 translations in all languages
keys = ['feat1Title', 'feat1Desc', 'feat2Title', 'feat2Desc', 'feat3Title', 'feat3Desc',
        'enter', 'get', 'view']

for key in keys:
    # Find pattern:  key: 'value',
    # Search for all occurrences (one per language)
    pattern = re.compile(rf'{key}:\s*\'([^\']*)\'')
    matches = pattern.findall(c)
    if matches:
        print(f'\n{key}:')
        for i, val in enumerate(matches):
            # Show repr to see hidden chars like \n
            display = repr(val)
            if len(display) > 100:
                display = display[:100] + '...'
            print(f'  [{i}] {display}')
