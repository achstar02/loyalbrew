import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    # 1. My Account: gold -> sky blue
    ('from-[#FBBF24] to-[#D97706] px-4 py-3.5 text-[#1a0a2e] ring-1 ring-[#FBBF24]/30 shadow-lg shadow-[#FBBF24]/15',
     'from-[#0ea5e9] to-[#0284c7] px-4 py-3.5 text-white ring-1 ring-sky-300/30 shadow-lg shadow-sky-500/20'),
    
    # 2. Order Now: indigo -> sky white  
    ('from-white/[0.95] to-[#eef2ff] px-4 py-3.5 text-[#1e1b4b] ring-1 ring-indigo-200/50',
     'from-white/[0.95] to-[#f0f9ff] px-4 py-3.5 text-[#0c4a6e] ring-1 ring-sky-200/50'),
    
    # 3. Stamp Card: purple -> cyan
    ('from-[#c084fc] to-[#a855f7] px-4 py-3.5 text-white ring-1 ring-purple-300/25 shadow-lg shadow-purple-500/15',
     'from-[#06b6d4] to-[#0891b2] px-4 py-3.5 text-white ring-1 ring-cyan-300/30 shadow-lg shadow-cyan-500/18'),
    
    # 4. Top Up: emerald -> blue
    ('from-[#34d399] to-[#059669] px-4 py-3.5 text-white ring-1 ring-emerald-300/25 shadow-lg shadow-emerald-500/12',
     'from-[#3b82f6] to-[#1d4ed8] px-4 py-3.5 text-white ring-1 ring-blue-300/30 shadow-lg shadow-blue-500/15'),
]

count = 0
for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        count += 1
        print(f'  OK: {old[:40]}...')
    else:
        print(f'  SKIP (not found): {old[:40]}...')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f'\nDone! {count}/{len(replacements)} replacements applied')
