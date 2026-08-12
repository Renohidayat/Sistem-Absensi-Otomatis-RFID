import re
import codecs

try:
    with codecs.open('admin.html', 'r', encoding='utf-16') as f:
        content = f.read()
except UnicodeError:
    with codecs.open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

# Remove column header from tables
content = content.replace('<th>Jam Pulang</th>', '')
content = content.replace('colspan="6"', 'colspan="5"')

# Remove Pengaturan Jam Pulang section
content = re.sub(r'<!-- CARD 2: Pengaturan Jam Pulang -->.*?<div class="mt-6', '<div class="mt-6', content, flags=re.DOTALL)

# Remove Pulang Dibuka and Pulang Ditutup from tabelRingkasanJadwal
content = content.replace('<th class="py-2">Pulang Dibuka</th>', '')
content = content.replace('<th class="py-2">Pulang Ditutup</th>', '')

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
