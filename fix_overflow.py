import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()

# The lb-glass class has overflow:hidden which can clip text
# Change it to overflow:visible
c = c.replace(
    'lb-glass {\n  position:relative; overflow:hidden;\n}',
    'lb-glass {\n  position:relative; overflow:visible;\n}'
)

# Also check if lb-card-shine has overflow:hidden (needed for the ::after sweep effect, but let's make sure the parent doesn't clip)
# The shine::after uses position absolute so the parent needs overflow:hidden for the sweep
# But we just changed lb-glass to visible - the card-shine still has its own overflow:hidden

with open(f,'w',encoding='utf-8') as fh: fh.write(c)
print('Fixed lb-glass overflow -> visible')
print(f'File size: {len(c):,} bytes')
