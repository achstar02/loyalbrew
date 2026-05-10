import sys, re
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

count = 0
errors = []

def add_translation(lang, key, value, insert_before_key=None):
    """在指定语言的翻译块中添加新的键值对"""
    global js, count
    # 检查是否已存在
    pattern = f"{key}\\s*:\\s*'[^']*'"
    if re.search(pattern, js):
        errors.append(f'ALREADY EXISTS {lang}.{key}')
        return False
    
    # 找到语言块的插入点（在某个已知键之前或 } 之前）
    if insert_before_key:
        target = f"{insert_before_key}:"
        if target in js:
            js = js.replace(target, f"    {key}: '{value}',\n    {insert_before_key}:", 1)
            count += 1
            return True
    
    # fallback: 在该语言的闭合 } 前插入
    # 找到 lang 块的最后一个 } （在下一个语言之前）
    errors.append(f'CANNOT FIND insert point for {lang}.{key}')
    return False

# ============================================================
# 新增的 i18n 键及其翻译
# 格式: (key, en_value, zh_value, ms_value, insert_before_key)
# ============================================================

new_keys = [
    ('floatViewCart', 'View Cart →', '查看购物车 →', 'Lihat Troli →', 'floatItem'),
    ('tngName', 'Touch & Go', 'Touch & Go', 'Touch & Go', 'tngUploadHint'),
    ('bankAmountLabel', 'Amount: RM0.00', '金额：RM0.00', 'Jumlah: RM0.00', 'tngAmountLabel'),
    ('mLoginHint', 'Enter your Merchant ID and password', '输入商家ID和密码', 'Masukkan ID Peniaga dan kata laluan', 'mInvalidCredentials'),
    ('filterAll', 'All', '全部', 'Semua', 'filterPending'),
    ('filterPending', 'Pending', '待处理', 'Ditunggu', 'filterPreparing'),
    ('filterPreparing', 'Preparing', '准备中', 'Menyediakan', 'filterDone'),
    ('filterDone', 'Done', '已完成', 'Selesai', 'cashPayCounter'),
    ('filterAllC', 'All', '全部', 'Semua', 'complaintOpenBtn'),
    ('complaintOpenBtn', 'Open', '待处理', 'Dibuka', 'complaintInProgressBtn'),
    ('complaintInProgressBtn', 'In Progress', '处理中', 'Sedang Diproses', 'complaintResolvedBtn'),
    ('complaintResolvedBtn', 'Resolved', '已解决', 'Selesai', 'myShopLink'),
    ('mPromoPriceLbl', 'Promo Price (RM)', '促销价 (RM)', 'Harga Promo (RM)', 'mPromoPriceDesc'),
    ('noActiveNewItems', 'No active new items', '没有进行中的新品', 'Tiada item baharu aktif', 'mNoActiveItems'),
    ('noPastLaunches', 'No past launches', '没有历史发布', 'Tiada pelancaran lepas', 'mNoPastLaunches'),
    ('mRulePerOrderOpt', 'Every purchase = 1 stamp', '每次购买=1印章', 'Setiap pembelian = 1 setem', 'mRulePerAmountOpt'),
    ('mRulePerAmountOpt', 'Every RM X spent = 1 stamp', '每消费RM X=1印章', 'Setiap RM X dibelanjakan = 1 setem', 'mRulePerItemOpt'),
    ('mRulePerItemOpt', 'Purchase specific item = 1 stamp', '购买指定商品=1印章', 'Beli item tertentu = 1 setem', 'mRewardType'),
    ('mRewardFreeItemOpt', 'Free Menu Item', '免费菜单项目', 'Item Menu Percuma', 'mRewardFlatDiscountOpt'),
    ('mRewardFlatDiscountOpt', 'Flat Discount (RM off)', '固定减免(RM)', 'Diskaun Tetap (RM)', 'mRewardPctDiscountOpt'),
    ('mRewardBonusPointsOpt', 'Bonus Points', '奖励积分', 'Mata Bonus', 'mFreeItemLabel'),
    ('mFreeItemLabel', 'Free Item', '免费商品', 'Item Percuma', 'card_color_theme'),
    ('noStampCardsYet', 'No stamp cards yet', '还没有印章卡', 'Belum ada kad setem', 'mNoStampCardsYet'),
    ('searchForAMember', 'Search for a member', '搜索会员', 'Cari Ahli', 'mNoMembersFound'),
    ('noPendingRequests', 'No pending requests', '暂无待处理请求', 'Tiada permohonan tertunda', 'mNoPendingRequests'),
    ('minAmount', 'Min Amount (RM)', '最低金额(RM)', 'Jumlah Min (RM)', 'expiryDate'),
    ('expiryDate', 'Expiry Date', '到期日期', 'Tarikh Luput', 'optional'),
    ('myShopLink', 'My Shop Link', '我的店铺链接', 'Pautan Kedai Saya', 'shopLinkDesc'),
    ('shopLinkDesc', 'Share this link or QR code with customers. They scan it to visit your shop and register as your member.', '分享此链接或二维码给顾客。扫码访问店铺并注册成为会员。', 'Kongsi pautan atau kod QR ini dengan pelanggan. Imbas untuk lawati kedai dan daftar sebagai ahli.', 'copyLinkBtn'),
    ('copyLinkBtn', 'Copy', '复制', 'Salin', 'shopQRCodeLabel'),
    ('shopQRCodeLabel', 'Shop QR Code', '店铺二维码', 'Kod QR Kedai', 'qrHowToUse'),
    ('qrHowToUse', 'How to use:', '使用方法：', 'Cara guna:', 'qrPrintHint'),
    ('qrPrintHint', 'Print this QR and put at cashier / entrance', '打印此二维码并放在收银台/入口', 'Cetak kod QR ini dan letak di kaunter / pintu masuk', 'qrTableHint'),
    ('qrTableHint', 'Use table QR below for ordering', '用下方桌号二维码点餐', 'Gunakan kod QR meja di bawah untuk memesan', 'printShopQRBtn'),
    ('printShopQRBtn', 'Print Shop QR', '打印店铺二维码', 'Cetak Kod QR Kedai', 'tableQrDesc'),
    ('tableQrDesc', 'Each table gets a unique QR code. Customers scan to order directly.', '每张桌有唯一二维码，顾客扫码直接下单。', 'Setiap meja mendapat kod QR unik. Pelanggan imbas untuk memesan terus.', 'referralCommissionRateLabel'),
    ('referralCommissionRateLabel', 'Referral Commission Rate', '推荐佣金率', 'Kadar Komisi Rujukan', 'currentRateLbl'),
    ('currentRateLbl', 'Current rate:', '当前费率：', 'Kadar semasa:', 'noPendingPaymentProofs'),
    ('noPendingPaymentProofs', 'No pending payment proofs', '暂无待处理付款凭证', 'Tiada bukti pembayaran tertunda', 'leaveEmptyBanner'),
    ('leaveEmptyBanner', 'Leave empty to use default banner', '留空使用默认横幅', 'Biarkan kosong untuk guna banner default', 'smallTextHint'),
    ('smallTextHint', 'Small text above the main title (e.g. "Welcome Back")', '主标题上方的小文字（如"欢迎回来"）', 'Teks kecil di atas tajuk utama (cth "Selamat Kembali")', 'bigTitleHint'),
    ('bigTitleHint', 'The big bold title on landing page (e.g. "What\'s your drink today?")', '首页大标题（如"今天想喝什么？"）', 'Tajuk besar di halaman utama (cth "Minuman anda hari ini?")', 'higherShowsFirst'),
    ('higherShowsFirst', 'Higher number = shown first', '数字越大越靠前', 'Nombor lebih besar ditunjukkan dulu', 'kitchenDisplayLbl'),
    ('kitchenDisplayLbl', 'Kitchen Display', '厨房显示', 'Papar Dapur', 'refreshLbl'),
    ('refreshLbl', 'Refresh', '刷新', 'Segar Semula', 'statusNewLbl'),
    ('statusNewLbl', 'New', '新', 'Baharu', 'preparingLbl'),
    ('preparingLbl', 'Preparing', '准备中', 'Menyediakan', 'doneLbl'),
    ('doneLbl', 'Done', '已完成', 'Selesai', 'getNotifiedWhenReady'),
    ('getNotifiedWhenReady', 'Get Notified When Ready!', '准备好了通知我！', 'Dapat Notifikasi Bila Siap!', 'enableNotificationsBtn'),
    ('enableNotificationsBtn', 'Enable Notifications', '启用通知', 'Dayakan Notifikasi', 'maybeLaterBtn'),
    ('maybeLaterBtn', 'Maybe Later', '稍后再说', 'Nanti Saja', 'referralProgramTitle'),
    ('referralProgramTitle', 'Referral Program', '推荐计划', 'Plan Rujukan', 'referralProgramDescText'),
    ('referralProgramDescText', 'Share your phone number as a referral code. When your friend makes their first order, you earn a commission credited to your wallet!', '分享手机号作为推荐码。好友首单后佣金自动入账钱包！', 'Kongsi nombor telefon anda sebagai kod rujukan. Bila rakan membuat pesanan pertama, anda dapat komisi dimasukkan ke dompet!', 'copyReferralBtn'),
    ('copyReferralBtn', 'Copy', '复制', 'Salin', 'commissionHistoryTitle'),
    ('commissionHistoryTitle', 'Commission History', '佣金记录', 'Sejarah Komisi', 'friendsReferredTitle'),
    ('friendsReferredTitle', 'Friends You Referred', '你推荐的好友', 'Rakan Anda Rujuk', 'complaintDetailTitle'),
    ('complaintDetailTitle', 'Complaint Detail', '投诉详情', 'Butiran Aduan', 'markResolvedBtn'),
    ('markResolvedBtn', 'Mark Resolved', '标记为已解决', 'Tanda Sebagai Selesai', 'orderDetailsTitle'),
    ('orderDetailsTitle', 'Order Details', '订单详情', 'Butiran Pesanan', 'loyalbrew_lang'),
]

# 分别为 en/zh/ms 三个语言块添加
for key, en_val, zh_val, ms_val, before in new_keys:
    # EN - 通常已有默认值作为fallback，只需确认
    en_pattern = rf"\b{key}\s*:"
    if not re.search(en_pattern, js):
        # 在 en 块添加
        add_translation('en', key, en_val, before)
    
    # ZH
    zh_old_len = len(js)
    # 在 ms 块前找 zh 的插入点
    add_translation('zh', key, zh_val, before)
    
    # MS  
    add_translation('ms', key, ms_val, before)

print(f'Applied: {count} translations')
if errors:
    print(f'\nIssues ({len(errors)}):')
    for e in errors[:20]:
        print(f'  {e}')
    if len(errors) > 20:
        print(f'  ... and {len(errors)-20} more')

# 保存
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nSaved app.js! Size: {len(js)}')
