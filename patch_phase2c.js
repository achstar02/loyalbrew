// Phase 2 最终补丁 - 使用精确匹配
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

let count = 0;
function patch(old, nw) {
  if (c.includes(old)) { c = c.replace(old, nw); count++; console.log('✅ PATCH OK'); }
  else { console.error('❌ NOT FOUND'); console.error('Searching for:', JSON.stringify(old.substring(0,80))); }
}

// Patch 1: phone 必填验证 - 在 password 检查的 return 后、下一个 if 之前插入
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
    if(err) err.style.display = 'none';`
);

// Patch 2: updateCartSummary points rate
patch(
`const pts = Math.floor(total);\n    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`,
`const _psRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(total * _psRate);\n    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`
);

// Patch 3: addPoints points rate  
patch(
`const pts = Math.floor(bill);\n\n    // Firestore members docId is phone number`,
`const _apRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;\n    const pts = Math.floor(bill * _apRate);\n\n    // Firestore members docId is phone number`
);

fs.writeFileSync(f, c, 'utf8');
console.log(`\nDone: ${count}/3 patches applied`);
