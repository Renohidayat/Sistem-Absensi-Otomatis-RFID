import codecs
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer('id="siswaRiwayatPage"', html)]
print('siswaRiwayatPage found at indices:', matches)

if len(matches) > 1:
    print('Context of FIRST duplicate:')
    print(html[max(0, matches[0]-50):matches[0]+500])
    print('\n\nContext of SECOND duplicate:')
    print(html[matches[1]-50:matches[1]+500])
