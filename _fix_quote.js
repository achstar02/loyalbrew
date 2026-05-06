const fs = require('fs');
let c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
// Fix unescaped single quotes in the newly added translation strings
c = c.replace(/What's your drink today/g, "What\\'s your drink today");
fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', c);
console.log('Fixed quote escaping');
// Verify
try {
  new Function(c);
  console.log('SYNTAX OK!');
} catch(e) {
  console.log('Still has error:', e.message.slice(0,100));
}