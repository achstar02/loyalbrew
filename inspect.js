const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Check line endings
const crlf = (c.match(/\r\n/g) || []).length;
const lf = (c.match(/[^\r]\n/g) || []).length;
console.log('CRLF lines:', crlf, 'LF-only lines:', lf);

// Find 初始点数
let idx = c.indexOf('初始点数');
console.log('初始点数 at char:', idx);
if (idx > -1) {
  // Show 400 chars before it, escaping control chars
  let before = c.slice(idx - 400, idx);
  console.log('=== BEFORE 初始点数 (400 chars) ===');
  console.log(before.replace(/\r/g, '{CR}').replace(/\n/g, '{LF}'));
}

// Find validation code
let idx2 = c.indexOf('请填写商家名称和商家ID');
console.log('\n请填写商家名称和商家ID at char:', idx2);
if (idx2 > -1) {
  let ctx = c.slice(idx2 - 300, idx2 + 100);
  console.log('=== CONTEXT ===');
  console.log(ctx.replace(/\r/g, '{CR}').replace(/\n/g, '{LF}'));
}

// Check if password field already exists
let idx3 = c.indexOf('mreg-password');
console.log('\nmreg-password exists:', idx3 > -1, 'at:', idx3);
