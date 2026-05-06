// 检查当前文件状态 - 看看之前的patch是否已部分生效
const fs = require('fs');
const c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

const checks = [
  'getPointsSettings',
  '_psRate', 
  '_apRate',
  '_regPhone',
  '请填写有效的联系电话',
  '(必填)',
  'event.currentTarget.classList.add',
];

for (const s of checks) {
  const idx = c.indexOf(s);
  console.log(idx >= 0 ? `✅ FOUND "${s}" at ${idx}` : `❌ NOT FOUND: ${s}`);
}
