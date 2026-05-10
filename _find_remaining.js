const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Find remaining 3 old Firebase URLs with context
const s = 'loyalbrew-app-2f8c7.web.app/?m=${m.id}';
let idx = c.indexOf(s);
let count = 0;
while (idx !== -1) {
  count++;
  console.log(`\n--- #${count} at pos ${idx} ---`);
  console.log(c.substring(idx - 100, idx + 160));
  idx = c.indexOf(s, idx + 1);
}
