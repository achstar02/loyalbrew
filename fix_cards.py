import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()

# Fix bottom cards: add min-height and ensure proper spacing
# The cards have "flex items-center gap-3" layout - make sure text doesn't overflow
# Change card padding from p-4 to p-4 with better structure

# Add explicit line height to card titles and descriptions to prevent overlap
c = c.replace(
    'text-sm font-bold tracking-tight" data-i18n="feat1Title',
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat1Title'
)
c = c.replace(
    'text-sm font-bold tracking-tight" data-i18n="feat2Title',
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat2Title'
)
c = c.replace(
    'text-sm font-bold tracking-tight" data-i18n="feat3Title',
    'text-sm font-bold tracking-tight leading-snug" data-i18n="feat3Title'
)

# Ensure descriptions have proper line height too
c = c.replace(
    'mt-0.5 text-xs text-white/70" data-i18n="feat1Desc',
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat1Desc'
)
c = c.replace(
    'mt-0.5 text-xs text-white/70" data-i18n="feat2Desc',
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat2Desc'
)
c = c.replace(
    'mt-0.5 text-xs text-white/70" data-i18n="feat3Desc',
    'mt-0.5 text-xs text-white/70 leading-relaxed" data-i18n="feat3Desc'
)

with open(f,'w',encoding='utf-8') as fh: fh.write(c)
print('Fixed card text spacing')
print(f'File size: {len(c):,} bytes')
