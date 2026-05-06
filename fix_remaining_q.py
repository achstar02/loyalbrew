import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

fixes = [
    # Merchant language buttons
    ("setMerchantLang('zh')\" id=\"mlang-zh\">??</button>", "setMerchantLang('zh')\" id=\"mlang-zh\">中文</button>"),
    ("setMerchantLang('ta')\" id=\"mlang-ta\">?????</button>", "setMerchantLang('ta')\" id=\"mlang-ta\">தமிழ்</button>"),
    
    # Commission icon
    ('<div class="commission-rule-icon">??</div>', '<div class="commission-rule-icon">💰</div>'),
    
    # Merchant settings labels
    ('Welcome Text / ???', 'Welcome Text / 欢迎文字'),
    ('Main Title / ???', 'Main Title / 主标题'),
    
    # Stamp card badge
    ('<div class="stamp-complete-badge">?? COMPLETE!</div>', '<div class="stamp-complete-badge">✅ COMPLETE!</div>'),
    
    # Big stamp icon
    ('<div style="font-size:3rem;line-height:1">??</div>', '<div style="font-size:3rem;line-height:1">☕</div>'),
    
    # New items text
    ('just for you ??', 'just for you ✨'),
    
    # Referral hero icon
    ('<div class="referral-hero-icon">??</div>', '<div class="referral-hero-icon">🎁</div>'),
]

count = 0
for old, new in fixes:
    if old in c:
        c = c.replace(old, new)
        count += 1
        print(f'  Fixed: {old[:60]}')
    else:
        print(f'  Missed: {old[:60]}')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f'\n{count} more fixes applied. Total file size: {len(c):,} bytes')
