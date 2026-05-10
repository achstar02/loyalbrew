import re, subprocess

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Find all }, patterns (comma before closing brace - invalid in objects)
# But we need to be careful: arrays can have trailing commas
# Let's find the exact error location
result = subprocess.run(['node', '-e', '''
try {
  new Function(require("fs").readFileSync("C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js","utf-8"));
} catch(e) {
  // Try to find the error position
  const code = require("fs").readFileSync("C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js","utf-8");
  console.log("Error:", e.message);
  // Show context around common issues
  const lines = code.split("\\n");
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].match(/},\\s*$/)) {
      console.log((i+1) + ": " + lines[i].trim().substring(0,80));
    }
  }
}
'''], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr[:300])
