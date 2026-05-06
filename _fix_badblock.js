const fs = require('fs');
let c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// Find the bad block: starts at "// Update login button text" and ends at "savePoints2"
const badStart = c.indexOf('  // Update login button text when language changes');
const badEnd = c.indexOf("savePoints2: 'Save Points Settings',}");

if (badStart > 0 && badEnd > badStart) {
  // Find what's after the bad block to reconnect properly
  const afterBad = c.indexOf('\n// ===== DEFAULT MENU DATA =====');
  if (afterBad > badEnd) {
    // Remove the bad block
    c = c.slice(0, badStart) + '\n' + c.slice(afterBad);
    console.log('Removed bad block from line', c.slice(0, badStart).split('\n').length, 'to around', badEnd);
  }
}

fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', c);

// Verify
try {
  new Function(c);
  console.log('SYNTAX OK!');
} catch(e) {
  console.log('Still error:', e.message);
}