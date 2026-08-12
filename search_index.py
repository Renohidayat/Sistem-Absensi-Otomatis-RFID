import codecs
with codecs.open('index.html','r',encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
for i, line in enumerate(lines):
    if 'jam' in line.lower() or 'pulang' in line.lower() or 'riwayat' in line.lower() or 'loadSiswa' in line.lower():
        print(f'Line {i+1}: {line.rstrip()[:150]}')
