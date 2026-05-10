import re

# Full diagnostic: understand the corrupted MERCHANT_LANGS structure
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

ml_pos = js.find('const MERCHANT_LANGS')
en_pos = js.find('en:', ml_pos)
ms_pos = js.find('ms:', ml_pos)
zh_pos = js.find('zh:', ml_pos)
ta_pos = js.find('ta:', ml_pos)

print(f'Position order (ascending):')
for name, pos in [('en', en_pos), ('ms', ms_pos), ('zh', zh_pos), ('ta', ta_pos)]:
    print(f'  {name}: {pos}')

print(f'\nBlock layout (by position):')
blocks_by_pos = sorted([(en_pos, 'en'), (ms_pos, 'ms'), (zh_pos, 'zh'), (ta_pos, 'ta')])
for pos, name in blocks_by_pos:
    print(f'  {name}: {pos}')

# Show what's at the boundary between each block
print(f'\n=== Around en_pos (297947) ===')
print(js[en_pos-10:en_pos+200].encode('ascii', errors='replace').decode())
print(f'\n=== Around ms_pos (299057) ===')
print(js[ms_pos-10:ms_pos+100].encode('ascii', errors='replace').decode())
print(f'\n=== Around zh_pos (305771) ===')
print(js[zh_pos-10:zh_pos+200].encode('ascii', errors='replace').decode())
print(f'\n=== Around ta_pos (319732) ===')
print(js[ta_pos-10:ta_pos+100].encode('ascii', errors='replace').decode())
