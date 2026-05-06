const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');
let changes = 0;

// 1. Add password field before the grid div with credits/phone
const oldHTML = `      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +\n        '<div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">初始点数`;
const newHTML = `      '<div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">登录密码 * <span style="color:#475569">(Password)</span></label>' +\n        '<input id="mreg-password" type="password" placeholder="至少4位" style="width:100%;padding:11px 14px;background:#1e293b;border:1px solid #334155;color:#f1f5f9;border-radius:10px;font-size:0.95rem;box-sizing:border-box;outline:none" onfocus="this.style.borderColor=\\'#3b82f6\\'" onblur="this.style.borderColor=\\'#334155\\'"></div>' +\n      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +\n        '<div><label style="display:block;color:#94a3b8;font-size:0.78rem;font-weight:600;margin-bottom:6px">初始点数`;

if (c.includes(oldHTML)) {
  c = c.replace(oldHTML, newHTML);
  changes++;
  console.log('✓ Step 1: Added password input field');
} else {
  console.log('✗ Step 1: Pattern not found for password field');
  // Debug: show what's actually there
  let idx = c.indexOf('初始点数');
  if (idx > -1) {
    let snippet = c.slice(idx - 200, idx + 50);
    console.log('  Actual text near 初始点数:', JSON.stringify(snippet));
  }
}

// 2. Update validation in _saSubmitReg
const oldValidate = `  var merchantId = idEl ? idEl.value.trim() : "";
  var credits = creditsEl ? parseFloat(creditsEl.value) : 100;
  if(isNaN(credits) || credits < 0) credits = 100;
  var phone = phoneEl ? phoneEl.value.trim() : "";
  if(!name || !merchantId) {
    if(err) { err.textContent = "请填写商家名称和商家ID"; err.style.display = "block"; }
    return;
  }`;

const newValidate = `  var merchantId = idEl ? idEl.value.trim() : "";
  var password = document.getElementById("mreg-password") ? document.getElementById("mreg-password").value.trim() : "";
  var credits = creditsEl ? parseFloat(creditsEl.value) : 100;
  if(isNaN(credits) || credits < 0) credits = 100;
  var phone = phoneEl ? phoneEl.value.trim() : "";
  if(!name || !merchantId || !password) {
    if(err) { err.textContent = "请填写商家名称、商家ID和密码"; err.style.display = "block"; }
    return;
  }
  if(password.length < 4) {
    if(err) { err.textContent = "密码至少需要4位"; err.style.display = "block"; }
    return;
  }`;

if (c.includes(oldValidate)) {
  c = c.replace(oldValidate, newValidate);
  changes++;
  console.log('✓ Step 2: Added password validation');
} else {
  console.log('✗ Step 2: Pattern not found for validation');
  let idx = c.indexOf('请填写商家名称和商家ID');
  if (idx > -1) {
    let snippet = c.slice(idx - 200, idx + 100);
    console.log('  Actual text near validation:', JSON.stringify(snippet));
  }
}

// 3. Save password to Firestore (check if already done)
if (c.includes('password: password,')) {
  console.log('✓ Step 3: Password save already exists (from previous run)');
  changes++;
} else {
  const oldSave = `phone: phone || null,
          email: null,
          createdAt: now,`;
  const newSave = `phone: phone || null,
          email: null,
          password: password,
          createdAt: now,`;
  if (c.includes(oldSave)) {
    c = c.replace(oldSave, newSave);
    changes++;
    console.log('✓ Step 3: Added password to Firestore save');
  } else {
    console.log('✗ Step 3: Pattern not found for Firestore save');
  }
}

if (changes > 0) {
  fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', c, 'utf8');
  console.log(`\nDone: ${changes}/3 changes applied`);
} else {
  console.log('\nNo changes applied');
}
