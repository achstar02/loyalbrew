const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Find all occurrences of old Firebase URL
const s = 'loyalbrew-app-2f8c7.web.app';
let idx = c.indexOf(s);
while (idx !== -1) {
  console.log(`pos ${idx}: ...${c.substring(idx - 40, idx + 100)}...`);
  idx = c.indexOf(s, idx + 1);
}
