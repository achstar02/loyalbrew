import sys, re
sys.stdout.reconfigure(encoding='utf-8')
JS = r'C:\Users\Administrator\CodeBuddy\20260416214625\app.js'
with open(JS,'r',encoding='utf-8') as f: js = f.read()

# 找所有目标键的值
keys = ['mRulePerOrderOpt', 'kitchenDisplayLbl', 'getNotifiedWhenReady', 
        'myShopLink', 'tngName', 'referralProgramTitle', 'maybeLaterBtn',
        'filterAll', 'placeOrder', 'stamp_rule']

for key in keys:
    matches = list(re.finditer(re.escape(key) + r"\s*:\s*'([^']*)'", js))
    print(f"\n=== {key} ({len(matches)} occurrences) ===")
    for i, m in enumerate(matches):
        val = m.group(1)
        pos = m.start()
        # Show surrounding context to identify which block
        ctx_start = max(0, pos - 30)
        ctx_end = min(len(js), pos + len(val) + 50)
        # Just show value and position
        has_cn = any('\u4e00' <= c <= '\u9fff' for c in val)
        lang_hint = 'ZH' if has_cn else ('EN' if val and (val[0].isupper() or val[0] in '✨🎉') else '?')
        print(f"  [{i}] @{pos} [{lang_hint}] = {val[:70]}")
