const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Add fb initialization to merchantLogin
const oldLoginStart = `async function merchantLogin() {
  var user = document.getElementById('m-user').value.trim();
  var pass = document.getElementById('m-pass').value.trim();`;

const newLoginStart = `async function merchantLogin() {
  var fb = window.__lbFirebase;
  if (!fb || !fb.db) { showToast("Firebase not ready", "error"); return; }
  var user = document.getElementById('m-user').value.trim();
  var pass = document.getElementById('m-pass').value.trim();`;

if (c.includes(oldLoginStart)) {
  c = c.replace(oldLoginStart, newLoginStart);
  fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', c, 'utf8');
  console.log('✓ Added fb initialization to merchantLogin()');
} else {
  console.log('✗ Pattern not found - may already be fixed');
}
