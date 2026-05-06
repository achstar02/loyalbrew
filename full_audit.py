#!/usr/bin/env python3
"""LoyalBrew Full Audit — check all functions, DOM refs, logic issues"""
import re, sys, json

APP_JS = r"C:\Users\Administrator\CodeBuddy\20260416214625\app.js"
INDEX_HTML = r"C:\Users\Administrator\CodeBuddy\20260416214625\index.html"

with open(APP_JS, encoding='utf-8') as f:
    js = f.read()
with open(INDEX_HTML, encoding='utf-8') as f:
    html = f.read()

lines_js = js.split('\n')
lines_html = html.split('\n')

print("=" * 80)
print("LoyalBrew 全功能审查报告")
print("=" * 80)

# ─── 1. Extract all getElementById references from JS ───
js_ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js)
js_ids_unique = sorted(set(js_ids))
js_ids_count = {k: js_ids.count(k) for k in js_ids_unique}

# ─── 2. Extract all IDs from HTML ───
html_ids = re.findall(r'id=["\']([^"\']+)["\']', html)
html_ids_set = set(html_ids)

# ─── 3. IDs referenced in JS but missing from HTML ───
missing_in_html = [i for i in js_ids_unique if i not in html_ids_set]
# Filter out dynamic IDs (containing template literals, etc)
truly_missing = [i for i in missing_in_html if '${' not in i and '+' not in i and 'business-' not in i]

print("\n" + "=" * 80)
print("🔴 第一部分：JS 中引用但 HTML 中缺失的 DOM ID")
print("=" * 80)
for mid in truly_missing:
    # Find line numbers
    line_nums = [idx+1 for idx, line in enumerate(lines_js) if f"getElementById('{mid}')" in line or f'getElementById("{mid}")' in line]
    print(f"  ❌ #{mid}  (JS 行号: {line_nums[:5]})")

# ─── 4. Extract all function definitions ───
func_defs = re.findall(r'^function\s+(\w+)\s*\(', js, re.MULTILINE)
# Also arrow functions assigned to vars
arrow_funcs = re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(', js)

print("\n" + "=" * 80)
print("📋 第二部分：函数定义列表")
print("=" * 80)
print(f"  声明函数: {len(func_defs)} 个")
print(f"  箭头/赋值函数: {len(arrow_funcs)} 个")
print(f"  函数名: {', '.join(func_defs[:30])}...")
print(f"  箭头函数: {', '.join(arrow_funcs[:10])}...")

# ─── 5. Check onclick handlers in HTML that reference non-existent functions ───
onclick_funcs = re.findall(r'onclick="(\w+)\(', html)
onchange_funcs = re.findall(r'onchange="(\w+)\(', html)
oninput_funcs = re.findall(r'oninput="(\w+)\(', html)
onsubmit_funcs = re.findall(r'onsubmit="(\w+)\(', html)
all_handlers = set(onclick_funcs + onchange_funcs + oninput_funcs + onsubmit_funcs)

print("\n" + "=" * 80)
print("📋 第三部分：HTML 事件处理函数检查")
print("=" * 80)
missing_funcs = []
for hf in sorted(all_handlers):
    # Check if function exists in JS
    if f'function {hf}(' not in js and f'function {hf} (' not in js:
        # Check arrow/const
        if f'const {hf} =' not in js and f'let {hf} =' not in js and f'var {hf} =' not in js:
            missing_funcs.append(hf)
            print(f"  ❌ HTML 调用函数 {hf}() 但 JS 中未定义!")

if not missing_funcs:
    print("  ✅ 所有 HTML 事件处理函数在 JS 中均已定义")

# ─── 6. Check critical function existence and key logic ───
critical_funcs = [
    'initApp', 'showPage', 'customerLogin', 'customerRegister',
    'placeOrder', 'merchantLogin', 'merchantLogout',
    'loadMerchantDashboard', 'switchMerchantTab',
    'loadComplaintPage', 'submitComplaint', 'renderMyComplaints',
    'initComplaintsMgmtTab',
    'loadTopupPage', 'confirmTopup', 'approveTopup', 'rejectTopup',
    'loadReferralPage', 'triggerReferralCommission',
    'createStampCard', 'renderMerchantStampCards', 'awardStampsForOrder',
    'loadStampPage',
    'getMemberWallet', 'saveMemberWallet', 'topupWallet',
    'initMerchantShopQR', 'checkTableParam', 'checkMerchantParam',
    'filterComplaints',
    'renderMenuMgmt', 'populateNewItemSelect',
    'loadPromoSettings', 'loadShopSettings', 'loadPointsSettings',
    'initStampMgmtTab', 'initTopupMgmtTab', 'initCommissionsTab',
    'renderMerchantAds', 'renderMerchantOrders',
]

print("\n" + "=" * 80)
print("📋 第四部分：关键函数存在性检查")
print("=" * 80)
for fn in critical_funcs:
    exists = f'function {fn}(' in js or f'function {fn} (' in js
    status = "✅" if exists else "❌ 缺失"
    print(f"  {status} {fn}()")

# ─── 7. Check for common JS errors ───
print("\n" + "=" * 80)
print("📋 第五部分：常见 JS 错误检查")
print("=" * 80)

# Unclosed strings in i18n translations (previous bug)
bad_strings = []
for i, line in enumerate(lines_js):
    # Check for mismatched quotes in t() / mt() calls
    matches = re.finditer(r'(?:t|mt)\(["\']', line)
    for m in matches:
        quote_char = m.group()[-1]
        # Count that quote char after the match
        rest = line[m.end():]
        if quote_char not in rest.split(')')[0]:
            bad_strings.append((i+1, line.strip()[:120]))

if bad_strings:
    print("  ❌ 疑似未闭合翻译字符串:")
    for ln, text in bad_strings[:10]:
        print(f"    行 {ln}: {text}")
else:
    print("  ✅ 翻译字符串检查通过")

# Check for duplicate function definitions
func_name_lines = {}
for i, line in enumerate(lines_js):
    m = re.match(r'^function\s+(\w+)\s*\(', line)
    if m:
        fn = m.group(1)
        if fn not in func_name_lines:
            func_name_lines[fn] = []
        func_name_lines[fn].append(i+1)

dupes = {k: v for k, v in func_name_lines.items() if len(v) > 1}
if dupes:
    print("  ⚠️ 重复定义的函数:")
    for fn, lns in dupes.items():
        print(f"    {fn}() 定义在行: {lns}")
else:
    print("  ✅ 无重复函数定义")

# ─── 8. Check FSSync / DB layer ───
print("\n" + "=" * 80)
print("📋 第六部分：FSSync / DB 层检查")
print("=" * 80)

# Check DB methods
db_methods = re.findall(r'DB\.(\w+)\s*=\s*(?:async\s*)?\(', js)
db_methods += re.findall(r'DB\.(\w+)\s*=\s*function', js)
print(f"  DB 对象方法: {len(set(db_methods))} 个")
print(f"  方法名: {', '.join(sorted(set(db_methods)))}")

# Check FSSync
fsync_present = 'FSSync' in js or 'fsSync' in js
print(f"  FSSync 层: {'✅ 存在' if fsync_present else '❌ 缺失'}")

# Check getMemberWallet structure
wallet_line = [i+1 for i, l in enumerate(lines_js) if 'function getMemberWallet' in l or 'getMemberWallet =' in l]
save_wallet_line = [i+1 for i, l in enumerate(lines_js) if 'function saveMemberWallet' in l or 'saveMemberWallet =' in l]
print(f"  getMemberWallet: 行 {wallet_line}")
print(f"  saveMemberWallet: 行 {save_wallet_line}")

# Check wallet uses Array format
for wl in wallet_line[:1]:
    start = wl - 1
    chunk = '\n'.join(lines_js[start:start+20])
    is_array = 'Array.isArray' in chunk or '=[]' in chunk or 'push(' in chunk
    print(f"  钱包数据结构: {'✅ Array格式' if is_array else '⚠️ 需检查'}")

# ─── 9. Check Firestore rules ───
print("\n" + "=" * 80)
print("📋 第七部分：Firestore 安全规则检查")
print("=" * 80)
rules_path = r"C:\Users\Administrator\CodeBuddy\20260416214625\firestore.rules"
try:
    with open(rules_path, encoding='utf-8') as f:
        rules = f.read()
    # Check for open write rules
    if 'allow write: if true;' in rules or 'allow read, write: if true;' in rules:
        print("  ⚠️ 存在完全开放的写入规则 (allow write: if true)")
    if 'allow read: if true;' in rules:
        print("  ⚠️ 存在完全开放的读取规则 (allow read: if true)")
    print(f"  规则文件长度: {len(rules)} 字符")
    # Show rules summary
    allow_lines = [l.strip() for l in rules.split('\n') if l.strip().startswith('allow')]
    print(f"  allow 规则数: {len(allow_lines)}")
    for al in allow_lines:
        print(f"    {al}")
except FileNotFoundError:
    print("  ❌ firestore.rules 文件不存在!")

# ─── 10. Check index.html page structure ───
print("\n" + "=" * 80)
print("📋 第八部分：页面结构检查")
print("=" * 80)

# Check all page divs
page_divs = re.findall(r'id="(page-[^"]+)"', html)
print(f"  页面 div: {', '.join(page_divs)}")

# Check merchant tab divs
tab_divs = re.findall(r'id="(tab-[^"]+)"', html)
print(f"  商家 Tab: {', '.join(tab_divs)}")

# ─── 11. Check merchant-specific function calls in switchMerchantTab ───
print("\n" + "=" * 80)
print("📋 第九部分：商家 Tab 初始化函数检查")
print("=" * 80)
tab_init_map = {
    'tab-new-items': 'populateNewItemSelect',
    'tab-stamp-mgmt': 'initStampMgmtTab',
    'tab-topup-mgmt': 'initTopupMgmtTab',
    'tab-complaints': 'initComplaintsMgmtTab',
    'tab-commissions': 'initCommissionsTab',
    'tab-ads': 'renderMerchantAds',
    'tab-qr': 'initMerchantShopQR',
    'tab-settings': 'loadPromoSettings',
}
for tab, fn in tab_init_map.items():
    tab_in_html = tab in html
    fn_in_js = f'function {fn}(' in js or f'function {fn} (' in js
    print(f"  {tab}: HTML={'✅' if tab_in_html else '❌'}, Init函数 {fn}(): JS={'✅' if fn_in_js else '❌'}")

# ─── 12. Check customer-facing pages ───
print("\n" + "=" * 80)
print("📋 第十部分：顾客端页面功能检查")
print("=" * 80)

# Check complaint phone input
complaint_phone_in_html = 'complaint-phone' in html
complaint_phone_in_js = 'complaint-phone' in js
print(f"  投诉页手机号输入框 (id=complaint-phone): HTML={'✅' if complaint_phone_in_html else '❌ 缺失'}, JS引用={'✅' if complaint_phone_in_js else '无'}")

# Check topup phone input
topup_phone_in_html = 'topup-phone' in html
topup_phone_in_js = 'topup-phone' in js
print(f"  充值页手机号输入框 (id=topup-phone): HTML={'✅' if topup_phone_in_html else '❌ 缺失'}, JS引用={'✅' if topup_phone_in_js else '无'}")

# Check stamp phone input
stamp_phone_in_html = 'stamp-phone' in html
stamp_phone_in_js = 'stamp-phone' in js
print(f"  印花卡页手机号输入框 (id=stamp-phone): HTML={'✅' if stamp_phone_in_html else '❌ 缺失'}, JS引用={'✅' if stamp_phone_in_js else '无'}")

# Check takeaway phone/time
takeaway_phone_in_html = 'takeaway-phone' in html
takeaway_time_in_html = 'takeaway-time' in html
print(f"  外卖手机号 (id=takeaway-phone): HTML={'✅' if takeaway_phone_in_html else '❌ 缺失'}")
print(f"  外卖取餐时间 (id=takeaway-time): HTML={'✅' if takeaway_time_in_html else '❌ 缺失'}")

# Check cart phone
cart_phone_in_html = 'cart-phone' in html
print(f"  购物车手机号 (id=cart-phone): HTML={'✅' if cart_phone_in_html else '❌ 缺失'}")

# Check use-wallet-checkbox
wallet_cb_in_html = 'use-wallet-checkbox' in html
print(f"  钱包扣款复选框 (id=use-wallet-checkbox): HTML={'✅' if wallet_cb_in_html else '❌ 缺失'}")

# Check order-notes
order_notes_in_html = 'order-notes' in html
print(f"  订单备注 (id=order-notes): HTML={'✅' if order_notes_in_html else '❌ 缺失'}")

# ─── 13. Check Firebase init ───
print("\n" + "=" * 80)
print("📋 第十一部分：Firebase 初始化检查")
print("=" * 80)

firebase_init_path = r"C:\Users\Administrator\CodeBuddy\20260416214625\firebase-init.js"
try:
    with open(firebase_init_path, encoding='utf-8') as f:
        fi = f.read()
    has_firestore = 'getFirestore' in fi or 'firebase.firestore' in fi
    has_auth = 'getAuth' in fi or 'firebase.auth' in fi
    has_ready = '__lbFirebaseReady' in fi
    print(f"  Firestore 引用: {'✅' if has_firestore else '❌'}")
    print(f"  Auth 引用: {'✅' if has_auth else '❌'}")
    print(f"  Ready 标志 (__lbFirebaseReady): {'✅' if has_ready else '❌'}")
    print(f"  firebase-init.js 长度: {len(fi)} 字符")
except FileNotFoundError:
    print("  ❌ firebase-init.js 文件不存在!")

# ─── 14. Check firebase.json ───
print("\n" + "=" * 80)
print("📋 第十二部分：firebase.json 配置检查")
print("=" * 80)
fb_json_path = r"C:\Users\Administrator\CodeBuddy\20260416214625\firebase.json"
try:
    with open(fb_json_path, encoding='utf-8') as f:
        fbj = json.load(f)
    hosting = fbj.get('hosting', {})
    public = hosting.get('public', 'N/A')
    print(f"  hosting.public: {public}")
    rewrites = hosting.get('rewrites', [])
    print(f"  rewrites: {len(rewrites)} 条")
    for rw in rewrites:
        print(f"    {rw}")
except FileNotFoundError:
    print("  ❌ firebase.json 文件不存在!")
except json.JSONDecodeError as e:
    print(f"  ❌ firebase.json 解析错误: {e}")

# ─── 15. Summary ───
print("\n" + "=" * 80)
print("📊 审查总结")
print("=" * 80)
print(f"  JS 文件: {len(lines_js)} 行")
print(f"  HTML 文件: {len(lines_html)} 行")
print(f"  JS 引用的 DOM ID: {len(js_ids_unique)} 个")
print(f"  HTML 定义的 ID: {len(html_ids_set)} 个")
print(f"  JS 引用但 HTML 缺失的 ID: {len(truly_missing)} 个")
print(f"  声明函数: {len(func_defs)} 个")
print(f"  重复定义: {len(dupes)} 个")
print(f"  HTML 事件处理函数缺失: {len(missing_funcs)} 个")
