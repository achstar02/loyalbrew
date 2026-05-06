// Phase 2 补丁: 联系电话必填 + switchMerchantTab修复 + pointsRate集成
const fs = require('fs');
const f = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let c = fs.readFileSync(f, 'utf8');

let count = 0;
function patch(old, nw) {
  if (c.includes(old)) { c = c.replace(old, nw); count++; }
  else { console.error('❌ NOT FOUND:\n' + old.substring(0, 120)); }
}

// ===== 1. 联系电话改为必填 =====
// 1a. 标签: (可选) → (必填)
patch(
  '联系电话 <span style="color:#475569">(可选)</span>',
  '联系电话 <span style="color:#f87171">(必填)</span>'
);

// 1b. 验证逻辑: 增加 phone 必填检查（在 password 检查之后）
patch(
  `if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }`,
  `if(password.length < 4) {
      if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
      return;
    }
    if(!phone || phone.trim().length < 6) {
      if(err) { err.textContent = "请填写有效的联系电话"; err.style.display = "block"; }
      if(phoneEl) phoneEl.focus();
      return;
    }`
);

// 1c. 错误提示文字更新
patch(
  `"请填写商家名称、商家ID和密码"`,
  `"请填写商家名称、商家ID、密码和联系电话"`
);

// ===== 2. switchMerchantTab event guard =====
patch(
`function switchMerchantTab(tabId) {
  document.querySelectorAll('.mtab').forEach(t => { t.classList.remove('active'); t.classList.add('hidden'); });
  document.querySelectorAll('.mnav').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.remove('hidden');
  document.getElementById(tabId).classList.add('active');
  event.currentTarget.classList.add('active');`,
`function switchMerchantTab(tabId) {
  document.querySelectorAll('.mtab').forEach(t => { t.classList.remove('active'); t.classList.add('hidden'); });
  document.querySelectorAll('.mnav').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.remove('hidden');
  document.getElementById(tabId).classList.add('active');
  if (event && event.currentTarget) event.currentTarget.classList.add('active');`
);

// ===== 3. Points Rate 集成 - updateCartSummary =====
patch(
`  const pts = Math.floor(total);
    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`,
`  const _psRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
    const pts = Math.floor(total * _psRate);
    document.getElementById('sum-subtotal').textContent = 'RM' + subtotal.toFixed(2);`
);

// ===== 4. Points Rate 集成 - addPoints =====
patch(
`  const pts = Math.floor(bill);
  
    // Firestore members docId is phone number`,
`  const _apRate = (typeof getPointsSettings === 'function' ? getPointsSettings() : null)?.rate || 1;
    const pts = Math.floor(bill * _apRate);
  
    // Firestore members docId is phone number`
);

fs.writeFileSync(f, c, 'utf8');
console.log(`✅ Phase 2 补丁完成，共 ${count} 处替换`);
