import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()

# 1. Fix button text: remove whitespace-nowrap, allow 2 lines, reduce icon size slightly
c = c.replace(
    'text-[11px] font-extrabold leading-tight whitespace-nowrap',
    'text-[10px] font-extrabold leading-snug text-center'
)

# 2. Reduce icon container from h-10 w-10 to h-9 w-9 to give more room for text
c = c.replace(
    'inline-flex h-10 w-10 items-center justify-center rounded-2xl',
    'inline-flex h-8 w-8 items-center justify-center rounded-xl'
)

# 3. Reduce gap between icon and text
# Change gap-2 to gap-1 in the 4 buttons only (be careful not to affect other elements)
# The buttons have: gap-2 rounded-2xl bg-gradient-to-b
# Let's just reduce py-4 to py-3 for more compact buttons
c = c.replace(
    'px-2 py-4 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-customer\')">',
    'px-1.5 py-3 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-customer\')">'
)
c = c.replace(
    'px-2 py-4 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-menu\')">',
    'px-1.5 py-3 text-[#2a1a10] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-menu\')">'
)
c = c.replace(
    'px-2 py-4 text-white ring-1 ring-white/20 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-stamp\')">',
    'px-1.5 py-3 text-white ring-1 ring-white/20 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-stamp\')">'
)
c = c.replace(
    'px-2 py-4 text-[#072016] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-topup\')">',
    'px-1.5 py-3 text-[#072016] ring-1 ring-black/10 transition hover:-translate-y-0.5 active:translate-y-0" onclick="showPage(\'page-topup\')">'
)

with open(f,'w',encoding='utf-8') as fh: fh.write(c)
print(f'Fixed button layout. File size: {len(c):,} bytes')
