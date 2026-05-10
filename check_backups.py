import os
base = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
for ext in ['', '.bak', '.bak2', '.bak3', '.bak4', '.bak5', '.bak6', '.bak_ta', '.bak_ta_complete', '.bak_v2', '.bak_v3']:
    path = base + ext
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_corruption = 'newIte  ms:' in content
        has_zh = 'zh: {' in content
        size = len(content)
        name = '(current)' if ext == '' else ext
        print(f'{name}: {size} chars, corrupted={has_corruption}, has_zh={has_zh}')
