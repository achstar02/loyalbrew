// 提取 password 验证 + 周围完整文本
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

const idx = c.indexOf('password.length < 4');
if (idx >= 0) {
  // 取更长的范围
  const raw = c.substring(idx, idx + 300);
  console.log('=== password area ===');
  console.log(raw);
}

// 也检查错误提示文字
const idx2 = c.indexOf('请填写商家名称');
if (idx2 >= 0) {
  console.log('\n=== error msg ===');
  console.log(c.substring(idx2, idx2 + 80));
}
