// 用二进制方式精确查看字符
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
const c = fs.readFileSync(f, 'utf8');

const idx = c.indexOf("return;\n  }\n  if(err)");
if (idx >= 0) {
  // 显示前后各40字符的hex
  const chunk = c.substring(idx - 10, idx + 60);
  console.log('Chars:', [...chunk].map(ch => ch === '\n' ? '\\n' : ch === '\r' ? '\\r' : ch === ' ' ? '␣' : ch).join(''));
  console.log('JSON:', JSON.stringify(chunk));
} else {
  console.log('Pattern not found at all');
  // 尝试更短的搜索
  const idx2 = c.indexOf("if(err) err.style.display");
  if (idx2 >= 0) {
    const chunk = c.substring(idx2 - 20, idx2 + 50);
    console.log('Found alt, JSON:', JSON.stringify(chunk));
    console.log('Chars:', [...chunk].map(ch => ch === '\n' ? '\\n' : ch === '\r' ? '\\r' : ch === ' ' ? '␣' : ch).join(''));
  }
}
