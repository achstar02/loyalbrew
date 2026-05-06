#!/usr/bin/env python3
"""Fix translation issues in LoyalBrew app.js"""

import re

FILE = r"C:\Users\Administrator\CodeBuddy\20260416214625\app.js"

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

original = content

# ── 1. EN: Remove duplicate trailing block (after orderDetailWalletDeductLabel) ──
# The EN block ends at "orderDetailWalletDeductLabel: 'Wallet Deduction'," + "  },\n"
# then there's a duplicate block starting at "stampCollectedDetail:" through "orderDetailWalletDeductLabel: 'Wallet Deduction',\n  },"
en_dup_pattern = (
    r"orderDetailWalletDeductLabel: 'Wallet Deduction',\n  },\n"
    r"    stampCollectedDetail: 'View your card to claim rewards',\n"
    r"    walletTopupPending: 'Awaiting merchant approval',\n"
    r"    myOrdersEmpty: 'No orders found',\n"
    r"    myOrdersNoOrdersYet: 'No orders yet',\n"
    r"    walletTxnsEmpty: 'No wallet transactions yet',\n"
    r"    topupHistoryEmpty: 'No top up history yet',\n"
    r"    complaintsEmpty: 'No complaints found',\n"
    r"    orderDetailTitle: 'Order Details',\n"
    r"    orderDetailOrderId: 'Order ID',\n"
    r"    orderDetailStatus: 'Status',\n"
    r"    orderDetailType: 'Type',\n"
    r"    orderDetailDate: 'Date',\n"
    r"    orderDetailItems: 'Items Ordered',\n"
    r"    orderDetailSubtotal: 'Subtotal',\n"
    r"    orderDetailTax: 'SST',\n"
    r"    walletTopupLabel: 'Top Up',\n"
    r"    paymentCash: 'Cash',\n"
    r"    paymentTng: 'Touch & Go',\n"
    r"    paymentBank: 'Bank Transfer',\n"
    r"    statusPending: 'Pending',\n"
    r"    statusPreparing: 'Preparing',\n"
    r"    statusDone: 'Done',\n"
    r"    stampRedeemTitle: 'Congratulations!',\n"
    r"    stampRedeemMsg: 'You\\'ve collected all stamps!',\n"
    r"    stampRedeemClaim: 'Claim Reward',\n"
    r"    stampRedeemLater: 'Maybe Later',\n"
    r"    newItemsTitle: 'What\\'s New at LoyalBrew!',\n"
    r"    newItemsMsg: 'Fresh launches just for you 🎉',\n"
    r"    newItemsOrderNow: 'Order Now',\n"
    r"    newItemsClose: 'Close',\n"
    r"    referralReferral: 'Referral Program',\n"
    r"    referralInviteFriends: 'Invite Friends, Earn Commission!',\n"
    r"    referralShareCode: 'Share your phone number as a referral code\. When your friend makes their first order, you earn a commission credited to your wallet!',\n"
    r"    referralCopyCode: 'Copy',\n"
    r"    referralFriendsReferred: 'Friends Referred',\n"
    r"    referralTotalEarned: 'Total Earned',\n"
    r"    referralCommissionRate: 'Commission Rate',\n"
    r"    referralCommissionHistory: 'Commission History',\n"
    r"    referralFriendsYouReferred: 'Friends You Referred',\n"
    r"    referralNoCommissions: 'No commissions yet\. Start referring!',\n"
    r"    referralNoFriends: 'No friends referred yet\.',\n"
    r"    complaintSubmitComplaint: 'Submit Complaint',\n"
    r"    complaintCategory: 'Complaint Category',\n"
    r"    complaintDescription: 'Description',\n"
    r"    complaintUploadPhoto: 'Upload Photo \(optional\)',\n"
    r"    complaintTapUpload: 'Tap to upload photo',\n"
    r"    complaintOrderIdOpt: 'Order ID \(optional\)',\n"
    r"    complaintSubmit: 'Submit Complaint',\n"
    r"    complaintMyComplaints: 'My Complaints',\n"
    r"    complaintComplaintDetail: 'Complaint Detail',\n"
    r"    complaintResponse: 'Response / Action Taken',\n"
    r"    complaintResolve: 'Mark Resolved',\n"
    r"    complaintClose: 'Close',\n"
    r"    complaintNoPhoto: 'Photo attached',\n"
    r"    complaintResolveDone: 'Complaint marked as resolved ✅',\n"
    r"    complaintDetailTitle: 'Complaint Detail',\n"
    r"    complaintEnterResponse: 'Enter your response\.\\.\\.',\n"
    r"    newItemsBanner: 'NEW',\n"
    r"    newItemsSpecial: 'Special:',\n"
    r"    newItemsWas: 'was',\n"
    r"    newItemsUntil: 'Until:',\n"
    r"    newItemsNoEnd: 'No end date',\n"
    r"    complaintPhotoAlt: 'Photo',\n"
    r"    awaitingMerchantApproval: 'Awaiting merchant approval',\n"
    r"    newItemsNewTag: 'NEW',\n"
    r"    stampComplete: 'COMPLETE!',\n"
    r"    complaintTab: 'Complaint',\n"
    r"    referralTab: 'Referral',\n"
    r"    orderDetailTotal: 'Total',\n"
    r"    orderDetailPointsEarned: 'Points Earned',\n"
    r"    orderDetailWalletPaid: 'Wallet',\n"
    r"    orderDetailWalletDeductLabel: 'Wallet Deduction',\n"
    r"  \},\n"
)

match = re.search(en_dup_pattern, content)
if match:
    print(f"[OK] Found EN duplicate block at pos {match.start()}-{match.end()}")
    content = content[:match.start()] + content[match.end():]
else:
    print("[SKIP] EN duplicate block not found (may already be fixed or pattern mismatch)")

# ── 2. ZH: Remove duplicate trailing block ──
# ZH block ends with "orderDetailWalletDeductLabel: '钱包扣款'," + "  },"
zh_dup_pattern = (
    r"orderDetailWalletDeductLabel: '钱包扣款',\n"
    r"    stampCollectedDetail: 'View your card to claim rewards',\n"
    r"    walletTopupPending: 'Awaiting merchant approval',\n"
    r"    myOrdersEmpty: 'No orders found',\n"
    r"    myOrdersNoOrdersYet: 'No orders yet',\n"
    r"    walletTxnsEmpty: 'No wallet transactions yet',\n"
    r"    topupHistoryEmpty: 'No top up history yet',\n"
    r"    complaintsEmpty: 'No complaints found',\n"
    r"    orderDetailTitle: 'Order Details',\n"
    r"    orderDetailOrderId: 'Order ID',\n"
    r"    orderDetailStatus: 'Status',\n"
    r"    orderDetailType: 'Type',\n"
    r"    orderDetailDate: 'Date',\n"
    r"    orderDetailItems: 'Items Ordered',\n"
    r"    orderDetailSubtotal: 'Subtotal',\n"
    r"    orderDetailTax: 'SST',\n"
    r"    walletTopupLabel: 'Top Up',\n"
    r"    paymentCash: 'Cash',\n"
    r"    paymentTng: 'Touch & Go',\n"
    r"    paymentBank: 'Bank Transfer',\n"
    r"    statusPending: 'Pending',\n"
    r"    statusPreparing: 'Preparing',\n"
    r"    statusDone: 'Done',\n"
    r"    stampRedeemTitle: 'Congratulations!',\n"
    r"    stampRedeemMsg: 'You\\'ve collected all stamps!',\n"
    r"    stampRedeemClaim: 'Claim Reward',\n"
    r"    stampRedeemLater: 'Maybe Later',\n"
    r"    newItemsTitle: 'What\\'s New at LoyalBrew!',\n"
    r"    newItemsMsg: 'Fresh launches just for you 🎉',\n"
    r"    newItemsOrderNow: 'Order Now',\n"
    r"    newItemsClose: 'Close',\n"
    r"    referralReferral: 'Referral Program',\n"
    r"    referralInviteFriends: 'Invite Friends, Earn Commission!',\n"
    r"    referralShareCode: 'Share your phone number as a referral code\. When your friend makes their first order, you earn a commission credited to your wallet!',\n"
    r"    referralCopyCode: 'Copy',\n"
    r"    referralFriendsReferred: 'Friends Referred',\n"
    r"    referralTotalEarned: 'Total Earned',\n"
    r"    referralCommissionRate: 'Commission Rate',\n"
    r"    referralCommissionHistory: 'Commission History',\n"
    r"    referralFriendsYouReferred: 'Friends You Referred',\n"
    r"    referralNoCommissions: 'No commissions yet\. Start referring!',\n"
    r"    referralNoFriends: 'No friends referred yet\.',\n"
    r"    complaintSubmitComplaint: 'Submit Complaint',\n"
    r"    complaintCategory: 'Complaint Category',\n"
    r"    complaintDescription: 'Description',\n"
    r"    complaintUploadPhoto: 'Upload Photo \(optional\)',\n"
    r"    complaintTapUpload: 'Tap to upload photo',\n"
    r"    complaintOrderIdOpt: 'Order ID \(optional\)',\n"
    r"    complaintSubmit: 'Submit Complaint',\n"
    r"    complaintMyComplaints: 'My Complaints',\n"
    r"    complaintComplaintDetail: 'Complaint Detail',\n"
    r"    complaintResponse: 'Response / Action Taken',\n"
    r"    complaintResolve: 'Mark Resolved',\n"
    r"    complaintClose: 'Close',\n"
    r"    complaintNoPhoto: 'Photo attached',\n"
    r"    complaintResolveDone: 'Complaint marked as resolved ✅',\n"
    r"    complaintDetailTitle: 'Complaint Detail',\n"
    r"    complaintEnterResponse: 'Enter your response\.\\.\\.',\n"
    r"    newItemsBanner: 'NEW',\n"
    r"    newItemsSpecial: 'Special:',\n"
    r"    newItemsWas: 'was',\n"
    r"    newItemsUntil: 'Until:',\n"
    r"    newItemsNoEnd: 'No end date',\n"
    r"    complaintPhotoAlt: 'Photo',\n"
    r"    awaitingMerchantApproval: 'Awaiting merchant approval',\n"
    r"    newItemsNewTag: 'NEW',\n"
    r"    stampComplete: 'COMPLETE!',\n"
    r"    complaintTab: 'Complaint',\n"
    r"    referralTab: 'Referral',\n"
    r"    orderDetailTotal: 'Total',\n"
    r"    orderDetailPointsEarned: 'Points Earned',\n"
    r"    orderDetailWalletPaid: 'Wallet',\n"
    r"    orderDetailWalletDeductLabel: 'Wallet Deduction',\n"
    r"  \},\n"
)

match2 = re.search(zh_dup_pattern, content)
if match2:
    print(f"✓ Found ZH duplicate block at pos {match2.start()}-{match2.end()}")
    content = content[:match2.start()] + content[match2.end():]
else:
    print("✗ ZH duplicate block not found (may already be fixed or pattern mismatch)")

# ── 3. ZH: Add missing walletBalance ──
# walletBalance should be after useWallet in the ZH section
# Current ZH has: useWallet: '使用钱包余额付款', walletBalance is MISSING
# Fix: insert walletBalance: '余额' after useWallet in ZH

# Find ZH section and add walletBalance
zh_pattern = r"(    useWallet: '使用钱包余额付款',)\n    (paymentMethod:)"
zh_replacement = r"\1\n    walletBalance: '余额',\n    \2"
new_content = re.sub(zh_pattern, zh_replacement, content)
if new_content != content:
    print("[OK] Added missing walletBalance to ZH")
    content = new_content
else:
    print("[SKIP] walletBalance in ZH not inserted (may already exist or pattern mismatch)")

# ── 4. TA: Fix walletBalance position ──
# TA has walletBalance after topUpGet/noBonus/bestDeal/free area, should be near payWallet/useWallet
# Current TA near topUpWallet: walletBalance: 'இருப்பு', (wrong position)
# Fix: remove from wrong position, ensure it's near payWallet/useWallet

# First, remove walletBalance from TA's wrong position (after topUpGet area)
# The wrong placement is: topUpGet: 'பெறுங்கள்', noBonus: 'போனஸ் இல்லை', bestDeal: 'சிறந்த டீல்', free: 'இலவசம்',
# followed by orCustomAmount, then walletBalance wrongly placed after topUpGet

# Remove walletBalance from wrong position (after free: 'இலவசம்',)
ta_remove_wrong = re.sub(
    r"    free: 'இலவசம்',\n    walletBalance: 'இருப்பு',\n",
    "    free: 'இலவசம்',\n",
    content
)
if ta_remove_wrong != content:
    print("✓ Removed walletBalance from wrong position in TA")
    content = ta_remove_wrong
else:
    print("✗ walletBalance not removed from wrong position (may not be there or already fixed)")

# Add walletBalance to TA in correct position (near payWallet/useWallet)
ta_add_correct = re.sub(
    r"(    useWallet: 'வாலட் இருப்பைப் பயன்படுத்து',)\n    (    paymentMethod:)",
    r"\1\n    walletBalance: 'இருப்பு',\n    \2",
    content
)
if ta_add_correct != content:
    print("✓ Added walletBalance to correct position in TA")
    content = ta_add_correct
else:
    # Try alternate useWallet text
    ta_add_correct2 = re.sub(
        r"(    useWallet: 'வாலட் இருப்பைப் பயன்படுத்து',)\n(    paymentMethod:)",
        r"\1\n    walletBalance: 'இருப்பு',\n\2",
        content
    )
    if ta_add_correct2 != content:
        print("✓ Added walletBalance to correct position in TA (alt)")
        content = ta_add_correct2
    else:
        print("✗ walletBalance not added to TA (useWallet text may differ)")

# Write the fixed file
with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDone! File written to {FILE}")
print(f"Changes: {len(original) - len(content)} chars removed ({len(original)} → {len(content)})")
