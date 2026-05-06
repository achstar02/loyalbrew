import sys
sys.stdout.reconfigure(encoding='utf-8')
f='C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f,'r',encoding='utf-8') as fh: c=fh.read()
old = "text-[12px] font-extrabold leading-none"
new = "text-[11px] font-extrabold leading-tight whitespace-nowrap"
count = c.count(old)
c = c.replace(old, new)
print(f'Replaced {count} occurrences of button text class')
with open(f,'w',encoding='utf-8') as fh: fh.write(c)
print(f'File size: {len(c):,} bytes')
