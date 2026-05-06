const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');
let changes = 0;

// 4. Change MERCHANT_DOC_PATH from const to let
const oldDecl = 'const MERCHANT_DOC_PATH = { col: \'merchants\', id: \'test_shop\' };';
const newDecl = 'let MERCHANT_DOC_PATH = { col: \'merchants\', id: \'test_shop\' };';
if (c.includes(oldDecl)) {
  c = c.replace(oldDecl, newDecl);
  changes++;
  console.log('✓ Step 4: MERCHANT_DOC_PATH changed from const to let');
} else if (c.includes(newDecl)) {
  console.log('✓ Step 4: Already let (from previous run)');
  changes++;
} else {
  console.log('✗ Step 4: Pattern not found');
}

// 5. Rewrite merchantLogin() - find it
let loginIdx = c.indexOf('function merchantLogin()');
if (loginIdx === -1) loginIdx = c.indexOf('async function merchantLogin()');
console.log('merchantLogin at char:', loginIdx);
if (loginIdx > -1) {
  // Find the function body - read next 1000 chars
  let funcText = c.slice(loginIdx, loginIdx + 1500);
  console.log('=== merchantLogin start (500 chars) ===');
  console.log(funcText.slice(0, 500));
  console.log('=== ... ===');
  console.log(funcText.slice(500, 1000));
}

// 6. Find merchantLogout
let logoutIdx = c.indexOf('function merchantLogout()');
console.log('\nmerchantLogout at char:', logoutIdx);
if (logoutIdx > -1) {
  let funcText = c.slice(logoutIdx, logoutIdx + 500);
  console.log('=== merchantLogout ===');
  console.log(funcText.slice(0, 500));
}

// 7. Find the login page HTML
let loginPageIdx = c.indexOf('page-merchant-login');
console.log('\npage-merchant-login at char:', loginPageIdx);

// 8. Find merchant login page in index.html
const html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');
let htmlIdx = html.indexOf('page-merchant-login');
console.log('index.html page-merchant-login at char:', htmlIdx);
if (htmlIdx > -1) {
  console.log('=== HTML context ===');
  console.log(html.slice(htmlIdx - 50, htmlIdx + 600));
}

if (changes > 0) {
  fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', c, 'utf8');
  console.log(`\nStep 4 applied: ${changes} change(s)`);
} else {
  console.log('\nNo changes applied this round');
}
