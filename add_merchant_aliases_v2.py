import re, os

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'

with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

# Map: HTML data-mi18n unprefixed keys -> MERCHANT_LANGS m-prefixed keys
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
    'members_count': 'mStatMembers',
    # Quick action buttons
    'myOrders': 'mBtnViewOrders2',
    'menuMgmt2': 'mBtnMenuMgmt2',
    'shopSettings2': 'mBtnShopSettings2',
    'kitchenDisplay2': 'mBtnKitchenDisplay2',
    'viewOrders2': 'mBtnViewOrders2',
    # Overview content
    'quickActions': 'mTitleQuickActions',
    'add_points_manually': 'mAddPointsManually',
    # New Item page
    'launchNewItem': 'mNiLaunch',
    'selectItem': 'mSelectMenuItem',
    'noActiveItems': 'mNoActiveItems',
    'noPastLaunches': 'mNoPastLaunches',
}

# Find MERCHANT_LANGS and its blocks
ml_pos = js.find('const MERCHANT_LANGS')
en_pos = js.find('en:', ml_pos)
zh_pos = js.find('zh:', ml_pos)
ms_pos = js.find('ms:', ml_pos)
ta_pos = js.find('ta:', ml_pos)

print(f'MERCHANT_LANGS: {ml_pos}')
print(f'  en: {en_pos}')
print(f'  ms: {ms_pos}')
print(f'  zh: {zh_pos}')
print(f'  ta: {ta_pos}')

# Find the end of each block by tracking brace depth
def find_block_end(js, start):
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
                    return i + 1
        i += 1
    return i

en_end = find_block_end(js, en_pos)
# zh block ends at ms_pos (since zh is last block)
zh_end = ms_pos
# ms block ends at zh_pos  
ms_end = zh_pos
ta_end = find_block_end(js, ta_pos)

print(f'Block boundaries:')
print(f'  en: {en_pos}-{en_end}')
print(f'  zh: {zh_pos}-{zh_end} (ms in between! zh_end=ms_pos)')
print(f'  ms: {ms_pos}-{ms_end}')
print(f'  ta: {ta_pos}-{ta_end}')

blocks = {
    'en': (en_pos, en_end),
    'zh': (zh_pos, zh_end),
    'ms': (ms_pos, ms_end),
    'ta': (ta_pos, ta_end),
}

# Backup
backup_path = JS + '.bak_fix'
with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(js)
print(f'\nBackup saved to: {backup_path}')

added = {b: 0 for b in blocks}
for block_name, (b_start, b_end) in blocks.items():
    block = js[b_start:b_end]
    
    for unprefixed, actual in KEY_ALIASES.items():
        # Skip if actual key doesn't exist in this block
        if actual not in block:
            continue
        # Skip if unprefixed already exists
        if unprefixed in block:
            continue
        
        # Extract the value of the actual key
        pattern = actual + r":\s*'([^']*)'"
        m = re.search(pattern, block)
        if not m:
            pattern2 = actual + r':\s*"([^"]*)"'
            m2 = re.search(pattern2, block)
            if m2:
                val = m2.group(1)
                sep = '": "'
            else:
                continue
        else:
            val = m.group(1)
            sep = "': '"
        
        # Insert alias right after the actual key line
        # Find the end of the actual key's line
        actual_end = m.end() if m else m2.end()
        # Find next comma or newline to end the line
        line_end = actual_end
        while line_end < len(block) and block[line_end] not in (',', '\n', '\r'):
            line_end += 1
        if line_end < len(block) and block[line_end] == ',':
            line_end += 1
        
        alias = f', {unprefixed}: {sep}{val}{sep[0]}'
        block = block[:line_end] + alias + block[line_end:]
        added[block_name] += 1
    
    js = js[:b_start] + block + js[b_end:]
    print(f'  {block_name}: added {added[block_name]} aliases')

print(f'\nTotal added: en={added["en"]}, zh={added["zh"]}, ms={added["ms"]}, ta={added["ta"]}')

# Verify syntax with node
import subprocess
test_js = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\test_syntax.js'
with open(test_js, 'w', encoding='utf-8') as f:
    f.write(js)

result = subprocess.run(
    ['node', '-e', f'try{{new Function(require("fs").readFileSync(r"{JS}", "utf-8"));console.log("OK")}}catch(e){{console.log("SYNTAX ERROR:", e.message)}}'],
    capture_output=True, text=True, timeout=30,
    cwd=r'C:\Users\Administrator\CodeBuddy\20260416214625'
)
print(f'\nSyntax check: {result.stdout.strip() or result.stderr.strip() or "no output"}')

# If OK, save
if 'OK' in result.stdout:
    with open(JS, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f'Saved!')
else:
    print(f'FAILED - restore from backup')

# Cleanup
try:
    os.remove(test_js)
except:
    pass
