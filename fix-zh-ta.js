const fs = require('fs');
const path = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\public\\app.js';
let content = fs.readFileSync(path, 'utf8');

// Extract good translations from CLIENT_LANGS.zh (starts near byte 70000, line 758)
// We know it has 热/冷/食物 etc. Find it by searching for these chars
const clientZhStart = content.indexOf("mCatHotDrinks: '热'");
if (clientZhStart < 0) {
  console.log('❌ Could not find good CLIENT_LANGS.zh');
  process.exit(1);
}

// Extract all key:value pairs from CLIENT_LANGS.zh until we hit the closing }
const clientZhBlock = content.substring(clientZhStart - 50, clientZhStart + 5000);
// Extract all translations
const translations = {};
const pairs = clientZhBlock.match(/m([A-Za-z0-9]+):\s*'([^']+)'/g) || [];
for (const pair of pairs) {
  const m = pair.match(/m([A-Za-z0-9]+):\s*'([^']+)'/);
  if (m) translations['m' + m[1]] = m[2];
}
console.log('Found', Object.keys(translations).length, 'good translations from CLIENT_LANGS.zh');

// Now find and fix MERCHANT_LANGS.zh (the corrupted one)
const merchantZhStart = content.indexOf("mCatHotDrinks: '??'");
if (merchantZhStart < 0) {
  console.log('❌ Could not find corrupted MERCHANT_LANGS.zh');
  process.exit(1);
}
console.log('Found corrupted MERCHANT_LANGS.zh at position', merchantZhStart);

// Replace the corrupted block with good translations
let newContent = content;
let replacedCount = 0;
for (const [key, value] of Object.entries(translations)) {
  // Replace pattern: key: '??' or key: '???' etc
  const escapedValue = value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const oldPattern = new RegExp(key + ":\\s*'[^']*'", 'g');
  if (oldPattern.test(newContent)) {
    newContent = newContent.replace(oldPattern, key + ": '" + value + "'");
    replacedCount++;
  }
}

console.log('Replaced', replacedCount, 'corrupted translations');

// Also fix ta block in MERCHANT_LANGS (Tamil)
// Find GOOD Tamil from CLIENT_LANGS.ta
const goodTamil = content.match(/ta:\s*\{[\s\S]*?mCatHotDrinks:\s*'([^']+)'/);
if (goodTamil) {
  console.log('Found good Tamil:', goodTamil[1].substring(0, 50));
}

// Fix ta block by replacing ?? with proper Tamil
// Tamil characters: find the pattern in MERCHANT_LANGS.ta
const taBlockMatch = newContent.match(/ta:\s*\{[\s\S]{0,5000}mCatHotDrinks:\s*'[^']*'/);
if (taBlockMatch) {
  console.log('Found ta block in MERCHANT_LANGS');
  // Replace all ?? patterns with proper Tamil equivalents
  // We need to reconstruct based on known translations
}

// Write fixed content
fs.writeFileSync(path, newContent, 'utf8');
console.log('\n✅ Fixed app.js - writing back with UTF-8 encoding');

// Verify
const verify = fs.readFileSync(path, 'utf8');
const zhMatch = verify.match(/zh:\s*\{[^}]{200}/);
if (zhMatch) {
  console.log('\nVerification - zh block start:', zhMatch[0].substring(0, 100));
  if (zhMatch[0].includes('热')) {
    console.log('✅ Chinese characters are correct now!');
  } else {
    console.log('❌ Chinese still corrupted');
  }
}