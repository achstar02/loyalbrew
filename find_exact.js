// 精确查找3处失败位置的原始文本
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

const searches = [
  'if(password.length < 4)',
  'const pts = Math.floor(total)',
  'const pts = Math.floor(bill)'
];

for (const s of searches) {
  const idx = c.indexOf(s);
  if (idx >= 0) {
    console.log('--- Found: ' + s + ' at index ' + idx + ' ---');
    console.log(JSON.stringify(c.substring(Math.max(0, idx - 30), idx + 100)));
    console.log('');
  } else {
    console.log('NOT FOUND: ' + s);
  }
}
