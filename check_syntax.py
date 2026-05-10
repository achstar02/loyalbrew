import subprocess, tempfile, os

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

# Read the file that was generated (with error)
# Actually, the script didn't save because of syntax error
# Let's check what the node error details are

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Write to temp and get detailed error
tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')

# Let me try a different approach - just check if current file is OK
result = subprocess.run(['node', '-e', 
    'try { new Function(require("fs").readFileSync("' + JS.replace('\\','/') + '", "utf-8")); console.log("CURRENT FILE OK") } catch(e) { console.log("ERROR:", e.message); console.log(e.stack) }'], 
    capture_output=True, text=True)
print('Current file:', result.stdout.strip())
if result.stderr:
    print('Stderr:', result.stderr.strip()[:500])
