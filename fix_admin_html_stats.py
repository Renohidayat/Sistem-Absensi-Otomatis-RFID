import codecs

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_stat_header = '''          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statSiswa">Siswa</label>
              <select class="w-full" id="statSiswa">
                <option value="">-- Pilih Siswa --</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statBulan">Bulan</label>
              <input class="w-full" id="statBulan" type="month">
            </div>
            <button class="btn btn-primary h-[38px]" id="btnTampilkanStatistik">Tampilkan</button>
          </div>'''

new_stat_header = '''          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statJurusan">Jurusan</label>
              <select class="w-full sm:w-auto" id="statJurusan">
                <option value="">-- Semua Jurusan --</option>
                <option value="PSPT">PSPT</option>
                <option value="TKR/TKRO">TKR/TKRO</option>
                <option value="TSM/TBSM">TSM/TBSM</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statKelas">Kelas</label>
              <select class="w-full sm:w-auto" id="statKelas">
                <option value="">-- Semua Kelas --</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statSiswa">Siswa</label>
              <select class="w-full" id="statSiswa">
                <option value="">-- Semua Siswa (Rekap) --</option>
              </select>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="statBulan">Bulan</label>
              <input class="w-full" id="statBulan" type="month">
            </div>
            <button class="btn btn-primary h-[38px]" id="btnTampilkanStatistik">Tampilkan</button>
          </div>'''

html = html.replace(old_stat_header, new_stat_header)

# Cache bust the admin.html file too so it reloads UIManager again just in case
html = html.replace('js/app.js?v=7', 'js/app.js?v=8')

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
