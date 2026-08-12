import codecs
import re

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix layout Laporan to 6 cols (4 inputs + 2 buttons)
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end mb-8">', '<div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-end mb-8">')

# Add Laporan Filters
lap_filters = '''            <div class="flex flex-col gap-2">
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
html = html.replace('<button class="btn btn-primary h-[38px]" id="btnTampilkanLaporan">Tampilkan</button>', lap_filters + '\n            <button class="btn btn-primary h-[38px]" id="btnTampilkanLaporan">Tampilkan</button>')

# Fix layout Statistik to 5 cols (3 inputs + 1 month + 1 button)
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end mb-8">', '<div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">')

# Add Statistik Filters
stat_filters = '''            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statJurusan">Jurusan</label>
              <select class="w-full" id="statJurusan">
                <option value="">-- Semua Jurusan --</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR">TKR/TKRO</option>
                <option value="TSM">TSM/TBSM</option>
                <option value="Lainnya">Lainnya</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statKelas">Kelas</label>
              <select class="w-full" id="statKelas">
                <option value="">-- Semua Kelas --</option>
              </select>
            </div>'''
html = html.replace('<div class="flex flex-col gap-2">\n              <label class="text-xs text-slate-500" for="statSiswa">Siswa</label>', stat_filters + '\n            <div class="flex flex-col gap-2">\n              <label class="text-xs text-slate-500" for="statSiswa">Siswa</label>')

# Add Jumlah Siswa Grouping button
html = html.replace('<button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="angkatan">Angkatan</button>', '<button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="jurusan">Jurusan</button>\n              <button class="px-3 py-1.5 text-xs font-semibold rounded-md text-slate-500 hover:text-slate-800 transition-all cursor-pointer group-btn" data-group-mode="angkatan">Angkatan (Tahun)</button>')

# Add Stat Box Total Jurusan
stat_box_jurusan = '''            <div class="stat-box bg-purple-50 border border-purple-100 p-4 rounded-lg flex items-center justify-between">
              <div>
                <div class="stat-num text-3xl font-bold text-purple-500" id="jmTotalJurusan">0</div>
                <div class="stat-label text-xs text-slate-500 mt-1">Total Jurusan</div>
              </div>
              <span class="material-symbols-outlined text-[36px] text-purple-200">category</span>
            </div>'''
html = html.replace('<div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">', '<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">')
html = re.sub(r'(<span class="material-symbols-outlined text-\[36px\] text-orange-200">calendar_today</span>\s*</div>\s*</div>)', r'\1\n' + stat_box_jurusan, html)


with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
