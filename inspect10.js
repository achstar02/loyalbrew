const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Find _safeLoadMerchantCredits and the actual loadMerchantCredits
let idx = c.indexOf('_safeLoadMerchantCredits');
console.log('_safeLoadMerchantCredits at:', idx);
if (idx > -1) {
  console.log(c.slice(idx, idx + 400));
}

idx = c.indexOf('function loadMerchantCredits');
if (idx === -1) idx = c.indexOf('async function loadMerchantCredits');
console.log('\nloadMerchantCredits at:', idx);
if (idx > -1) {
  console.log(c.slice(idx, idx + 800));
}
