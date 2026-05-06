f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'rb') as fh:
    lines = fh.readlines()

line2 = lines[1] if len(lines) > 1 else b'N/A'
print('Line 2 length:', len(line2), 'bytes')
print('Line 2 hex:', line2.hex())
print('Line 2 repr:', repr(line2))

for i in range(len(line2)):
    b = line2[i]
    if b > 126 or (b < 32 and b not in (9, 10, 13)):
        c = chr(b) if b >= 32 else 'CTRL'
        print('  Unusual byte at pos', i, ':', hex(b), '(' + c + ')')

content = b''.join(lines)
bad_chars = {0x2018: 'left single quote', 0x2019: 'right single quote', 0x201c: 'left double quote', 0x201d: 'right double quote', 0x2013: 'en-dash', 0x2014: 'em-dash', 0x00a0: 'non-breaking space'}
pos = 0
while pos < len(content):
    b = content[pos]
    code = None
    if (b & 0xe0) == 0xc0 and pos+1 < len(content):
        code = ((b & 0x1f) << 6) | (content[pos+1] & 0x3f)
    elif (b & 0xf0) == 0xe0 and pos+2 < len(content):
        code = ((b & 0x0f) << 12) | ((content[pos+1] & 0x3f) << 6) | (content[pos+2] & 0x3f)
    if code and code in bad_chars:
        line_num = content[:pos].count(b'\n') + 1
        print('  Line', line_num, ', pos', pos, ': found', bad_chars[code], '(U+' + format(code, '04X') + ')')
    pos += 1

print('\nDone checking.')
