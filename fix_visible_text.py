import sys, re
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

fixes = [
    # Language buttons - visible text
    ('onclick="setLang(\'zh\')">??</button>', 'onclick="setLang(\'zh\')">中文</button>'),
    ('onclick="setLang(\'ta\')">?????</button>', 'onclick="setLang(\'ta\')">தமிழ்</button>'),
    
    # HTML comments with garbled Chinese
    ('<!-- ????(??) -->', '<!-- 我的账号 -->'),
    ('<!-- ????(??) -->', '<!-- 立即点餐 -->'),  # 2nd occurrence
    ('<!-- ???(??) -->', '<!-- 印章卡 -->'),
    ('<!-- ??(??) -->', '<!-- 充值 -->'),
    ('<!-- ?????? -->', '<!-- 促销活动 -->'),
    
    # Button visible text with garbled content
    ('Save Shop Info / ??????', 'Save Shop Info / 保存店铺信息'),
    ('Enter your phone &amp; tap ?? to earn points', 'Enter your phone &amp; tap + to earn points'),
    
    # Tagline garbled
    ('Order ï¿½ Earn Points ï¿½ Get Rewards', 'Order · Earn Points · Get Rewards'),
    
    # Other visible text
    ('?? <span id="topup-wallet-bonus">', '+<span id="topup-wallet-bonus">'),
]

count = 0
for old, new in fixes:
    if old in c:
        c = c.replace(old, new, 1)
        count += 1
        print(f'  OK: {old[:50]}')
    else:
        print(f'  SKIP (not found): {old[:50]}')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f'\nApplied {count} fixes')
