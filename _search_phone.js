const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Search for URL param handling
const terms = ['?m=', 'getParam', 'URLSearch', 'merchantPhone', 'phone', 'phoneNumber', 'location.search'];
for (const s of terms) {
  let idx = c.indexOf(s);
  let count = 0;
  while (idx !== -1 && count < 5) {
    console.log(`[${s}] pos ${idx}: ...${c.substring(Math.max(0, idx - 60), idx + 100).replace(/\n/g, ' ')}`);
    idx = c.indexOf(s, idx + 1);
    count++;
  }
}
