import codecs

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_block = """          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">
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
          </div>\n"""

# Find the start and end indices
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end mb-8">' in line and 'Siswa' in "".join(lines[i:i+5]):
        start_idx = i
    if start_idx != -1 and 'id="btnTampilkanStatistik"' in line:
        end_idx = i + 1 # Include the closing div in the next line
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [new_block] + lines[end_idx+1:]
    with codecs.open('admin.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("SUCCESS")
else:
    print("FAILED TO FIND BLOCK")
