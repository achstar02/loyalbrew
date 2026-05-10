import re, subprocess

JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\deploy\app.js'
with open(JS, 'r', encoding='utf-8') as f:
    js = f.read()

print(f'app.js: {len(js)} chars')

# Find loadMerchantDashboard
fn_pos = js.find('function loadMerchantDashboard')
if fn_pos < 0:
    fn_pos = js.find('loadMerchantDashboard = function')
print(f'loadMerchantDashboard: {fn_pos}')

# Show first 600 chars
if fn_pos >= 0:
    print('=== First 600 chars ===')
    print(js[fn_pos:fn_pos+600])
    print('...')
    
# Also show mt() function
mt_pos = js.find('function mt(')
print(f'function mt(): {mt_pos}')
print(js[mt_pos:mt_pos+300])

# Check en block of MERCHANT_LANGS for key merchant keys
ml_pos = js.find('const MERCHANT_LANGS')
en_pos = js.find('en:', ml_pos)
ms_pos = js.find('ms:', ml_pos)
en_block = js[en_pos:ms_pos]

keys_to_check = ['overview','members','menuItems','menuMgmt2','shopSettings2',
                 'kitchenDisplay2','add_points_manually','quickActions','stats',
                 'addPoints','phone','billAmount','willEarn','points','title',
                 'viewOrders2','menuMgmt2','newItems','newItem2','shopSettings',
                 'kitchenDisplay','adManagement','complaints','commissions','qrCode',
                 'settings','ads']
print('\n=== Key lookup in MERCHANT_LANGS.en ===')
for k in keys_to_check:
    m = re.search(rf"{k}\s*:\s*'([^']+)'", en_block)
    if m:
        print(f'  {k} = {m.group(1)[:40]}')
    else:
        print(f'  {k} = MISSING')