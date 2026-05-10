// Check if backup file has valid JS syntax
const fs = require('fs');
const code = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js.bak', 'utf8');
try {
    new Function(code);
    console.log('BACKUP IS VALID JS - no syntax errors!');
} catch(e) {
    console.log('SYNTAX ERROR:', e.message);
}
