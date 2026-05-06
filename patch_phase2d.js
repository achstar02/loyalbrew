// Phase 2 最终补丁 v3 - 基于当前文件实际内容
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

let count = 0;
function patch(old, nw, label) {
  if (c.includes(old)) { c = c.replace(old, nw); count++; console.log('✅', label); }
  else { console.error('❌ FAILED:', label); }
}

// --- Patch 1: 联系电话必填验证 ---
// 当前文本: password check -> if(err) display none -> var btn
// 目标: 在中间插入 phone 验证
patch(
`if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }
    if(err) err.style.display = 'none';`,
`if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }
    var _regPhone = phoneEl ? phoneEl.value.trim() : "";
    if(!_regPhone || _regPhone.length < 6) {
      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }
      if(phoneEl) phoneEl.focus();
      return;
    }
    if(err) err.style.display = 'none';`,
'Phone required validation'
);

// --- Patch 2: updateCartSummary pointsRate ---
patch(
'const pts = Math.floor(total);\n    document.getElementById',
"const _psRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(total * _psRate);\n    document.getElementById",
'updateCartSummary pointsRate'
);

// --- Patch 3: addPoints pointsRate ---
patch(
'const pts = Math.floor(bill);\n\n    // Firestore members docId is phone number',
"const _apRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(bill * _apRate);\n\n    // Firestore members docId is phone number",
'addPoints pointsRate'
);

fs.writeFileSync(f, c, 'utf8');
console.log(`\nTotal: ${count}/3 patches applied`);
