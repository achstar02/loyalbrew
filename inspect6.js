const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\firebase-init.js', 'utf8');

// Check what's exported
let idx = c.indexOf('window.__lbFirebase');
if (idx > -1) {
  console.log('=== Firebase exports ===');
  console.log(c.slice(idx, idx + 2000));
}
