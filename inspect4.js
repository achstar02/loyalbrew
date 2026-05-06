const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Find merchant_saved references
let idx = 0;
while (true) {
  idx = c.indexOf('merchant_saved', idx);
  if (idx === -1) break;
  let start = Math.max(0, idx - 100);
  let end = Math.min(c.length, idx + 200);
  console.log(`--- At char ${idx} ---`);
  console.log(c.slice(start, end));
  console.log('');
  idx += 14;
}
