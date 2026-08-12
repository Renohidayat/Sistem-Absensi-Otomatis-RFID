import codecs
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
import re
print("Occurrences of id='siswaRiwayatPage':", html.count('id="siswaRiwayatPage"'))
print("Occurrences of class='siswa-stat-grid':", html.count('class="siswa-stat-grid"'))
print("Occurrences of <table:", html.count('<table'))
