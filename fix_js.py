f = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
with open(f, 'rb') as fh:
    content = fh.read()

# Replace the invalid UTF-8 replacement character sequence (EF BF BD)
before = content.count(b'\xef\xbf\xbd')
print('Found', before, 'occurrences of U+FFFD (replacement character)')

# Replace with safe question mark
fixed = content.replace(b'\xef\xbf\xbd', b'?')

# Also fix any other common corrupted sequences that cause JS syntax errors
# Common issues: double-encoded UTF-8, BOM-like sequences in middle of file

with open(f, 'wb') as fh:
    fh.write(fixed)

print('Fixed! Replaced all invalid characters with ?')
print('File size:', len(content), '->', len(fixed))
