import codecs
import re

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add SheetJS library
if 'xlsx.full.min.js' not in html:
    html = html.replace('<!-- Chart.js -->', '<!-- SheetJS (Excel) -->\n  <script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>\n  <!-- Chart.js -->')

# 2. Modify formRegistrasi
reg_html_addition = '''
              <div class="flex flex-col gap-2">
                <label class="text-xs font-semibold text-slate-500" for="regAngkatan">Tahun Angkatan</label>
                <input id="regAngkatan" placeholder="Contoh: 2023" required="" type="number" min="2000" max="2050">
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-xs font-semibold text-slate-500" for="regJurusan">Jurusan</label>
                <select id="regJurusan" required="" class="w-full text-sm py-2 px-3 border border-slate-300 rounded-lg bg-slate-50 text-slate-800">
                  <option value="">-- Pilih Jurusan --</option>
                  <option value="PSPT">PSPT</option>
                  <option value="TKR">TKR/TKRO</option>
                  <option value="TSM">TSM/TBSM</option>
                  <option value="Lainnya">Lainnya</option>
                </select>
              </div>'''

html = re.sub(r'(<input id="regKelas"[^>]+>\s*</div>)', r'\1' + reg_html_addition, html)

# 3. Modify modalEditSiswa
edit_html_addition = '''
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-slate-500" for="editAngkatan">Tahun Angkatan</label>
          <input id="editAngkatan" type="number" min="2000" max="2050" required class="text-sm py-2 px-3 border border-slate-300 rounded-lg bg-slate-50 text-slate-800">
        </div>
        <div class="flex flex-col gap-2">
          <label class="text-xs font-semibold text-slate-500" for="editJurusan">Jurusan</label>
          <select id="editJurusan" class="w-full text-sm py-2 px-3 border border-slate-300 rounded-lg bg-slate-50 text-slate-800" required>
            <option value="">-- Pilih Jurusan --</option>
            <option value="PSPT">PSPT</option>
            <option value="TKR">TKR/TKRO</option>
            <option value="TSM">TSM/TBSM</option>
            <option value="Lainnya">Lainnya</option>
          </select>
        </div>'''

html = re.sub(r'(<input id="editKelas"[^>]+>\s*</div>)', r'\1' + edit_html_addition, html)

# 4. Modify Tabel Siswa Headers
html = html.replace('<th>Kelas</th>', '<th>Kelas</th>\n                    <th>Jurusan</th>\n                    <th>Angkatan</th>')

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
