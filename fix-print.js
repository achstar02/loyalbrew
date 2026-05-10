const fs = require('fs');
const path = 'C:/Users/Administrator/CodeBuddy/20260416214625/app.js';

let content = fs.readFileSync(path, 'utf8');

// 目标替换
const target = `printWindow.document.write('.name{font-size:24px;font-weight:700;margin:8px 0 4px}');
printWindow.document.write('.id{font-size:13px;color:#888;margin-bottom:20px}</style>');
printWindow.document.write('</head><body>');
printWindow.document.write('<div class="name">' + escHtml(name) + '</div>');`;

const replacement = `printWindow.document.write('.name{font-size:24px;font-weight:700;margin:8px 0 20px}</style>');
printWindow.document.write('</head><body>');
printWindow.document.write('<div class="name">' + escHtml(name) + '</div>');`;

if (content.includes(target)) {
    content = content.replace(target, replacement);
    fs.writeFileSync(path, content, 'utf8');
    console.log('✅ 已修复打印预览，移除商家ID显示');
} else {
    console.log('❌ 未找到目标代码');
}