import codecs

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'id="inputJamMasukTutup"' in line:
        pass
    if 'required class="w-full">' in line and 'inputJamMasukTutup' in new_lines[-3]:
        # we found the end of the inputJamMasukTutup element
        pass
    if '<!-- ============ PAGE: PENGATURAN JAM ============ -->' in line:
        pass

# Actually let's just find the exact index of `<div class="card mb-6">` that follows `inputJamMasukTutup`
insert_index = -1
for i, line in enumerate(lines):
    if 'Ringkasan Jadwal Mingguan' in line:
        insert_index = i - 2 # point to `<div class="card mb-6">`
        break

if insert_index != -1:
    card_pulang = '''
            <!-- CARD 2: Pengaturan Jam Pulang -->
            <div class="card mb-0 flex flex-col gap-6 h-full">
              <div class="flex items-center gap-2 border-b border-slate-200 pb-3 mb-1">
                <span class="material-symbols-outlined text-blue-600 text-[22px]">logout</span>
                <h3 class="text-sm font-bold uppercase tracking-wider text-slate-800">Jam Pulang Sekolah</h3>
              </div>
              <div class="flex flex-col gap-1.5">
                <div class="flex flex-col">
                  <label class="text-xs font-semibold text-slate-700" for="inputJamPulangBuka">Jam Pulang Dibuka</label>
                  <span class="text-xs text-slate-500 font-normal leading-normal">Siswa dapat mulai melakukan absensi pulang.</span>
                </div>
                <input id="inputJamPulangBuka" type="text" placeholder="15:00" maxlength="5"
                  pattern="^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$" title="Format jam harus 24 jam (HH:MM), contoh: 15:00"
                  required class="w-full">
              </div>
              <div class="flex flex-col gap-1.5 mt-auto">
                <div class="flex flex-col">
                  <label class="text-xs font-semibold text-slate-700" for="inputJamPulangTutup">Jam Pulang Ditutup</label>
                  <span class="text-xs text-slate-500 font-normal leading-normal">Setelah waktu ini absensi pulang ditutup.</span>
                </div>
                <input id="inputJamPulangTutup" type="text" placeholder="17:00" maxlength="5"
                  pattern="^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$" title="Format jam harus 24 jam (HH:MM), contoh: 17:00"
                  required class="w-full">
              </div>
            </div>
          </div> <!-- Close panelWaktuHari -->
'''
    lines.insert(insert_index, card_pulang)
    with codecs.open('admin.html', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
    print("SUCCESS")
else:
    print("FAILED")
