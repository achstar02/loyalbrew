import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Check around the injection points
ml_start = js.find('const MERCHANT_LANGS')
# Check en block ending
en_area = js[305450:305500]
print(f'EN block end area: {repr(en_area)}')

zh_area = js[311070:311130]
print(f'\nZH block end area: {repr(zh_area)}')

ms_area = js[318880:318940]
print(f'\nMS block end area: {repr(ms_area)}')

ta_area = js[327220:327290]
print(f'\nTA block end area: {repr(ta_area)}')
