const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');
let html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');
let changes = 0;

// =====================================================
// Step 5: Rewrite merchantLogin() to verify against Firestore
// =====================================================
const oldLogin = `function merchantLogin() {
  const user = document.getElementById('m-user').value.trim();
  const pass = document.getElementById('m-pass').value.trim();
  const remember = document.getElementById('m-remember').checked;
  if (user === 'admin' && pass === '1234') {
    if (remember) {
      localStorage.setItem('loyalbrew_merchant_saved', JSON.stringify({ user, pass }));
    } else {
      localStorage.removeItem('loyalbrew_merchant_saved');
    }
    merchantLoggedIn = true;
    showPage('page-merchant');
    // Load credits once merchant enters dashboard (async, Firebase-safe)
    _safeLoadMerchantCredits();
    // Super admin (optional): determined by Firebase Auth email
    initSuperAdminMode();
  } else {
    showToast(mt('mInvalidCredentials') || t('invalidCredentials'), 'error');
  }
}`;

const newLogin = `async function merchantLogin() {
  var user = document.getElementById('m-user').value.trim();
  var pass = document.getElementById('m-pass').value.trim();
  var remember = document.getElementById('m-remember').checked;
  var btn = document.querySelector('#page-merchant-login .btn-merchant');
  if (!user || !pass) {
    showToast('Please enter Merchant ID and Password', 'error');
    return;
  }
  if (btn) { btn.disabled = true; btn.textContent = 'Logging in...'; }
  try {
    // Look up merchant in Firestore by ID
    var docRef = fb.doc(fb.db, 'merchants', user);
    var docSnap = await fb.getDoc(docRef);
    if (!docSnap.exists()) {
      showToast('Merchant ID not found', 'error');
      return;
    }
    var mData = docSnap.data();
    // Check if merchant is deleted
    if (mData.status === 'deleted') {
      showToast('This merchant account has been deactivated', 'error');
      return;
    }
    // Verify password
    if (mData.password !== pass) {
      showToast('Incorrect password', 'error');
      return;
    }
    // Login success - set MERCHANT_DOC_PATH to this merchant
    MERCHANT_DOC_PATH = { col: 'merchants', id: user };
    if (remember) {
      localStorage.setItem('loyalbrew_merchant_saved', JSON.stringify({ user, pass }));
    } else {
      localStorage.removeItem('loyalbrew_merchant_saved');
    }
    merchantLoggedIn = true;
    window._currentMerchantId = user;
    window._currentMerchantName = mData.name || user;
    showPage('page-merchant');
    _safeLoadMerchantCredits();
    initSuperAdminMode();
    showToast('Welcome, ' + (mData.name || user) + '!', 'success');
  } catch (e) {
    console.error('merchantLogin error:', e);
    showToast('Login failed: ' + e.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = mt('mLoginBtn') || 'Login to Dashboard'; }
  }
}`;

if (c.includes(oldLogin)) {
  c = c.replace(oldLogin, newLogin);
  changes++;
  console.log('✓ Step 5: Rewrote merchantLogin() with Firestore verification');
} else {
  console.log('✗ Step 5: Pattern not found for merchantLogin()');
}

// =====================================================
// Step 6: Rewrite merchantLogout() to clear merchant session
// =====================================================
const oldLogout = `function merchantLogout() {
  merchantLoggedIn = false;
  // Only clear fields if not remembering
  const saved = JSON.parse(localStorage.getItem('loyalbrew_merchant_saved') || 'null');
  if (!saved) {
    document.getElementById('m-user').value = '';
    document.getElementById('m-pass').value = '';
  }
  showPage('page-landing');
}`;

const newLogout = `function merchantLogout() {
  merchantLoggedIn = false;
  MERCHANT_DOC_PATH = { col: 'merchants', id: 'test_shop' };
  window._currentMerchantId = null;
  window._currentMerchantName = null;
  _merchantCredits = null;
  // Only clear fields if not remembering
  var saved = JSON.parse(localStorage.getItem('loyalbrew_merchant_saved') || 'null');
  if (!saved) {
    document.getElementById('m-user').value = '';
    document.getElementById('m-pass').value = '';
  }
  showPage('page-landing');
}`;

if (c.includes(oldLogout)) {
  c = c.replace(oldLogout, newLogout);
  changes++;
  console.log('✓ Step 6: Rewrote merchantLogout() with session cleanup');
} else {
  console.log('✗ Step 6: Pattern not found for merchantLogout()');
}

// =====================================================
// Step 7: Update login page HTML - change label and hint
// =====================================================
const oldLabel = `<label><i class="fas fa-user-tie"></i> <span data-mi18n="mUsername" data-i18n="username">Username</span></label>
        <input type="text" id="m-user" placeholder="admin" autocomplete="username" />`;

const newLabel = `<label><i class="fas fa-user-tie"></i> <span data-mi18n="mUsername" data-i18n="username">Merchant ID</span></label>
        <input type="text" id="m-user" placeholder="e.g. 0123456789" autocomplete="username" />`;

if (html.includes(oldLabel)) {
  html = html.replace(oldLabel, newLabel);
  changes++;
  console.log('✓ Step 7: Updated login page label (Username → Merchant ID)');
} else {
  console.log('✗ Step 7: Pattern not found for login label');
}

// Step 7b: Update hint text
const oldHint = `<p class="hint" data-i18n="demo_label">Demo: <strong data-i18n="admin_label">admin</strong> / <strong>1234</strong></p>`;
const newHint = `<p class="hint">Enter your Merchant ID and password</p>`;

if (html.includes(oldHint)) {
  html = html.replace(oldHint, newHint);
  changes++;
  console.log('✓ Step 7b: Updated hint text (removed demo credentials)');
} else {
  console.log('✗ Step 7b: Pattern not found for hint text');
}

// =====================================================
// Step 8: Auto-fill saved merchant credentials on page load
// =====================================================
// Find where merchant saved credentials are loaded
const oldAutoFill = `// Auto-fill saved merchant credentials`;
let autoFillIdx = c.indexOf(oldAutoFill);
console.log('\nAuto-fill comment at:', autoFillIdx);
if (autoFillIdx > -1) {
  let ctx = c.slice(autoFillIdx, autoFillIdx + 400);
  console.log('Context:', ctx);
}

// Write files
fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', c, 'utf8');
fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', html, 'utf8');
console.log(`\nDone: ${changes} changes applied`);
