const fs = require('fs');
const html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');

let idx = html.indexOf('Demo:');
if (idx === -1) idx = html.indexOf('demo_label');
console.log('Demo at:', idx);
if (idx > -1) {
  console.log(html.slice(idx - 50, idx + 200));
}

// Also check for the new hint
idx = html.indexOf('Enter your Merchant ID');
console.log('\nNew hint at:', idx);
