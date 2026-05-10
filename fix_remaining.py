import sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html'
with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

count = 0
errors = []

def fix(old, new, label=''):
    global html, count
    if old not in html:
        errors.append(f'MISSING: {label}')
        return False
    html = html.replace(old, new, 1)
    count += 1
    return True

# 订单筛选 - 同一行格式
fix('filterOrders(\'all\', this)" all>All', 'filterOrders(\'all\', this)" all data-i18n="filterAll">All', 'filterAll')
fix('filterOrders(\'pending\', this)" pending>Pending', 'filterOrders(\'pending\', this)" pending data-i18n="filterPending">Pending', 'filterPending')
fix('filterOrders(\'preparing\', this)" preparing>Preparing', 'filterOrders(\'preparing\', this)" preparing data-i18n="filterPreparing">Preparing', 'filterPreparing')
fix('filterOrders(\'done\', this)" done>Done', 'filterOrders(\'done\', this)" done data-i18n="filterDone">Done', 'filterDone')

# 投诉筛选 - 同一行格式
fix('filterComplaints(\'all\', this)" all>All', 'filterComplaints(\'all\', this)" all data-i18n="filterAllC">All', 'filterAllC')
fix('filterComplaints(\'open\', this)" open>Open', 'filterComplaints(\'open\', this)" open data-i18n="complaintOpenBtn">Open', 'complaintOpenBtn')
fix('filterComplaints(\'in_progress\', this)" in_progress>In Progress', 'filterComplaints(\'in_progress\', this)" in_progress data-i18n="complaintInProgressBtn">In Progress', 'complaintInProgressBtn')
fix('filterComplaints(\'resolved\', this)" resolved>Resolved', 'filterComplaints(\'resolved\', this)" resolved data-i18n="complaintResolvedBtn">Resolved', 'complaintResolvedBtn')

# Copy buttons - 两种不同格式
# Shop link copy: fa-copy"></i> <span>Copy</span>
fix('fa-copy"></i> <span>Copy</span>\n          </button>\n          ', 'fa-copy"></i> <span data-i18n="copyLinkBtn">Copy</span>', 'copyLinkBtn')
# Referral copy: fa-copy"></i>Copy (no span)
fix('fa-copy"></i>Copy</button>', 'fa-copy"></i><span data-i18n="copyReferralBtn">Copy</span></button>', 'copyReferralBtn')

print(f'Applied: {count}, Errors: {len(errors)}')
for e in errors:
    print(f'  {e}')

if len(html) > 1000 and count > 0:
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Saved! Size: {len(html)}')
