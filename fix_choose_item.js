// Fix Choose an item in app.js
const fs = require('fs');
const file = 'C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\app.js';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
    "'<option value=\"\">-- Choose an item --</option>'",
    "`<option value=''>` + mt('mChooseAnItem') + `</option>`"
);
console.log('Fixed Choose an item');

fs.writeFileSync(file, content, 'utf8');
console.log('Done!');
