import sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html'
with open(SRC, 'r', encoding='utf-8') as f:
    h = f.read()

old = 'copyMerchantLink()" style="white-space:nowrap"><i class="fas fa-copy"></i> <span>Copy</span>'
new = 'copyMerchantLink()" style="white-space:nowrap"><i class="fas fa-copy"></i> <span data-i18n="copyLinkBtn">Copy</span>'
h = h.replace(old, new, 1)

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(h)

print(f'Done! copyLinkBtn count: {h.count("copyLinkBtn")}, total data-i18n: {h.count("data-i18n")}')
