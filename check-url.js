const fs = require('fs');
const c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
const matches = c.match(/\?m=[^'"]+/g);
console.log('URL patterns found:');
if (matches) {
  matches.slice(0, 20).forEach(m => console.log(m));
} else {
  console.log('No matches found');
}
