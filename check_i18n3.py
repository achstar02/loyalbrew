import re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r"C:\Users\Administrator\CodeBuddy\20260416214625\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 找出所有 index.html 中的硬编码英文文本（在 >...< 之间，且没有 data-i18n）
# 这些是导致中英混合的根本原因
issues = []
lines = html.split('\n')
in_script = False
in_style = False

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    
    if '<script' in stripped and '</script>' not in stripped:
        in_script = True
    if '</script>' in stripped:
        in_script = False
        continue
    if '<style' in stripped and '</style>' not in stripped:
        in_style = True
    if '</style>' in stripped:
        in_style = False
        continue
    if in_script or in_style:
        continue
    
    # 跳过已有 data-i18n 的行
    if 'data-i18n' in line:
        continue
    
    # 跳过纯结构行
    if re.match(r'^\s*<(div|span|section|article|main|header|footer|nav|form|ul|ol|li|table|tr|td|th|thead|tbody|canvas|input|select|option|button|a|img|br|hr|p|h[1-6]|label|textarea|details|summary|dialog|modal|svg|path|circle|rect|line|polyline|polygon|g|defs|linearGradient|stop|text|tspan|clipPath|mask|use|symbol|template|slot|noscript|picture|source|video|audio|track|map|area|object|param|embed|iframe|frame|frameset|noframes|bdo|bdi|ruby|rt|rp|time|data|code|pre|samp|kbd|var|cite|q|abbr|dfn|ins|del|mark|small|big|sub|sup|strong|em|b|i|u|s|strike|font|center|blockquote|address|dl|dt|dd|figure|figcaption|aside|menu|menuitem|dir|legend|fieldset|optgroup|colgroup|col|caption|base|link|meta|title|head|html|body|!DOCTYPE)\b', stripped):
        pass  # still check for text content
    
    # Find English text between tags
    # Pattern: >English Text<
    for m in re.finditer(r'>((?:[A-Z][a-zA-Z0-9\s&;:\'\"/.,\-+*#@=_!?()%$]+|(?:Every|Free|Stamp|Redeem|Place|Order|Merchant|Pending|Preparing|Done|Active|Kitchen|Search|Member|Expiry|Copy|Print|Commission|Referral|History|Friends|Complaint|Detail|Resolved|Order|Enable|Notification|Maybe|Leave|empty|default|Higher|number|shown|first|Refresh|Use|table|below|for|Enter|your|ID|and|password|Admin|Open|Progress|Shop|Link|QR|Code|Payment|Proofs|Rate|Launches|Items|Card|Rule|Type|Request|Points|Item|Menu|Date|Mark|Touch|Go)[^<]{0,80}))<', line):
        text = m.group(1).strip()
        # Skip known non-UI patterns
        skip_patterns = [
            'http', 'https', 'www.', 'class=', 'style=', 'id=', 'href=',
            'src=', 'alt=', 'data-', 'onclick', 'onchange', 'onsubmit',
            'aria-', 'role=', 'type=', 'name=', 'value=', 'placeholder',
            'DOCTYPE', 'doctype', '&nbsp;', '&amp;', '&lt;', '&gt;',
            'div ', 'span ', 'svg ', 'path ', 'rect ', 'circle ',
            'px;', '%', 'rgb', 'hsl', 'var(', 'calc(', 'rgba',
            'flex', 'grid', 'none', 'block', 'hidden', 'relative',
            'utf-8', 'viewport', 'content=', 'charset', 'X-UA',
            'chrome=', 'edge=', 'ie=', 'mozilla', 'apple',
            'Mm', 'Rm', 'Sst', 'Id', 'Url', 'Qr', 'Api',
            '\n', '\t', '  ', '   '
        ]
        clean = text.replace('&amp;', '&').replace('&#39;', "'").strip()
        if len(clean) < 3:
            continue
        if any(s in clean.lower() for s in skip_patterns):
            continue
        # Must start with uppercase or common UI words
        if not (clean[0].isupper() or clean.split()[0].lower() in ['every','free','stamp','redeem','place','my','no','use','enter']):
            continue
        issues.append((i, clean, line.strip()[:120]))

print(f"Found {len(issues)} hardcoded English strings in HTML:\n")
for lineno, text, ctx in issues:
    print(f"  Line {lineno}: '{text}'")
    print(f"           {ctx}")
    print()
