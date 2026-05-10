import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Check each injection point
# EN block end: around 305472
pos = 305472
area = js[pos-60:pos+100]
print(f'EN block end area:\n{repr(area)}\n')

# ZH block end
pos = 311100
area = js[pos-60:pos+100]
print(f'ZH block end area:\n{repr(area)}\n')

# MS block end
pos = 318920
area = js[pos-60:pos+100]
print(f'MS block end area:\n{repr(area)}\n')

# TA block end
pos = 327270
area = js[pos-60:pos+100]
print(f'TA block end area:\n{repr(area)}\n')
