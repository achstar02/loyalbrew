const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Find the fb initialization
let idx = c.indexOf('window.__lbFirebase');
if (idx === -1) idx = c.indexOf('__lbFirebase');
console.log('__lbFirebase at:', idx);

// Find fb = or const fb or var fb
idx = c.indexOf('var fb =');
if (idx === -1) idx = c.indexOf('const fb =');
if (idx === -1) idx = c.indexOf('let fb =');
if (idx > -1) {
  console.log('fb assignment at:', idx);
  console.log(c.slice(idx, idx + 200));
} else {
  // Try broader search
  idx = c.indexOf('fb = window.__lbFirebase');
  if (idx > -1) {
    console.log('fb assignment at:', idx);
    console.log(c.slice(idx, idx + 200));
  } else {
    console.log('fb assignment not found with simple patterns');
    // Search for __lbFirebase assignment
    let idx2 = 0;
    while (true) {
      idx2 = c.indexOf('__lbFirebase', idx2);
      if (idx2 === -1) break;
      console.log(`__lbFirebase ref at ${idx2}:`, c.slice(Math.max(0,idx2-30), idx2+80));
      idx2 += 12;
    }
  }
}
