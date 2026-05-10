import shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
src = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js'
dst = 'C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js'
shutil.copy2(src, dst)
import os
print(f'Copied! Deploy size: {os.path.getsize(dst)} bytes')
