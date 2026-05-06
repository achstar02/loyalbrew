import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# Fix card 2: add min-h, lb-glass, lb-card-shine, animation
old2a = '<div class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur">\n          <div class="flex items-center gap-3 min-h-[40px]">\n            <span class="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20 shrink-0">\n              <i class="fas fa-star text-lg"></i>'
new2a = '<div class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in" style="animation-delay:.5s">\n          <div class="flex items-center gap-3 min-h-[40px]">\n            <span class="flex-shrink-0 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20">\n              <i class="fas fa-star text-base"></i>'

if old2a in c:
    c = c.replace(old2a, new2a)
    print('Fixed card 2 header')
else:
    print('Card 2 header not found exactly')

# Fix card 3
old3a = '<div class="rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur">\n          <div class="flex items-center gap-3 min-h-[40px]">\n            <span class="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20 shrink-0">\n              <i class="fas fa-gift text-lg"></i>'
new3a = '<div class="min-h-[64px] rounded-2xl bg-white/12 p-4 ring-1 ring-white/20 backdrop-blur lb-glass lb-card-shine lb-animate-in" style="animation-delay:.6s">\n          <div class="flex items-center gap-3 min-h-[40px]">\n            <span class="flex-shrink-0 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/12 ring-1 ring-white/20">\n              <i class="fas fa-gift text-base"></i>'

if old3a in c:
    c = c.replace(old3a, new3a)
    print('Fixed card 3 header')
else:
    print('Card 3 header not found exactly')

# Now fix ALL feat title/desc to have whitespace-nowrap + overflow ellipsis
# This is the KEY fix - prevents text from wrapping and overlapping
c = c.replace(
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat1Title',
    'text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat1Title'
)
c = c.replace(
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat2Title',
    'text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat2Title'
)
c = c.replace(
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat3Title',
    'text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat3Title'
)

c = c.replace(
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat1Desc',
    'mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat1Desc'
)
c = c.replace(
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat2Desc',
    'mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat2Desc'
)
c = c.replace(
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat3Desc',
    'mt-0.5 text-xs text-white/70 leading-tight whitespace-nowrap overflow-hidden text-ellipsis" data-i18n="feat3Desc'
)

# Also ensure all flex-1 divs have min-w-0 (critical for text-ellipsis to work in flexbox)
c = c.replace(
    '<div class="flex-1 min-w-0">\n              <div class="text-sm font-bold leading-snug whitespace-nowrap',
    '<div class="flex-1 min-w-0">\n              <div class="text-sm font-bold leading-snug whitespace-nowrap'
)  # already good

# For cards 2&3 that still have old flex-1 without min-w-0
c = c.replace(
    '<div class="flex-1 min-w-0">\n              <div class="text-sm font-bold tracking-tight leading-snug"',
    '<div class="flex-1 min-w-0">\n              <div class="text-sm font-bold leading-snug whitespace-nowrap overflow-hidden text-ellipsis"'
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f'\nFile size: {len(c):,} bytes')
