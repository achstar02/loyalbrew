import os, subprocess

base = r'C:\Users\Administrator\CodeBuddy\20260416214625'
print('=== Backup Check ===')
for ext in ['', '.bak', '.bak2', '.bak5', '.bak6']:
    path = os.path.join(base, 'app.js' + ext)
    if os.path.exists(path):
        size = os.path.getsize(path)
        # Quick check for corruption
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        corrupted = 'newIte  ms:' in content or 'newIte  ms: {' in content
        print(f'{ext or "(current)"}: {size} chars, corrupted={corrupted}')

print('\n=== Deploy Check ===')
deploy_js = os.path.join(base, 'deploy', 'app.js')
if os.path.exists(deploy_js):
    size = os.path.getsize(deploy_js)
    with open(deploy_js, 'r', encoding='utf-8') as f:
        content = f.read()
    corrupted = 'newIte  ms:' in content
    print(f'deploy/app.js: {size} chars, corrupted={corrupted}')
