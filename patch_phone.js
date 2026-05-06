// 最终补丁: 仅修复 phone 必填验证
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

// 从debug输出确认精确文本:
// "return;\n  }\n  if(err) err.style.display = 'none';\n  var btn"
const oldText = `    return;
  }
  if(err) err.style.display = 'none';
  var btn`;

const newText = `    return;
  }
    var _regPhone = phoneEl ? phoneEl.value.trim() : "";
    if(!_regPhone || _regPhone.length < 6) {
      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }
      if(phoneEl) phoneEl.focus();
      return;
    }
  if(err) err.style.display = 'none';
  var btn`;

if (c.includes(oldText)) {
  c = c.replace(oldText, newText);
  fs.writeFileSync(f, c, 'utf8');
  console.log('✅ Phone required validation patched!');
} else {
  console.error('❌ Still not matching');
  // 找到确切位置
  const idx = c.indexOf("password.length < 4");
  console.error('Debug:', JSON.stringify(c.substring(idx+100, idx+200)));
}
