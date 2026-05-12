const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\public\\app.js', 'utf8');

// Find all occurrences of mCatHotDrinks with different values
const regex = /mCatHotDrinks:\s*'([^']+)'/g;
let match;
const occurrences = [];
while ((match = regex.exec(content)) !== null) {
  occurrences.push({ value: match[1], pos: match.index });
  console.log('Found:', match[1], 'at position', match.index);
}

// Show context around each
for (const occ of occurrences) {
  const ctx = content.substring(Math.max(0, occ.pos - 100), occ.pos + 200);
  console.log('\n--- Context ---');
  console.log(ctx.substring(0, 150));
}