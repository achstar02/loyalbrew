const fs = require('fs');
let c = fs.readFileSync('./app.js', 'utf8');

// 1. Add password field to registration modal - find the pattern between merchant ID input and credits input
const oldPattern = `<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">初始点数`;
const newPattern = `<div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">登录密码 * <span style="color:#475569">(Password)</span></label>
        <input id="mreg-password" type="password" placeholder="至少4位" style="width:100%;padding:11px 14px;background:#1e293b;border:1px solid #334155;color:#f1f5f9;border-radius:10px;font-size:0.95rem;box-sizing:border-box;outline:none" onfocus="this.style.borderColor='#3b82f6'" onblur="this.style.borderColor='#334155'"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">初始点数`;

if(c.includes(oldPattern)) {
  c = c.replace(oldPattern, newPattern);
  console.log('✓ Added password input field');
} else {
  console.log('✗ Pattern not found for password field');
}

// 2. Update validation in _saSubmitReg - read password element and validate
const oldValidate = `var name = nameEl ? nameEl.value.trim() : "";
  var merchantId = idEl ? idEl.value.trim() : "";
  var credits = creditsEl ? parseFloat(creditsEl.value) : 100;
  var phone = phoneEl ? phoneEl.value.trim() : "";
  if(!name || !merchantId) {
    if(err) { err.textContent = "请填写商家名称和商家ID"; err.style.display = "block"; }
    return;
  }`;

const newValidate = `var name = nameEl ? nameEl.value.trim() : "";
  var merchantId = idEl ? idEl.value.trim() : "";
  var password = document.getElementById("mreg-password")?.value.trim() || "";
  var credits = creditsEl ? parseFloat(creditsEl.value) : 100;
  var phone = phoneEl ? phoneEl.value.trim() : "";
  if(!name || !merchantId || !password) {
    if(err) { err.textContent = "请填写商家名称、商家ID和密码"; err.style.display = "block"; }
    return;
  }
  if(password.length < 4) {
    if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
    return;
  }`;

if(c.includes(oldValidate)) {
  c = c.replace(oldValidate, newValidate);
  console.log('✓ Added password validation');
} else {
  console.log('✗ Pattern not found for validation');
}

// 3. Save password to Firestore
const oldSave = `phone: phone || null,
          email: null,
          createdAt: now,`;
const newSave = `phone: phone || null,
          email: null,
          password: password,
          createdAt: now,`;

if(c.includes(oldSave)) {
  c = c.replace(oldSave, newSave);
  console.log('✓ Added password to Firestore save');
} else {
  console.log('✗ Pattern not found for Firestore save');
}

fs.writeFileSync('./app.js', c, 'utf8');
console.log('Done');