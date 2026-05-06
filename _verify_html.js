const fs = require('fs');
const h = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');
console.log('HTML size:', h.length, 'chars');
console.log('mChooseAnItem opt found:', h.includes('data-mi18n-opt="mChooseAnItem"'));
