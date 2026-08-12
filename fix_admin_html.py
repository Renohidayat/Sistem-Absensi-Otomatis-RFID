import codecs

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 'Data Absensi' in line:
        new_lines.append(line)
        # inject the missing part!
        new_lines.append('''          <div class="overflow-x-auto">
            <table>
              <thead>
                <tr>
                  <th>No</th>
                  <th>Nama</th>
                  <th>NISN</th>
                  <th>UID Kartu</th>
                  <th>Jam Masuk</th>
                  <th>Jam Pulang</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="tabelAbsensi">
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!-- ============ PAGE: LAPORAN & EXPORT ============ -->
      <div class="page" id="page-laporan">
        <div class="card">
          <div class="subhead-style text-lg font-bold mb-6 text-slate-800">Filter Rentang Tanggal</div>
          <div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-end mb-8">
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="tglMulai">Dari</label>
              <input class="w-full" id="tglMulai" type="date">
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs text-slate-500" for="tglAkhir">Sampai</label>
              <input class="w-full" id="tglAkhir" type="date">
            </div>
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
            </div>
            <button class="btn btn-primary h-[38px]" id="btnTampilkanLaporan">Tampilkan</button>
            <button class="btn btn-success h-[38px]" id="btnExportCSV">Export ke CSV</button>
          </div>
          <div class="grid grid-cols-3 gap-4 mb-8">
            <div class="stat-box">
              <div class="stat-num" id="lapTotal">0</div>
              <div class="stat-label">Total Record</div>
            </div>
            <div class="stat-box">
              <div class="stat-num text-blue-600" id="lapHadir">0</div>
              <div class="stat-label">Hadir</div>
            </div>
            <div class="stat-box">
              <div class="stat-num text-orange-500" id="lapTerlambat">0</div>
              <div class="stat-label">Terlambat</div>
            </div>
          </div>
          <div class="subhead-style text-lg font-bold mb-4 text-slate-800">Hasil</div>
          <div class="overflow-x-auto">
            <table>
              <thead>
                <tr>
                  <th>Tanggal</th>
                  <th>Nama</th>
                  <th>NISN</th>
                  <th>Kelas</th>
                    <th>Jurusan</th>
                    <th>Angkatan</th>
                  <th>Status</th>
                  <th>Jam Masuk</th>
                  <th>Jam Pulang</th>
                </tr>
              </thead>
              <tbody id="tabelLaporan">
                <tr>
                  <td class="whitespace-nowrap text-center py-8 text-slate-500" colspan="9">Pilih rentang tanggal lalu klik Tampilkan</td>
                </tr>
''')
    elif i >= 122 and i <= 126: # skip the broken lines
        continue
    else:
        new_lines.append(line)

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    for line in new_lines:
        f.write(line)
