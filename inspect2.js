const fs = require('fs');
const html = fs.readFileSync('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\index.html', 'utf8');
const i = html.indexOf('id="page-merchant-login"');
if (i > -1) {
  console.log(html.slice(i, i + 2000));
} else {
  console.log('Not found');
}
