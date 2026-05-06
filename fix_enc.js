const fs = require('fs');
const buf = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js');
const latin1 = buf.toString('latin1');
const fixed = Buffer.from(latin1, 'utf8');
const fixedStr = fixed.toString('utf8');
// Check result
const idx = fixedStr.indexOf('loginLabel');
console.log('loginLabel context:', fixedStr.substring(idx, idx + 80));
// Save over original
fs.writeFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', fixed);
console.log('Fixed: ' + buf.length + ' -> ' + fixed.length + ' bytes');
