with open('C:\\Users\\Administrator\\CodeBuddy\\20260416214625\\deploy\\app.js', 'r', encoding='utf-8') as f:
    js = f.read()

phrases = [
    'Welcome Back',
    'What\'s your drink today',
    'Connect to get started',
    'Member Login',
    'Order Now',
    'My Stamp Cards',
    'Top Up',
    'My Account'
]

for phrase in phrases:
    pos = js.find(phrase)
    if pos >= 0:
        print('FOUND:', repr(phrase))
        print('  Context:', repr(js[pos-30:pos+len(phrase)+30]))
        print()
    else:
        print('NOT FOUND:', repr(phrase))
