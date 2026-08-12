import codecs

with codecs.open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add overflow-y to desktop aside
if 'height: 100vh;' in css and 'overflow-y: auto;' not in css:
    css = css.replace('height: 100vh;', 'height: 100vh;\n  overflow-y: auto;')

with codecs.open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Bust cache
with codecs.open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()
with codecs.open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js.replace('v=14', 'v=15'))
    
with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()
with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('js/app.js?v=14', 'js/app.js?v=15').replace('css/style.css?v=2', 'css/style.css?v=3'))
