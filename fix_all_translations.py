"""
LoyalBrew i18n 全面修复脚本
============================
问题：
1. MS 块翻译值全是英文（应该用马来文）
2. ZH 块缺失 21 个键
3. MS 块缺失 157 个键
4. EN 块部分值被错误写成马来文

修复策略：
- 从 EN 块提取所有键值对
- 为每个键生成正确的 ZH 和 MS 翻译
- 重构 LANGS 对象
"""

import sys, re

sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# ===== 提取三个语言块 =====
langs_start = js.index('const LANGS = {')

# EN block
en_match = re.search(r'\ben\s*:\s*\{', js[langs_start:])
en_block_start = langs_start + en_match.end()
depth = 1; i = en_block_start
while i < len(js) and depth > 0:
    if js[i] == '{': depth += 1
    elif js[i] == '}': depth -= 1
    i += 1
en_raw = js[en_block_start:i-1]
print(f"EN raw: {len(en_raw)} chars")

# ZH block (after en)
zh_match = re.search(r'\bzh\s*:\s*\{', js[i:])
zh_block_start = i + zh_match.end()
depth = 1; j2 = zh_block_start
while j2 < len(js) and depth > 0:
    if js[j2] == '{': depth += 1
    elif js[j2] == '}': depth -= 1
    j2 += 1
zh_raw = js[zh_block_start:j2-1]
print(f"ZH raw: {len(zh_raw)} chars")

# MS block (after zh)
ms_match = re.search(r'\bms\s*:\s*\{', js[j2:])
ms_block_start = j2 + ms_match.end()
depth = 1; j3 = ms_block_start
while j3 < len(js) and depth > 0:
    if js[j3] == '{': depth += 1
    elif js[j3] == '}': depth -= 1
    j3 += 1
ms_raw = js[ms_block_start:j3-1]
print(f"MS raw: {len(ms_raw)} chars")

# ===== 从 EN 块提取所有键值对 =====
def extract_kv(block_text):
    """Extract key:value pairs from a JS object block"""
    pairs = {}
    # Match key: 'value' patterns
    for m in re.finditer(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", block_text):
        key = m.group(1)
        val = m.group(2)
        pairs[key] = val
    return pairs

en_pairs = extract_kv(en_raw)
zh_pairs = extract_kv(zh_raw)
ms_pairs = extract_kv(ms_raw)

print(f"\nEN keys: {len(en_pairs)}, ZH keys: {len(zh_pairs)}, MS keys: {len(ms_pairs)}")

# ===== 定义完整翻译表 =====
# 格式: key -> (zh_value, ms_value)
# 只为缺失或错误的键提供翻译

translations = {
    # === Landing ===
    'tagline': ('下单 · 赚积分 · 领奖励', 'Tempah · Dapat Mata · Terima Ganjaran'),
    'loginLabel': ('会员登录', 'Log Masuk Ahli'),
    'myAccount': ('我的账户', 'Akaun Saya'),
    'orderNow': ('立即点餐', 'Tempah Sekarang'),
    'myStampCard': ('我的印章卡', 'Kad Setem Saya'),
    'topUp': ('充值', 'Isi Semula'),
    'merchant': ('商家', 'Peniaga'),
    'feat1Title': ('扫码点餐', 'Imbas & Tempah'),
    'feat1Desc': ('扫描桌码，秒速下单', 'Imbas kod meja, tempah dalam beberapa saat'),
    'feat2Title': ('赚取积分', 'Dapatkan Mata'),
    'feat2Desc': ('消费 RM1 = 获得 1 积分', 'RM1 dibelanjakan = 1 mata diperoleh'),
    'feat3Title': ('免费饮品', 'Minuman Percuma'),
    'feat3Desc': ('兑换免费饮料', 'Tebus minuman percuma'),

    # === Menu ===
    'menu': ('菜单', 'Menu'),
    'dineIn': ('堂食', 'Makan Di Sini'),
    'takeaway': ('外卖', 'Bawa Pulang'),
    'table': ('桌号', 'Meja'),
    'change': ('找零', 'Baki'),
    'selectTable': ('选择桌号', 'Pilih Meja Anda'),
    'enterTable': ('输入桌号开始点餐', 'Masukkan nombor meja untuk mula tempah'),
    'confirmTable': ('确认桌号', 'Sahkan Meja'),
    'invalidTable': ('请输入有效的桌号', 'Sila masukkan nombor meja yang sah'),
    
    # === Categories ===
    'catAll': ('全部', 'Semua'),
    'catNewItems': ('✨ 新品', '✨ Item Baharu'),
    'catHotDrinks': ('热饮', 'Minuman Panas'),
    'catColdDrinks': ('冷饮', 'Minuman Sejuk'),
    'catFood': ('食物', 'Makanan'),
    'catDesserts': ('甜点', 'Pencuci Mulut'),
    'catSnacks': ('小吃', 'Mudahan'),

    # === Float Cart ===
    'floatViewCart': ('查看购物车 →', 'Lihat Troli →'),
    'floatItem': ('件', 'item'),
    'floatItems': ('件', 'item'),
    
    # === Takeaway ===
    'takeawayOrder': ('外卖订单', 'Pesanan Bawa Pulang'),
    'noPickupTime': ('未设置取餐时间', 'Tiada masa ambil ditetapkan'),
    'pickup': ('自取', 'Ambil Sendiri'),
    
    # === Cart ===
    'yourOrder': ('您的订单', 'Pesanan Anda'),
    'orderType': ('订单类型', 'Jenis Pesanan'),
    'phoneNumber': ('电话号码', 'Nombor Telefon'),
    'pickupTime': ('取餐时间', 'Masa Ambil'),
    'pickupHint': ('我们会在这个时间准备好您的订单。', 'Kami akan sediakan pesanan anda pada masa ini.'),
    'loyaltyPoints': ('积分与印章', 'Mata & Setem'),
    'earnHint': ('输入手机号并点击 🔍 赚取积分和印章', 'Masukkan nombor telefon & tekan 🔍 untuk dapat mata & setem'),
    'phoneLoyalty': ('手机号码（赚取积分和印章）', 'Nombor Telefon (dapat mata & setem)'),
    'payWallet': ('钱包支付', 'Bayar dengan Dompet'),
    'useWallet': ('使用钱包余额支付', 'Gunakan baki dompet untuk bayar'),
    'walletBalance': ('余额', 'Baki'),
    'paymentMethod': ('支付方式', 'Kaedah Pembayaran'),
    'cartEmpty': ('购物车是空的', 'Troli kosong'),
    'browseMenu': ('浏览菜单', 'Lihat Menu'),
    'eachUnit': ('每份', 'setiap'),
    'removeItem': ('移除', 'Buang'),
    'orderSummary': ('订单摘要', 'Ringkasan Pesanan'),
    'subtotal': ('小计', 'Subjumlah'),
    'sst': ('服务税 (6%)', 'SST (6%)'),
    'walletDeduction': ('钱包抵扣', 'Potongan Dompet'),
    'totalLabel': ('总计', 'Jumlah'),
    'pointsEarnLabel': ('将获得积分', 'Mata akan diperoleh'),
    'specialRequest': ('特殊要求', 'Permohonan Khas'),
    'specialRequestPlaceholder': ('例如：少糖、去冰...', 'cth: kurang gula, tiada ais...'),
    'placeOrder': ('下单', 'Tempah'),
    'cartDineIn': ('堂食', 'Makan Di Sini'),
    'cartTakeaway': ('外卖', 'Bawa Pulang'),
    'cartChange': ('找零', 'Baki'),
    
    # === Confirm Details ===
    'confirmType': ('类型', 'Jenis'),
    'confirmTable2': ('桌号', 'Meja'),
    'confirmPhone': ('电话', 'Telefon'),
    'confirmPickup': ('取餐时间', 'Masa Ambil'),
    'confirmItems': ('商品', 'Item'),
    'confirmWalletPaid': ('钱包已付', 'Dompet Dibayar'),
    'confirmTotalPaid': ('实付总额', 'Jumlah Dibayar'),
    'confirmPayment': ('支付', 'Pembayaran'),
    'confirmPointsEarned': ('获得积分', 'Mata Diperoleh'),
    'confirmNote': ('备注', 'Catatan'),
    'pendingVerification': ('待验证', 'Menunggu Pengesahan'),
    'confirmTypeDineIn': ('🪑 堂食', '🪑 Makan Di Sini'),
    'confirmTypeTakeaway': ('🛍️ 外卖', '🛍️ Bawa Pulang'),
    
    # === Cash Pay ===
    'cashPayCounter': ('请到柜台付款，然后点击下方按钮。', 'Sila bayar di kaunter, kemudian tekan butang di bawah.'),
    'cashPaidBtn': ('已付款 — 通知厨房', 'Saya Sudah Bayar — Maklumkan Dapur'),
    'cashPaidDone': ('付款确认！厨房正在准备您的订单。', 'Pembayaran disahkan! Dapur sed menyediakan pesanan anda.'),
    'confirmReceivedBtn': ('确认收货 / 完成订单', 'Sahkan Terima / Lengkapkan Pesanan'),
    'orderCompletedMsg': ('🎉 订单完成！感谢您的惠顾。', '🎉 Pesanan selesai! Terima kasih atas pesanan anda.'),
    'orderCompletedTitle': ('订单已完成', 'Pesanan Selesai'),
    
    # === Toast ===
    'toastTakeaway': ('🛍️ 外卖订单已提交！', '🛍️ Pesanan bawa pulang dihantar!'),
    'toastDineIn': ('🍳 订单已发送至厨房！', '🍳 Pesanan dihantar ke dapur!'),
    'toastNoPhone': ('请输入手机号以使用外卖功能', 'Sila masukkan nombor telefon untuk bawa pulang'),
    'toastNoTime': ('请设置取餐时间', 'Sila tetapkan masa ambil'),
    'toastNoProof': ('请先上传付款截图', 'Sila muat naik tangkapan skrin pembayaran dahulu'),
    
    # === Stamp ===
    'enterPhone': ('输入手机号', 'Masukkan Nombor Telefon'),
    'notMember': ('还不是会员？', 'Bukan ahli lagi?'),
    'registerHere': ('在此注册', 'Daftar di sini'),
    
    # === Order Confirm ===
    'orderPlaced': ('订单已提交！', 'Pesanan Dihantar!'),
    'thankYou': ('谢谢！', 'Terima Kasih!'),
    'orderSent': ('您的订单已发送至厨房。', 'Pesanan anda telah dihantar ke dapur.'),
    'orderMore': ('继续点餐', 'Tempah Lagi'),
    'viewStamp': ('查看印章卡', 'Lihat Kad Setem'),
    'backHome': ('返回首页', 'Kembali ke Utama'),
    
    # === Takeaway Modal ===
    'takeawayModalTitle': ('外卖订单', 'Pesanan Bawa Pulang'),
    'takeawayModalSubtitle': ('输入取餐详情', 'Masukkan butiran ambil sendiri'),
    'confirmTakeaway': ('确认外卖', 'Sahkan Bawa Pulang'),
    'cancelBtn': ('取消', 'Batal'),
    'pickupReadyHint': ('我们会在这个时间准备好您的订单。', 'Kami akan sediakan pesanan anda pada masa ini.'),
    
    # === Payment ===
    'tngScanTitle': ('扫码通过 Touch & Go 支付', 'Imbas untuk Bayar melalui Touch & Go'),
    'bankAmountLabel': ('金额：RM0.00', 'Jumlah: RM0.00'),
    'tngAmountLabel': ('金额', 'Jumlah'),
    'tngName': ('Touch & Go', 'Touch & Go'),
    'tngUploadHint': ('付款后请在下方上传截图。', 'Selepas bayar, sila muat naik tangkapan skrin di bawah.'),
    'uploadScreenshot': ('上传付款截图', 'Muat Naik Tangkapan Skrin Pembayaran'),
    'uploadReceipt': ('上传转账凭证', 'Muat Naik Resit Pemindahan'),
    'uploadSizeHint': ('JPG / PNG 最大5MB', 'JPG / PNG maksimum 5MB'),
    'bankTitle': ('银行转账信息', 'Butiri Pemindahan Bank'),
    
    # === Stamp Card ===
    'stampReward': ('奖励', 'Ganjaran'),
    'stampClaimBtn': ('领取奖励', 'Tebus Ganjaran'),
    'stampPerPurchase': ('每笔购买获得1个印章', 'Setiap pembelian = 1 setem'),
    'stampPerAmount': ('每消费 RM{v} 获得1个印章', 'Setiap RM{v} dibelanjakan = 1 setem'),
    'stampPerItem': ('每购买 {item} 获得1个印章', 'Setiap beli {item} = 1 setem'),
    'stampPerItemGeneric': ('每购买符合条件的商品获得1个印章', 'Setiap item layak = 1 setem'),
    'stampFreeItem': ('免费 {item}', '{item} Percuma'),
    'stampFreeItemGeneric': ('免费商品', 'Item Percuma'),
    'stampRmOff': ('减免 RM{v}', 'RM{v} Off'),
    'stampPctOff': ('折扣 {v}%', '{v}% Off'),
    'stampBonusPoints': ('+{v} 奖励积分', '+{v} Mata Bonus'),
    'stampsToUnlock': ('还需 {n} 个印章解锁奖励', 'Perlu {n} lagu setem untuk buka ganjaran'),
    'stampsToUnlockPlural': ('还需 {n} 个印章解锁奖励', 'Perlu {n} lagi setem untuk buka ganjaran'),
    'stampCollected': ('已收集', 'Dikumpul'),
    'stampEmpty': ('空', 'Kosong'),
    'stampCompleted': ('已完成 {n}×', 'Selesai {n}×'),
    
    # === Customer Auth ===
    'login': ('登录', 'Log Masuk'),
    'register': ('注册', 'Daftar'),
    'fullName': ('全名', 'Nama Penuh'),
    'memberDeactivatedMsg': ('您的账户已被停用。请联系商家。', 'Akaun anda telah dinyahaktifkan. Sila hubungi peniaga.'),
    
    # === Dashboard ===
    'memberLabel': ('会员', 'Ahli'),
    'totalPoints': ('总积分', 'Jumlah Mata'),
    'memberId': ('会员ID', 'ID Ahli'),
    'tierProgress': ('等级进度', 'Kemajuan Tier'),
    'tierBronze': ('青铜\n0', 'Gangsa\n0'),
    'tierSilver': ('白银\n200', 'Perak\n200'),
    'tierGold': ('黄金\n500', 'Emas\n500'),
    'tierPlatinum': ('铂金\n1000', 'Platinum\n1000'),
    'redeemRewards': ('兑换奖励', 'Tebus Ganjaran'),
    'viewAllStampCards': ('查看所有印章卡', 'Lihat Semua Kad Setem'),
    'myOrders': ('我的订单', 'Pesanan Saya'),
    'viewAllOrders': ('查看所有订单', 'Lihat Semua Pesanan'),
    'referralCommissions': ('推荐佣金', 'Komisi Rujukan'),
    'myReferralProgram': ('我的推荐计划', 'Plan Rujukan Saya'),
    'transactionHistory': ('交易记录', 'Sejarah Transaksi'),
    'logout': ('退出登录', 'Log Keluar'),
    'submitComplaint': ('提交投诉', 'Hantar Aduan'),
    
    # === My Orders Page ===
    'loginRequired': ('需要会员登录', 'Log Masuk Ahli Diperlukan'),
    'loginToViewOrders': ('请登录以查看订单历史。', 'Sila log masuk untuk lihat sejarah pesanan.'),
    'goToLogin': ('前往登录', 'Pergi ke Log Masuk'),
    'filterAll': ('全部', 'Semua'),
    'filterPending': ('待处理', 'Ditunggu'),
    'filterPreparing': ('准备中', 'Menyediakan'),
    'filterDone': ('已完成', 'Selesai'),
    'filterAllC': ('全部', 'Semua'),  # customer filter
    
    # === Top Up ===
    'topUpWallet': ('充值钱包', 'Isi Semula Dompet'),
    'myWallet': ('我的钱包', 'Dompet Saya'),
    'bonusIncluded': ('含奖励', 'termasuk bonus'),
    'topUpBonusTitle': ('充值优惠！', 'Bonus Isi Semula!'),
    'topUpBonusDesc': ('充值 RM100 得 RM120 额度（免费送 RM20！）', 'Isi semula RM100 dapat kredit RM120 (PERCUMA RM20!)'),
    'selectTopUpAmount': ('选择充值金额', 'Pilih Jumlah Isi Semula'),
    'topUpGet': ('得', 'Dapat'),
    'noBonus': ('无奖励', 'Tiada bonus'),
    'bestDeal': ('超值', 'TERBAIK'),
    'free': ('免费', 'PERCUMA'),
    'orCustomAmount': ('或输入自定义金额(RM)', 'Atau masukkan jumlah tersendiri (RM)'),
    'topUpCustomHint': ('最低 RM10。RM100 以上有奖励。', 'Minimum RM10. Bonus untuk RM100 dan ke atas.'),
    'youPay': ('您支付', 'Anda Bayar'),
    'youGet': ('您得到', 'Anda Dapat'),
    'bonusLabel': ('奖励', 'Bonus'),
    'confirmTopUp': ('确认充值', 'Sahkan Isi Semula'),
    'walletHistory': ('钱包记录', 'Sejarah Dompet'),
    
    # === Wallet Dashboard ===
    'availableBalance': ('可用余额', 'Baki Tersedia'),
    'totalToppedUp': ('总充值额', 'Jumlah Diisi Semula'),
    'totalBonusEarned': ('总奖励收益', 'Jumlah Bonus Diperoleh'),
    
    # === Tier Hint ===
    'sinceLabel': ('加入于', 'Ahli Sejak'),
    'pointsToReach': ('还需 {n} 点达到 {tier}！', 'Perlu {n} mata lagi untuk capai {tier}!'),
    'highestTier': ('🏆 您已达到最高等级！', '🏆 Anda sudah mencapai tier tertinggi!'),
    'tierNameSilver': ('白银', 'Perak'),
    'tierNameGold': ('黄金', 'Emas'),
    'tierNamePlatinum': ('铂金', 'Platinum'),
    
    # === Upload ===
    'screenshotUploaded': ('截图已上传，待商家验证。', 'Tangkapan skrin dimuat naik. Menunggu pengesahan peniaga.'),
    'screenshotUploaded2': ('截图已上传', 'Tangkapan skrin dimuat naik'),
    'tapToChange': ('点击更换', 'Tekan untuk tukar'),
    
    # === Error Toasts ===
    'selectTableFirst': ('请先选择桌号！', 'Sila pilih meja dahulu!'),
    'photoUnder5MB': ('照片必须小于5MB', 'Foto mesti bawah 5MB'),
    
    # === Promos ===
    'noPromos': ('暂无促销活动', 'Tiada promosi buat masa ini'),
    'noComplaintsYet': ('暂无投诉', 'Belum ada aduan'),
    
    # === Merchant Categories ===
    'mCatHotDrinks': ('热饮', 'Minuman Panas'),
    'mCatColdDrinks': ('冷饮', 'Minuman Sejuk'),
    'mCatFood': ('食物', 'Makanan'),
    'mCatDesserts': ('甜点', 'Pencuci Mulut'),
    'mCatSnacks': ('小吃', 'Mudahan'),
    'mCatPromotions': ('促销', 'Promosi'),
    'mPromoPrice': ('促销价 (RM)', 'Harga Promo (RM)'),
    'mPromoPriceLbl': ('促销价 (RM)', 'Harga Promo (RM)'),
    'mPromoPriceDesc': ('可选 — 用于非高峰时段特惠', 'pilihan — untuk promosi waktu biasa'),
    
    # === Merchant Login ===
    'mLoginBtn': ('登录', 'Log Masuk'),
    'mVerify': ('验证', 'Sahkan'),
    'mRefreshed': ('已刷新', 'Dikemas Kini'),
    'mLoginHint': ('输入商家ID和密码', 'Masukkan ID Peniaga dan kata laluan'),
    'mInvalidCredentials': ('账号或密码错误！', 'Kata laluan salah!'),
    'mMemberActive': ('正常', 'Aktif'),
    'mMemberInactive': ('已停用', 'Dinyahaktif'),
    'mActivateMember': ('激活会员', 'Aktifkan Ahli'),
    'mDeactivateMember': ('停用会员', 'Nyahaktif Ahli'),
    'mActivateBtn': ('激活', 'Aktifkan'),
    'mDeactivateBtn': ('停用', 'Nyahaktif'),
    'mConfirmActivate': ('确认激活此会员？', 'Sahkan aktifkan ahli ini?'),
    'mConfirmDeactivate': ('确认停用此会员？', 'Sahkan nyahaktifkan ahli ini?'),
    
    # === Merchant Orders ===
    'mOrderDone': ('完成', 'Selesai'),
    'mOrderPrepare': ('准备中', 'Menyediakan'),
    'mOrderCompleted': ('已完成', 'Selesai'),
    'mOrderPickup': ('可取餐', 'Siap Diambil'),
    'mOrderTable': ('桌号', 'Meja'),
    'mOrderTakeaway': ('外卖', 'Bawa Pulang'),
    'mOrderMovedPreparing': ('已移至准备中', 'Dipindahkan ke Menyediakan'),
    'mFirstOrderDone': ('首单已完成！', 'Pesanan pertama selesai!'),
    'mNotOrderedYet': ('尚未下单', 'Belum tempah'),
    'mNoOrdersFound': ('未找到订单。', 'Tiada pesanan dijumpai.'),
    'mNoOrdersCategory': ('此分类下无订单。', 'Tiada pesanan dalam kategori ini.'),
    
    # === Merchant Kitchen ===
    'mKitchenStartCooking': ('开始制作', 'Mula Memasak'),
    'mKitchenCookingStarted': ('已开始制作', 'Telah Mula Memasak'),
    'mKitchenMarkDone': ('标记完成', 'Tanda Selesai'),
    'mKitchenCompleted': ('已完成', 'Selesai'),
    'mKitchenOrderCompleted': ('订单完成', 'Pesanan Selesai'),
    'mKitchenGuest': ('顾客', 'Pelanggan'),
    'mKitchenTable': ('桌号', 'Meja'),
    'mKitchenTakeaway': ('外卖', 'Bawa Pulang'),
    'mKitchenPickup': ('自取', 'Ambil Sendiri'),
    
    # === Merchant Members ===
    'mEnterPhone': ('输入手机号', 'Masukkan nombor telefon'),
    'mEnterCardName': ('输入卡名', 'Masukkan nama kad'),
    'mFillNamePrice': ('填写名称和价格', 'Isi nama dan harga'),
    'searchForAMember': ('搜索会员', 'Cari Ahli'),
    'mNoMembersFound': ('未找到会员。', 'Ahli tidak dijumpai.'),
    'mNoMembersYet': ('暂无会员。', 'Belum ada ahli.'),
    
    # === Merchant Stamp Cards ===
    'mStampActivate': ('激活', 'Aktifkan'),
    'mStampActive': ('正常', 'Aktif'),
    'mStampPause': ('暂停', 'Jeda'),
    'mStampPaused': ('已暂停', 'Dijedakan'),
    'mStampDelete': ('删除', 'Padam'),
    'mStampMembers': ('会员数', 'Bilangan Ahli'),
    'mStampPerItem': ('按商品', 'Ikut Item'),
    'mStampPerPurchase': ('按购买', 'Ikut Pembelian'),
    'mStampPerRM': ('按金额', 'Ikut Jumlah'),
    'mStampsLabel': ('印章数', 'Bilangan Setem'),
    'noStampCardsYet': ('还没有印章卡', 'Belum ada kad setem'),
    'mNoStampCardsYet': ('还没有印章卡。', 'Belum ada kad setem.'),
    
    # === Merchant New Items ===
    'mNiLaunch': ('发布', 'Lancarkan'),
    'mNiWas': ('原价', 'Harga Asal'),
    'mNiSpecial': ('特价：', 'Istimewa:'),
    'mNiEnds': ('截止：', 'Tamat:'),
    'mNiNoEndDate': ('无截止日期', 'Tiada tarikh tamat'),
    'mNiDeactivate': ('停用', 'Nyahaktif'),
    'mNiDelete': ('删除', 'Padam'),
    'noActiveNewItems': ('没有进行中的新品', 'Tiada item baharu aktif'),
    'mNoActiveItems': ('没有进行中的新品。', 'Tiada item baharu aktif.'),
    'noPastLaunches': ('没有历史发布', 'Tiada pelancaran lepas'),
    'mNoPastLaunches': ('没有历史发布。', 'Tiada pelancaran lepas.'),
    
    # === Merchant Top-up ===
    'mTopupSubmitted': ('充值请求已提交！', 'Permintaan isi semula dihantar!'),
    'mTopupApproved': ('已批准', 'Diluluskan'),
    'mTopupRejected': ('已拒绝', 'Ditolak'),
    'noPendingRequests': ('暂无待处理请求', 'Tiada permohonan tertunda'),
    'mNoPendingRequests': ('暂无待处理请求。', 'Tiada permohonan tertunda.'),
    'mNoTopupHistory': ('暂无充值记录。', 'Tiada sejarah isi semula.'),
    'mMinTopupAmount': ('最低充值金额为 RM10', 'Minimum isi semula RM10'),
    
    # === Merchant Wallet/Points ===
    'mBalance': ('余额', 'Baki'),
    'mPoints': ('积分', 'Mata'),
    'mNoTransactions': ('暂无交易记录。', 'Tiada transaksi.'),
    
    # === Merchant Bonus Rules ===
    'mAddRule': ('添加规则', 'Tambah Peraturan'),
    'mDeleteRule': ('删除规则', 'Padam Peraturan'),
    'mBonusPercent': ('奖励比例', 'Kadar Bonus'),
    'mBonusPct': ('%', '%'),
    'mBonusPtsLabel': ('奖励积分', 'Mata Bonus'),
    'mBonusExpiry': ('有效期', 'Tempoh Sah'),
    'mNoExpiry': ('永久有效', 'Tiada Luput'),
    'mMinAmt': ('最低金额(RM)', 'Jumlah Min (RM)'),
    'mEnterValidBill': ('请输入有效金额', 'Sila masukkan jumlah sah'),
    'mEnterValidRate': ('请输入有效费率(1-100)', 'Sila masukkan kadar sah (1-100)'),
    
    # === Merchant Reward Types ===
    'mRewardFreeItem': ('免费商品', 'Item Percuma'),
    'mRewardFlatDiscount': ('固定减免(RM)', 'Diskaun Tetap (RM)'),
    'mRewardPctDiscount': ('百分比折扣(%)', 'Diskaun Peratusan (%)'),
    'mRewardBonusPoints': ('奖励积分', 'Mata Bonus'),
    'mPurchase': ('购买', 'Pembelian'),
    'mRmOff': ('减免RM', 'RM Off'),
    'mPctOff': ('折扣%', '% Off'),
    'mFreePrefix': ('免费', 'PERCUMA'),
    'mFreeItem': ('免费商品', 'Item Percuma'),
    'mFreeCoffee': ('免费咖啡', 'Kopi Percuma'),
    
    # === Merchant Complaints ===
    'mComplaintOpen': ('待处理', 'Dibuka'),
    'mComplaintInProgress': ('处理中', 'Sedang Diproses'),
    'mComplaintResolved': ('已解决', 'Selesai'),
    'mComplaintNoPhoto': ('无照片', 'Tiada Foto'),
    'mApprove': ('通过', 'Luluskan'),
    'mReject': ('拒绝', 'Tolak'),
    'mNoComplaintsFound': ('未找到投诉。', 'Tiada aduan dijumpai.'),
    
    # === Merchant Commissions ===
    'mNoCommissions': ('未找到佣金记录。', 'Tiada rekod komisi dijumpai.'),
    
    # === Merchant Payment Proof ===
    'mPaymentVerified': ('已验证', 'Disahkan'),
    'mPaymentRejected': ('已拒绝', 'Ditolak'),
    'mNoPaymentProofs': ('未找到付款凭证。', 'Tiada bukti pembayaran dijumpai.'),
    'mPhotoUnder5MB': ('照片必须小于5MB', 'Foto mesti bawah 5MB'),
    
    # === Merchant QR ===
    'mQRNotReady': ('二维码未就绪', 'QR Belum Bersedia'),
    'mQRPrint': ('打印二维码', 'Cetak Kod QR'),
    'mQRTable': ('桌码二维码', 'Kod QR Meja'),
    
    # === Merchant Menu ===
    'mSelectMenuItem': ('选择菜单项', 'Pilih Item Menu'),
    'mChooseAnItem': ('选择一个商品', 'Pilih Satu Item'),
    'mExpired': ('已过期', 'Luput'),
    
    # === Merchant Detail View ===
    'mDetailStatus': ('状态', 'Status'),
    'mDetailDate': ('日期', 'Tarikh'),
    'mDetailCustomer': ('顾客', 'Pelanggan'),
    'mDetailOrder': ('订单', 'Pesanan'),
    'mDetailCategory': ('分类', 'Kategori'),
    'mDetailPrevResponse': ('上次回复', 'Respons Sebelumnya'),
    
    # === Other Keys ===
    'points': ('积分', 'Mata'),
    'noStampCards': ('无印章卡', 'Tiada Kad Setem'),
    'expiryDate': ('到期日期', 'Tarikh Luput'),
    'bankAccountDisplay': ('银行账户', 'Akaun Bank'),
    'commission_rate': ('推荐佣金率', 'Kadar Komisi Rujukan'),
    'credited_to_referrer_s_wallet_after_first_order': ('首单完成后自动入账推荐人钱包', 'Auto masuk dompet rujukan selepas pesanan pertama'),
    'customer_complaints': ('顾客投诉', 'Aduan Pelanggan'),
    'enter_your_referrer_s_phone_number_to_link_commissions': ('输入推荐人手机号以关联佣金', 'Masukkan nombor telefon rujukan untuk hubung komisi'),
    'friends_referred': ('你推荐的好友', 'Rakan Anda Rujuk'),
    'generate_qr_codes': ('生成二维码', 'Jana Kod QR'),
    'generate_table_qr_codes': ('生成桌码二维码', 'Jana Kod QR Meja'),
    'in_progress': ('进行中', 'Sedang Berjalan'),
    'kitchen_display': ('厨房显示', 'Papar Dapur'),
    'member_stamp_progress': ('印章进度', 'Kemajuan Setem'),
    'member_wallet_balances': ('钱包余额', 'Baki Dompet'),
    'merchantNameDisplay': ('商家名称', 'Nama Peniaga'),
    'new': ('新', 'Baharu'),
    'no_friends_referred_yet': ('暂无推荐好友', 'Belum ada rakan dirujuk'),
    'no_pending_payment_proofs': ('暂无待处理付款凭证', 'Tiada bukti pembayaran tertunda'),
    'number_of_tables': ('桌数', 'Bilangan Meja'),
    'pending_payment_proofs': ('待处理付款凭证', 'Bukti Pembayaran Tertunda'),
    'pending_top_up_requests': ('待处理充值请求', 'Permintaan Isi Semula Tertunda'),
    'refresh': ('刷新', 'Segar Semula'),
    'resolved': ('已解决', 'Selesai'),
    'search_for_a_member': ('搜索会员', 'Cari Ahli'),
    'top_up_bonus_settings': ('充值奖励设置', 'Tetapan Bonus Isi Semula'),
    'top_up_history': ('充值记录', 'Sejarah Isi Semula'),
    'total_earned': ('总收入', 'Jumlah Diperoleh'),
    'will_earn': ('将获得', 'Akan Dapat'),
    'selectMenuItem': ('请选择菜单项', 'Sila pilih item menu'),
    'enterPhoneNumber': ('请输入手机号', 'Sila masukkan nombor telefon'),
    'memberNotFound': ('未找到会员，请先注册。', 'Ahli tidak dijumpai. Sila daftar dahulu.'),
    'noUnclaimedRewards': ('无可领取奖励', 'Tiada ganjaran belum ditebus'),
    'enterCardName': ('请输入卡名', 'Sila masukkan nama kad'),
    'enterRewardValue': ('请输入奖励值', 'Sila masukkan nilai ganjaran'),
    'minimumTopup': ('最低充值 RM10', 'Minimum isi semula RM10'),
    'selectTopupAmount': ('请选择充值金额', 'Sila pilih jumlah isi semula'),
    'sessionExpired': ('会话已过期，请重新输入手机号', 'Sesi tamat, sila masukkan semula nombor telefon'),
    'memberNotFoundShort': ('未找到会员', 'Ahli tidak dijumpai'),
    'pleaseLoginFirst': ('请先登录会员', 'Sila log masuk ahli dahulu'),
    'pleaseDescribeIssue': ('请描述您的问题', 'Sila terangkan masalah anda'),
    'enterPhoneToLogin': ('请输入手机号登录', 'Sila masukkan nombor telefon untuk log masuk'),
    'memberNotFoundExcl': ('未找到会员！', 'Ahli tidak dijumpai!'),
    'enterValidBill': ('请输入有效金额', 'Sila masukkan jumlah sah'),
    'fillNamePrice': ('填写名称和价格', 'Isi nama dan harga'),
    'qrNotReady': ('二维码尚未就绪', 'QR belum bersedia'),
    'complaintSubmitted': ('✅ 投诉已提交！我们会尽快回复您。', '✅ Aduan dihantar! Kami akan balas anda secepat mungkin.'),
    'submitComplaint': ('提交投诉', 'Hantar Aduan'),
    'submitComplaintBtn': ('提交投诉', 'Hantar Aduan'),
    'newComplaint': ('新投诉', 'Aduan Baharu'),
    'complaintCategory': ('投诉分类', 'Kategori Aduan'),
    'food_quality': ('食品质量', 'Kualiti Makanan'),
    'other': ('其他', 'Lain-lain'),
    'pricing_issue': ('价格问题', 'Isu Harga'),
    'waiting_time': ('等待时间', 'Masa Menunggu'),
    'wrong_order': ('订单错误', 'Pesanan Salah'),
    'service': ('服务', 'Perkhidmatan'),
    'cleanliness': ('卫生', 'Kebersihan'),
    'description': ('描述', 'Penerangan'),
    'uploadPhotoOptional': ('上传照片(可选)', 'Muat Naik Foto (pilihan)'),
    'tap_to_upload_photo': ('点击上传照片', 'Tekan untuk muat naik foto'),
    'photo_upload_hint': ('JPG/PNG 最大5MB', 'JPG/PNG maksimum 5MB'),
    'order_id_optional': ('订单号(可选)', 'ID Pesanan (pilihan)'),
    'myComplaints': ('我的投诉', 'Aduan Saya'),
    'stampCollectedMsg': ('印章已收集！', 'Setem dikumpulkan!'),
    'stampCollectedDetail': ('查看印章卡领取奖励', 'Lihat kad setem untuk tebus ganjaran'),
    'walletTopupPending': ('等待商家审批', 'Menunggu kelulusan peniaga'),
    'myOrdersEmpty': ('未找到订单', 'Tiada pesanan dijumpai'),
    'myOrdersNoOrdersYet': ('暂无订单', 'Belum ada pesanan'),
    'walletTxnsEmpty': ('暂无钱包交易', 'Tiada transaksi dompet'),
    'txnNoTransactions': ('暂无交易', 'Tiada transaksi'),
    'topupHistoryEmpty': ('暂无充值记录', 'Tiada sejarah isi semula'),
    'complaintsEmpty': ('暂无投诉', 'Tiada aduan'),
    'photoUploadHint': ('JPG/PNG 最大5MB', 'JPG/PNG maksimum 5MB'),
    'orderDetailTitle': ('订单详情', 'Butiran Pesanan'),
    'orderDetailOrderId': ('订单号', 'ID Pesanan'),
    'orderDetailStatus': ('状态', 'Status'),
    'orderDetailType': ('类型', 'Jenis'),
    'orderDetailDate': ('日期', 'Tarikh'),
    'orderDetailItems': ('订购商品', 'Item Dipesan'),
    'orderDetailSubtotal': ('小计', 'Subjumlah'),
    'orderDetailTax': ('服务税', 'SST'),
    'walletTopupLabel': ('充值', 'Isi Semula'),
    'paymentCash': ('现金', 'Tunai'),
    'paymentTng': ('Touch & Go', 'Touch & Go'),
    'paymentBank': ('银行转账', 'Pemindahan Bank'),
    'statusPending': ('待处理', 'Ditunggu'),
    'statusPreparing': ('准备中', 'Menyediakan'),
    'statusDone': ('已完成', 'Selesai'),
    'stampRedeemTitle': ('恭喜！', 'Tahniah!'),
    'stampRedeemMsg': ('您已集齐所有印章！', 'Anda telah mengumpul semua setem!'),
    'stampRedeemClaim': ('领取奖励', 'Tebus Ganjaran'),
    'stampRedeemLater': ('稍后再说', 'Nanti Saja'),
    'newItemsTitle': ('LoyalBrew 新品推荐！', 'Item Baharu di LoyalBrew!'),
    'newItemsMsg': ('新鲜上市，专为您定制 🎉', 'Pelancaran baharu khas untuk anda 🎉'),
    'newItemsOrderNow': ('立即点餐', 'Tempah Sekarang'),
    'newItemsClose': ('关闭', 'Tutup'),
    'referralReferral': ('推荐计划', 'Plan Rujukan'),
    'referralInviteFriends': ('邀请好友，赚佣金！', 'Jemput Rakan, Dapat Komisi!'),
    'referralShareCode': ('分享您的手机号作为推荐码。好友首单后佣金自动入账钱包！', 'Kongsi nombor telefon anda sebagai kod rujukan. Bila rakan membuat pesanan pertama, anda dapat komisi dimasukkan ke dompet!'),
    'referralCopyCode': ('复制', 'Salin'),
    'referralFriendsReferred': ('你推荐的好友', 'Rakan Anda Rujuk'),
    'referralTotalEarned': ('总收入', 'Jumlah Diperoleh'),
    'referralCommissionRate': ('推荐佣金率', 'Kadar Komisi Rujukan'),
    'referralCommissionHistory': ('佣金记录', 'Sejarah Komisi'),
    'referralFriendsYouReferred': ('你推荐的好友', 'Rakan Anda Rujuk'),
    'referralNoCommissions': ('暂无佣金记录。开始推荐吧！', 'Tiada rekod komisi. Mula rujuk sekarang!'),
    'referralNoFriends': ('暂无推荐好友。', 'Belum ada rakan dirujuk.'),
    'complaintSubmitComplaint': ('提交投诉', 'Hantar Aduan'),
    'complaintCategory': ('投诉分类', 'Kategori Aduan'),
    'complaintDescription': ('描述', 'Penerangan'),
    'complaintUploadPhoto': ('上传照片(可选)', 'Muat Naik Foto (pilihan)'),
    'complaintTapUpload': ('点击上传照片', 'Tekan untuk muat naik foto'),
    'complaintOrderIdOpt': ('订单号(可选)', 'ID Pesanan (pilihan)'),
    'complaintSubmit': ('提交投诉', 'Hantar Aduan'),
    'complaintMyComplaints': ('我的投诉', 'Aduan Saya'),
    'complaintComplaintDetail': ('投诉详情', 'Butiran Aduan'),
    'complaintResponse': ('回复/处理措施', 'Respons / Tindakan'),
    'complaintResolve': ('标记已解决', 'Tanda Sebagai Selesai'),
    'complaintClose': ('关闭', 'Tutup'),
    'complaintNoPhoto': ('已附照片', 'Foto Dilampirkan'),
    'complaintResolveDone': ('✅ 投诉已标记为已解决', '✅ Aduan ditandakan sebagai selesai'),
    'friendsReferredTitle': ('你推荐的好友', 'Rakan Anda Rujuk'),
    'complaintDetailTitle': ('投诉详情', 'Butiran Aduan'),
    'complaintEnterResponse': ('请输入回复...', 'Masukkan respons anda...'),
    'newItemsBanner': ('NEW', 'BARU'),
    'newItemsSpecial': ('特价：', 'Istimewa:'),
    'newItemsWas': ('原价', 'Harga Asal'),
    'newItemsUntil': ('截止：', 'Tamat:'),
    'newItemsNoEnd': ('无截止日期', 'Tiada Tarikh Tamat'),
    'complaintPhotoAlt': ('照片', 'Foto'),
    'awaitingMerchantApproval': ('等待商家审批', 'Menunggu Kelulusan Peniaga'),
    'newItemsNewTag': ('NEW', 'BARU'),
    'stampComplete': ('✅ 完成！', '✅ SELESAI!'),
    'complaintTab': ('投诉', 'Aduan'),
    'referralTab': ('推荐', 'Rujukan'),
    'orderDetailTotal': ('总计', 'Jumlah'),
    'orderDetailPointsEarned': ('获得积分', 'Mata Diperoleh'),
    'orderDetailWalletPaid': ('钱包', 'Dompet'),
    'orderDetailWalletDeductLabel': ('钱包抵扣', 'Potongan Dompet'),
    'referralCommissionEarned': ('已获佣金', 'Komisi Diperoleh'),
    'referralCurrentRate': ('当前费率：', 'Kadar Semasa:'),
    'referralSharePrompt': ('分享手机号 {phone} 作为推荐码，从好友首单赚取 {rate}% 佣金！', 'Kongsi nombor {phone} sebagai kod rujukan, dapat {rate}% dari pesanan pertama rakan!'),
    
    # === Ads ===
    'ads': ('广告', 'Iklan'),
    'create_ad': ('创建广告', 'Cipta Iklan Baru'),
    'ad_title': ('广告标题', 'Tajuk Iklan'),
    'ad_link': ('链接URL(可选)', 'URL Pautan (pilihan)'),
    'start_date': ('开始日期', 'Tarikh Mula'),
    'end_date': ('结束日期', 'Tarikh Tamat'),
    'ad_image': ('广告图片', 'Gambar Iklan'),
    'click_to_upload_ad_image': ('点击上传广告图片', 'Klik untuk muat naik gambar iklan'),
    'ad_position': ('展示位置', 'Posisi Paparan'),
    'ad_priority': ('优先级', 'Keutamaan'),
    'higher_shows_first': ('数字越大越靠前', 'Nombor lebih besar ditunjukkan dulu'),
    'active_ads': ('活跃广告', 'Iklan Aktif'),
    'no_active_ads': ('暂无活跃广告', 'Tiada iklan aktif'),
    'all_ads': ('全部广告', 'Semua Iklan'),
    'no_ads_yet': ('暂无广告', 'Belum ada iklan'),
    'ad_statistics': ('广告统计', 'Statistik Iklan'),
    'landing_page_top': ('首页顶部', 'Bahagian Atas Halaman Utama'),
    'promosAndDeals': ('促销与优惠', 'Promosi & Tawaran'),
    'viewAllPromos': ('查看所有促销', 'Lihat Semua Promosi'),
    'allPromos': ('全部促销', 'Semua Promosi'),
    'noPromosNow': ('暂无促销活动，敬请期待！', 'Tiada promosi buat masa ini. Sila semak kemudian!'),
    
    # === Shop Settings ===
    'welcomeBack': ('欢迎回来', 'Selamat Kembali'),
    'drinkToday': ('今天想喝什么？', 'Minuman anda hari ini?'),
    'firebaseNote': ('主按钮将连接 Firebase：检查商家额度，成功后自动扣减1。', 'Butang utama akan sambung ke Firebase: semak kredit peniaga, tolak 1 secara auto bila berjaya.'),
    'enter': ('输入', 'Masukkan'),
    'get': ('获取', 'Dapatkan'),
    'view': ('查看', 'Lihat'),
    'back': ('返回', 'Kembali'),
    'superAdmin': ('超管', 'Admin Super'),
    'quickActions': ('快捷操作', 'Tindakan Pantas'),
    'viewOrders2': ('查看订单', 'Lihat Pesanan'),
    'menuMgmt2': ('菜单管理', 'Urusan Menu'),
    'shopSettings2': ('店铺设置', 'Tetapan Kedai'),
    'kitchenDisplay2': ('厨房显示', 'Papar Dapur'),
    'confirmPoints': ('确认积分', 'Sahkan Mata'),
    'topUpGateway': ('充值(支付网关)', 'Isi Semula (Gateway Pembayaran)'),
    'shopInfo': ('店铺信息', 'Maklumat Kedai'),
    'shopName': ('店铺名称', 'Nama Kedai'),
    'announcement': ('公告', 'Pengumuman'),
    'bannerUrl': ('横幅图片URL', 'URL Gambar Banner'),
    'saveShop': ('保存店铺信息', 'Simpan Maklumat Kedai'),
    'pointsSettings': ('积分设置', 'Tetapan Mata'),
    'pointsPerRM': ('每RM积分', 'Mata per RM'),
    'savePoints2': ('保存积分设置', 'Simpan Tetapan Mata'),
    
    # === Settings Hints ===
    'leaveEmptyBanner': ('留空使用默认横幅', 'Biarkan kosong untuk guna banner default'),
    'smallTextHint': ('主标题上方的小文字（如"欢迎回来"）', 'Teks kecil di atas tajuk utama (cth "Selamat Kembali")'),
    'bigTitleHint': ('首页大标题（如"今天想喝什么？"）', 'Tajuk besar di halaman utama (cth "Minuman anda hari ini?")'),
    'higherShowsFirst': ('数字越大越靠前', 'Nombor lebih besar ditunjukkan dulu'),
    'kitchenDisplayLbl': ('厨房显示', 'Papar Dapur'),
    'refreshLbl': ('刷新', 'Segar Semula'),
    'statusNewLbl': ('新', 'Baharu'),
    'preparingLbl': ('准备中', 'Menyediakan'),
    'doneLbl': ('已完成', 'Selesai'),
    'getNotifiedWhenReady': ('准备好了通知我！', 'Dapat Notifikasi Bila Siap!'),
    'enableNotificationsBtn': ('启用通知', 'Dayakan Notifikasi'),
    'maybeLaterBtn': ('稍后再说', 'Nanti Saja'),
    'referralProgramTitle': ('推荐计划', 'Plan Rujukan'),
    'referralProgramDescText': ('分享手机号作为推荐码。好友首单后佣金自动入账钱包！', 'Kongsi nombor telefon anda sebagai kod rujukan. Bila rakan membuat pesanan pertama, anda dapat komisi dimasukkan ke dompet!'),
    'copyReferralBtn': ('复制', 'Salin'),
    'commissionHistoryTitle': ('佣金记录', 'Sejarah Komisi'),
    'markResolvedBtn': ('标记为已解决', 'Tanda Sebagai Selesai'),
    'orderDetailsTitle': ('订单详情', 'Butiran Pesanan'),
    'myShopLink': ('我的店铺链接', 'Pautan Kedai Saya'),
    'shopLinkDesc': ('分享此链接或二维码给顾客。扫码访问店铺并注册成为会员。', 'Kongsi pautan atau kod QR ini dengan pelanggan. Imbas untuk lawati kedai dan daftar sebagai ahli.'),
    'copyLinkBtn': ('复制', 'Salin'),
    'shopQRCodeLabel': ('店铺二维码', 'Kod QR Kedai'),
    'qrHowToUse': ('使用方法：', 'Cara guna:'),
    'qrPrintHint': ('打印此二维码并放在收银台/入口', 'Cetak kod QR ini dan letak di kaunter / pintu masuk'),
    'qrTableHint': ('用下方桌号二维码点餐', 'Gunakan kod QR meja di bawah untuk memesan'),
    'printShopQRBtn': ('打印店铺二维码', 'Cetak Kod QR Kedai'),
    'tableQrDesc': ('每张桌有唯一二维码，顾客扫码直接下单。', 'Setiap meja mendapat kod QR unik. Pelanggan imbas untuk memesan terus.'),
    'referralCommissionRateLabel': ('推荐佣金率', 'Kadar Komisi Rujukan'),
    'currentRateLbl': ('当前费率：', 'Kadar semasa:'),
    'noPendingPaymentProofs': ('暂无待处理付款凭证', 'Tiada bukti pembayaran tertunda'),
    'recommendedSize': ('建议尺寸：750×300px', 'Cadangan saiz: 750×300px'),
    'optional': ('可选', 'pilihan'),
    'required': ('必填', 'wajib'),
}

# ===== 构建新的 ZH 和 MS 块 =====
def build_block(pairs_dict, existing_block):
    """Build a new language block from translations dict, preserving structure"""
    lines = []
    added_keys = set()
    
    # First, go through existing block line by line to preserve order/comments
    for line in existing_block.split('\n'):
        stripped = line.strip()
        # Check if this line has a key:value pair
        m = re.match(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", stripped)
        if m:
            key = m.group(1)
            if key in translations:
                zh_val, ms_val = translations[key]
                # We're building specific language block - use correct value
                # This function is generic, caller decides which value
                added_keys.add(key)
            lines.append(line)
        else:
            lines.append(line)
    
    return '\n'.join(lines), added_keys

# Build new ZH block
zh_new_lines = []
zh_added = set()
for line in zh_raw.split('\n'):
    stripped = line.strip()
    m = re.match(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", stripped)
    if m:
        key = m.group(1)
        if key in translations:
            zh_val, ms_val = translations[key]
            # Replace with Chinese translation
            indent = len(line) - len(line.lstrip())
            zh_new_lines.append(' ' * indent + f"{key}: '{zh_val}',")
            zh_added.add(key)
        else:
            zh_new_lines.append(line)
    else:
        zh_new_lines.append(line)

# Add missing ZH keys at the end of ZH block
missing_zh = [k for k in translations if k not in zh_added]
if missing_zh:
    # Find last } position to insert before it
    insert_line = None
    for idx, line in enumerate(zh_new_lines):
        if line.strip() == '}':
            insert_line = idx
            break
    if insert_line:
        for key in missing_zh:
            zh_val, ms_val = translations[key]
            zh_new_lines.insert(insert_line, f"    {key}: '{zh_val}',")
        zh_added.update(missing_zh)

zh_new_block = '\n'.join(zh_new_lines)

# Build new MS block  
ms_new_lines = []
ms_added = set()
for line in ms_raw.split('\n'):
    stripped = line.strip()
    m = re.match(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", stripped)
    if m:
        key = m.group(1)
        if key in translations:
            zh_val, ms_val = translations[key]
            # Replace with Malay translation
            indent = len(line) - len(line.lstrip())
            ms_new_lines.append(' ' * indent + f"{key}: '{ms_val}',")
            ms_added.add(key)
        else:
            ms_new_lines.append(line)
    else:
        ms_new_lines.append(line)

# Add missing MS keys
missing_ms = [k for k in translations if k not in ms_added]
if missing_ms:
    insert_line = None
    for idx, line in enumerate(ms_new_lines):
        if line.strip() == '}':
            insert_line = idx
            break
    if insert_line:
        for key in missing_ms:
            zh_val, ms_val = translations[key]
            ms_new_lines.insert(insert_line, f"    {key}: '{ms_val}',")
        ms_added.update(missing_ms)

ms_new_block = '\n'.join(ms_new_lines)

# Also fix EN block - replace wrong Malay values with English
en_new_lines = []
for line in en_raw.split('\n'):
    stripped = line.strip()
    m = re.match(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", stripped)
    if m:
        key = m.group(1)
        current_val = m.group(2)
        # If this key has a translation, check if EN value was corrupted
        if key in translations:
            zh_val, ms_val = translations[key]
            # Get original English from our knowledge or keep current
            # The EN values should be English - let's check if current looks like Malay
            malay_indicators = ['setem', 'pesanan', 'item', 'menu', 'kad', 'dompet', 
                               'tempah', 'sila', 'anda', 'kami', 'untuk', 'dengan',
                               'pembelian', 'peniaga', 'ahli', 'mula', 'sekarang']
            is_malay = any(ind in current_val.lower() for ind in malay_indicators)
            if is_malay and key in en_pairs:
                # Restore from original en_pairs which should have English
                orig_en = en_pairs.get(key, current_val)
                indent = len(line) - len(line.lstrip())
                en_new_lines.append(' ' * indent + f"{key}: '{orig_en}',")
                continue
        en_new_lines.append(line)
    else:
        en_new_lines.append(line)

en_new_block = '\n'.join(en_new_lines)

print(f"\n=== Results ===")
print(f"ZH: {len(zh_added)} keys translated ({len(missing_zh)} added)")
print(f"MS: {len(ms_added)} keys translated ({len(missing_ms)} added)")

# Rebuild the file precisely
# We know exact positions:
#   en_block_start to i-1 = en block content (without { })
#   zh_block_start to j2-1 = zh block content
#   ms_block_start to j3-1 = ms block content
#
# Structure is: const LANGS = { en: {...}, zh: {...}, ms: {...} }
# We need to replace the content inside each language's { }

# Find the exact text markers
en_marker_end = i  # position after en's closing }
zh_colon_pos = js.index('zh:', en_marker_end)  # zh: position
zh_open_brace = js.index('{', zh_colon_pos) + 1  # after zh: {
ms_colon_pos = js.index('ms:', j2)  # ms: position  
ms_open_brace = js.index('{', ms_colon_pos) + 1  # after ms: {
ms_close_brace = j3  # position of ms's closing }

new_js = (
    js[:en_block_start] +  # before en content
    en_new_block +  # new en content
    '\n}' +
    js[en_marker_end:zh_open_brace] +  # ', zh: {' 
    zh_new_block +  # new zh content
    '\n}' +
    js[j2:ms_open_brace] +  # ', ms: {'
    ms_new_block +  # new ms content
    '\n}' +
    js[ms_close_brace:]  # after ms's closing }
)

with open(JS, 'w', encoding='utf-8') as f:
    f.write(new_js)

print(f"\nSaved app.js! New size: {len(new_js)} bytes (was {len(js)})")
