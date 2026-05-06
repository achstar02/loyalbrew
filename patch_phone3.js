// 最终版本 - 完全精确的空白符
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

// 从debug确认的精确文本:
// "; }\n    return;\n  }\n  if(err) err.style.display = \"none\";\n  var btn
const oldText = `"; }\n    return;\n  }\n  if(err) err.style.display = "none";\n  var btn`;

const newText = `"; }\n    return;\n  }\n    var _regPhone = phoneEl ? phoneEl.value.trim() : "";\n    if(!_regPhone || _regPhone.length < 6) {\n      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }\n      if(phoneEl) phoneEl.focus();\n      return;\n    }\n  if(err) err.style.display = "none";\n  var btn`;

if (c.includes(oldText)) {
  c = c.replace(oldText, newText);
  fs.writeFileSync(f, c, 'utf8');
  console.log('✅ Phone required validation - DONE!');
} else {
  console.error('❌ No match. Trying broader search...');
  // 用更短的唯一字符串
  const idx = c.indexOf('err.style.display = "none"');
  if (idx >= 0) {
    const ctx = c.substring(idx - 30, idx + 50);
    console.error('Context around target:', JSON.stringify(ctx));
  }
}
