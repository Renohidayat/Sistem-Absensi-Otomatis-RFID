import codecs
import re

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Filter dropdowns in Laporan page
laporan_filters_addition = '''
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="lapJurusan">Jurusan</label>
              <select class="w-full" id="lapJurusan">
                <option value="">Semua Jurusan</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR">TKR/TKRO</option>
                <option value="TSM">TSM/TBSM</option>
                <option value="Lainnya">Lainnya</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="lapKelas">Kelas</label>
              <select class="w-full" id="lapKelas">
                <option value="">Semua Kelas</option>
              </select>
            </div>'''

html = re.sub(r'(<div class="flex flex-col gap-2">\s*<label class="text-xs text-slate-500" for="tglAkhir">.*?</div>)', r'\1' + laporan_filters_addition, html, flags=re.DOTALL)

# Fix the grid layout for filters in Laporan to be grid-cols-1 md:grid-cols-6
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end mb-8">', '<div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-end mb-8">')

# 2. Add filter dropdowns in Statistik page
statistik_filters_addition = '''
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statJurusan">Jurusan</label>
              <select class="w-full" id="statJurusan">
                <option value="">-- Pilih Jurusan --</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR">TKR/TKRO</option>
                <option value="TSM">TSM/TBSM</option>
                <option value="Lainnya">Lainnya</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statKelas">Kelas</label>
              <select class="w-full" id="statKelas">
                <option value="">-- Pilih Kelas --</option>
              </select>
            </div>'''

# Replace the existing statSiswa dropdown layout to accommodate 3 dropdowns + month + button
html = re.sub(r'<div class="flex flex-col gap-2">\s*<label class="text-xs text-slate-500" for="statSiswa">.*?</div>', statistik_filters_addition + '\n            <div class="flex flex-col gap-2">\n              <label class="text-xs text-slate-500" for="statSiswa">Siswa</label>\n              <select class="w-full" id="statSiswa">\n                <option value="">-- Pilih Siswa --</option>\n              </select>\n            </div>', html, flags=re.DOTALL)

# Fix the grid layout for filters in Statistik to be grid-cols-1 md:grid-cols-5
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end mb-8">', '<div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">')

# 3. Add Tombol Pengelompokan Jurusan in Jumlah Siswa
html = html.replace('<button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="angkatan">Angkatan</button>', '<button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="jurusan">Jurusan</button>\n              <button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="angkatan">Tahun Angkatan</button>')

# Add Stat box for Total Jurusan
stat_box_jurusan = '''
            <div class="stat-box bg-purple-50 border border-purple-100 p-4 rounded-lg flex items-center justify-between">
              <div>
                <div class="stat-num text-3xl font-bold text-purple-500" id="jmTotalJurusan">3</div>
                <div class="stat-label text-xs text-slate-500 mt-1">Total Jurusan</div>
              </div>
              <span class="material-symbols-outlined text-[36px] text-purple-200">category</span>
            </div>'''
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">', '<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">')
html = html.replace('<!-- ============ PAGE: REGISTRASI SISWA ============ -->', stat_box_jurusan + '\n          </div>\n          <div id="jumlahMuridContent">\n            <div class="text-center py-8 text-slate-400">Memuat data siswa...</div>\n          </div>\n        </div>\n      </div>\n      <!-- ============ PAGE: REGISTRASI SISWA ============ -->')
html = re.sub(r'(<div class="stat-box bg-orange-50.*?</svg>\s*</div>\s*</div>\s*</div>\s*</div>)', r'\1\n' + stat_box_jurusan, html, flags=re.DOTALL)


with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
