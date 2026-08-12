import codecs
with codecs.open('js/UIManager.js','r',encoding='utf-8') as f:
    html = f.read()
print('jam count:', html.count('jam'))
print('pulang count:', html.count('pulang'))

# Find lines with 'jam' or 'pulang'
lines = html.split('\n')
for i, line in enumerate(lines):
    if 'jam' in line.lower() or 'pulang' in line.lower():
        print(f'Line {i+1}: {line.rstrip()[:120]}')
