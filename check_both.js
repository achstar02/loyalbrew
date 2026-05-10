const fs = require('fs');
// Check source
let code = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
try { new Function(code); console.log('SOURCE app.js: VALID'); } catch(e) { console.log('SOURCE ERROR:', e.message); }
// Check deploy
code = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'utf8');
try { new Function(code); console.log('DEPLOY app.js: VALID'); } catch(e) { console.log('DEPLOY ERROR:', e.message); }
// Line counts
const srcLines = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8').split('\n').length;
const depLines = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/deploy/app.js', 'utf8').split('\n').length;
console.log('Source lines:', srcLines, '| Deploy lines:', depLines);
