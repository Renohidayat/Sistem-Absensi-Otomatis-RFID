import codecs, re
with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

ids = re.findall(r"getElementById\('([^']+)'\)", js_code)
missing = []
for i in ids:
    if f'id="{i}"' not in html_code and f"id='{i}'" not in html_code:
        missing.append(i)

print('Missing IDs in admin.html:', missing)
