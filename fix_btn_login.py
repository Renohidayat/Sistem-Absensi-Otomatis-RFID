import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('type="submit" class="w-full bg-gradient-to-r', 'type="submit" class="btn-login w-full bg-gradient-to-r')

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS")
