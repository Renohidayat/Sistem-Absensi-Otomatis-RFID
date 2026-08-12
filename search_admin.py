import codecs
with codecs.open('admin.html','r',encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
for i, line in enumerate(lines):
    if 'Jam Masuk' in line or 'Jam Pulang' in line or 'tabelAbsensi' in line or 'tabelLaporan' in line:
        print(f'Line {i+1}: {line.rstrip()[:150]}')
