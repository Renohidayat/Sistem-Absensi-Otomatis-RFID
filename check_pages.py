import codecs, re
with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()
pages = re.findall(r'class="page"[^>]*id="([^"]+)"', html)
print('Pages found:', pages)
