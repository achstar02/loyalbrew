import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\index.html", "r", encoding="utf-8") as f:
    html = f.read()

original = html
count = 0

# 简单替换列表: (old_str, new_str)
replacements = [
    # 浮动购物车
    ('<span>View Cart ?</span>', '<span data-i18n="floatViewCart">View Cart ?</span>'),
    ('<span>Touch &amp; Go</span>', '<span data-i18n="tngName">Touch &amp; Go</span>'),
    ('<small id="bank-amount-display">Amount: RM0.00</small>', '<small id="bank-amount-display" data-i18n="bankAmountLabel">Amount: RM0.00</small>'),
    
    # 商家登录
    ('<i class="fas fa-store"></i>Merchant</h2>', '<i class="fas fa-store"></i><span data-i18n="merchant">Merchant</span></h2>'),
    ('<p class="hint">Enter your Merchant ID and password</p>', '<p class="hint" data-i18n="mLoginHint">Enter your Merchant ID and password</p>'),
    ('<span id="merchant-header-name">Admin</span>', '<span id="merchant-header-name" data-i18n="admin">Admin</span>'),
    
    # 订单筛选按钮 (第一组)
    ('" all>All</button>', '" all data-i18n="filterAll">All</button>'),
    ('" pending>Pending</button>', '" pending data-i18n="filterPending">Pending</button>'),
    ('" preparing>Preparing</button>', '" preparing data-i18n="filterPreparing">Preparing</button>'),
    ('" done>Done</button>', '" done data-i18n="filterDone">Done</button>'),
    
    # Promo Price
    ('<span>Promo Price (RM)</span>', '<span data-i18n="mPromoPrice2">Promo Price (RM)</span>'),
    
    # New Items
    ('no_active_new_items>No active new items', 'data-i18n="noActiveNewItems">No active new items'),
    ('no_past_launches>No past launches', 'data-i18n="noPastLaunches">No past launches'),
    
    # 印章规则选项
    ('>Every purchase = 1 stamp</option>', ' data-i18n="mRulePerOrderOpt">Every purchase = 1 stamp</option>'),
    ('>Every RM X spent = 1 stamp</option>', ' data-i18n="mRulePerAmountOpt">Every RM X spent = 1 stamp</option>'),
    ('>Purchase specific item = 1 stamp</option>', ' data-i18n="mRulePerItemOpt">Purchase specific item = 1 stamp</option>'),
    
    # 奖励类型选项
    ('free_menu_item>Free Menu Item</option>', 'free_menu_item data-i18n="mRewardFreeItemOpt">Free Menu Item</option>'),
    ('flat_discount>Flat Discount (RM off)</option>', 'flat_discount data-i18n="mRewardFlatDiscountOpt">Flat Discount (RM off)</option>'),
    ('bonus_points>Bonus Points</option>', 'bonus_points data-i18n="mRewardBonusPointsOpt">Bonus Points</option>'),
    (' free_item>Free Item</label>', ' free_item data-i18n="mFreeItemLabel">Free Item</label>'),
    
    # Stamp Cards
    ('no_stamp_cards_yet>No stamp cards yet', 'data-i18n="noStampCardsYet">No stamp cards yet'),
    ('search_for_a_member>Search for a member', 'data-i18n="searchForAMember">Search for a member'),
    ('no_pending_requests>No pending request', 'data-i18n="noPendingRequests">No pending request'),
    (' min_amount>Min Amount (RM)</label>', ' min_amount data-i18n="minAmount">Min Amount (RM)</label>'),
    (' expiry_date>Expiry Date', ' expiry_date data-i18n="expiryDate">Expiry Date'),
    
    # 投诉筛选按钮
    ('complaints-filter">\n            <button class="filter-btn active" onclick="filterComplaints(\'all\', this)"\n all>All</button>',
     'complaints-filter">\n            <button class="filter-btn active" onclick="filterComplaints(\'all\', this)"\n all data-i18n="filterAllC">All</button>'),
    ('" open>Open</button>', '" open data-i18n="complaintOpenBtn">Open</button>'),
    ('" in_progress>In Progress</button>', '" in_progress data-i18n="complaintInProgressBtn">In Progress</button>'),
    ('" resolved>Resolved</button>', '" resolved data-i18n="complaintResolvedBtn">Resolved</button>'),
    
    # Shop Link / QR
    ('<span>My Shop Link</span></h3>', '<span data-i18n="myShopLink">My Shop Link</span></h3>'),
    ('Share this link or QR code with customers. They scan it to visit your shop and register as your member.</p>',
     'data-i18n="shopLinkDesc">Share this link or QR code with customers. They scan it to visit your shop and register as your member.</p>'),
    ('fa-copy"></i> <span>Copy</span>', 'fa-copy"></i> <span data-i18n="copyLinkBtn">Copy</span>'),
    ('Shop QR Code</p>', 'data-i18n="shopQRCodeLabel">Shop QR Code</p>'),
    ('How to use:</h4>', 'data-i18n="qrHowToUse">How to use:</h4>'),
    ('<li>Print this QR and put at cashier / entrance</li>', '<li data-i18n="qrPrintHint">Print this QR and put at cashier / entrance</li>'),
    ('<li>Use table QR below for ordering</li>', '<li data-i18n="qrTableHint">Use table QR below for ordering</li>'),
    ('<span>Print Shop QR</span></button>', '<span data-i18n="printShopQRBtn">Print Shop QR</span></button>'),
    ('qr_description>Each table gets a unique QR code. Customers scan to order directly.</p>',
     'data-i18n="tableQrDesc">Each table gets a unique QR code. Customers scan to order directly.</p>'),
    
    # Referral
    ('referral_commission_rate>Referral Commission Rate</strong>',
     'data-i18n="referralCommissionRateLabel">Referral Commission Rate</strong>'),
    ('<span>Current rate:</span><strong', '<span data-i18n="currentRateLbl">Current rate:</span><strong'),
    ('no_pending_payment_proofs>No pending payment proofs',
     'data-i18n="noPendingPaymentProofs">No pending payment proofs'),
    
    # Shop Settings hints
    ('Leave empty to use default banner</p>', 'data-i18n="leaveEmptyBanner">Leave empty to use default banner</p>'),
    ('Small text above the main title (e.g. "Welcome Back")</p>', 'data-i18n="smallTextHint">Small text above the main title (e.g. "Welcome Back")</p>'),
    ("The big bold title on landing page (e.g. \"What's your drink today?\")</p>",
     'data-i18n="bigTitleHint">The big bold title on landing page (e.g. "What\'s your drink today?")</p>'),
    ('higher_shows_first>Higher number = shown first</p>', 'data-i18n="higherShowsFirst">Higher number = shown first</p>'),
    
    # Kitchen Display
    ('<span kitchen_display>Kitchen Display</span>', '<span kitchen_display data-i18n="kitchenDisplayLbl">Kitchen Display</span>'),
    ('<span refresh>Refresh</span>', '<span refresh data-i18n="refreshLbl">Refresh</span>'),
    ('<span new>New</span><span class="kbadge"', '<span new data-i18n="statusNewLbl">New</span><span class="kbadge"'),
    ('<span preparing>Preparing</span><span class="kbadge"', '<span preparing data-i18n="preparingLbl">Preparing</span><span class="kbadge"'),
    ('<span done>Done</span></button>', '<span done data-i18n="doneLbl">Done</span></button>'),
    
    # Notifications
    ('id="notif-prompt-title" style="text-align:center;font-size:1.05rem;margin-bottom:8px">Get Notified When Ready!</h3>',
     'id="notif-prompt-title" data-i18n="getNotifiedWhenReady" style="text-align:center;font-size:1.05rem;margin-bottom:8px">Get Notified When Ready!</h3>'),
    ('id="notif-prompt-enable-btn">Enable Notifications</span>', 'id="notif-prompt-enable-btn" data-i18n="enableNotificationsBtn">Enable Notifications</span>'),
    ('id="notif-prompt-skip-btn">Maybe Later</span>', 'id="notif-prompt-skip-btn" data-i18n="maybeLaterBtn">Maybe Later</span>'),
    
    # Referral Program section
    ('<i class="fas fa-share-alt"></i>Referral Program</h2>', '<i class="fas fa-share-alt"></i><span data-i18n="referralProgramTitle">Referral Program</span></h2>'),
    ('Share your phone number as a referral code. When your friend makes their first order, you earn a commission credited to your wallet!</p>',
     'data-i18n="referralProgramDescText">Share your phone number as a referral code. When your friend makes their first order, you earn a commission credited to your wallet!</p>'),
    ('fa-copy"></i>Copy</button>', 'fa-copy"></i><span data-i18n="copyReferralBtn">Copy</span></button>'),
    ('<i class="fas fa-list"></i>Commission History</h3>', '<i class="fas fa-list"></i><span data-i18n="commissionHistoryTitle">Commission History</span></h3>'),
    ('<i class="fas fa-users"></i>Friends You Referred</h3>', '<i class="fas fa-users"></i><span data-i18n="friendsReferredTitle">Friends You Referred</span></h3>'),
    
    # Complaint Detail
    ('color:#e53935"></i>Complaint Detail</h3>', 'color:#e53935"></i><span data-i18n="complaintDetailTitle">Complaint Detail</span></h3>'),
    ('fa-check"></i>Mark Resolved</button>', 'fa-check"></i><span data-i18n="markResolvedBtn">Mark Resolved</span></button>'),
    ('color:#8B4513"></i>Order Details</h3>', 'color:#8B4513"></i><span data-i18n="orderDetailsTitle">Order Details</span></h3>'),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new, 1)
        count += 1
    else:
        print(f"  MISSING: {old[:70]}")

print(f"\nApplied {count}/{len(replacements)} replacements")

if html != original:
    with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved index.html")
else:
    print("NO CHANGES!")
