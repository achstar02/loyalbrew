import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复语言按钮
content = content.replace('id="mlang2-zh">?</button>', 'id="mlang2-zh">中文</button>')
content = content.replace('id="mlang2-ta">?</button>', 'id="mlang2-ta">தமிழ்</button>')

# 修复注释
content = content.replace('<!-- ?????? -->', '<!-- 会员注册 -->')
content = content.replace('<!-- ??QR? -->', '<!-- 扫码QR -->')

# 修复其他问号文本
content = content.replace('Customers scan ? auto enter your shop', 'Customers scan → auto enter your shop')
content = content.replace('They register ? become YOUR member', 'They register → become YOUR member')

with open(r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed!')
