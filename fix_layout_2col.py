import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()

# ============================================================
# FIX 1: Change grid from 4 columns to 2 columns (2x2 grid)
# This gives each button much more width for text
# ============================================================
c = c.replace(
    'grid grid-cols-4 gap-3',
    'grid grid-cols-2 gap-3'
)

# ============================================================
# FIX 2: Make buttons wider - horizontal layout with icon left, text right
# Change from flex-col (vertical) to flex-row (horizontal)
# Find the 4 button blocks and change their inner layout
# ============================================================

# Button 1 - My Account: change to horizontal layout
old_btn1 = '''<button class="lb-bounce lb-bd1 lb-btn-hover flex flex-col items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-[#FFD700] to-[#FF9500] px-1.5 py-3 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-customer')">
            <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-white/35 ring-1 ring-black/10">
              <i class="fas fa-user text-lg"></i>
            <span class="text-[10px] font-extrabold leading-snug text-center" data-i18n="myAccount">My Account</span></button>'''

new_btn1 = '''<button class="lb-bounce lb-bd1 lb-btn-hover flex items-center justify-start gap-3 rounded-2xl bg-gradient-to-b from-[#FFD700] to-[#FF9500] px-4 py-3.5 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-customer')">
            <span class="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-white/35 ring-1 ring-black/10 shrink-0">
              <i class="fas fa-user text-base"></i>
            </span>
            <span class="text-[13px] font-bold" data-i18n="myAccount">My Account</span></button>'''

c = c.replace(old_btn1, new_btn1)

# Button 2 - Order Now
old_btn2 = '''<button class="lb-bounce lb-bd2 lb-btn-hover flex flex-col items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-white to-orange-50 px-1.5 py-3 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-menu')">
            <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-black/5 ring-1 ring-black/10">
              <i class="fas fa-utensils text-lg"></i>
            <span class="text-[10px] font-extrabold leading-snug text-center" data-i18n="orderNow">Order Now</span></button>'''

new_btn2 = '''<button class="lb-bounce lb-bd2 lb-btn-hover flex items-center justify-start gap-3 rounded-2xl bg-gradient-to-b from-white to-orange-50 px-4 py-3.5 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-menu')">
            <span class="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-black/5 ring-1 ring-black/10 shrink-0">
              <i class="fas fa-utensils text-base"></i>
            </span>
            <span class="text-[13px] font-bold" data-i18n="orderNow">Order Now</span></button>'''

c = c.replace(old_btn2, new_btn2)

# Button 3 - Stamp Card
old_btn3 = '''<button class="lb-bounce lb-bd3 lb-btn-hover flex flex-col items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-[#9d7bff] to-[#6d45ff] px-1.5 py-3 text-white ring-1 ring-white/20 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-stamp')">
            <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-white/18 ring-1 ring-white/20">
              <i class="fas fa-stamp text-lg"></i>
            <span class="text-[10px] font-extrabold leading-snug text-center" data-i18n="myStampCard">My Stamp Card</span></button>'''

new_btn3 = '''<button class="lb-bounce lb-bd3 lb-btn-hover flex items-center justify-start gap-3 rounded-2xl bg-gradient-to-b from-[#9d7bff] to-[#6d45ff] px-4 py-3.5 text-white ring-1 ring-white/20 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-stamp')">
            <span class="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-white/18 ring-1 ring-white/20 shrink-0">
              <i class="fas fa-stamp text-base"></i>
            </span>
            <span class="text-[13px] font-bold" data-i18n="myStampCard">My Stamp Card</span></button>'''

c = c.replace(old_btn3, new_btn3)

# Button 4 - Top Up
old_btn4 = '''<button class="lb-bounce lb-bd4 lb-btn-hover flex flex-col items-center justify-center gap-2 rounded-2xl bg-gradient-to-b from-[#46e6b6] to-[#18c48f] px-1.5 py-3 text-[#072016] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-topup')">
            <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-white/30 ring-1 ring-black/10">
              <i class="fas fa-wallet text-lg"></i>
            <span class="text-[10px] font-extrabold leading-snug text-center" data-i18n="topUp">Top Up</span></button>'''

new_btn4 = '''<button class="lb-bounce lb-bd4 lb-btn-hover flex items-center justify-start gap-3 rounded-2xl bg-gradient-to-b from-[#46e6b6] to-[#18c48f] px-4 py-3.5 text-[#072016] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage('page-topup')">
            <span class="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-white/30 ring-1 ring-black/10 shrink-0">
              <i class="fas fa-wallet text-base"></i>
            </span>
            <span class="text-[13px] font-bold" data-i18n="topUp">Top Up</span></button>'''

c = c.replace(old_btn4, new_btn4)

with open(f,'w',encoding='utf-8') as fh: fh.write(c)

# Verify
checks = [
    ('grid-cols-2', '2-column grid'),
    ('flex items-center justify-start', 'horizontal button layout'),
    ('text-[13px] font-bold', 'larger button text'),
]
print('Layout changes applied:')
for pattern, desc in checks:
    count = c.count(pattern)
    print(f'  {pattern}: {count}x ({desc})')
print(f'\nFile size: {len(c):,} bytes')
