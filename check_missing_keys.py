import sys, re
sys.stdout.reconfigure(encoding='utf-8')

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# 检查所有新增的 key 是否在 zh 和 ms 中存在
new_keys = [
    'floatViewCart', 'tngName', 'bankAmountLabel', 'mLoginHint',
    'filterAll', 'filterPending', 'filterPreparing', 'filterDone',
    'filterAllC', 'complaintOpenBtn', 'complaintInProgressBtn', 'complaintResolvedBtn',
    'mPromoPriceLbl', 'noActiveNewItems', 'noPastLaunches',
    'mRulePerOrderOpt', 'mRulePerAmountOpt', 'mRulePerItemOpt',
    'mRewardFreeItemOpt', 'mRewardFlatDiscountOpt', 'mRewardBonusPointsOpt', 'mFreeItemLabel',
    'noStampCardsYet', 'searchForAMember', 'noPendingRequests',
    'minAmount', 'expiryDate',
    'myShopLink', 'shopLinkDesc', 'copyLinkBtn', 'shopQRCodeLabel',
    'qrHowToUse', 'qrPrintHint', 'qrTableHint', 'printShopQRBtn', 'tableQrDesc',
    'referralCommissionRateLabel', 'currentRateLbl', 'noPendingPaymentProofs',
    'leaveEmptyBanner', 'smallTextHint', 'bigTitleHint', 'higherShowsFirst',
    'kitchenDisplayLbl', 'refreshLbl', 'statusNewLbl', 'preparingLbl', 'doneLbl',
    'getNotifiedWhenReady', 'enableNotificationsBtn', 'maybeLaterBtn',
    'referralProgramTitle', 'referralProgramDescText', 'copyReferralBtn',
    'commissionHistoryTitle', 'friendsReferredTitle',
    'complaintDetailTitle', 'markResolvedBtn', 'orderDetailsTitle',
]

print(f'{"Key":<35} {"EN":<6} {"ZH":<6} {"MS":<6}')
print('-' * 55)
missing_zh = []
missing_ms = []

for key in new_keys:
    en = bool(re.search(rf'\b{key}\s*:', js))
    # 更精确：检查是否在 zh 块中
    zh_idx = js.find('zh:')
    ms_idx = js.find('ms:')
    zh_block = js[zh_idx:ms_idx] if zh_idx > 0 and ms_idx > 0 else ''
    ms_block = js[ms_idx:js.find('\n, ta:') if ms_idx > 0 else '']
    
    in_zh = bool(re.search(rf'\b{key}\s*:', zh_block)) if zh_block else False
    in_ms = bool(re.search(rf'\b{key}\s*:', ms_block)) if ms_block else False
    
    status = f'{"✅" if en else "❌"}     {"✅" if in_zh else "❌"}     {"✅" if in_ms else "❌"}'
    print(f'{key:<35} {status}')
    if not in_zh: missing_zh.append(key)
    if not in_ms: missing_ms.append(key)

print(f'\nMissing ZH ({len(missing_zh)}): {missing_zh}')
print(f'Missing MS ({len(missing_ms)}): {missing_ms}')
