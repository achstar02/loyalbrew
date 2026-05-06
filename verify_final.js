const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');
let html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');

console.log('========================================');
console.log('Phase 1: Merchant Auth Refactor - Final Verification');
console.log('========================================');

const checks = [
  ['1. Registration modal: password input', c.includes('mreg-password')],
  ['2. Registration: password validation (4 chars)', c.includes('密码至少需要4位')],
  ['3. Registration: password saved to Firestore', c.includes('password: password,')],
  ['4. MERCHANT_DOC_PATH is mutable (let)', c.includes('let MERCHANT_DOC_PATH')],
  ['5. merchantLogin is async + Firestore', c.includes('async function merchantLogin()') && c.includes("fb.doc(fb.db, 'merchants', user)")],
  ['6. merchantLogin: fb initialization', c.includes('var fb = window.__lbFirebase') && c.indexOf('var fb = window.__lbFirebase', c.indexOf('async function merchantLogin()')) > -1],
  ['7. merchantLogin: MERCHANT_DOC_PATH set', c.includes('MERCHANT_DOC_PATH = { col: \'merchants\', id: user }')],
  ['8. merchantLogin: deleted check', c.includes("mData.status === 'deleted'")],
  ['9. merchantLogin: password verify', c.includes('mData.password !== pass')],
  ['10. merchantLogout: reset MERCHANT_DOC_PATH', c.includes('function merchantLogout()') && c.slice(c.indexOf('function merchantLogout()'), c.indexOf('function merchantLogout()') + 500).includes("MERCHANT_DOC_PATH = { col: 'merchants', id: 'test_shop' }")],
  ['11. Login page: label Merchant ID', html.includes('Merchant ID</span>')],
  ['12. Login page: no demo hint in merchant section', !html.includes('Demo: <strong>admin</strong>')],
];

let pass = 0;
checks.forEach(([label, ok]) => {
  console.log(`${ok ? '✓' : '✗'} ${label}`);
  if (ok) pass++;
});
console.log(`\nResult: ${pass}/${checks.length} checks passed`);
