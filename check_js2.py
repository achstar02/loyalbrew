f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'rb') as fh:
    content = fh.read()

# Check around position 27303
pos = 27303
start = max(0, pos - 100)
end = min(len(content), pos + 100)
snippet = content[start:end]
print('Around pos 27303:')
print('...')
print(snippet)
print('...')

# Also show line number
line_num = content[:pos].count(b'\n') + 1
print('\nLine number at pos 27303:', line_num)

# Find the exact line
lines = content.split(b'\n')
if line_num <= len(lines):
    line = lines[line_num - 1]
    print(f'\nLine {line_num} ({len(line)} bytes):')
    print(repr(line))
    
    # Check for non-ascii in this line
    for i, b in enumerate(line):
        if b > 126 or (b < 32 and b not in (9, 13)):
            print(f'  Non-ASCII at col {i}: hex={b:02x}')
