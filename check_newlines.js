// 检查换行符 + 精确提取目标文本
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// 检查换行符类型
const crlfCount = (c.match(/\r\n/g) || []).length;
const lfOnly = (c.match(/(?<!\r)\n/g) || []).length;
console.log(`CRLF: ${crlfCount}, LF-only: ${lfOnly}`);

// 精确提取3处目标周围的原始字节
const targets = ['Math.floor(total)', 'Math.floor(bill)', "请填写商家名称、商家ID和密码"];
for (const t of targets) {
  const idx = c.indexOf(t);
  if (idx >= 0) {
    // 取前后各80字符，显示包括换行符
    const raw = c.substring(Math.max(0, idx - 80), idx + 80);
    console.log('\n=== ' + t + ' ===');
    console.log('RAW repr:', JSON.stringify(raw));
  }
}
