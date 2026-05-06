var fs = require('fs');
var c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
// Replace button onclick to use modal
c = c.replace(/_saToggleRegisterForm\(\)"/g, '_saOpenRegModal()"');
// Remove old global binding (now we have our own)
c = c.replace(/window._saToggleRegisterForm = _saToggleRegisterForm;/g, '// global already');
// Also update any other references
c = c.replace(/_saGenerateMerchantId\(\)"/g, '_saGenId2()"');
c = c.replace(/window._saGenerateMerchantId = _saGenerateMerchantId;/g, '// global already');
c = c.replace(/_saSubmitRegister\(\)"/g, '_saSubmitReg()"');
c = c.replace(/window._saSubmitRegister = _saSubmitRegister;/g, '// global already');
fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', c);
console.log('Updated all onclick references');