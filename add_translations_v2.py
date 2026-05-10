import sys, re
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# 精确定位 LANGS 对象中的语言块
langs_start = js.index('const LANGS = {')

# 找 en: 块
en_match = re.search(r'\ben\s*:\s*\{', js[langs_start:])
en_block_start = langs_start + en_match.end()
# 找到匹配的 }
depth = 1; i = en_block_start
while i < len(js) and depth > 0:
    if js[i] == '{': depth += 1
    elif js[i] == '}': depth -= 1
    i += 1
en_block = js[en_block_start:i-1]
print(f'EN block: {len(en_block)} chars, ends at {i}')

# 找 zh: 块 (在 en 之后)
zh_match = re.search(r'\bzh\s*:\s*\{', js[i:])
zh_block_start = i + zh_match.end()
depth = 1; j2 = zh_block_start
while j2 < len(js) and depth > 0:
    if js[j2] == '{': depth += 1
    elif js[j2] == '}': depth -= 1
    j2 += 1
zh_block = js[zh_block_start:j2-1]
print(f'ZH block: {len(zh_block)} chars, ends at {j2}')

# 找 ms: 块 (在 zh 之后)
ms_match = re.search(r'\bms\s*:\s*\{', js[j2:])
ms_block_start = j2 + ms_match.end()
depth = 1; j3 = ms_block_start
while j3 < len(js) and depth > 0:
    if js[j3] == '{': depth += 1
    elif js[j3] == '}': depth -= 1
    j3 += 1
ms_block = js[ms_block_start:j3-1]
print(f'MS block: {len(ms_block)} chars, ends at {j3}')

# 需要添加的翻译
translations = [
    ('floatViewCart', '查看购物车 →', 'Lihat Troli →'),
    ('tngName', 'Touch & Go', 'Touch & Go'),
    ('bankAmountLabel', '金额：RM0.00', 'Jumlah: RM0.00'),
    ('mLoginHint', '输入商家ID和密码', 'Masukkan ID Peniaga dan kata laluan'),
    ('filterAll', '全部', 'Semua'),
    ('filterPending', '待处理', 'Ditunggu'),
    ('filterPreparing', '准备中', 'Menyediakan'),
    ('filterDone', '已完成', 'Selesai'),
    ('filterAllC', '全部', 'Semua'),
    ('complaintOpenBtn', '待处理', 'Dibuka'),
    ('complaintInProgressBtn', '处理中', 'Sedang Diproses'),
    ('complaintResolvedBtn', '已解决', 'Selesai'),
    ('mPromoPriceLbl', '促销价 (RM)', 'Harga Promo (RM)'),
    ('noActiveNewItems', '没有进行中的新品', 'Tiada item baharu aktif'),
    ('noPastLaunches', '没有历史发布', 'Tiada pelancaran lepas'),
    ('mRulePerOrderOpt', '每次购买=1印章', 'Setiap pembelian = 1 setem'),
    ('mRulePerAmountOpt', '每消费RM X=1印章', 'Setiap RM X dibelanjakan = 1 setem'),
    ('mRulePerItemOpt', '购买指定商品=1印章', 'Beli item tertentu = 1 setem'),
    ('mRewardFreeItemOpt', '免费菜单项目', 'Item Menu Percuma'),
    ('mRewardFlatDiscountOpt', '固定减免(RM)', 'Diskaun Tetap (RM)'),
    ('mRewardBonusPointsOpt', '奖励积分', 'Mata Bonus'),
    ('mFreeItemLabel', '免费商品', 'Item Percuma'),
    ('noStampCardsYet', '还没有印章卡', 'Belum ada kad setem'),
    ('searchForAMember', '搜索会员', 'Cari Ahli'),
    ('noPendingRequests', '暂无待处理请求', 'Tiada permohonan tertunda'),
    ('minAmount', '最低金额(RM)', 'Jumlah Min (RM)'),
    ('expiryDate', '到期日期', 'Tarikh Luput'),
    ('myShopLink', '我的店铺链接', 'Pautan Kedai Saya'),
    ('shopLinkDesc', '分享此链接或二维码给顾客。扫码访问店铺并注册成为会员。', 'Kongsi pautan atau kod QR ini dengan pelanggan. Imbas untuk lawati kedai dan daftar sebagai ahli.'),
    ('copyLinkBtn', '复制', 'Salin'),
    ('shopQRCodeLabel', '店铺二维码', 'Kod QR Kedai'),
    ('qrHowToUse', '使用方法：', 'Cara guna:'),
    ('qrPrintHint', '打印此二维码并放在收银台/入口', 'Cetak kod QR ini dan letak di kaunter / pintu masuk'),
    ('qrTableHint', '用下方桌号二维码点餐', 'Gunakan kod QR meja di bawah untuk memesan'),
    ('printShopQRBtn', '打印店铺二维码', 'Cetak Kod QR Kedai'),
    ('tableQrDesc', '每张桌有唯一二维码，顾客扫码直接下单。', 'Setiap meja mendapat kod QR unik. Pelanggan imbas untuk memesan terus.'),
    ('referralCommissionRateLabel', '推荐佣金率', 'Kadar Komisi Rujukan'),
    ('currentRateLbl', '当前费率：', 'Kadar semasa:'),
    ('noPendingPaymentProofs', '暂无待处理付款凭证', 'Tiada bukti pembayaran tertunda'),
    ('leaveEmptyBanner', '留空使用默认横幅', 'Biarkan kosong untuk guna banner default'),
    ('smallTextHint', '主标题上方的小文字（如"欢迎回来"）', 'Teks kecil di atas tajuk utama (cth "Selamat Kembali")'),
    ('bigTitleHint', '首页大标题（如"今天想喝什么？"）', 'Tajuk besar di halaman utama (cth "Minuman anda hari ini?")'),
    ('higherShowsFirst', '数字越大越靠前', 'Nombor lebih besar ditunjukkan dulu'),
    ('kitchenDisplayLbl', '厨房显示', 'Papar Dapur'),
    ('refreshLbl', '刷新', 'Segar Semula'),
    ('statusNewLbl', '新', 'Baharu'),
    ('preparingLbl', '准备中', 'Menyediakan'),
    ('doneLbl', '已完成', 'Selesai'),
    ('getNotifiedWhenReady', '准备好了通知我！', 'Dapat Notifikasi Bila Siap!'),
    ('enableNotificationsBtn', '启用通知', 'Dayakan Notifikasi'),
    ('maybeLaterBtn', '稍后再说', 'Nanti Saja'),
    ('referralProgramTitle', '推荐计划', 'Plan Rujukan'),
    ('referralProgramDescText', '分享手机号作为推荐码。好友首单后佣金自动入账钱包！', 'Kongsi nombor telefon anda sebagai kod rujukan. Bila rakan membuat pesanan pertama, anda dapat komisi dimasukkan ke dompet!'),
    ('copyReferralBtn', '复制', 'Salin'),
    ('commissionHistoryTitle', '佣金记录', 'Sejarah Komisi'),
    ('friendsReferredTitle', '你推荐的好友', 'Rakan Anda Rujuk'),
    ('complaintDetailTitle', '投诉详情', 'Butiran Aduan'),
    ('markResolvedBtn', '标记为已解决', 'Tanda Sebagai Selesai'),
    ('orderDetailsTitle', '订单详情', 'Butiran Pesanan'),
]

count_zh = 0
count_ms = 0

for key, zh_val, ms_val in translations:
    key_pattern = rf"\b{key}\s*:"
    
    # ZH
    if not re.search(key_pattern, zh_block):
        insert_point = zh_block.rfind('\n}')
        if insert_point > 0:
            zh_block = zh_block[:insert_point] + f"\n    {key}: '{zh_val}'," + zh_block[insert_point:]
            count_zh += 1
    
    # MS
    if not re.search(key_pattern, ms_block):
        insert_point = ms_block.rfind('\n}')
        if insert_point > 0:
            ms_block = ms_block[:insert_point] + f"\n    {key}: '{ms_val}'," + ms_block[insert_point:]
            count_ms += 1

print(f'Added ZH: {count_zh}, MS: {count_ms}')

# 重建文件：保留 en 块不变，替换 zh 和 ms 块
new_js = js[:zh_block_start] + zh_block + '\n}' + js[j2:j2+3] + ms_block + '\n}' + js[j3:]

with open(JS, 'w', encoding='utf-8') as f:
    f.write(new_js)

print(f'Saved app.js! Size: {len(new_js)}')
