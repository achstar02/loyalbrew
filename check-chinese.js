// Verify Chinese text encoding in app.js
const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\public\\app.js';
const content = fs.readFileSync(path, 'utf8');

// Find the zh: block in LANGS (line 6996 area)
const zhMatch = content.match(/zh:\s*\{[^}]{1000}/);
if (zhMatch) {
  console.log('First 200 chars of zh block:');
  console.log(zhMatch[0].substring(0, 200));
  console.log('\n--- Checking for replacement chars ---');
  if (zhMatch[0].includes('\uFFFD')) {
    console.log('❌ Found replacement characters (U+FFFD) in zh block');
  } else {
    console.log('✅ No replacement chars in first 1000 chars');
  }
}

// Find the ta: block
const taMatch = content.match(/ta:\s*\{[^}]{500}/);
if (taMatch) {
  console.log('\nFirst 200 chars of ta block:');
  console.log(taMatch[0].substring(0, 200));
  if (taMatch[0].includes('\uFFFD')) {
    console.log('❌ Found replacement characters in ta block');
  } else {
    console.log('✅ No replacement chars in ta block');
  }
}

// Check overall file
const totalReplacements = (content.match(/\uFFFD/g) || []).length;
console.log(`\nTotal replacement chars in file: ${totalReplacements}`);

// Count question marks in zh block
if (zhMatch) {
  const questionMarks = (zhMatch[0].match(/\?/g) || []).length;
  console.log(`Question marks in zh block: ${questionMarks}`);
  if (questionMarks > 5) {
    console.log('❌ zh block likely corrupted');
  }
}