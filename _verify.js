const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
const checks = [
  ['fb.auth.onAuthStateChanged (bug - should be 0)', (c.match(/fb\.auth\.onAuthStateChanged/g)||[]).length],
  ['fb.auth().onAuthStateChanged (correct - should be 2)', (c.match(/fb\.auth\(\)\.onAuthStateChanged/g)||[]).length],
  ['_safeLoadMerchantCredits function', c.includes('function _safeLoadMerchantCredits')],
  ['Firebase SDK wait loop', c.includes('while (!fb?.auth && attempts < 50)')],
  ['signOut uses fb.auth()', c.includes('fb.auth().signOut')],
  ['_safeLoadMerchantCredits calls', (c.match(/_safeLoadMerchantCredits\(\)/g)||[]).length],
  ['SUPER_ADMIN_EMAIL declared', (c.match(/const SUPER_ADMIN_EMAIL/g)||[]).length],
  ['showSuperAdminPage definition', c.includes('window.showSuperAdminPage = async function')],
  ['async IIFE in INIT', c.includes('(async () => {')],
];
checks.forEach(([l,v]) => {
  const pass = typeof v === 'boolean' ? v : v > 0;
  console.log((pass ? '✅' : '❌') + ' ' + l + ' → ' + v);
});
console.log('\nFile size: ' + (c.length/1024).toFixed(0) + ' KB');
