import re

html_path = 'C:/Users/Administrator/CodeBuddy/20260416214625/deploy/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# The merchant nav tabs use data-i18n but should use data-mi18n
# Map of current data-i18n keys -> correct data-mi18n keys for MERCHANT_LANGS
nav_key_map = {
    'overview': 'mTabOverview',
    'orders': 'mTabOrders',
    'menu_items': 'mTabMenu',
    'members': 'mTabMembers',
    'new_items': 'mTabNewItems',
    'stamp_cards': 'mTabStamp',
    'top_up': 'mTabTopup',
    'complaints': 'mTabComplaints',
    'commissions': 'mTabCommissions',
    'qr_codes': 'mTabQR',
    'settings': 'mTabSettings',
    'ads': 'mTabAds',
}

# Also fix the overview page stats and quick actions
overview_key_map = {
    'members': 'mStatMembers',
    'points_issued': 'mStatPoints',
    'orders_today': 'mStatOrders',
    'revenue_today': 'mStatRevenue',
    'quickActions': 'mTitleQuickActions',
    'viewOrders2': 'mBtnViewOrders2',
    'menuMgmt2': 'mBtnMenuMgmt2',
    'shopSettings2': 'mBtnShopSettings2',
    'kitchenDisplay2': 'mBtnKitchenDisplay2',
    'add_points_manually': 'mAddPointsManually',
    'phone_number': 'mPhoneNumber',
    'bill_amount': 'mBillAmount',
    'will_earn': 'mWillEarn',
    'points': 'mPoints',
    'add_points': 'mAddPoints',
}

count = 0
for old_key, new_key in {**nav_key_map, **overview_key_map}.items():
    # Replace data-i18n="old_key" with data-mi18n="new_key" in the merchant section only
    # We need to be careful to only replace within the merchant dashboard area
    pattern = f'data-i18n="{old_key}"'
    replacement = f'data-mi18n="{new_key}"'
    new_html, n = re.subn(pattern, replacement, html)
    if n > 0:
        html = new_html
        count += n
        print(f'  Replaced: data-i18n="{old_key}" -> data-mi18n="{new_key}" ({n}x)')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nTotal replacements: {count}')
print('Done!')
