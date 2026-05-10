"""
LoyalBrew i18n 最终修复 v4
===========================
策略：
1. 从 HTML 的 data-i18n 属性提取所有需要的键
2. 从 EN 块获取英文原文作为 fallback
3. 为每个缺失的 ZH/MS 键生成翻译
4. 精确替换 ZH 和 MS 块
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# ===== 1. 从 HTML 提取所有需要的键 =====
HTML = r'C:\Users\Administrator\CodeBuddy\20260416214625\index.html'
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()

html_keys = set(re.findall(r'data-i18n="([^"]+)"', html))
print(f"HTML has {len(html_keys)} unique i18n keys")

# Also check app.js for t() calls to find dynamically used keys
js_t_keys = set(re.findall(r"\bt\('([^']+)'\)", js))
print(f"app.js t() calls use {len(js_t_keys)} unique keys")

all_needed = html_keys | js_t_keys
print(f"Total unique keys needed: {len(all_needed)}")

# ===== 2. 精确定位 LANGS 块 =====
langs_start = js.index('const LANGS = {')

en_m = re.search(r'\ben\s*:\s*\{', js[langs_start:])
eo = langs_start + en_m.end()
depth = 1; p = eo
while depth > 0:
    if js[p] == '{': depth += 1
    elif js[p] == '}': depth -= 1
    p += 1

zh_m = re.search(r'\bzh\s*:\s*\{', js[p:])
zo = p + zh_m.end()
depth = 1; z2 = zo
while depth > 0:
    if js[z2] == '{': depth += 1
    elif js[z2] == '}': depth -= 1
    z2 += 1

ms_m = re.search(r'\bms\s*:\s*\{', js[z2:])
mo = z2 + ms_m.end()
depth = 1; m2 = mo
while depth > 0:
    if js[m2] == '{': depth += 1
    elif js[m2] == '}': depth -= 1
    m2 += 1

zh_block = js[zo:z2-1]
ms_block = js[mo:m2-1]
en_block = js[eo:p-1]

def extract_kv(block):
    pairs = {}
    for m in re.finditer(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", block):
        pairs[m.group(1)] = m.group(2)
    return pairs

en_kv = extract_kv(en_block)
zh_kv = extract_kv(zh_block)
ms_kv = extract_kv(ms_block)

print(f"\nEN keys: {len(en_kv)}, ZH keys: {len(zh_kv)}, MS keys: {len(ms_kv)}")

missing_zh = all_needed - set(zh_kv.keys())
missing_ms = all_needed - set(ms_kv.keys())
print(f"Missing in ZH: {len(missing_zh)}")
print(f"Missing in MS: {len(missing_ms)}")

# ===== 3. 完整翻译表（只包含缺失的键）=====
T = {
    # === 顾客端 ===
    'filterAll': ('全部', 'Semua'),
    'filterAllC': ('全部', 'Semua'),
    'filterPending': ('待处理', 'Ditunggu'),
    'filterPreparing': ('准备中', 'Menyediakan'),
    'filterDone': ('已完成', 'Selesai'),
    'placeOrder': ('下单', 'Tempah'),
    'myAccount': ('我的账户', 'Akaun Saya'),
    'stampCard': ('印章卡', 'Kad Setem'),
    'stamp_rule': ('印章规则', 'Peraturan Setem'),
    'reward_type': ('奖励类型', 'Jenis Ganjaran'),
    'everyPurchase1Stamp': ('每笔购买=1印章', 'Setiap pembelian = 1 setem'),
    'freeMenuItem': ('免费菜单项目', 'Item Menu Percuma'),
    'redeemReward': ('兑换奖励', 'Tebus Ganjaran'),
    'login_to_dashboard': ('登录后台', 'Log Masuk ke Papan Pemuka'),
    'merchant_login': ('商家登录', 'Log Masuk Peniaga'),
    'new_items': ('新品', 'Item Baharu'),
    'whats_new_title': ('新品推荐', 'Item Baharu'),
    'stamp_cards': ('印章卡', 'Kad Setem'),
    'orders': ('订单', 'Pesanan'),
    'orders_today': ('今日订单', 'Pesanan Hari Ini'),
    'commissions': ('佣金', 'Komisen'),
    'complaints': ('投诉', 'Aduan'),
    'members': ('会员', 'Ahli'),
    'settings': ('设置', 'Tetapan'),
    'overview': ('概览', 'Ringkasan'),
    'kitchen': ('厨房', 'Dapur'),
    'admin': ('管理', 'Urusan'),
    'top_up': ('充值', 'Isi Semula'),
    'qr_codes': ('二维码', 'Kod QR'),
    'menu_items': ('菜单项', 'Item Menu'),
    'points_issued': ('已发积分', 'Mata Diberikan'),
    'revenue_today': ('今日营收', 'Hasil Hari Ini'),
    'recent_transactions': ('最近交易', 'Transaksi Terkini'),
    'create_account': ('创建账户', 'Cipta Akaun'),
    'password': ('密码', 'Kata Laluan'),
    'username': ('用户名', 'Nama Pengguna'),
    'save_password': ('保存密码', 'Simpan Kata Laluan'),
    'demo_label': ('演示', 'Demo'),
    'category': ('分类', 'Kategori'),
    'item_name': ('商品名称', 'Nama Item'),
    'item_photo': ('商品图片', 'Foto Item'),
    'price_label': ('价格(RM)', 'Harga (RM)'),
    'emoji_icon': ('表情图标', 'Ikon Emoji'),
    'remove_photo': ('移除照片', 'Buang Foto'),
    'card_name': ('卡名称', 'Nama Kad'),
    'card_emoji_icon': ('卡表情/图标', 'Emoji/Ikon Kad'),
    'stamps_required_to_complete': ('完成所需印章数', 'Setem Diperlukan untuk Lengkap'),
    'stamps_collected': ('已收集印章', 'Setem Dikumpul'),
    'card_color_theme': ('卡颜色主题', 'Tema Warna Kad'),
    'minAmount': ('最低金额(RM)', 'Jumlah Min (RM)'),
    'mFreeItemLabel': ('免费商品标签', 'Label Item Percuma'),
    'expiryDate': ('到期日期', 'Tarikh Luput'),
    'launch_date': ('发布日期', 'Tarikh Lancar'),
    'end_date': ('结束日期', 'Tarikh Tamat'),
    'start_date': ('开始日期', 'Tarikh Mula'),
    'activeDays': ('活跃天数', 'Hari Aktif'),
    'startTime': ('开始时间', 'Masa Mula'),
    'endTime': ('结束时间', 'Masa Tamat'),
    'enablePromo': ('启用促销', 'Dayakan Promosi'),
    'busyThreshold': ('忙碌阈值', 'Ambang Sibuk'),
    'mon': ('一', 'Isn'),
    'tue': ('二', 'Sel'),
    'wed': ('三', 'Rabu'),
    'thu': ('四', 'Khamis'),
    'fri': ('五', 'Jumaat'),
    'sat': ('六', 'Sabtu'),
    'sun': ('日', 'Ahad'),
    'hot_drinks': ('热饮', 'Minuman Panas'),
    'cold_drinks': ('冷饮', 'Minuman Sejuk'),
    'food': ('食物', 'Makanan'),
    'desserts': ('甜点', 'Pencuci Mulut'),
    'snacks': ('小吃', 'Mudahan'),
    'cash': ('现金', 'Tunai'),
    'bank_transfer': ('银行转账', 'Pemindahan Bank'),
    'sst': ('服务税 (6%)', 'SST (6%)'),
    'congratulations': ('恭喜！', 'Tahniah!'),
    'close': ('关闭', 'Tutup'),
    'create_stamp_card': ('创建印章卡', 'Cipta Kad Setem'),
    'launch_new_item': ('发布新品', 'Lancarkan Item Baharu'),
    'add_new_item': ('添加新商品', 'Tambah Item Baharu'),
    'past_launches': ('历史发布', 'Pelancaran Lalu'),
    'active_new_launches': ('进行中的发布', 'Pelancaran Aktif'),
    'active_stamp_cards': ('活跃印章卡', 'Kad Setem Aktif'),
    'active_ads': ('活跃广告', 'Iklan Aktif'),
    'all_members': ('全部会员', 'Semua Ahli'),
    'all_orders': ('全部订单', 'Semua Pesanan'),
    'no_active_ads': ('暂无活跃广告', 'Tiada iklan aktif'),
    'no_ads_yet': ('暂无广告', 'Belum ada iklan'),
    'no_commissions_yet': ('暂无佣金记录', 'Tiada rekod komisi'),
    'no_friends_referred_yet': ('暂无推荐好友', 'Belum ada rakan dirujuk'),
    'no_pickup_time_set': ('未设置取餐时间', 'Tiada masa ambil ditetapkan'),
    'noPendingPaymentProofs': ('暂无待处理付款凭证', 'Tiada bukti pembayaran tertunda'),
    'noPromosNow': ('暂无促销活动', 'Tiada promosi buat masa ini'),
    'number_of_tables': ('桌数', 'Bilangan Meja'),
    'pending_payment_proofs': ('待处理付款凭证', 'Bukti Pembayaran Tertunda'),
    'pending_top_up_requests': ('待处理充值请求', 'Permintaan Isi Semula Tertunda'),
    'select_menu_item': ('选择菜单项', 'Pilih Item Menu'),
    'invite_friends_title': ('邀请好友', 'Jemput Rakan'),
    'commission_settings': ('佣金设置', 'Tetapan Komisi'),
    'commission_records': ('佣金记录', 'Rekod Komisi'),
    'new_complaint': ('新投诉', 'Aduan Baharu'),
    'confirm_deactivate': ('确认停用', 'Sahkan Nyahaktif'),
    'deactivate_member': ('停用会员', 'Nyahaktif Ahli'),
    'email_optional': ('邮箱(可选)', 'Emel (pilihan)'),
    'response_action_taken': ('回复/处理措施', 'Respons / Tindakan'),
    'promoEngineTitle': ('促销引擎', 'Enjin Promosi'),
    'promoEngineDesc': ('自动为顾客推荐促销活动', 'Auto cadangkan promosi kepada pelanggan'),
    'promoHideHint': ('隐藏此提示', 'Sembunyikan petunjuk ini'),
    
    # === 商家端 (m prefix) ===
    'mRulePerOrderOpt': ('每次购买=1印章', 'Setiap pembelian = 1 setem'),
    'mRulePerAmountOpt': ('每消费RM X=1印章', 'Setiap RM X dibelanjakan = 1 setem'),
    'mRulePerItemOpt': ('购买指定商品=1印章', 'Beli item tertentu = 1 setem'),
    'mRewardFreeItemOpt': ('免费菜单项目', 'Item Menu Percuma'),
    'mRewardFlatDiscountOpt': ('固定减免(RM)', 'Diskaun Tetap (RM)'),
    'mRewardBonusPointsOpt': ('奖励积分', 'Mata Bonus'),
    'mPromoPriceLbl': ('促销价 (RM)', 'Harga Promo (RM)'),
    'mLoginHint': ('输入商家ID和密码', 'Masukkan ID Peniaga dan kata laluan'),
    'searchForAMember': ('搜索会员', 'Cari Ahli'),
    'noStampCardsYet': ('还没有印章卡', 'Belum ada kad setem'),
    'noActiveNewItems': ('没有进行中的新品', 'Tiada item baharu aktif'),
    'noPastLaunches': ('没有历史发布', 'Tiada pelancaran lepas'),
    'noPendingRequests': ('暂无待处理请求', 'Tiada permohonan tertunda'),
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
    'friendsReferredTitle': ('你推荐的好友', 'Rakan Anda Rujuk'),
    'markResolvedBtn': ('标记为已解决', 'Tanda Sebagai Selesai'),
    'orderDetailsTitle': ('订单详情', 'Butiran Pesanan'),
    'complaintOpenBtn': ('待处理', 'Dibuka'),
    'complaintInProgressBtn': ('处理中', 'Sedang Diproses'),
    'complaintResolvedBtn': ('已解决', 'Selesai'),
    'tngName': ('Touch & Go', 'Touch & Go'),
    'leaveEmptyBanner': ('留空使用默认横幅', 'Biarkan kosong untuk guna banner default'),
    'smallTextHint': ('主标题上方的小文字（如"欢迎回来"）', 'Teks kecil di atas tajuk utama (cth "Selamat Kembali")'),
    'bigTitleHint': ('首页大标题（如"今天想喝什么？"）', 'Tajuk besar di halaman utama (cth "Minuman anda hari ini?")'),
    'higherShowsFirst': ('数字越大越靠前', 'Nombor lebih besar ditunjukkan dulu'),
    'recommendedSize': ('建议尺寸：750×300px', 'Cadangan saiz: 750×300px'),
    'optional': ('可选', 'pilihan'),
    'add_points_manually': ('手动加分', 'Tambah Mata Secara Manual'),
    'add_bonus_rule': ('添加奖励规则', 'Tambah Peraturan Bonus'),
    'add_rule': ('添加规则', 'Tambah Peraturan'),
    'add_to_menu': ('添加到菜单', 'Tambah ke Menu'),
    'phone_number': ('电话号码', 'Nombor Telefon'),
    'bill_amount': ('账单金额(RM)', 'Jumlah Bil (RM)'),
    'uploadPhotoOptional': ('上传照片(可选)', 'Muat Naik Foto (pilihan)'),
    'tap_to_upload_photo': ('点击上传照片', 'Tekan untuk muat naik foto'),
    'photo_upload_hint': ('JPG/PNG 最大5MB', 'JPG/PNG maksimum 5MB'),
    'order_id_optional': ('订单号(可选)', 'ID Pesanan (pilihan)'),
}

# ===== 4. 构建新的 ZH 和 MS 块 =====
def build_new_block(old_block, lang, existing_kv):
    lines = old_block.split('\n')
    new_lines = []
    added_in_block = set()
    replaced = 0
    
    for line in lines:
        stripped = line.strip()
        m = re.match(r"(\w[\w-]*)\s*:\s*'([^']*(?:\\'[^']*)*)'", stripped)
        if m:
            key = m.group(1)
            if key in T:
                val = T[key][0] if lang == 'zh' else T[key][1]
                indent = len(line) - len(line.lstrip())
                new_lines.append(' ' * indent + f"{key}: '{val}',")
                added_in_block.add(key)
                replaced += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Add missing keys before the last }
    missing = [k for k in T if k not in added_in_block and k in all_needed]
    if missing:
        last_brace = '\n}'.join(new_lines).rfind('\n}')
        # Simpler approach: find last line that is just whitespace + }
        insert_idx = None
        for idx in range(len(new_lines)-1, -1, -1):
            if new_lines[idx].strip() == '}':
                insert_idx = idx
                break
        if insert_idx is not None:
            insert_lines = []
            for key in sorted(missing):  # sort for consistency
                val = T[key][0] if lang == 'zh' else T[key][1]
                insert_lines.append(f"    {key}: '{val}',")
            new_lines = new_lines[:insert_idx] + insert_lines + [new_lines[insert_idx]]
    
    return '\n'.join(new_lines), replaced, len(missing) if 'missing' in dir() else 0

zh_new, zh_replaced, zh_added_count = build_new_block(zh_block, 'zh', zh_kv)
ms_new, ms_replaced, ms_added_count = build_new_block(ms_block, 'ms', ms_kv)

print(f"\nZH: Replaced {zh_replaced} existing keys")
print(f"MS: Replaced {ms_replaced} existing keys")

# ===== 5. 精确替换 =====
new_js = (
    js[:zo] +           # before ZH content
    zh_new + '\n}' +    # new ZH content
    js[z2:mo] +         # between ZH } and MS {
    ms_new + '\n}' +    # new MS content  
    js[m2:]             # after MS }
)

with open(JS, 'w', encoding='utf-8') as f:
    f.write(new_js)

print(f"\n✅ Saved! Size: {len(new_js)} (was {len(js)})")

# ===== 6. 验证 =====
# Reload and spot-check
with open(JS, 'r', encoding='utf-8') as f:
    js2 = f.read()

# Re-find positions
zh_m2 = re.search(r'\bzh\s*:\s*\{', js2[z2-100000:])  # search around old area
# Better: just search from LANGS
langs2 = js2.index('const LANGS = {')
# Skip to zh block by counting braces... just verify a few keys
check_keys = ['mRulePerOrderOpt', 'filterAll', 'placeOrder', 'kitchenDisplayLbl', 
              'getNotifiedWhenReady', 'myShopLink', 'stamp_rule', 'reward_type',
              'tngName', 'referralProgramTitle', 'maybeLaterBtn']

# Find all occurrences of each key and check if any have correct translation
final_pass = 0
final_fail = 0
for key in check_keys:
    matches = list(re.finditer(re.escape(key) + r"\s*:\s*'([^']*)'", js2))
    found_zh = False
    found_ms = False
    for mm in matches:
        val = mm.group(1)
        pos = mm.start()
        # Determine which block based on position
        if pos > mo and pos < mo + len(ms_new) + 10000:
            if lang == 'ms':
                pass
        # Simple heuristic: check value
        has_cn = any('\u4e00' <= c <= '\u9fff' for c in val)
        is_ms_val = len(val) > 0 and not any('\u4e00' <= c <= '\u9fff' for c in val[:3]) and '\u0b80' not in val
        if has_cn: found_zh = True
        if is_ms_val and not has_cn: found_ms = True
    
    if found_zh and found_ms:
        print(f"✅ {key}")
        final_pass += 1
    else:
        print(f"❌ {key} (zh={found_zh}, ms={found_ms})")
        final_fail += 1

print(f"\n=== Final: {final_pass}/{final_pass+final_fail} passed ===")
