// 用 split/join 方式做替换，避免换行符问题
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

let count = 0;

// Patch 1: phone 必填验证 - 用 split 定位
const phoneTarget = `    return;
  }
  if(err) err.style.display = 'none';`;
const phoneReplace = `    return;
  }
    var _regPhone = phoneEl ? phoneEl.value.trim() : "";
    if(!_regPhone || _regPhone.length < 6) {
      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }
      if(phoneEl) phoneEl.focus();
      return;
    }
  if(err) err.style.display = 'none';`;

// 只替换 password 检查后的那个实例（通过上下文确认）
// 找 password.length < 4 后面的第一个 "return;\n  }\n  if(err)"
const pwdIdx = c.indexOf('password.length < 4');
if (pwdIdx >= 0) {
  const afterPwd = c.substring(pwdIdx);
  const targetIdx = afterPwd.indexOf(phoneTarget);
  if (targetIdx >= 0) {
    c = c.substring(0, pwdIdx + targetIdx) + phoneReplace + c.substring(pwdIdx + targetIdx + phoneTarget.length);
    count++;
    console.log('✅ Phone required validation');
  } else {
    console.error('❌ Phone target not found after password check');
    // debug: 显示后面的200字符
    console.error('Context:', JSON.stringify(afterPwd.substring(0, 300)));
  }
} else {
  console.error('❌ password.length < 4 not found');
}

// Patch 2: updateCartSummary pointsRate
const totalIdx = c.indexOf('Math.floor(total)');
if (totalIdx >= 0) {
  const oldText = 'const pts = Math.floor(total);';
  const newText = 'const _psRate = (typeof getPointsSettings === "function" ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(total * _psRate);';
  if (c.includes(oldText)) {
    c = c.replace(oldText, newText);
    count++;
    console.log('✅ updateCartSummary pointsRate');
  } else {
    console.error('❌ Math.floor(total) exact text mismatch');
    console.error('Context:', JSON.stringify(c.substring(totalIdx, totalIdx + 80)));
  }
}

// Patch 3: addPoints pointsRate  
const billIdx = c.indexOf('Math.floor(bill)');
if (billIdx >= 0) {
  const oldText2 = 'const pts = Math.floor(bill);';
  const newText2 = 'const _apRate = (typeof getPointsSettings === "function" ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(bill * _apRate);';
  if (c.includes(oldText2)) {
    c = c.replace(oldText2, newText2);
    count++;
    console.log('✅ addPoints pointsRate');
  } else {
    console.error('❌ Math.floor(bill) exact text mismatch');
    console.error('Context:', JSON.stringify(c.substring(billIdx, billIdx + 80)));
  }
}

fs.writeFileSync(f, c, 'utf8');
console.log(`\nTotal: ${count}/3 patches applied`);
