const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Find initMerchantSavedPassword full function
let idx = c.indexOf('function initMerchantSavedPassword()');
if (idx > -1) {
  console.log('=== initMerchantSavedPassword ===');
  console.log(c.slice(idx, idx + 400));
}

// Find onMerchantRememberChange
idx = c.indexOf('function onMerchantRememberChange');
if (idx > -1) {
  console.log('\n=== onMerchantRememberChange ===');
  console.log(c.slice(idx, idx + 300));
}

// Check if there's auto-login logic (auto-submit on page load)
idx = c.indexOf('initMerchantSavedPassword()');
if (idx > -1) {
  console.log('\n=== Call site ===');
  console.log(c.slice(Math.max(0, idx - 100), idx + 200));
}
