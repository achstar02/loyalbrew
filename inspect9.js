const fs = require('fs');
let c = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js', 'utf8');

// Find merchantLogin function and see how fb is referenced
let idx = c.indexOf('async function merchantLogin()');
console.log('merchantLogin at:', idx);
if (idx > -1) {
  let func = c.slice(idx, idx + 1000);
  // Check for fb references
  let fbRefs = [];
  let fIdx = 0;
  while (true) {
    fIdx = func.indexOf('fb.', fIdx);
    if (fIdx === -1) break;
    fbRefs.push(func.slice(fIdx, fIdx + 40));
    fIdx++;
  }
  console.log('fb references in merchantLogin:', fbRefs);

  // Check if fb is a local var or global
  let beforeFunc = c.slice(Math.max(0, idx - 500), idx);
  if (beforeFunc.includes('var fb =') || beforeFunc.includes('const fb =') || beforeFunc.includes('let fb =')) {
    console.log('fb is local to enclosing scope');
  } else {
    console.log('fb is likely global (window.__lbFirebase)');
  }
}

// Check the global fb assignment
idx = c.indexOf('var fb = window.__lbFirebase');
if (idx > -1) {
  console.log('\nGlobal fb at:', idx);
  console.log(c.slice(Math.max(0, idx - 100), idx + 200));
}

// Check for other fb = assignments
let allFb = [];
let sIdx = 0;
while (true) {
  sIdx = c.indexOf('fb = window.__lbFirebase', sIdx);
  if (sIdx === -1) break;
  allFb.push(sIdx);
  sIdx++;
}
console.log('\nAll fb = window.__lbFirebase:', allFb);

sIdx = 0;
while (true) {
  sIdx = c.indexOf('fb =', sIdx);
  if (sIdx === -1) break;
  let ctx = c.slice(sIdx, sIdx + 60);
  if (ctx.startsWith('fb = window') || ctx.startsWith('fb =await') || ctx.startsWith('fb = await') || ctx.startsWith('fb = doc')) {
    console.log(`fb = at ${sIdx}: ${ctx}`);
  }
  sIdx++;
}
