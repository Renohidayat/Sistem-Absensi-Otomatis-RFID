import codecs
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer('id="siswaRiwayatPage"', html)]

print('Context of FIRST duplicate (end):')
print(html[matches[0]+1500:matches[0]+2500])

print('\n\nContext of SECOND duplicate (end):')
print(html[matches[1]+1500:matches[1]+2500])
