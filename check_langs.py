# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js.bak', 'r', encoding='utf-8-sig') as f:
    content = f.read()

idx = content.find('const LANGS =')
start = content.find('{', idx)
depth = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i
            break

langs_block = content[idx:end+1]
print('LANGS block length:', len(langs_block), 'chars')

for lang in ['en', 'zh', 'ms', 'ta']:
    q = "'" + lang + "'"
    key_pos = langs_block.find(q)
    c = lang + ':'
    colon_pos = langs_block.find(c)
    print('  {}: key at {}, colon at {}'.format(lang, key_pos, colon_pos))

# Also count keys per language
for lang in ['en', 'zh', 'ms', 'ta']:
    pattern = "'" + lang + "':"
    count = langs_block.count(pattern)
    print('  {} block appears {} time(s)'.format(lang, count))
