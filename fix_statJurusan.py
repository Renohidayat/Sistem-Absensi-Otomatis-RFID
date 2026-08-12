import codecs

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the values in statJurusan
old_stat = '''              <select class="w-full sm:w-auto" id="statJurusan">
                <option value="">-- Semua Jurusan --</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR/TKRO">TKR/TKRO</option>
                <option value="TSM/TBSM">TSM/TBSM</option>
              </select>'''

new_stat = '''              <select class="w-full sm:w-auto" id="statJurusan">
                <option value="">-- Semua Jurusan --</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR">TKR/TKRO</option>
                <option value="TSM">TSM/TBSM</option>
                <option value="Lainnya">Lainnya</option>
              </select>'''

html = html.replace(old_stat, new_stat)

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
