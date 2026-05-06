// 检查 switchMerchantTab event guard
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');
const idx = c.indexOf('event.currentTarget.classList.add');
if (idx >= 0) {
  console.log(c.substring(idx - 30, idx + 80));
}
