var fs = require('fs');
var c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');
var i = c.indexOf('<!-- 新增商家表单 -->');
console.log('Found at', i);
if (i !== -1) {
  console.log(c.slice(i, i + 400));
}