const fs = require('fs');
const b = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\public\\app.js');

// Search for the zh block with Chinese chars (热/冷/食物 etc)
const searchChinese = Buffer.from('热', 'utf8');
const searchTamil = Buffer.from('சூடான', 'utf8');

const pos1 = b.indexOf(searchChinese);
const pos2 = b.indexOf(searchTamil);

console.log('Position of Chinese 热:', pos1);
console.log('Position of Tamil சூடான:', pos2);

if (pos1 > 0) {
  const slice = b.slice(pos1 - 50, pos1 + 100);
  console.log('\nContext around 热:');
  console.log('Bytes:', slice.toString('hex'));
  console.log('UTF8:', slice.toString('utf8'));
}

// Also show where the zh block with '??' actually is
const zhStart = b.indexOf(Buffer.from("zh: {", 'utf8'));
console.log('\nFirst zh: { position:', zhStart);
if (zhStart > 0) {
  const zhSlice = b.slice(zhStart, zhStart + 200);
  console.log('First 200 chars of zh block:');
  console.log(zhSlice.toString('utf8').substring(0, 200));
}

// Check line 758 position (from grep earlier)
console.log('\nLine 758 context (around index 70000):');
const line758 = b.slice(69900, 70000);
console.log(line758.toString('utf8').substring(0, 100));