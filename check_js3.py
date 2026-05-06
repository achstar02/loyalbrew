f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'rb') as fh:
    content = fh.read()

# The error says pos 27303, col 13
# Let's check a wider range around that position for ANY multi-byte UTF-8
print('Scanning for multi-byte/non-ASCII chars in app.js...')
count = 0
pos = 0
while pos < len(content):
    b = content[pos]
    if b >= 0x80:
        # Multi-byte sequence
        seq_len = 1
        if (b & 0xe0) == 0xc0: seq_len = 2
        elif (b & 0xf0) == 0xe0: seq_len = 3
        elif (b & 0xf8) == 0xf0: seq_len = 4
        
        seq = content[pos:pos+seq_len]
        try:
            char = seq.decode('utf-8')
            line_num = content[:pos].count(b'\n') + 1
            col = pos - content.rfind(b'\n', 0, pos)
            # Only show near the error position or interesting chars
            if abs(pos - 27303) < 500 or ord(char) > 0xff:
                print(f'  Pos {pos} (Line {line_num}, Col {col}): U+{ord(char):04X} {repr(char)} bytes={seq.hex()}')
                count += 1
                if count > 50:
                    print('  ... (too many, stopping)')
                    break
        except:
            line_num = content[:pos].count(b'\n') + 1
            print(f'  Pos {pos} (Line {line_num}): INVALID UTF-8 bytes={seq.hex()}')
    pos += 1

if count == 0:
    print('No non-ASCII characters found in app.js!')
    
# Also specifically check the i18n strings area - look for curly quotes in translations
import re
text = content.decode('utf-8', errors='replace')
for m in re.finditer(r'[\u2018\u2019\u201c\u201d\u2013\u2014\u00a0]', text):
    p = m.start()
    line_num = text[:p].count('\n') + 1
    print(f'  Smart quote at pos {p} (Line {line_num}): U+{ord(m.group()):04X} {repr(m.group())}')
