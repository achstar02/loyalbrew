import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('style.css', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    # 会员卡 !important: 橙 → 深蓝
    ('background:linear-gradient(135deg,#FF6B00,#FF8C00,#FFB347) !important;border-radius:18px;padding:22px;color:white;margin-bottom:14px;box-shadow:0 8px 28px rgba(255,107,0,0.35)',
     'background:linear-gradient(135deg,#0c4a6e,#0369a1,#0ea5e9) !important;border-radius:18px;padding:22px;color:white;margin-bottom:14px;box-shadow:0 8px 28px rgba(14,165,233,0.3)'),
    
    # 会员卡原始: 咖啡 → 深蓝
    ('background:linear-gradient(135deg,#2c1810,#8B4513,#D2691E); border-radius:18px; padding:22px; color:white; margin-bottom:14px; box-shadow:0 8px 28px rgba(139,69,19,0.4)',
     'background:linear-gradient(135deg,#0f172a,#1e3a5f,#0ea5e9); border-radius:18px; padding:22px; color:white; margin-bottom:14px; box-shadow:0 8px 28px rgba(14,165,233,0.25)'),
    
    # section-card hover
    ('box-shadow:0 6px 24px rgba(255,107,0,1);transform:translateY(-2px)',
     'box-shadow:0 6px 24px rgba(14,165,233,0.2);transform:translateY(-2px)'),
    
    # h3 i 图标
    ('color:#FF6B00 !important', 'color:#0284c7 !important'),
    
    # tier-step done
    ('color:#FF6B00 !important', 'color:#0ea5e9 !important'),
    
    # tier-line done
    ('background:#FF6B00 !important', 'background:#0ea5e9 !important'),
    
    # btn-outline-brown
    ('color:#FF6B00 !important;border-color:#FF6B00 !important', 'color:#0284c7 !important;border-color:#0284c7 !important'),
    ('background:#FF6B00 !important;color:white !important', 'background:#0284c7 !important;color:white !important'),
    
    # 原始咖啡色图标
    ('color:#8B4513', 'color:#0369a1'),
    
    # btn-outline-brown original
    ('color:#8B4513; border:2px solid #8B4513', 'color:#0369a1; border:2px solid #0369a1'),
    
    # 紫色按钮 → 青色
    ('background:linear-gradient(135deg,#4a148c,#7b1fa2); color:white', 'background:linear-gradient(135deg,#0891b2,#06b6d4); color:white'),
    
    # 绿色按钮 → 蓝色
    ('background:linear-gradient(135deg,#1b5e20,#388e3c); color:white', 'background:linear-gradient(135deg,#1d4ed8,#3b82f6); color:white'),
    
    # tier-bronze badge
    ('background:#fff3e0; color:#e65100', 'background:#e0f2fe; color:#0369a1'),
]

count = 0
for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        count += 1
        print(f'  OK: {old[:50]}...')
    else:
        print(f'  SKIP: {old[:50]}...')

# app-header dark background
c = c.replace(
    '.app-header { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; position:sticky; top:0; z-index:100; }',
    '.app-header { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; position:sticky; top:0; z-index:100; background:linear-gradient(90deg,#0f172a,#1e293b); color:white; }'
)
count += 1
print(f'  OK: app-header dark bg')

# back-btn style
c = c.replace(
    '.app-header h2 { font-size:1rem; font-weight:600; }',
    '.app-header h2 { font-size:1rem; font-weight:600; }\n.back-btn { background:rgba(59,130,246,0.2); border:none; color:#93c5fd; width:36px; height:36px; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center; font-size:0.9rem; }\n.back-btn:hover { background:rgba(59,130,246,0.35); }'
)
count += 1
print(f'  OK: back-btn style')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(c)

print(f'\nDone! {count} replacements applied to style.css')
