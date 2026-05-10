import re

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Map unprefixed keys (used in HTML) to their actual MERCHANT_LANGS keys
# Format: unprefixed_key: actual_key
KEY_ALIASES = {
    # Tab navigation
    'overview': 'mTabOverview',
    'orders': 'mTabOrders',
    'menu_items': 'mTabMenu',
    'members': 'mTabMembers',
    'new_items': 'mTabNewItems',
    'stamp_cards': 'mTabStamp',
    'topup': 'mTabTopup',
    'complaints': 'mTabComplaints',
    'commissions': 'mTabCommissions',
    'qr_codes': 'mTabQR',
    'settings': 'mTabSettings',
    'ads': 'mTabAds',
    # Stats cards
    'points_issued': 'mStatPointsIssued',
    'orders_today': 'mStatOrdersToday',
    'revenue_today': 'mStatRevenueToday',
    # Quick action buttons
    'myOrders': 'mBtnViewOrders2',
    'menuMgmt2': 'mBtnMenuMgmt2',
    'shopSettings2': 'mBtnShopSettings2',
    'kitchenDisplay2': 'mBtnKitchenDisplay2',
    # Overview content
    'quickActions': 'mTitleQuickActions',
    'add_points_manually': 'mAddPointsManually',
    'members2': 'mStatMembers',  # Overview shows members count
    # New Item page
    'launchNewItem': 'mNiLaunch',
    'selectItem': 'mSelectMenuItem',
    'noActiveItems': 'mNoActiveItems',
    'noPastLaunches': 'mNoPastLaunches',
    # Form labels
    'myAccount': 'mTitleMyAccount',
    'orderHistory': 'mOrderHistory',
    'noOrdersYet': 'mNoOrdersYet',
    'topUp': 'mTitleTopUp',
    'walletBalance': 'mBalance',
    'noTransactionsYet': 'mNoTransactions',
}

# Find MERCHANT_LANGS blocks
ml_pos = js.find('const MERCHANT_LANGS')
en_pos = js.find('en:', ml_pos)
zh_pos = js.find('zh:', ml_pos)
ms_pos = js.find('ms:', ml_pos)
ta_pos = js.find('ta:', ml_pos)

# Determine block boundaries
def get_block_end(js, start_pos, next_keys):
    for k in next_keys:
        p = js.find(k, start_pos + 1)
        if p > start_pos:
            return p
    return start_pos + 100000

next_keys = ['ta:', '};', '// ', 'const ', 'window.', 'function ']
en_end = get_block_end(js, en_pos, next_keys)
zh_end = get_block_end(js, zh_pos, next_keys)
ms_end = get_block_end(js, ms_pos, next_keys)
ta_end = get_block_end(js, ta_pos, next_keys)

print(f'Block positions:')
print(f'  en: {en_pos}-{en_end} ({en_end-en_pos} chars)')
print(f'  zh: {zh_pos}-{zh_end} ({zh_end-zh_pos} chars)')
print(f'  ms: {ms_pos}-{zh_pos} ({zh_pos-ms_pos} chars) (ms is BETWEEN en and zh!)')
print(f'  ta: {ta_pos}-{ta_end} ({ta_end-ta_pos} chars)')

# Find exact end of each block (closing brace followed by comma or newline)
def find_block_end(js, start):
    # Find the closing '}' of the object
    depth = 0
    in_string = False
    string_char = None
    i = start
    while i < len(js):
        c = js[i]
        if in_string:
            if c == '\\' and i + 1 < len(js):
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'", '`'):
                in_string = True
                string_char = c
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return i

en_end = find_block_end(js, en_pos) + 1
zh_end = find_block_end(js, zh_pos) + 1
ms_end = find_block_end(js, ms_pos) + 1
ta_end = find_block_end(js, ta_pos) + 1

print(f'Block boundaries (corrected):')
print(f'  en: {en_pos}-{en_end}')
print(f'  zh: {zh_pos}-{zh_end}')
print(f'  ms: {ms_pos}-{ms_end}')
print(f'  ta: {ta_pos}-{ta_end}')

# For each language block, find each unprefixed key and add the alias
added_counts = {}

for block_name, block_start, block_end in [('en', en_pos, en_end), ('zh', zh_pos, zh_end), ('ms', ms_pos, ms_end), ('ta', ta_pos, ta_end)]:
    block = js[block_start:block_end]
    count = 0
    
    for unprefixed, actual in KEY_ALIASES.items():
        # Check if the actual key exists in this block
        if actual not in block:
            continue
        # Check if the unprefixed key already exists
        if unprefixed in block:
            continue
        
        # Find where to insert (right after the actual key)
        # Pattern: "actual_key: 'value'," or "actual_key: 'value'\n"
        pattern = actual + r":\s*'[^']*'"
        match = re.search(pattern, block)
        if match:
            # Insert unprefixed key alias after the actual key
            insert_pos = match.end()
            alias_line = f", {unprefixed}: '{match.group().split(':')[1].strip()}'"
            block = block[:insert_pos] + alias_line + block[insert_pos:]
            count += 1
    
    added_counts[block_name] = count
    print(f'  Added {count} aliases to {block_name} block')
    
    # Reconstruct the JS
    js = js[:block_start] + block + js[block_end:]

# Save
with open(JS, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'\nDone! Added aliases to all language blocks.')
print(f'Total: en={added_counts["en"]}, zh={added_counts["zh"]}, ms={added_counts["ms"]}, ta={added_counts["ta"]}')
