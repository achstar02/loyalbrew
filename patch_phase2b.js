// Phase 2 补丁 (剩余3处): 联系电话必填验证 + pointsRate集成
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

let count = 0;
function patch(old, nw) {
  if (c.includes(old)) { c = c.replace(old, nw); count++; console.log('✅', old.substring(0,60)); }
  else { console.error('❌ NOT FOUND:', old.substring(0,80)); }
}

// ===== 1. 联系电话必填验证（在 password 长度检查后）=====
patch(
`  if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }`,
`  if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }
    var phone = phoneEl ? phoneEl.value.trim() : "";
    if(!phone || phone.length < 6) {
      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }
      if(phoneEl) phoneEl.focus();
      return;
    }`
);

// ===== 2. Points Rate - updateCartSummary =====
patch(
`  const pts = Math.floor(total);
    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`,
`  const _psRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
    const pts = Math.floor(total * _psRate);
    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`
);

// ===== 3. Points Rate - addPoints =====
patch(
`  const pts = Math.floor(bill);

    // Firestore members docId is phone number`,
`  const _apRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
    const pts = Math.floor(bill * _apRate);

    // Firestore members docId is phone number`
);

fs.writeFileSync(f, c, 'utf8');
console.log(`\n✅ 剩余补丁完成，共 ${count} 处替换`);
