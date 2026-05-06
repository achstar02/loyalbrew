// 检查当前文件中3处的实际文本
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

const searches = ['password.length < 4', 'Math.floor(total)', 'Math.floor(bill)'];
for (const s of searches) {
  const idx = c.indexOf(s);
  if (idx >= 0) {
    const start = Math.max(0, idx - 50);
    const snippet = c.substring(start, idx + 120);
    console.log('=== ' + s + ' ===');
    // 显示不可见字符
    console.log(JSON.stringify(snippet));
    console.log('');
  } else {
    console.log('NOT FOUND:', s);
  }
}
