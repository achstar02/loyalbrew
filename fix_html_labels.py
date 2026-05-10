import re

with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\index.html','r',encoding='utf-8') as f:
    html = f.read()

replacements = [
    ('Banner Image URL', '横幅图片链接'),
    ('Save Shop Info', '保存店铺信息'),
    ('Points Settings', '积分设置'),
    ('Points per RM', '每 RM 积分'),
    ('Shop Settings', '店铺设置'),
]

for old, new in replacements:
    html = html.replace(old, new)
    print(f"Replaced: {old}")

with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\index.html','w',encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! Size: {len(html)}")
