"""
Fix missing i18n keys - v3 (quote-aware parsing, correct boundaries)
"""
import re, os, tempfile, subprocess

DEPLOY_DIR = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy'
JS_PATH = os.path.join(DEPLOY_DIR, 'app.js')
HTML_PATH = os.path.join(DEPLOY_DIR, 'index.html')

with open(JS_PATH, 'r', encoding='utf-8-sig') as f:
    js = f.read()
with open(HTML_PATH, 'r', encoding='utf-8-sig') as f:
    html = f.read()

print(f"JS: {len(js)} chars")

# Extract HTML keys
html_keys = set(re.findall(r'data-i18n="([^"]+)"', html))
mi18n_key = None
m = re.search(r'data-mi18n="([^"]+)"', html)
if m:
    mi18n_key = m.group(1)
print(f"HTML data-i18n keys: {len(html_keys)}, data-mi18n: {mi18n_key}")

# Quote-aware block parser
def find_block_end(content, block_name, start_pos):
    colon = content.find(block_name + ': {', start_pos)
    if colon < 0:
        colon = content.find(block_name + ':{', start_pos)
    if colon < 0:
        return -1, -1
    i = colon + len(block_name) + 2
    depth = 0
    in_string = False
    string_char = None
    while i < len(content):
        c = content[i]
        if in_string:
            if c == '\\': i += 2; continue
            if c == string_char: in_string = False; string_char = None
        elif c in '"\'':
            in_string = True; string_char = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return i
        i += 1
    return -1

def extract_keys(content, block_name, start_pos):
    end_pos = find_block_end(content, block_name, start_pos)
    block_start = content.find(block_name + ': {', start_pos)
    if block_start < 0: block_start = content.find(block_name + ':{', start_pos)
    if end_pos < 0 or block_start < 0: return set()
    keys = set()
    depth = 0; in_str = False; str_c = None
    i = block_start + len(block_name) + 2
    while i < end_pos:
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == str_c: in_str = False; str_c = None
        elif c in '"\'':
            in_str = True; str_c = c
        elif c == '{': depth += 1
        elif c == '}': depth -= 1
        elif c == ':' and depth == 1:
            ks = content.rfind(' ', block_start, i)
            if ks > block_start:
                k = content[ks+1:i].strip()
                if re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', k):
                    keys.add(k)
        i += 1
    return keys

# Find block positions
langs_pos = js.find('const LANGS')
ml_pos = js.find('const MERCHANT_LANGS')
print(f"LANGS at {langs_pos}, MERCHANT_LANGS at {ml_pos}")

# Translations for missing keys
ZH = {
    'activeDays':'营业日','active_new_launches':'进行中的新品','active_stamp_cards':'进行中的集章卡',
    'add_bonus_rule':'添加奖励规则','add_new_item':'添加新品','add_points_manually':'手动加分',
    'add_rule':'添加规则','add_to_menu':'添加到菜单','admin':'管理员','all_members':'所有会员',
    'all_orders':'全部订单','announcement_text':'公告内容','bankAmountLabel':'银行金额',
    'bank_transfer':'银行转账','bigTitleHint':'大标题提示','bill_amount':'账单金额',
    'busyThreshold':'忙碌阈值','cancel':'取消','card_color_theme':'卡片颜色主题',
    'card_emoji_icon':'卡片表情/图标','commissionHistoryTitle':'佣金记录','complaintInProgressBtn':'处理中',
    'complaintOpenBtn':'待处理投诉','complaintResolvedBtn':'已解决投诉','copyLinkBtn':'复制链接',
    'copyReferralBtn':'复制推荐链接','currentRateLbl':'当前费率','doneLbl':'完成',
    'enableNotificationsBtn':'启用通知','enablePromo':'启用促销','endTime':'结束时间',
    'expiryDate':'到期日期','filterAllC':'全部','fri':'周五','friendsReferredTitle':'已推荐好友',
    'getNotifiedWhenReady':'就绪时通知我','higherShowsFirst':'越高越前','kitchenDisplayLbl':'厨房显示屏',
    'leaveEmptyBanner':'留空则不显示横幅','loyalbrew_brand':'LoyalBrew','mFreeItemLabel':'免费项目',
    'mLoginHint':'使用您的会员账号登录','mPromoPriceLbl':'促销价','mRewardBonusPointsOpt':'奖励积分',
    'mRewardFlatDiscountOpt':'固定折扣 (RM)','mRewardFreeItemOpt':'免费菜单项目',
    'mon':'周一','newLaunchSettings':'新品发布设置','notificationEnabled':'通知已启用',
    'notificationPrompt':'开启通知接收订单状态更新','openAppToRedeem':'打开App兑换',
    'orderHistoryTitle':'订单历史','past_new_launches':'过往新品','pendingVerifications':'待验证',
    'phoneNumberLabel':'电话号码','points_to_reward':'奖励积分','preparingOrders':'准备中',
    'promoSettings':'促销设置','rateThisItem':'评价此项目','readyOrders':'可取餐',
    'recentOrders':'最近订单','referralLinkCopied':'推荐链接已复制','referralProgramTitle':'推荐计划',
    'referrerRewardDesc':'推荐好友下单后，您将获得奖励','registration':'注册','resetPoints':'重置积分',
    'rewardDescription':'奖励描述','rewardPoints':'奖励积分','rewardsEarned':'已获奖励',
    'saveChanges':'保存更改','saveSettings':'保存设置','scanQRToJoin':'扫描二维码加入',
    'scanToRedeem':'扫码兑换','selectLanguage':'选择语言','selectReward':'选择奖励',
    'sendToKitchen':'发送到厨房','settingsSaved':'设置已保存','specialPrice':'特别价格',
    'startTime':'开始时间','statusOpen':'待处理','stepDescription':'步骤描述',
    'submitReview':'提交评价','sun':'周日','tableNumber':'桌号','tableQRCode':'桌位二维码',
    'thu':'周四','tierName':'等级名称','tierPointsRequired':'所需积分','timeRange':'时间段',
    'titleName':'标题名称','toastedOrderReady':'您的订单已准备好！','toastedPointsAdded':'积分已添加！',
    'toastedWelcome':'欢迎回来','tue':'周二','unlockReward':'解锁奖励','usedPoints':'已用积分',
    'validFrom':'有效期从','verify_payment':'验证支付','viewHistory':'查看历史',
    'viewMenuItems':'查看菜单','view_orders':'查看订单','visibilityNote':'公开可见',
    'walletBalance':'钱包余额','wed':'周三','welcomeTitle':'欢迎标题','writeReview':'写评价',
    'yourReferralLink':'您的推荐链接','zalo_url':'Zalo链接'
}
MS = {
    'activeDays':'Hari Aktif','active_new_launches':'Pelancaran Baharu Aktif','active_stamp_cards':'Kad Setem Aktif',
    'add_bonus_rule':'Tambah Bonus','add_new_item':'Tambah Item Baharu','add_points_manually':'Tambah Mata Secara Manual',
    'add_rule':'Tambah Peraturan','add_to_menu':'Tambah ke Menu','admin':'Admin','all_members':'Semua Ahli',
    'all_orders':'Semua Pesanan','announcement_text':'Teks Pengumuman','bankAmountLabel':'Jumlah Bank',
    'bank_transfer':'Pemindahan Bank','bigTitleHint':'Petua Tajuk Besar','bill_amount':'Jumlah Bil',
    'busyThreshold':'Ambang Sibuk','cancel':'Batal','card_color_theme':'Tema Warna Kad',
    'card_emoji_icon':'Ikon Emoji Kad','commissionHistoryTitle':'Sejarah Komisen','complaintInProgressBtn':'Dalam Proses',
    'complaintOpenBtn':'Aduan Terbuka','complaintResolvedBtn':'Aduan Selesai','copyLinkBtn':'Salin Link',
    'copyReferralBtn':'Salin Link Rujukan','currentRateLbl':'Kadar Semasa','doneLbl':'Selesai',
    'enableNotificationsBtn':'Aktifkan Pemberitahuan','enablePromo':'Aktifkan Promosi','endTime':'Masa Tamat',
    'expiryDate':'Tarikh Luput','filterAllC':'Semua','fri':'Jumaat','friendsReferredTitle':'Kawan Dirujuk',
    'getNotifiedWhenReady':'Beritahu Saya Apabila Sedia','higherShowsFirst':'Tinggi Ditunjukkan Dahulu','kitchenDisplayLbl':'Paparan Dapur',
    'leaveEmptyBanner':'Biarkan kosong untuk tanpa sepanduk','loyalbrew_brand':'LoyalBrew','mFreeItemLabel':'Item Percuma',
    'mLoginHint':'Log masuk dengan akaun ahli anda','mPromoPriceLbl':'Harga Promosi','mRewardBonusPointsOpt':'Mata Bonus',
    'mRewardFlatDiscountOpt':'Diskaun Tetap (RM)','mRewardFreeItemOpt':'Item Menu Percuma',
    'mon':'Isnin','newLaunchSettings':'Tetapan Pelancaran Baharu','notificationEnabled':'Pemberitahuan Dihidupkan',
    'notificationPrompt':'Hidupkan pemberitahuan untuk kemas kini pesanan','openAppToRedeem':'Buka App untuk Tebus',
    'orderHistoryTitle':'Sejarah Pesanan','past_new_launches':'Pelancaran Lama','pendingVerifications':'Penentusahan Terpanding',
    'phoneNumberLabel':'Nombor Telefon','points_to_reward':'Mata untuk Ganjaran','preparingOrders':'Menyediakan',
    'promoSettings':'Tetapan Promosi','rateThisItem':'Nilaikan Item Ini','readyOrders':'Sedia untuk Diambil',
    'recentOrders':'Pesanan Terkini','referralLinkCopied':'Link Rujukan Disalin','referralProgramTitle':'Program Rujukan',
    'referrerRewardDesc':'Anda akan mendapat ganjaran apabila kawan membuat pesanan','registration':'Pendaftaran','resetPoints':'Set Semula Mata',
    'rewardDescription':'Penerangan Ganjaran','rewardPoints':'Mata Ganjaran','rewardsEarned':'Ganjaran Diperolehi',
    'saveChanges':'Simpan Perubahan','saveSettings':'Simpan Tetapan','scanQRToJoin':'Imbas QR untuk Sertai',
    'scanToRedeem':'Imbas untuk Tebus','selectLanguage':'Pilih Bahasa','selectReward':'Pilih Ganjaran',
    'sendToKitchen':'Hantar ke Dapur','settingsSaved':'Tetapan Disimpan','specialPrice':'Harga Khas',
    'startTime':'Masa Mula','statusOpen':'Terbuka','stepDescription':'Penerangan Langkah',
    'submitReview':'Hantar Semakan','sun':'Ahad','tableNumber':'Nombor Meja','tableQRCode':'QR Meja',
    'thu':'Khamis','tierName':'Nama Tahap','tierPointsRequired':'Mata yang Diperlukan','timeRange':'Julat Masa',
    'titleName':'Nama Tajuk','toastedOrderReady':'Pesanan anda sedia!','toastedPointsAdded':'Mata ditambah!',
    'toastedWelcome':'Selamat Datang','tue':'Selasa','unlockReward':'Buka Ganjaran','usedPoints':'Mata Digunakan',
    'validFrom':'Sah Dari','verify_payment':'Sahkan Pembayaran','viewHistory':'Lihat Sejarah',
    'viewMenuItems':'Lihat Item Menu','view_orders':'Lihat Pesanan','visibilityNote':'Boleh Dilihat Umum',
    'walletBalance':'Baki Dompet','wed':'Rabu','welcomeTitle':'Tajuk Selamat Datang','writeReview':'Tulis Semakan',
    'yourReferralLink':'Link Rujukan Anda','zalo_url':'Pautan Zalo'
}
TA = {
    'activeDays':'செயல்படும் நாட்கள்','active_new_launches':'செயலில் உள்ள புதிய வெளியீடுகள்','active_stamp_cards':'செயலில் உள்ள ஸ்டாம்ப் கார்டுகள்',
    'add_bonus_rule':'போனஸ் விதி சேர்','add_new_item':'புதிய பொருள் சேர்','add_points_manually':'கைமுறையாக புள்ளிகள் சேர்',
    'add_rule':'விதி சேர்','add_to_menu':'மெனுவில் சேர்','admin':'நிர்வாகி','all_members':'அனைத்து உறுப்பினர்கள்',
    'all_orders':'அனைத்து ஆர்டர்கள்','announcement_text':'அறிவிப்பு உரை','bankAmountLabel':'வங்கி தொகை',
    'bank_transfer':'வங்கி மாற்றம்','bigTitleHint':'பெரிய தலைப்பு உதவி','bill_amount':'பில் தொகை',
    'busyThreshold':'பிஸியான அளவு','cancel':'ரத்து','card_color_theme':'கார்டு நிற தீம்',
    'card_emoji_icon':'கார்டு இமோஜி/ஐகான்','commissionHistoryTitle':'கமிஷன் வரலாறு','complaintInProgressBtn':'செயல்பாட்டில்',
    'complaintOpenBtn':'திறந்த புகார்','complaintResolvedBtn':'தீர்க்கப்பட்ட புகார்','copyLinkBtn':'இணைப்பை நகல் செய்',
    'copyReferralBtn':'ரெஃபரல் இணைப்பை நகல் செய்','currentRateLbl':'தற்போதைய விகிதம்','doneLbl':'முடிந்தது',
    'enableNotificationsBtn':'அறிவிப்புகளை இயக்கு','enablePromo':'ஊக்குவிப்பை இயக்கு','endTime':'முடிவு நேரம்',
    'expiryDate':'காலாவதி தேதி','filterAllC':'அனைத்தும்','fri':'வெள்ளி','friendsReferredTitle':'ரெஃபரல் நண்பர்கள்',
    'getNotifiedWhenReady':'தயாரானவுடன் அறிய','higherShowsFirst':'உயர் முதலில் காட்டு','kitchenDisplayLbl':'சமையலறை காட்சி',
    'leaveEmptyBanner':'பேனர் இல்லாமல் விடவும்','loyalbrew_brand':'LoyalBrew',
    'mFreeItemLabel':'இலவச பொருள்','mLoginHint':'உறுப்பினர் கணக்கால் உள்நுழையவும்',
    'mPromoPriceLbl':'ஊக்கு விலை','mRewardBonusPointsOpt':'போனஸ் புள்ளிகள்',
    'mRewardFlatDiscountOpt':'நிலையான தள்ளுபடி (RM)','mRewardFreeItemOpt':'இலவச மெனு பொருள்',
    'mon':'திங்கள்','newLaunchSettings':'புதிய வெளியீடு அமைப்புகள்',
    'notificationEnabled':'அறிவிப்பு இயக்கப்பட்டது','notificationPrompt':'ஆர்டர் நிலை புதுப்பிப்புகளுக்கு அறிவிப்புகளை இயக்கவும்',
    'openAppToRedeem':'ரிடீம் செய்ய ஆப்ஸைத் திறக்கவும்','orderHistoryTitle':'ஆர்டர் வரலாறு',
    'past_new_launches':'கடந்த புதிய வெளியீடுகள்','pendingVerifications':'நிலுவையில் உள்ள சரிபார்ப்புகள்',
    'phoneNumberLabel':'தொலைபேசி எண்','points_to_reward':'வெகுமதி புள்ளிகள்','preparingOrders':'தயாரிக்கும்',
    'promoSettings':'ஊக்குவிப்பு அமைப்புகள்','rateThisItem':'இந்த பொருளை மதிப்பிடவும்',
    'readyOrders':'ஆர்டர் தயார்','recentOrders':'சமீபத்திய ஆர்டர்கள்','referralLinkCopied':'ரெஃபரல் இணைப்பு நகல் செய்யப்பட்டது',
    'referralProgramTitle':'ரெஃபரல் திட்டம்','referrerRewardDesc':'நண்பர் ஆர்டர் செய்யும்போது நீங்கள் வெகுமதி பெறுவீர்கள்',
    'registration':'பதிவு','resetPoints':'புள்ளிகளை மீட்டமை','rewardDescription':'வெகுமதி விளக்கம்',
    'rewardPoints':'வெகுமதி புள்ளிகள்','rewardsEarned':'வெகுமதிகள் பெறப்பட்டன','saveChanges':'மாற்றங்களை சேமி',
    'saveSettings':'அமைப்புகளை சேமி','scanQRToJoin':'QR ஸ்கேன் செய்யவும்','scanToRedeem':'ரிடீம் செய்ய ஸ்கேன்',
    'selectLanguage':'மொழியைத் தேர்ந்தெடுக்கவும்','selectReward':'வெகுமதியைத் தேர்ந்தெடுக்கவும்',
    'sendToKitchen':'சமையலறைக்கு அனுப்பவும்','settingsSaved':'அமைப்புகள் சேமிக்கப்பட்டன',
    'specialPrice':'சிறப்பு விலை','startTime':'தொடக்க நேரம்','statusOpen':'திறந்த',
    'stepDescription':'படி விளக்கம்','submitReview':'மதிப்பீட்டைச் சமர்ப்பிக்கவும்','sun':'ஞாயிறு',
    'tableNumber':'மேசை எண்','tableQRCode':'மேசை QR குறியீடு','thu':'வியாழன்',
    'tierName':'நிலை பெயர்','tierPointsRequired':'தேவையான புள்ளிகள்','timeRange':'நேரம் வரம்பு',
    'titleName':'தலைப்பு பெயர்','toastedOrderReady':'உங்கள் ஆர்டர் தயார்!','toastedPointsAdded':'புள்ளிகள் சேர்க்கப்பட்டன!',
    'toastedWelcome':'மீண்டும் வருகிறோம்','tue':'செவ்வாய்','unlockReward':'வெகுமதியைத் திறக்கவும்',
    'usedPoints':'பயன்படுத்திய புள்ளிகள்','validFrom':'சரியானது','verify_payment':'பணம் சரிபார்',
    'viewHistory':'வரலாற்றைக் காண்க','viewMenuItems':'மெனு பொருட்களைக் காண்க','view_orders':'ஆர்டர்களைக் காண்க',
    'visibilityNote':'பொதுவாக காணக்கூடியது','walletBalance':'பணப்பை இருப்பு','wed':'புதன்',
    'welcomeTitle':'வரவேற்பு தலைப்பு','writeReview':'மதிப்பீடு எழுதுக','yourReferralLink':'உங்கள் ரெஃபரல் இணைப்பு',
    'zalo_url':'Zalo இணைப்பு'
}
TRANSLATIONS = {'en': {}, 'zh': ZH, 'ms': MS, 'ta': TA}

def add_keys_to_block(content, block_name, all_keys, start_pos, trans):
    """Add missing keys to a language block with quote-aware parsing"""
    block_start = content.find(block_name + ': {', start_pos)
    if block_start < 0: block_start = content.find(block_name + ':{', start_pos)
    if block_start < 0: return content
    
    end_pos = find_block_end(content, block_name, start_pos)
    if end_pos < 0: return content
    
    existing = extract_keys(content, block_name, start_pos)
    to_add = [k for k in sorted(all_keys) if k not in existing]
    if not to_add:
        print(f"  {block_name}: all keys exist")
        return content
    
    print(f"  {block_name}: adding {len(to_add)} keys (existing: {len(existing)})")
    
    # Build new entries
    lines = []
    for key in to_add:
        val = trans.get(key, key)
        val_escaped = val.replace("'", "\\'")
        lines.append(f"    {key}: '{val_escaped}'")
    new_entries = ',\n'.join(lines)
    
    # Insert before the closing }
    char_before_close = content[end_pos - 1]
    if char_before_close == ',':
        new_content = content[:end_pos] + new_entries + content[end_pos:]
    else:
        new_content = content[:end_pos] + ',\n' + new_entries + content[end_pos:]
    
    return new_content

# Process LANGS
print("\n=== LANGS ===")
js_new = js
for lang in ['en', 'zh', 'ms', 'ta']:
    js_new = add_keys_to_block(js_new, lang, html_keys, langs_pos, TRANSLATIONS.get(lang, {}))

# Process MERCHANT_LANGS
print("\n=== MERCHANT_LANGS ===")
if mi18n_key:
    for lang in ['en', 'zh', 'ms', 'ta']:
        js_new = add_keys_to_block(js_new, lang, {mi18n_key}, ml_pos, TRANSLATIONS.get(lang, {}))
else:
    print("  No mi18n key")

# Validate BEFORE saving
print("\n=== Syntax validation ===")
tmp = os.path.join(tempfile.gettempdir(), 'app_validate.js')
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(js_new)
result = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
os.unlink(tmp)
if result.returncode != 0:
    print(f"SYNTAX ERROR: {result.stderr}")
    sys.exit(1)
print("SYNTAX OK")

# Save
with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(js_new)
print(f"\nSaved: {len(js_new)} chars")

# Update source
src = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(src, 'r', encoding='utf-8-sig') as f:
    pass
with open(src, 'w', encoding='utf-8') as f:
    f.write(js_new)
print("Source updated")

print("\n=== Done! Ready to deploy ===")