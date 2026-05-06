// Security audit script for LoyalBrew
const fs = require('fs');
const path = require('path');

const appPath = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js';
const htmlPath = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html';

const appCode = fs.readFileSync(appPath, 'utf8');
const htmlCode = fs.readFileSync(htmlPath, 'utf8');

console.log('=== LOYALBREW SECURITY AUDIT & PATCH SCRIPT ===\n');

// 1. Check current XSS mitigations
const hasEscapeHtml = /function escapeHtml/.test(appCode);
const hasSanitize = /function\s+sanitize\b/.test(appCode);
const hasInnerHTMLs = (appCode.match(/\.innerHTML\s*=/g) || []).length;
const hasTextContent = (appCode.match(/textContent\s*=/g) || []).length;

console.log('XSS Mitigations:');
console.log('  escapeHtml function:', hasEscapeHtml ? 'YES' : 'MISSING');
console.log('  sanitize function:', hasSanitize ? 'YES' : 'MISSING');
console.log('  innerHTML assignments:', hasInnerHTMLs);
console.log('  textContent assignments:', hasTextContent);

// 2. Find all innerHTML usages that might need fixing
const innerHTMLLines = [];
const regex = /^(.{0,6})\.innerHTML\s*=/gm;
let m;
while ((m = regex.exec(appCode)) !== null) {
  const lineNo = appCode.substring(0, m.index).split('\n').length;
  innerHTMLLines.push(lineNo);
}

// 3. Check safeLS password storage
const hasPlaintextPassword = /safeLS\.set\([^,]+,\s*[^)]*pass/.test(appCode);
console.log('\nPassword storage check:');
console.log('  Plaintext password in safeLS:', hasPlaintextPassword ? 'FOUND' : 'CLEAN');

// 4. Check Super Admin hardcoded email
const saEmailMatch = /SUPER_ADMIN_EMAIL\s*=\s*['"]([^'"]+)['"]/.exec(appCode);
if (saEmailMatch) {
  console.log('\nSuper Admin hardcoded email:', saEmailMatch[1]);
}

// 5. Check for Firebase Auth listener
const hasAuthListener = /initFirebaseAuthListener|onAuthStateChanged/.test(appCode);
console.log('\nAuth listener:', hasAuthListener ? 'YES' : 'MISSING');

// 6. Check file upload validation
const hasFileValidation = /photoUnder5MB|validateImage|checkFileType|file\.type|image\/(jpeg|png)/.test(appCode);
console.log('File upload validation:', hasFileValidation ? 'YES' : 'MISSING');

// 7. CSP nonce usage
const hasNonceGeneration = /__csp_nonce|nonce=/.test(htmlCode);
const hasNonceInScripts = (htmlCode.match(/nonce=/g) || []).length;
console.log('\nCSP Nonce in HTML:', hasNonceInScripts, 'instances');
console.log('__csp_nonce in HTML:', /__csp_nonce/.test(htmlCode) ? 'YES' : 'MISSING');

// 8. Check complaint/notes rendering
const complaintFields = ['complaint-desc', 'order-notes', 'reg-name', 'reg-email'];
for (const f of complaintFields) {
  const pat = new RegExp(`getElementById\\(['"]${f}['"]\\)[^;]*\\.value`);
  console.log(`  Input field '${f}':`, pat.test(appCode) ? 'found' : 'not found');
}

// 9. Check Firebase Firestore rules
const rulesPath = 'C:/Users/Administrator/CodeBuddy/20260416214625/firestore.rules';
if (fs.existsSync(rulesPath)) {
  const rules = fs.readFileSync(rulesPath, 'utf8');
  const hasRateLimit = /rateLimit|limit|throttle/.test(rules);
  console.log('\nFirestore rules rate limiting:', hasRateLimit ? 'YES' : 'MISSING');
}

// 10. Check for reCAPTCHA / rate limiting
const hasRateLimitCode = /rateLimit|attemptCount|failedAttempts|lockUntil|bruteForce/.test(appCode);
console.log('Client-side rate limiting:', hasRateLimitCode ? 'YES' : 'MISSING');

console.log('\n=== ANALYSIS COMPLETE ===');
console.log('\nKey findings to patch:');
console.log('1. CSP nonce needs actual nonce generation (replace placeholder)');
console.log('2. escapeHtml() needs to be used in all user-input rendering');
console.log('3. Super Admin: hardcoded email is security risk');
console.log('4. File uploads need server-side validation');
console.log('5. Need rate limiting on login/register');