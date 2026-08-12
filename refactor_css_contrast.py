import codecs

with codecs.open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Contrast fixes for variables
css = css.replace('--success: #16a34a;', '--success: #15803d;') # green-700
css = css.replace('--error: #dc2626;', '--error: #b91c1c;') # red-700
css = css.replace('--warning: #ea580c;', '--warning: #c2410c;') # orange-700

# Fix badge-live contrast
css = css.replace('color: var(--primary);', 'color: var(--primary-hover);')

# Increase table th contrast
css = css.replace('color: var(--text-muted);', 'color: var(--text-main);')

# Increase padding/radius for a polished look
css = css.replace('border-radius: 12px;', 'border-radius: 16px;')
css = css.replace('border-radius: 8px;', 'border-radius: 10px;')

with codecs.open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bust cache again
with codecs.open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()
with codecs.open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js.replace('v=12', 'v=13'))
    
with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()
with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('js/app.js?v=12', 'js/app.js?v=13').replace('css/style.css', 'css/style.css?v=2'))
    
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()
with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx.replace('js/app.js?v=12', 'js/app.js?v=13').replace('css/style.css', 'css/style.css?v=2'))
