const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
const s = 'loyalbrew-app-2f8c7.web.app';
let idx = c.indexOf(s);
if (idx === -1) {
  console.log('✅ No more old Firebase URLs found!');
} else {
  console.log('❌ Still found at pos', idx);
  while (idx !== -1) { console.log(c.substring(idx, idx+80)); idx = c.indexOf(s, idx+1); }
}
