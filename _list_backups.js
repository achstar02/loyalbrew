const fs = require('fs');
const dir = fs.readdirSync('C:/Users/Administrator/CodeBuddy/20260416214625');
const baks = dir.filter(f => f.endsWith('.bak') || f.includes('app.js'));
console.log('Files with bak or app.js:', baks.slice(0,20));