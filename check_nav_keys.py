with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find LANGS object (customer side, first one)
langs_pos = js.find('const LANGS')
print(f'LANGS at: {langs_pos}')

# Check for merchant nav keys in LANGS
search_area = js[langs_pos:langs_pos+50000]
for key in ['overview', 'menuMgmt2', 'viewOrders2', 'shopSettings2', 'kitchenDisplay2', 'quickActions', 'add_points_manually', 'members', 'points_issued', 'orders_today', 'revenue_today']:
    found = key in search_area
    print(f'  LANGS has "{key}": {found}')

# Also check if these keys exist in MERCHANT_LANGS (with or without prefix)
ml_pos = js.find('const MERCHANT_LANGS')
ml_area = js[ml_pos:ml_pos+100000]
print()
print('In MERCHANT_LANGS:')
for key in ['overview', 'menuMgmt2', 'viewOrders2', 'shopSettings2', 'kitchenDisplay2', 'quickActions', 'add_points_manually', 'mTabOverview', 'mBtnViewOrders2', 'mBtnMenuMgmt2', 'mBtnShopSettings2', 'mBtnKitchenDisplay2', 'mTitleQuickActions', 'mAddPointsManually', 'mStatMembers', 'mStatPointsIssued', 'mStatOrdersToday', 'mStatRevenueToday']:
    found = key in ml_area
    print(f'  "{key}": {found}')
