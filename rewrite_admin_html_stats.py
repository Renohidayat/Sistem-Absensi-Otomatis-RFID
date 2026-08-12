import codecs
import re

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_block = '''        <!-- Card: Statistik Jumlah Murid & Kelas -->
        <div class="card mt-6">
          <div class="subhead-style text-lg font-bold mb-6 text-slate-800">Statistik Data Siswa &amp; Kelas</div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-1 flex flex-col gap-4">
              <div class="stat-box bg-blue-50 border border-blue-100 p-5 rounded-lg">
                <div class="stat-num text-3xl font-bold text-blue-600" id="statTotalMurid">0</div>
                <div class="stat-label text-xs text-slate-500 mt-1">Total Siswa Terdaftar</div>
              </div>
              <div class="overflow-x-auto border border-slate-200 rounded-lg p-4 bg-white">
                <div class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2 border-b border-slate-200 pb-2">
                  Daftar Kelas</div>
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr>
                      <th class="py-1 text-[10px] text-slate-500 uppercase">Kelas</th>
                      <th class="py-1 text-[10px] text-slate-500 uppercase text-right">Jumlah</th>
                    </tr>
                  </thead>
                  <tbody id="tabelKelasMurid">
                    <tr>
                      <td colspan="2" class="text-center py-4 text-xs text-slate-400">Memuat data kelas...</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="md:col-span-2 border border-slate-200 rounded-lg p-4 bg-white flex flex-col">
              <div class="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-4">Grafik Distribusi Siswa per Kelas</div>
              <div class="h-[250px] relative">
                <canvas id="chartDistribusiMurid"></canvas>
              </div>
            </div>
          </div>
        </div>'''

new_block = '''        <!-- Card: Statistik Jumlah Murid & Kelas -->
        <div class="card mt-6 border-0 shadow-sm bg-slate-50/50">
          <div class="subhead-style text-lg font-bold mb-6 text-slate-800 flex items-center gap-2">
            <span class="material-symbols-outlined text-blue-600">analytics</span>
            Statistik Data Siswa &amp; Kelas
          </div>
          
          <!-- Top Stats Row -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="flex items-center gap-4 bg-gradient-to-br from-blue-500 to-blue-700 p-5 rounded-xl shadow-md text-white hover:-translate-y-1 transition-transform">
              <div class="p-3 bg-white/20 rounded-xl">
                <span class="material-symbols-outlined text-3xl">groups</span>
              </div>
              <div>
                <div class="text-3xl font-bold tracking-tight" id="statTotalMurid">0</div>
                <div class="text-xs text-blue-100 font-medium uppercase tracking-wider mt-1">Total Siswa</div>
              </div>
            </div>
            <div class="flex items-center gap-4 bg-gradient-to-br from-indigo-500 to-indigo-700 p-5 rounded-xl shadow-md text-white hover:-translate-y-1 transition-transform">
              <div class="p-3 bg-white/20 rounded-xl">
                <span class="material-symbols-outlined text-3xl">meeting_room</span>
              </div>
              <div>
                <div class="text-3xl font-bold tracking-tight" id="statTotalKelas">0</div>
                <div class="text-xs text-indigo-100 font-medium uppercase tracking-wider mt-1">Total Kelas</div>
              </div>
            </div>
            <div class="flex items-center gap-4 bg-gradient-to-br from-emerald-500 to-emerald-700 p-5 rounded-xl shadow-md text-white hover:-translate-y-1 transition-transform">
              <div class="p-3 bg-white/20 rounded-xl">
                <span class="material-symbols-outlined text-3xl">school</span>
              </div>
              <div>
                <div class="text-3xl font-bold tracking-tight" id="statTotalJurusan">0</div>
                <div class="text-xs text-emerald-100 font-medium uppercase tracking-wider mt-1">Total Jurusan</div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-1 flex flex-col gap-4">
              <div class="overflow-x-auto border border-slate-200 rounded-xl p-5 bg-white shadow-sm h-full">
                <div class="text-xs font-bold uppercase tracking-wider text-slate-800 mb-4 border-b border-slate-100 pb-3 flex justify-between items-center">
                  <span>Distribusi Kelas</span>
                  <span class="material-symbols-outlined text-slate-400 text-sm">pie_chart</span>
                </div>
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr>
                      <th class="py-2 text-[10px] text-slate-400 uppercase font-bold tracking-wider">Kelas / Jurusan</th>
                      <th class="py-2 text-[10px] text-slate-400 uppercase font-bold tracking-wider text-right">Jumlah</th>
                    </tr>
                  </thead>
                  <tbody id="tabelKelasMurid">
                    <tr>
                      <td colspan="2" class="text-center py-6 text-xs text-slate-400">Memuat data kelas...</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="md:col-span-2 border border-slate-200 rounded-xl p-5 bg-white shadow-sm flex flex-col">
              <div class="text-xs font-bold uppercase tracking-wider text-slate-800 mb-4 flex justify-between items-center">
                <span>Grafik Distribusi Siswa per Kelas</span>
                <span class="material-symbols-outlined text-slate-400 text-sm">bar_chart</span>
              </div>
              <div class="h-[250px] relative w-full flex-grow">
                <canvas id="chartDistribusiMurid"></canvas>
              </div>
            </div>
          </div>
        </div>'''

# Manual precise replacement to avoid indentation fails
start_idx = -1
end_idx = -1
lines = html.splitlines(True)
for i, line in enumerate(lines):
    if '<!-- Card: Statistik Jumlah Murid & Kelas -->' in line:
        start_idx = i
    if start_idx != -1 and '<!-- ============ PAGE: JUMLAH MURID ============ -->' in line:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_lines = lines[:start_idx] + [new_block + '\n\n'] + lines[end_idx:]
    html = ''.join(new_lines)
    
    # Cache bust again just in case
    html = html.replace('js/app.js?v=9', 'js/app.js?v=10')
    
    with codecs.open('admin.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS HTML")
else:
    print("FAILED TO FIND HTML BLOCK")

