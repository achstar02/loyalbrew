import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ============================================================
# FIX: Bottom 3 cards - complete layout overhaul
# The text overlap is caused by the card content not having
# proper height constraints + possible animation rendering bug
# ============================================================

old_cards = '''<!-- Bottom 3 translucent cards -->
      <section class="mt-6 space-y-3 pb-10">
        <div class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in lb-d6">
          <div class="flex items-center gap-3">
            <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-qrcode text-lg"></i>
            <div class="flex-1">
              <div class="text-sm font-bold tracking-tight leading-snug" data-i18n="feat1Title">Scan & Order</div>
              <div class="mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat1Desc">Scan table QR, order in seconds</div>
            </div>
            <span class="text-xs font-semibold text-white/80"><span data-i18n="enter">Enter</span></span>
        </div>

        <div class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur">
          <div class="flex items-center gap-3">
            <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-star text-lg"></i>
            <div class="flex-1">
              <div class="text-sm font-bold tracking-tight leading-snug" data-i18n="feat2Title">Earn Points</div>
              <div class="mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat2Desc">RM1 spent = 1 point earned</div>
            </div>
            <span class="text-xs font-semibold text-white/80"><span data-i18n="get">Get</span></span>
        </div>

        <div class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur">
          <div class="flex items-center gap-3">
            <span class="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-gift text-lg"></i>
            <div class="flex-1">
              <div class="text-sm font-bold tracking-tight leading-snug" data-i18n="feat3Title">Free Drinks</div>
              <div class="mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat3Desc">Redeem for free beverages</div>
            </div>
            <span class="text-xs font-semibold text-white/80"><span data-i18n="view">View</span></span>
        </div>'''

new_cards = '''<!-- Bottom 3 translucent cards -->
      <section class="mt-6 space-y-3 pb-10">
        <div class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in lb-d6">
          <div class="flex items-center gap-3 min-h-[40px]">
            <span class="flex-shrink-0 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-qrcode text-base"></i>
            </span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat1Title">Scan & Order</div>
              <div class="mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat1Desc">Scan table QR, order in seconds</div>
            </div>
            <span class="flex-shrink-0 ml-2 text-xs font-semibold text-white/80 opacity-90"><span data-i18n="enter">Enter ›</span></span>
          </div>
        </div>

        <div class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in" style="animation-delay:.5s">
          <div class="flex items-center gap-3 min-h-[40px]">
            <span class="flex-shrink-0 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-star text-base"></i>
            </span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat2Title">Earn Points</div>
              <div class="mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat2Desc">RM1 spent = 1 point earned</div>
            </div>
            <span class="flex-shrink-0 ml-2 text-xs font-semibold text-white/80 opacity-90"><span data-i18n="get">Get ›</span></span>
          </div>
        </div>

        <div class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in" style="animation-delay:.6s">
          <div class="flex items-center gap-3 min-h-[40px]">
            <span class="flex-shrink-0 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20">
              <i class="fas fa-gift text-base"></i>
            </span>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat3Title">Free Drinks</div>
              <div class="mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat3Desc">Redeem for free beverages</div>
            </div>
            <span class="flex-shrink-0 ml-2 text-xs font-semibold text-white/80 opacity-90"><span data-i18n="view">View ›</span></span>
          </div>
        </div>'''

if old_cards in c:
    c = c.replace(old_cards, new_cards)
    print('✅ Cards replaced with fixed layout')
else:
    print('❌ Could not find exact card block, trying partial fix...')
    # Fallback: just add key CSS fixes
    count = 0
    
    # Add min-height to all 3 card divs (the ones with feat titles)
    c = c.replace(
        'class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass',
        'class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass'
    )
    count += 1
    
    # Fix inner flex to have min-height and proper constraints
    c = c.replace(
        'class="flex items-center gap-3">',
        'class="flex items-center gap-3 min-h-[40px]">'
    )
    
    # Make icon container shrink-0
    c = c.replace(
        'inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-white/12 ring-1 ring-white/20">',
        'inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20 shrink-0">'
    )
    
    # Make text container flex-1 min-w-0
    c = c.replace(
        '<div class="flex-1">\n              <div class="text-sm font-bold',
        '<div class="flex-1 min-w-0">\n              <div class="text-sm font-bold'
    )
    
    print(f'✅ Applied {count} fallback fixes')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f'File size: {len(c):,} bytes')
