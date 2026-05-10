const fs = require('fs');
let c = fs.readFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', 'utf8');

// 找到包含 .id{font-size:13px 的行并删除它，以及对应的显示行
c = c.replace(
    "printWindow.document.write('.id{font-size:13px;color:#888;margin-bottom:20px}</style>');\n",
    ""
);

// 同时去掉对应的显示 div
c = c.replace(
    "printWindow.document.write('<div class=\"name\">' + escHtml(name) + '</div>');\n",
    "printWindow.document.write('<div class=\"name\">' + escHtml(name) + '</div>');"
);

// 调整 margin
c = c.replace(
    ".name{font-size:24px;font-weight:700;margin:8px 0 4px}",
    ".name{font-size:24px;font-weight:700;margin:8px 0 20px}"
);

fs.writeFileSync('C:/Users/Administrator/CodeBuddy/20260416214625/app.js', c, 'utf8');
console.log('Fixed: removed merchant ID from print preview');