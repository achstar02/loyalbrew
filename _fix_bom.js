const fs = require('fs');
let c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
// Remove BOM if present
if (c.charCodeAt(0) === 0xFEFF) {
  c = c.slice(1);
  console.log('BOM removed');
}
// Verify
try {
  new Function(c);
  console.log('SYNTAX OK!');
} catch(e) {
  console.log('Error:', e.message);
  // Try to find where
  const lines = c.split('\n');
  for(let i=0; i<lines.length; i++) {
    try {
      new Function(lines[i]);
    } catch(e2) {
      console.log('Issue around line', i+1, ':', lines[i].slice(0,60));
      break;
    }
  }
}
fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', c);