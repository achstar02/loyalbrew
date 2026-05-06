const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

console.log('=== Phase 1 Verification ===');
console.log('1. mreg-password field:', c.includes('mreg-password') ? '✓' : '✗');
console.log('2. Password validation:', c.includes('密码至少需要4位') ? '✓' : '✗');
console.log('3. Password in Firestore save:', c.includes('password: password,') ? '✓' : '✗');
console.log('4. MERCHANT_DOC_PATH is let:', c.includes('let MERCHANT_DOC_PATH') ? '✓' : '✗');
console.log('5. merchantLogin is async:', c.includes('async function merchantLogin()') ? '✓' : '✗');
console.log('6. Firestore lookup in login:', c.includes("fb.doc(fb.db, 'merchants', user)") ? '✓' : '✗');
console.log('7. MERCHANT_DOC_PATH set on login:', c.includes('MERCHANT_DOC_PATH = { col: \'merchants\', id: user }') ? '✓' : '✗');
console.log('8. merchantLogout resets path:', c.includes('MERCHANT_DOC_PATH = { col: \'merchants\', id: \'test_shop\' }') && c.indexOf('MERCHANT_DOC_PATH = { col: \'merchants\', id: \'test_shop\' }') < c.indexOf('function merchantLogout()') ? '⚠ two occurrences' : '✓');

const html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');
console.log('9. Login label Merchant ID:', html.includes('Merchant ID</span>') ? '✓' : '✗');
console.log('10. Hint updated:', !html.includes('Demo: <strong') ? '✓' : '✗');

// Count MERCHANT_DOC_PATH = occurrences
let count = 0;
let idx = 0;
while (true) {
  idx = c.indexOf('MERCHANT_DOC_PATH =', idx);
  if (idx === -1) break;
  count++;
  console.log(`   MERCHANT_DOC_PATH = at char ${idx}`);
  idx++;
}
console.log('Total MERCHANT_DOC_PATH = occurrences:', count);
