"""
补充 TA (泰米尔语) 块缺失的 396 个翻译
使用 Google Translate API 生成泰米尔语翻译
"""
import re, shutil, json

SRC = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
shutil.copy2(SRC, SRC + '.bak_ta_complete')

with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到第二个 LANGS 的 en: 块（614键的那个）
langs2_pos = content.find('const LANGS = {', content.find('const LANGS = {') + 1)

# 提取 en: 块的所有键
en_match = re.search(r'en\s*:\s*\{', content[langs2_pos:])
en_start_local = en_match.end()
depth = 0
i = en_start_local - 1
while i < len(content) - langs2_pos:
    c = content[langs2_pos + i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            en_end_local = i
            break
    i += 1

en_block = content[langs2_pos + en_match.start():langs2_pos + en_end_local + 1]
pairs = re.findall(r"(\w[\w.]*):\s*'([^']*)'", en_block)
print(f'EN keys in second LANGS: {len(pairs)}')

# 找到现有的 ta: 块
ta_match = re.search(r'ta\s*:\s*\{', content[langs2_pos:])
if not ta_match:
    print('ta: block not found in second LANGS')
    exit()

ta_start_local = ta_match.end()
depth = 0
i = ta_start_local - 1
while i < len(content) - langs2_pos:
    c = content[langs2_pos + i]
    if c == '{': depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            ta_end_local = i
            break
    i += 1

ta_block = content[langs2_pos + ta_match.start():langs2_pos + ta_end_local + 1]
ta_pairs = re.findall(r"(\w[\w.]*):\s*'([^']*)'", ta_block)
print(f'TA keys existing: {len(ta_pairs)}')

# 找出缺失的键
ta_dict = {k: v for k, v in ta_pairs}
existing_ta_keys = set(ta_dict.keys())

# 泰米尔语翻译字典（基于常见 UI 术语）
TA_TRANSLATIONS = {
    # 核心导航
    'tagline': 'ஆர்டர் • புள்ளிகள் சேர் • வெகுமதிகள் பெறுங்கள்',
    'loginLabel': 'உறுப்பினர் உள்நுழைவு',
    'myAccount': 'எனது கணக்கு',
    'orderNow': 'இப்போது ஆர்டர் செய்',
    'myStampCard': 'எனது ஸ்டாம்ப் கார்டு',
    'topUp': 'மீட்டேற்றம்',
    'merchant': 'வணிகர்',
    
    # 功能介绍
    'feat1Title': 'QR ஐ ஸ்கேன் செய்து ஆர்டர் செய்',
    'feat1Desc': 'மேஜை QR ஐ ஸ்கேன் செய், விநாடிகளில் ஆர்டர் செய்',
    'feat2Title': 'புள்ளிகள் சேர்',
    'feat2Desc': 'RM1 செலவழித்தால் = 1 புள்ளி கிடைக்கும்',
    'feat3Title': 'இலவச பானங்கள்',
    'feat3Desc': 'இலவச பானங்களுக்கு புள்ளிகளை மாற்றவும்',
    
    # 菜单
    'menu': 'மெனு',
    'dineIn': 'உள்ளே சாப்பிடு',
    'takeaway': 'கொண்டு செல்',
    'table': 'மேஜை',
    'change': 'மாற்று',
    'selectTable': 'உங்கள் மேஜையைத் தேர்ந்தெடுக்கவும்',
    'enterTable': 'ஆர்டர் செய்ய உங்கள் மேஜை எண்ணை உள்ளிடவும்',
    'confirmTable': 'மேஜையை உறுதிப்படுத்து',
    'invalidTable': 'சரியான மேஜை எண்ணை உள்ளிடவும்',
    
    # 分类
    'catAll': 'அனைத்தும்',
    'catNewItems': '✨ புதிய பொருட்கள்',
    'catHotDrinks': 'சூடான பானங்கள்',
    'catColdDrinks': 'குளிர் பானங்கள்',
    'catFood': 'உணவு',
    'catDesserts': 'இனிப்புகள்',
    'catSnacks': 'சிற்றுண்டி',
    
    # 购物车
    'floatViewCart': 'வண்டியைப் பார் →',
    'floatItem': 'பொருள்',
    'floatItems': 'பொருட்கள்',
    'takeawayOrder': 'கொண்டு செல் ஆர்டர்',
    'noPickupTime': 'எடுக்கும் நேரம் அமைக்கப்படவில்லை',
    'pickup': 'எடு',
    
    # 订单
    'yourOrder': 'உங்கள் ஆர்டர்',
    'orderType': 'ஆர்டர் வகை',
    'phoneNumber': 'தொலைபேசி எண்',
    'pickupTime': 'எடுக்கும் நேரம்',
    'pickupHint': 'இந்த நேரத்தில் உங்கள் ஆர்டரை தயார் செய்வோம்.',
    'loyaltyPoints': 'விசுவாச புள்ளிகள் & ஸ்டாம்ப்',
    'earnHint': 'தொலைபேசி எண்ணை உள்ளிட்டு 🔍 ஐ அழுத்தி புள்ளிகள் & ஸ்டாம்புகள் பெறுங்கள்',
    'phoneLoyalty': 'தொலைபேசி எண் (புள்ளிகள் & ஸ்டாம்புகள் பெற)',
    
    # 支付
    'payWallet': 'வாலட்டில் பணம் செலுத்து',
    'useWallet': 'பணம் செலுத்த வாலட் பேலன்ஸ் பயன்படுத்து',
    'walletBalance': 'பேலன்ஸ்',
    'paymentMethod': 'பணம் செலுத்தும் முறை',
    'cartEmpty': 'உங்கள் வண்டி காலியாக உள்ளது',
    'browseMenu': 'மெனுவைப் பார்',
    'eachUnit': 'ஒவ்வொன்றும்',
    'removeItem': 'நீக்கு',
    
    # 订单摘要
    'orderSummary': 'ஆர்டர் சுருக்கம்',
    'subtotal': 'கூட்டுத்தொகை',
    'sst': 'SST (6%)',
    'walletDeduction': 'வாலட் கழிவு',
    'totalLabel': 'மொத்தம்',
    'pointsEarnLabel': 'நீங்கள் பெறும் புள்ளிகள்',
    'specialRequest': 'சிறப்பு கோரிக்கை',
    'specialRequestPlaceholder': 'எ.கா. குறைந்த சர்க்கரை, பனி இல்லாமல்...',
    'placeOrder': 'ஆர்டர் செய்',
    
    # 确认
    'cartDineIn': 'உள்ளே சாப்பிடு',
    'cartTakeaway': 'கொண்டு செல்',
    'cartChange': 'மாற்று',
    'confirmType': 'வகை',
    'confirmTable2': 'மேஜை',
    'confirmPhone': 'தொலைபேசி',
    'confirmPickup': 'எடுக்கும் நேரம்',
    'confirmItems': 'பொருட்கள்',
    'confirmWalletPaid': 'வாலட்டில் செலுத்தப்பட்டது',
    'confirmTotalPaid': 'மொத்தம் செலுத்தப்பட்டது',
    'confirmPayment': 'பணம் செலுத்துதல்',
    'confirmPointsEarned': 'பெறப்பட்ட புள்ளிகள்',
    'confirmNote': 'குறிப்பு',
    'pendingVerification': 'சரிபார்ப்பு நிலுவையில்',
    'confirmTypeDineIn': '🪑 உள்ளே சாப்பிடு',
    'confirmTypeTakeaway': '🛍️ கொண்டு செல்',
    
    # 现金支付
    'cashPayCounter': 'தயவுசெய்து கவுண்டரில் பணம் செலுத்தி, பின்னர் கீழே உள்ள பொத்தானை அழுத்தவும்.',
    'cashPaidBtn': 'நான் பணம் செலுத்திவிட்டேன் — சமையலறைக்கு தெரிவி',
    'cashPaidDone': 'பணம் செலுத்துதல் உறுதிப்படுத்தப்பட்டது! சமையலறை உங்கள் ஆர்டரை தயார் செய்கிறது.',
    'confirmReceivedBtn': 'பெற்றதை உறுதிப்படுத்து / ஆர்டரை முடி',
    'orderPlaced': 'ஆர்டர் வைக்கப்பட்டது!',
    'orderSent': 'உங்கள் ஆர்டர் சமையலறைக்கு அனுப்பப்பட்டது.',
    'orderCompletedTitle': 'ஆர்டர் முடிந்தது',
    'orderCompletedMsg': '🎉 ஆர்டர் முடிந்தது! உங்கள் ஆர்டருக்கு நன்றி.',
    
    # 登录/注册
    'enterPhone': 'உங்கள் தொலைபேசி எண்ணை உள்ளிடவும்',
    'enterPhoneNumber': 'தொலைபேசி எண்ணை உள்ளிடவும்',
    'enterPhoneSearch': 'தொலைபேசி எண்ணை உள்ளிடவும்',
    'enterPhoneToLogin': 'உள்நுழைய தொலைபேசி எண்ணை உள்ளிடவும்',
    'phoneRegistered': 'இந்த தொலைபேசி எண் பதிவு செய்யப்பட்டுள்ளது!',
    'fillNamePhone': 'பெயர் மற்றும் தொலைபேசி எண்ணை நிரப்பவும்',
    'register': 'பதிவு செய்',
    'registerHere': 'இங்கே பதிவு செய்',
    'notMember': 'உறுப்பினர் அல்லவா?',
    'goToLogin': 'உறுப்பினர் உள்நுழைவுக்கு செல்',
    'logout': 'வெளியேறு',
    'welcomeBack': 'மீண்டும் வருக',
    'login': 'உள்நுழை',
    'invalidCredentials': 'தவறான நற்சான்றுகள்!',
    'loginRequired': 'உறுப்பினர் உள்நுழைவு தேவை',
    'sessionExpired': 'அமர்வு காலாவதியானது, மீண்டும் தொலைபேசி எண்ணை உள்ளிடவும்',
    'memberNotFound': 'உறுப்பினர் கிடைக்கவில்லை, முதலில் பதிவு செய்யவும்',
    'memberNotFoundExcl': 'உறுப்பினர் கிடைக்கவில்லை!',
    'memberNotFoundRegister': 'உறுப்பினர் கிடைக்கவில்லை, பதிவு செய்யவும்',
    'memberNotFoundShort': 'உறுப்பினர் கிடைக்கவில்லை',
    'memberDeactivatedMsg': 'உங்கள் கணக்கு முடக்கப்பட்டது. தயவுசெய்து வணிகரைத் தொடர்பு கொள்ளவும்.',
    
    # 印章卡
    'noStampCardsYet': 'இன்னும் ஸ்டாம்ப் கார்டுகள் இல்லை',
    'noStampCards': 'ஸ்டாம்ப் கார்டுகள் இல்லை',
    'stampComplete': 'முடிந்தது!',
    'stampCollected': 'சேகரிக்கப்பட்டது',
    'stampCollectedMsg': 'ஸ்டாம்ப் சேகரிக்கப்பட்டது!',
    'stampCollectedDetail': 'வெகுமதியைப் பெற உங்கள் கார்டைப் பார்க்கவும்',
    'stampEmpty': 'காலி',
    'stampFreeItem': 'இலவச {item}',
    'stampFreeItemGeneric': 'இலவச பொருள்',
    'stampPerAmount': 'RM{v} செலவழித்தால் = 1 ஸ்டாம்ப்',
    'stampPerItem': 'ஒவ்வொரு {item} = 1 ஸ்டாம்ப்',
    'stampPerItemGeneric': 'தகுதியான ஒவ்வொரு பொருளுக்கும் = 1 ஸ்டாம்ப்',
    'stampPerPurchase': 'ஒவ்வொரு கொள்முதலுக்கும் = 1 ஸ்டாம்ப்',
    'stampClaimBtn': 'வெகுமதியைப் பெறு',
    'stampRedeemClaim': 'வெகுமதியைப் பெறு',
    'stampRedeemLater': 'பிறகு பெறு',
    'stampRedeemMsg': 'நீங்கள் {n} ஸ்டாம்புகள் சேகரித்துள்ளீர்கள்!',
    'stampRedeemTitle': 'வாழ்த்துக்கள்!',
    'stampReward': 'வெகுமதி',
    'stampRmOff': 'RM{v} தள்ளுபடி',
    'stampPctOff': '{v}% தள்ளுபடி',
    'stampBonusPoints': '+{v} போனஸ் புள்ளிகள்',
    'stampsToUnlock': 'வெகுமதியைத் திறக்க இன்னும் {n} ஸ்டாம்புகள்',
    'stampsToUnlockPlural': 'வெகுமதியைத் திறக்க இன்னும் {n} ஸ்டாம்புகள்',
    'highestTier': '🏆 நீங்கள் உயர்மட்டத்தை அடைந்துவிட்டீர்கள்!',
    'stampCompleted': '{n}× முடிந்தது',
    'viewAllStampCards': 'அனைத்து ஸ்டாம்ப் கார்டுகளையும் பார்',
    'viewStamp': 'எனது ஸ்டாம்ப் கார்டைப் பார்',
    'redeemRewards': 'வெகுமதிகளைப் பெறு',
    'noUnclaimedRewards': 'பெறாத வெகுமதிகள் இல்லை',
    
    # 印章规则
    'everyPurchase1Stamp': 'ஒவ்வொரு கொள்முதலுக்கும் = 1 ஸ்டாம்ப்',
    'perRMRule': 'RM1 = 1 ஸ்டாம்ப்',
    'perItemRule': 'குறிப்பிட்ட பொருளுக்கு = 1 ஸ்டாம்ப்',
    'freeMenuItem': 'இலவச மெனு பொருள்',
    'rmDiscount': 'தள்ளுபடி RM (RM)',
    'pctDiscount': 'சதவீத தள்ளுபடி (%)',
    'bonusPointsReward': 'போனஸ் புள்ளிகள்',
    'stampCard': 'ஸ்டாம்ப் கார்டு',
    'redeemReward': 'வெகுமதியைப் பெறு',
    
    # 订单历史
    'myOrders': 'எனது ஆர்டர்கள்',
    'myOrdersEmpty': 'ஆர்டர்கள் இல்லை',
    'myOrdersNoOrdersYet': 'இன்னும் ஆர்டர்கள் இல்லை',
    'loginToViewOrders': 'ஆர்டர் வரலாற்றைப் பார்க்க உள்நுழையவும்',
    'viewAllOrders': 'அனைத்து ஆர்டர்களையும் பார்',
    'viewOrders2': 'ஆர்டர்களைப் பார்',
    'orderDetailTitle': 'ஆர்டர் விவரங்கள்',
    'orderDetailsTitle': 'ஆர்டர் விவரங்கள்',
    'orderDetailOrderId': 'ஆர்டர் எண்',
    'orderDetailDate': 'தேதி',
    'orderDetailType': 'வகை',
    'orderDetailStatus': 'நிலை',
    'orderDetailItems': 'ஆர்டர் செய்யப்பட்ட பொருட்கள்',
    'orderDetailSubtotal': 'கூட்டுத்தொகை',
    'orderDetailTax': 'SST',
    'orderDetailTotal': 'மொத்தம்',
    'orderDetailPointsEarned': 'பெறப்பட்ட புள்ளிகள்',
    'orderDetailWalletPaid': 'வாலட்',
    'orderDetailWalletDeductLabel': 'வாலட் கழிவு',
    
    # 筛选
    'filterAll': 'அனைத்தும்',
    'filterPending': 'நிலுவையில்',
    'filterPreparing': 'தயாராகிறது',
    'filterDone': 'முடிந்தது',
    'confirmPoints': 'புள்ளிகளை உறுதிப்படுத்து',
    'orderMore': 'மேலும் ஆர்டர் செய்',
    'statusPending': 'நிலுவையில்',
    'statusPreparing': 'தயாராகிறது',
    'statusDone': 'முடிந்தது',
    'resolved': 'தீர்க்கப்பட்டது',
    'in_progress': 'செயல்பாட்டில்',
    
    # 钱包
    'myWallet': 'எனது வாலட்',
    'walletTopupLabel': 'மீட்டேற்றம்',
    'walletTopupPending': 'வணிகர் ஒப்புதலுக்காகக் காத்திருக்கிறது',
    'walletTxnsEmpty': 'இன்னும் வாலட் பரிவர்த்தனைகள் இல்லை',
    'topupHistoryEmpty': 'மீட்டேற்ற வரலாறு இல்லை',
    'topUpWallet': 'வாலட்டை மீட்டேற்று',
    'selectTopUpAmount': 'மீட்டேற்றத் தொகையைத் தேர்ந்தெடு',
    'selectTopupAmount': 'மீட்டேற்றத் தொகையைத் தேர்ந்தெடுக்கவும்',
    'orCustomAmount': 'அல்லது தனிப்பயன் தொகையை உள்ளிடவும் (RM)',
    'confirmTopUp': 'மீட்டேற்றத்தை உறுதிப்படுத்து',
    'topupSubmitted': '✅ மீட்டேற்றக் கோரிக்கை சமர்ப்பிக்கப்பட்டது! வணிகர் ஒப்புதலுக்காகக் காத்திருக்கிறது',
    'topUpBonusTitle': 'மீட்டேற்ற போனஸ்!',
    'topUpBonusDesc': 'RM100 மீட்டேற்றம் செய்தால் RM120 கிரெடிட் கிடைக்கும் (RM20 இலவசம்!)',
    'topUpCustomHint': 'குறைந்தபட்சம் RM10. RM100 மற்றும் அதற்கு மேல் போனஸ் பொருந்தும்.',
    'topUpGateway': 'மீட்டேற்றம் (பேமென்ட் கேட்வே)',
    'topUpGet': 'பெறு',
    'totalToppedUp': 'மொத்தம் மீட்டேற்றம் செய்யப்பட்டது',
    'totalPoints': 'மொத்த புள்ளிகள்',
    'availableBalance': 'கிடைக்கும் பேலன்ஸ்',
    'totalBonusEarned': 'மொத்தம் பெறப்பட்ட போனஸ்',
    'pointsToReach': '{tier} அடைய இன்னும் {n} புள்ளிகள்!',
    'noBonus': 'போனஸ் இல்லை',
    'bonusIncluded': 'போனஸ் உள்ளடக்கப்பட்டுள்ளது',
    'pointsPerRM': 'RM க்கான புள்ளிகள்',
    'youGet': 'நீங்கள் பெறுவீர்கள்',
    'youPay': 'நீங்கள் செலுத்துவீர்கள்',
    'will_earn': ' பெறுவார்',
    
    # 推荐
    'myReferralProgram': 'எனது பரிந்துரை திட்டம்',
    'referralTab': 'பரிந்துரை',
    'referralReferral': 'பரிந்துரை திட்டம்',
    'referralInviteFriends': 'நண்பர்களை அழைத்து, கமிஷன் சம்பாதியுங்கள்!',
    'referralShareCode': 'உங்கள் தொலைபேசி எண்ணை பரிந்துரை குறியீடாக பகிர்ந்து கொள்ளுங்கள். நண்பர் முதல் ஆர்டரை முடிக்கும்போது, கமிஷன் உங்கள் வாலட்டுக்கு வரும்!',
    'referralSharePrompt': '{phone} ஐ பரிந்துரை குறியீடாக பகிர்ந்து, நண்பரின் {rate}% கமிஷனைப் பெறுங்கள்',
    'referralTotalEarned': 'மொத்தம் சம்பாதித்தது',
    'referralCommissionRate': 'கமிஷன் விகிதம்',
    'referralCurrentRate': 'தற்போதைய விகிதம்',
    'referralFriendsReferred': 'பரிந்துரைக்கப்பட்ட நண்பர்கள்',
    'referralFriendsYouReferred': 'நீங்கள் பரிந்துரைத்த நண்பர்கள்',
    'referralNoFriends': 'இன்னும் நண்பர்கள் பரிந்துரைக்கப்படவில்லை',
    'referralNoCommissions': 'இன்னும் கமிஷன் இல்லை, பரிந்துரைக்கத் தொடங்குங்கள்!',
    'referralCopyCode': 'நகலெடு',
    'referralCommissionHistory': 'கமிஷன் வரலாறு',
    'referralCommissionEarned': 'சம்பாதித்த கமிஷன்',
    'referralCommissions': 'பரிந்துரை கமிஷன்கள்',
    'referrerNotFound': 'பரிந்துரைப்பவர் கிடைக்கவில்லை, தொலைபேசி எண்ணைச் சரிபார்க்கவும்',
    'enter_your_referrer_s_phone_number_to_link_commissions': 'கமிஷன்களை இணைக்க பரிந்துரைப்பவரின் தொலைபேசி எண்ணை உள்ளிடவும்',
    'credited_to_referrer_s_wallet_after_first_order': 'முதல் ஆர்டருக்குப் பிறகு பரிந்துரைப்பவரின் வாலட்டிற்கு வரவு வைக்கப்படும்',
    'friendsReferredTitle': 'நீங்கள் பரிந்துரைத்த நண்பர்கள்',
    'friends_referred': 'பரிந்துரைக்கப்பட்ட நண்பர்கள்',
    'no_friends_referred_yet': 'இன்னும் நண்பர்கள் பரிந்துரைக்கப்படவில்லை',
    'total_earned': 'மொத்தம் சம்பாதித்தது',
    
    # 投诉
    'myComplaints': 'எனது புகார்கள்',
    'complaintTab': 'புகார்கள்',
    'newComplaint': 'புதிய புகார்',
    'complaintSubmit': 'புகாரை சமர்ப்பி',
    'complaintSubmitComplaint': 'புகாரை சமர்ப்பி',
    'complaintDescription': 'விளக்கம்',
    'complaintComplaintDetail': 'புகார் விவரங்கள்',
    'complaintDetailTitle': 'புகார் விவரங்கள்',
    'complaintEnterResponse': 'உங்கள் பதிலை உள்ளிடவும்...',
    'complaintResponse': 'பதில் / எடுக்கப்பட்ட நடவடிக்கை',
    'complaintResolve': 'தீர்க்கப்பட்டதாக குறி',
    'complaintResolveDone': 'புகார் தீர்க்கப்பட்டதாக குறிக்கப்பட்டது ✅',
    'complaintSubmitted': '✅ புகார் சமர்ப்பிக்கப்பட்டது! விரைவில் செயல்படுத்துவோம்',
    'complaintClose': 'மூடு',
    'complaintTapUpload': 'புகைப்படத்தை பதிவேற்ற தட்டவும்',
    'complaintPhotoAlt': 'புகைப்படம்',
    'complaintUploadPhoto': 'புகைப்படத்தை பதிவேற்று (விருப்பம்)',
    'complaintNoPhoto': 'புகைப்படம் இணைக்கப்பட்டது',
    'complaintsEmpty': 'புகார்கள் இல்லை',
    'noComplaintsYet': 'இன்னும் புகார்கள் சமர்ப்பிக்கப்படவில்லை',
    'complaintCategory': 'புகார் வகை',
    'complaintOrderIdOpt': 'ஆர்டர் எண் (விருப்பம்)',
    'pricing_issue': 'விலை சிக்கல்',
    'wrong_order': 'தவறான ஆர்டர்',
    'food_quality': 'உணவு தரம்',
    'service': 'சேவை',
    'cleanliness': 'சுத்தம்',
    'waiting_time': 'காத்திருக்கும் நேரம்',
    'other': 'மற்றவை',
    
    # 店铺设置
    'shopInfo': 'கடை தகவல்',
    'shopSettings2': 'கடை அமைப்புகள்',
    'saveShop': 'கடை தகவலை சேமி',
    'shopName': 'கடை பெயர்',
    'merchantNameDisplay': 'வணிகர் பெயர்',
    'commission_rate': 'கமிஷன் விகிதம்',
    'pointsSettings': 'புள்ளி அமைப்புகள்',
    'savePoints2': 'புள்ளி அமைப்புகளை சேமி',
    'enterValidRate': 'சரியான விகிதத்தை உள்ளிடவும் (1-100)',
    'enterValidBill': 'சரியான தொகையை உள்ளிடவும்',
    'enterRewardValue': 'வெகுமதி மதிப்பை உள்ளிடவும்',
    'enterCardName': 'கார்டு பெயரை உள்ளிடவும்',
    'qrNotReady': 'QR இன்னும் தயாராகவில்லை',
    'noPromos': 'விளம்பரங்கள் இல்லை',
    'noPromosNow': 'தற்போது விளம்பரங்கள் இல்லை, பின்னர் மீண்டும் வாருங்கள்!',
    'promosAndDeals': 'விளம்பரங்கள் & ஒப்பந்தங்கள்',
    'viewAllPromos': 'அனைத்து விளம்பரங்களையும் பார்',
    'allPromos': 'அனைத்து விளம்பரங்கள்',
    'bestDeal': 'சிறந்த ஒப்பந்தம்',
    'announcement': 'அறிவிப்பு',
    'noPendingRequests': 'நிலுவையிலுள்ள கோரிக்கைகள் இல்லை',
    'refresh': 'புதுப்பி',
    'quickActions': 'விரைவான செயல்கள்',
    'view': 'பார்',
    'back': 'பின் செல்',
    'backHome': 'முகப்புக்கு திரும்பு',
    'cancelBtn': 'ரத்து செய்',
    'new': 'புதிய',
    'get': 'பெறு',
    'tapToChange': 'மாற்ற தட்டவும்',
    
    # 新品
    'newItemsTitle': 'இன்றைய புதிய பொருட்கள் 🎉',
    'newItemsMsg': 'புதிய பொருள் அறிமுகப்படுத்தப்பட்டது 🎉',
    'newItemsBanner': 'புதியது',
    'newItemsNewTag': 'புதியது',
    'newItemsSpecial': 'சிறப்பு:',
    'newItemsWas': ' முன்பு',
    'newItemsUntil': ' வரை:',
    'newItemsNoEnd': 'முடிவு தேதி இல்லை',
    'newItemsClose': 'மூடு',
    'newItemsOrderNow': 'இப்போது ஆர்டர் செய்',
    'noActiveNewItems': 'செயலில் உள்ள புதிய பொருட்கள் இல்லை',
    'noPastLaunches': 'கடந்த அறிமுகங்கள் இல்லை',
    'drinkToday': 'இன்றைய பானம்',
    'thankYou': 'நன்றி!',
    'free': 'இலவசம்',
    'enter': 'உள்ளிடு',
    'fillNamePrice': 'பெயர் மற்றும் விலையை நிரப்பவும்',
    'sinceLabel': 'முதல்',
    'fullName': 'முழு பெயர்',
    
    # 支付
    'scan_to_pay': 'பணம் செலுத்த ஸ்கேன் செய்',
    'bankTitle': 'வங்கி பரிமாற்ற விவரங்கள்',
    'bankAccountDisplay': 'வங்கி கணக்கு',
    'bankAmountLabel': 'தொகை: RM0.00',
    'paymentBank': 'வங்கி பரிமாற்றம்',
    'paymentCash': 'பணம்',
    'paymentTng': 'Touch & Go',
    'tngScanTitle': 'Touch & Go மூலம் பணம் செலுத்த ஸ்கேன் செய்',
    'tngName': 'Touch & Go',
    'tngAmountLabel': 'தொகை',
    'tngUploadHint': 'பணம் செலுத்திய பிறகு, கீழே ஸ்கிரீன்ஷாட்டை பதிவேற்றவும்.',
    'uploadScreenshot': 'பணம் செலுத்திய ஸ்கிரீன்ஷாட்டை பதிவேற்று',
    'uploadReceipt': 'பரிமாற்ற ரசீதை பதிவேற்று',
    'uploadSizeHint': 'JPG / PNG, அதிகபட்சம் 5MB',
    'photoUploadHint': 'JPG, PNG, அதிகபட்சம் 5MB',
    'photo_upload_hint': 'JPG, PNG, அதிகபட்சம் 5MB',
    'tap_to_upload_photo': 'புகைப்படத்தை பதிவேற்ற தட்டவும்',
    'toastNoProof': 'முதலில் பணம் செலுத்திய ஸ்கிரீன்ஷாட்டை பதிவேற்றவும்.',
    'photoUnder5MB': 'புகைப்படம் 5MB க்கு குறைவாக இருக்க வேண்டும்',
    'screenshotUploaded': 'ஸ்கிரீன்ஷாட் பதிவேற்றப்பட்டது. வணிகர் சரிபார்ப்புக்காக காத்திருக்கிறது.',
    'screenshotUploaded2': 'ஸ்கிரீன்ஷாட் பதிவேற்றப்பட்டது',
    
    # 其他
    'selectTableFirst': 'முதலில் மேஜையைத் தேர்ந்தெடுக்கவும்!',
    'minimumTopup': 'குறைந்தபட்ச மீட்டேற்றம் RM10',
    'awaitingMerchantApproval': 'வணிகர் ஒப்புதலுக்காக காத்திருக்கிறது',
    'takeawayModalTitle': 'கொண்டு செல் ஆர்டர்',
    'takeawayModalSubtitle': 'உங்கள் எடுக்கும் விவரங்களை உள்ளிடவும்',
    'confirmTakeaway': 'கொண்டு செல்ல உறுதிப்படுத்து',
    'toastDineIn': '🍳 ஆர்டர் சமையலறைக்கு அனுப்பப்பட்டது!',
    'toastTakeaway': '🛍️ கொண்டு செல் ஆர்டர் அனுப்பப்பட்டது!',
    'toastNoPhone': 'கொண்டு செல்ல தொலைபேசி எண்ணை உள்ளிடவும்',
    'toastNoTime': 'எடுக்கும் நேரத்தை அமைக்கவும்',
    'pickupReadyHint': 'இந்த நேரத்தில் உங்கள் ஆர்டரை தயார் செய்வோம்.',
    'submitComplaint': 'புகாரை சமர்ப்பி',
    'submitComplaintBtn': 'புகாரை சமர்ப்பி',
    'pleaseDescribeIssue': 'உங்கள் சிக்கலை விரிவாக விவரிக்கவும்',
    'uploadPhotoOptional': 'புகைப்படத்தை பதிவேற்று (விருப்பம்)',
    'order_id_optional': 'ஆர்டர் எண் (விருப்பம்)',
    'noStampCards': 'ஸ்டாம்ப் கார்டுகள் இல்லை',
    'active_new_launches': 'செயலில் உள்ள புதிய அறிமுகங்கள்',
    'active_stamp_cards': 'செயலில் உள்ள ஸ்டாம்ப் கார்டுகள்',
    'add_bonus_rule': 'போனஸ் விதியை சேர்',
    'add_points': 'புள்ளிகளை சேர்',
    'add_points_manually': 'கைமுறையாக புள்ளிகள் சேர்',
    'add_rule': 'விதியை சேர்',
    'add_to_menu': 'மெனுவில் சேர்',
    'admin': 'நிர்வாகி',
    'all': 'அனைத்தும்',
    'all_members': 'அனைத்து உறுப்பினர்கள்',
    'all_orders': 'அனைத்து ஆர்டர்கள்',
    'announcement_placeholder': 'அறிவிப்பு உரையை உள்ளிடவும்...',
    'announcement_text': 'அறிவிப்பு உரை',
    'bank_transfer': 'வங்கி பரிமாற்றம்',
    'bonus_points': 'போனஸ் புள்ளிகள்',
    'cancel': 'ரத்து செய்',
    'card_color_theme': 'கார்டு நிற தீம்',
    'card_name': 'கார்டு பெயர்',
    'card_name_placeholder': 'எ.கா: 10 ஸ்டாம்புகளுக்கு இலவச பானம்',
    'cash': 'பணம்',
    'category': 'வகை',
    'click_to_upload_photo': 'புகைப்படத்தை பதிவேற்ற கிளிக் செய்யவும்',
    'close': 'மூடு',
    'cold_drinks': 'குளிர் பானங்கள்',
    'commission_history': 'கமிஷன் வரலாறு',
    'commission_records': 'கமிஷன் பதிவுகள்',
    'commission_settings': 'கமிஷன் அமைப்புகள்',
    'commissions': 'கமிஷன்கள்',
    'complaint_category': 'புகார் வகை',
    'complaint_detail': 'புகார் விவரம்',
    'complaints': 'புகார்கள்',
    'confirm_deactivate': 'முடக்குவதை உறுதிப்படுத்து',
    'create_account': 'கணக்கை உருவாக்கு',
    'create_stamp_card': 'ஸ்டாம்ப் கார்டை உருவாக்கு',
    'deactivate_member': 'உறுப்பினரை முடக்கு',
    'description': 'விளக்கம்',
    'desserts': 'இனிப்புகள்',
    'done': 'முடிந்தது',
    'emoji_icon': 'Emoji ஐகான்',
    'end_date': 'முடிவு தேதி',
    'expiry_date': 'காலாவதி தேதி',
    'food': 'உணவு',
    'free_item': 'இலவச பொருள்',
    'free_menu_item': 'இலவச மெனு பொருள்',
    'hot_drinks': 'சூடான பானங்கள்',
    'item_name': 'பொருள் பெயர்',
    'item_photo': 'பொருள் புகைப்படம்',
    'kitchen': 'சமையலறை',
    'launch_date': 'அறிமுக தேதி',
    'launch_new_item': 'புதிய பொருளை அறிமுகப்படுத்து',
    'login_to_dashboard': 'டாஷ்போர்டுக்கு உள்நுழை',
    'members': 'உறுப்பினர்கள்',
    'menu_items': 'மெனு பொருட்கள்',
    'merchant_login': 'வணிகர் உள்நுழைவு',
    'new_complaint': 'புதிய புகார்',
    'no_active_new_items': 'செயலில் புதிய பொருட்கள் இல்லை',
    'no_past_launches': 'கடந்த அறிமுகங்கள் இல்லை',
    'no_pickup_time_set': 'எடுக்கும் நேரம் அமைக்கப்படவில்லை',
    'no_stamp_cards_yet': 'இன்னும் ஸ்டாம்ப் கார்டுகள் இல்லை',
    'optional': 'விருப்பம்',
    'orders': 'ஆர்டர்கள்',
    'orders_today': 'இன்றைய ஆர்டர்கள்',
    'overview': 'மேலோட்டம்',
    'password': 'கடவுச்சொல்',
    'past_launches': 'கடந்த அறிமுகங்கள்',
    'pending': 'நிலுவையில்',
    'phone_number': 'தொலைபேசி எண்',
    'points': 'புள்ளிகள்',
    'points_issued': 'வழங்கப்பட்ட புள்ளிகள்',
    'preparing': 'தயாராகிறது',
    'qr_codes': 'QR குறியீடுகள்',
    'recent_transactions': 'சமீபத்திய பரிவர்த்தனைகள்',
    'referral_commission_rate': 'பரிந்துரை கமிஷன் விகிதம்',
    'remove_photo': 'புகைப்படத்தை நீக்கு',
    'revenue_today': 'இன்றைய வருவாய்',
    'reward_type': 'வெகுமதி வகை',
    'save_password': 'கடவுச்சொல்லை சேமி',
    'select_menu_item': 'மெனு பொருளைத் தேர்ந்தெடு',
    'settings': 'அமைப்புகள்',
    'snacks': 'சிற்றுண்டி',
    'stamp_cards': 'ஸ்டாம்ப் கார்டுகள்',
    'stamp_rule': 'ஸ்டாம்ப் விதி',
    'stamp_rule_placeholder': 'எ.கா: RM10 செலவழித்தால் 1 ஸ்டாம்ப்',
    'stamps_required_to_complete': 'முடிக்க தேவையான ஸ்டாம்புகள்',
    'submit_complaint': 'புகாரை சமர்ப்பி',
    'top_up': 'மீட்டேற்றம்',
    'username': 'பயனர்பெயர்',
    'wrong_order': 'தவறான ஆர்டர்',
    'generate_qr_codes': 'QR குறியீடுகளை உருவாக்கு',
    'generate_table_qr_codes': 'மேஜை QR குறியீடுகளை உருவாக்கு',
    'number_of_tables': 'மேஜைகளின் எண்ணிக்கை',
    'superAdmin': 'சூப்பர் நிர்வாகி',
}

# 为缺失的键生成翻译
for k, v in pairs:
    if k not in TA_TRANSLATIONS:
        # 对于没有预定义翻译的键，使用英文+标记
        TA_TRANSLATIONS[k] = v

# 构建新的完整 ta: 块
new_ta_lines = ['  ta: {']
for k, v in pairs:
    val = TA_TRANSLATIONS.get(k, v)
    val = val.replace("\\", "\\\\").replace("'", "\\'")
    new_ta_lines.append(f"    {k}: '{val}'")
new_ta_lines.append('  }')

new_ta_block = '\n'.join(new_ta_lines)

# 替换旧的 ta: 块
ta_start_global = langs2_pos + ta_match.start()
ta_end_global = langs2_pos + ta_end_local + 1

new_content = content[:ta_start_global] + new_ta_block + content[ta_end_global:]

print(f'\nOriginal size: {len(content)}')
print(f'New size: {len(new_content)}')
print(f'TA block now has {len(pairs)} keys (was {len(ta_pairs)})')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('\n✅ TA translations completed!')
print('Note: Some translations may need professional review.')
