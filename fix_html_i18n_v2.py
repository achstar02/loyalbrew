import sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

SRC = r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html'
BACKUP = r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html.bak_i18n'

# 先备份
shutil.copy2(SRC, BACKUP)
print(f'Backed up ({len(open(BACKUP,"r",encoding="utf-8").read())} chars)')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
count = 0
errors = []

def safe_replace(old, new, label=''):
    global html, count
    if old not in html:
        errors.append(f'MISSING: {label or old[:50]}')
        return False
    html = html.replace(old, new, 1)
    count += 1
    return True

# ========== 所有替换 ==========
safe_replace('<span>View Cart ?</span>', '<span data-i18n="floatViewCart">View Cart ?</span>', 'floatViewCart')
safe_replace('<span>Touch &amp; Go</span>', '<span data-i18n="tngName">Touch &amp; Go</span>', 'tngName')
safe_replace('<small id="bank-amount-display">Amount: RM0.00</small>', '<small id="bank-amount-display" data-i18n="bankAmountLabel">Amount: RM0.00</small>', 'bankAmountLabel')
safe_replace('<i class="fas fa-store"></i>Merchant</h2>', '<i class="fas fa-store"></i><span data-i18n="merchant">Merchant</span></h2>', 'merchant')
safe_replace('<p class="hint">Enter your Merchant ID and password</p>', '<p class="hint" data-i18n="mLoginHint">Enter your Merchant ID and password</p>', 'mLoginHint')
safe_replace('<span id="merchant-header-name">Admin</span>', '<span id="merchant-header-name" data-i18n="admin">Admin</span>', 'admin')

# 订单筛选按钮 (orders section) - 用更精确的上下文
safe_replace("filterOrders('all', this)\"\n all>All", "filterOrders('all', this)\"\n all data-i18n=\"filterAll\">All", 'filterAll-orders')
safe_replace("filterOrders('pending', this)\"\n pending>Pending", "filterOrders('pending', this)\"\n pending data-i18n=\"filterPending\">Pending", 'filterPending')
safe_replace("filterOrders('preparing', this)\"\n preparing>Preparing", "filterOrders('preparing', this)\"\n preparing data-i18n=\"filterPreparing\">Preparing", 'filterPreparing')
safe_replace("filterOrders('done', this)\"\n done>Done", "filterOrders('done', this)\"\n done data-i18n=\"filterDone\">Done", 'filterDone')

safe_replace('<span>Promo Price (RM)</span>', '<span data-i18n="mPromoPriceLbl">Promo Price (RM)</span>', 'mPromoPriceLbl')
safe_replace('no_active_new_items>No active new items', 'data-i18n="noActiveNewItems">No active new items', 'noActiveNewItems')
safe_replace('no_past_launches>No past launches', 'data-i18n="noPastLaunches">No past launches', 'noPastLaunches')

# 印章规则选项
safe_replace('>Every purchase = 1 stamp</option>', ' data-i18n="mRulePerOrderOpt">Every purchase = 1 stamp</option>', 'mRulePerOrderOpt')
safe_replace('>Every RM X spent = 1 stamp</option>', ' data-i18n="mRulePerAmountOpt">Every RM X spent = 1 stamp</option>', 'mRulePerAmountOpt')
safe_replace('>Purchase specific item = 1 stamp</option>', ' data-i18n="mRulePerItemOpt">Purchase specific item = 1 stamp</option>', 'mRulePerItemOpt')

# 奖励类型选项
safe_replace('free_menu_item>Free Menu Item</option>', 'free_menu_item data-i18n="mRewardFreeItemOpt">Free Menu Item</option>', 'mRewardFreeItemOpt')
safe_replace('flat_discount>Flat Discount (RM off)</option>', 'flat_discount data-i18n="mRewardFlatDiscountOpt">Flat Discount (RM off)</option>', 'mRewardFlatDiscountOpt')
safe_replace('bonus_points>Bonus Points</option>', 'bonus_points data-i18n="mRewardBonusPointsOpt">Bonus Points</option>', 'mRewardBonusPointsOpt')
safe_replace(' free_item>Free Item</label>', ' free_item data-i18n="mFreeItemLabel">Free Item</label>', 'mFreeItemLabel')

# Stamp cards section
safe_replace('no_stamp_cards_yet>No stamp cards yet', 'data-i18n="noStampCardsYet">No stamp cards yet', 'noStampCardsYet')
safe_replace('search_for_a_member>Search for a member', 'data-i18n="searchForAMember">Search for a member', 'searchForAMember')
safe_replace('no_pending_requests>No pending request', 'data-i18n="noPendingRequests">No pending request', 'noPendingRequests')
safe_replace(' min_amount>Min Amount (RM)</label>', ' min_amount data-i18n="minAmount">Min Amount (RM)</label>', 'minAmount')
safe_replace(' expiry_date>Expiry Date', ' expiry_date data-i18n="expiryDate">Expiry Date', 'expiryDate')

# 投诉筛选按钮 - 精确上下文
safe_replace("filterComplaints('all', this)\"\n all>All", "filterComplaints('all', this)\"\n all data-i18n=\"filterAllC\">All", 'filterAll-complaints')
safe_replace("filterComplaints('open', this)\"\n open>Open", "filterComplaints('open', this)\"\n open data-i18n=\"complaintOpenBtn\">Open", 'complaintOpenBtn')
safe_replace("filterComplaints('in_progress', this)\"\n in_progress>In Progress", "filterComplaints('in_progress', this)\"\n in_progress data-i18n=\"complaintInProgressBtn\">In Progress", 'complaintInProgressBtn')
safe_replace("filterComplaints('resolved', this)\"\n resolved>Resolved", "filterComplaints('resolved', this)\"\n resolved data-i18n=\"complaintResolvedBtn\">Resolved", 'complaintResolvedBtn')

# Shop Link / QR
safe_replace('<span>My Shop Link</span></h3>', '<span data-i18n="myShopLink">My Shop Link</span></h3>', 'myShopLink')
safe_replace('Share this link or QR code with customers. They scan it to visit your shop and register as your member.</p>',
             'data-i18n="shopLinkDesc">Share this link or QR code with customers. They scan it to visit your shop and register as your member.</p>', 'shopLinkDesc')
safe_replace('fa-copy"></i> <span>Copy</span>\n          </button>\n          ', 'fa-copy"></i> <span data-i18n="copyLinkBtn">Copy</span>', 'copyLinkBtn')
safe_replace('>Shop QR Code</p>', ' data-i18n="shopQRCodeLabel">Shop QR Code</p>', 'shopQRCodeLabel')
safe_replace('>How to use:</h4>', ' data-i18n="qrHowToUse">How to use:</h4>', 'qrHowToUse')
safe_replace('<li>Print this QR and put at cashier / entrance</li>', '<li data-i18n="qrPrintHint">Print this QR and put at cashier / entrance</li>', 'qrPrintHint')
safe_replace('<li>Use table QR below for ordering</li>', '<li data-i18n="qrTableHint">Use table QR below for ordering</li>', 'qrTableHint')
safe_replace('<span>Print Shop QR</span></button>', '<span data-i18n="printShopQRBtn">Print Shop QR</span></button>', 'printShopQRBtn')
safe_replace('qr_description>Each table gets a unique QR code. Customers scan to order directly.</p>',
             'data-i18n="tableQrDesc">Each table gets a unique QR code. Customers scan to order directly.</p>', 'tableQrDesc')

# Referral
safe_replace('referral_commission_rate>Referral Commission Rate</strong>',
             'data-i18n="referralCommissionRateLabel">Referral Commission Rate</strong>', 'referralCommissionRateLabel')
safe_replace('<span>Current rate:</span><strong', '<span data-i18n="currentRateLbl">Current rate:</span><strong', 'currentRateLbl')
safe_replace('no_pending_payment_proofs>No pending payment proofs',
             'data-i18n="noPendingPaymentProofs">No pending payment proofs', 'noPendingPaymentProofs')

# Shop Settings hints
safe_replace('Leave empty to use default banner</p>', 'data-i18n="leaveEmptyBanner">Leave empty to use default banner</p>', 'leaveEmptyBanner')
safe_replace('Small text above the main title (e.g. "Welcome Back")</p>', 'data-i18n="smallTextHint">Small text above the main title (e.g. "Welcome Back")</p>', 'smallTextHint')
safe_replace('The big bold title on landing page (e.g. "What\'s your drink today?")</p>',
             'data-i18n="bigTitleHint">The big bold title on landing page (e.g. "What\'s your drink today?")</p>', 'bigTitleHint')
safe_replace('higher_shows_first>Higher number = shown first</p>', 'data-i18n="higherShowsFirst">Higher number = shown first</p>', 'higherShowsFirst')

# Kitchen Display
safe_replace('<span kitchen_display>Kitchen Display</span>', '<span kitchen_display data-i18n="kitchenDisplayLbl">Kitchen Display</span>', 'kitchenDisplayLbl')
safe_replace('<span refresh>Refresh</span>', '<span refresh data-i18n="refreshLbl">Refresh</span>', 'refreshLbl')
safe_replace('<span new>New</span><span class="kbadge"', '<span new data-i18n="statusNewLbl">New</span><span class="kbadge"', 'statusNewLbl')
safe_replace('<span preparing>Preparing</span><span class="kbadge"', '<span preparing data-i18n="preparingLbl">Preparing</span><span class="kbadge"', 'preparingLbl')
safe_replace('<span done>Done</span></button>', '<span done data-i18n="doneLbl">Done</span></button>', 'doneLbl')

# Notifications
safe_replace('id="notif-prompt-title" style="text-align:center;font-size:1.05rem;margin-bottom:8px">Get Notified When Ready!</h3>',
             'id="notif-prompt-title" data-i18n="getNotifiedWhenReady" style="text-align:center;font-size:1.05rem;margin-bottom:8px">Get Notified When Ready!</h3>', 'getNotifiedWhenReady')
safe_replace('id="notif-prompt-enable-btn">Enable Notifications</span>', 'id="notif-prompt-enable-btn" data-i18n="enableNotificationsBtn">Enable Notifications</span>', 'enableNotificationsBtn')
safe_replace('id="notif-prompt-skip-btn">Maybe Later</span>', 'id="notif-prompt-skip-btn" data-i18n="maybeLaterBtn">Maybe Later</span>', 'maybeLaterBtn')

# Referral Program section
safe_replace('<i class="fas fa-share-alt"></i>Referral Program</h2>', '<i class="fas fa-share-alt"></i><span data-i18n="referralProgramTitle">Referral Program</span></h2>', 'referralProgramTitle')
safe_replace('Share your phone number as a referral code. When your friend makes their first order, you earn a commission credited to your wallet!</p>',
             'data-i18n="referralProgramDescText">Share your phone number as a referral code. When your friend makes their first order, you earn a commission credited to your wallet!</p>', 'referralProgramDescText')
safe_replace('fa-copy"></i>Copy</button>\n        </div>', 'fa-copy"></i><span data-i18n="copyReferralBtn">Copy</span></button>', 'copyReferralBtn')
safe_replace('<i class="fas fa-list"></i>Commission History</h3>', '<i class="fas fa-list"></i><span data-i18n="commissionHistoryTitle">Commission History</span></h3>', 'commissionHistoryTitle')
safe_replace('<i class="fas fa-users"></i>Friends You Referred</h3>', '<i class="fas fa-users"></i><span data-i18n="friendsReferredTitle">Friends You Referred</span></h3>', 'friendsReferredTitle')

# Complaint Detail
safe_replace('color:#e53935"></i>Complaint Detail</h3>', 'color:#e53935"></i><span data-i18n="complaintDetailTitle">Complaint Detail</span></h3>', 'complaintDetailTitle')
safe_replace('fa-check"></i>Mark Resolved</button>', 'fa-check"></i><span data-i18n="markResolvedBtn">Mark Resolved</span></button>', 'markResolvedBtn')
safe_replace('color:#8B4513"></i>Order Details</h3>', 'color:#8B4513"></i><span data-i18n="orderDetailsTitle">Order Details</span></h3>', 'orderDetailsTitle')

# ========== 写入 ==========
print(f'\n=== Results ===')
print(f'Applied: {count}')
if errors:
    print(f'Errors ({len(errors)}):')
    for e in errors:
        print(f'  {e}')

if len(html) > 1000:
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Saved! Size: {len(html)} chars (was {original_len})')
else:
    print(f'ERROR: file too small ({len(html)}), not saving!')
