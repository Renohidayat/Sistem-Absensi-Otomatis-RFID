import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the bug where replacing parentElement.innerHTML breaks the DOM reference
broken_code_recap = '''      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-200 text-slate-500">
              <th class="py-2">No</th>
              <th class="py-2">Nama Siswa</th>
              <th class="py-2">Kelas</th>
              <th class="py-2">Hadir</th>
              <th class="py-2">Terlambat</th>
              <th class="py-2">Tidak Hadir</th>
              <th class="py-2">Persentase</th>
            </tr>
          </thead>
          <tbody id="tabelStatistikDetail">
            ${siswasRelevan.sort((a,b)=>a.nama.localeCompare(b.nama)).map((s, i) => {
              const r = rekap[s.nama];
              const t = r.hadir + r.terlambat;
              const x = Math.max(totalHariDihitung - t, 0);
              const p = totalHariDihitung > 0 ? Math.round((t / totalHariDihitung) * 100) : 0;
              return \\`
                <tr class="border-b border-slate-200 hover:bg-slate-50">
                  <td class="py-2">${i+1}</td>
                  <td class="py-2 font-medium">${s.nama.replace(/_/g, ' ')}</td>
                  <td class="py-2">${r.kelas || '-'}</td>
                  <td class="py-2 text-emerald-600 font-bold">${r.hadir}</td>
                  <td class="py-2 text-orange-500 font-bold">${r.terlambat}</td>
                  <td class="py-2 text-red-500 font-bold">${x}</td>
                  <td class="py-2">${p}%</td>
                </tr>
              \\`;
            }).join('')}
          </tbody>
        </table>
      `;'''

# Note: The original broken code didn't even have id="tabelStatistikDetail" inside the tbody!

original_broken_code = '''      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-200 text-slate-500">
              <th class="py-2">No</th>
              <th class="py-2">Nama Siswa</th>
              <th class="py-2">Kelas</th>
              <th class="py-2">Hadir</th>
              <th class="py-2">Terlambat</th>
              <th class="py-2">Tidak Hadir</th>
              <th class="py-2">Persentase</th>
            </tr>
          </thead>
          <tbody>
            ${siswasRelevan.sort((a,b)=>a.nama.localeCompare(b.nama)).map((s, i) => {
              const r = rekap[s.nama];
              const t = r.hadir + r.terlambat;
              const x = Math.max(totalHariDihitung - t, 0);
              const p = totalHariDihitung > 0 ? Math.round((t / totalHariDihitung) * 100) : 0;
              return `
                <tr class="border-b border-slate-200 hover:bg-slate-50">
                  <td class="py-2">${i+1}</td>
                  <td class="py-2 font-medium">${s.nama.replace(/_/g, ' ')}</td>
                  <td class="py-2">${r.kelas || '-'}</td>
                  <td class="py-2 text-emerald-600 font-bold">${r.hadir}</td>
                  <td class="py-2 text-orange-500 font-bold">${r.terlambat}</td>
                  <td class="py-2 text-red-500 font-bold">${x}</td>
                  <td class="py-2">${p}%</td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;'''

fixed_recap_code = '''      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-200 text-slate-500">
              <th class="py-2">No</th>
              <th class="py-2">Nama Siswa</th>
              <th class="py-2">Kelas</th>
              <th class="py-2">Hadir</th>
              <th class="py-2">Terlambat</th>
              <th class="py-2">Tidak Hadir</th>
              <th class="py-2">Persentase</th>
            </tr>
          </thead>
          <tbody id="tabelStatistikDetail">
            ${siswasRelevan.sort((a,b)=>a.nama.localeCompare(b.nama)).map((s, i) => {
              const r = rekap[s.nama];
              const t = r.hadir + r.terlambat;
              const x = Math.max(totalHariDihitung - t, 0);
              const p = totalHariDihitung > 0 ? Math.round((t / totalHariDihitung) * 100) : 0;
              return \\`
                <tr class="border-b border-slate-200 hover:bg-slate-50">
                  <td class="py-2">${i+1}</td>
                  <td class="py-2 font-medium">${s.nama.replace(/_/g, ' ')}</td>
                  <td class="py-2">${r.kelas || '-'}</td>
                  <td class="py-2 text-emerald-600 font-bold">${r.hadir}</td>
                  <td class="py-2 text-orange-500 font-bold">${r.terlambat}</td>
                  <td class="py-2 text-red-500 font-bold">${x}</td>
                  <td class="py-2">${p}%</td>
                </tr>
              \\`;
            }).join('')}
          </tbody>
        </table>
      `;
      // Restore the DOM reference!
      this.dom.tabelStatistikDetail = document.getElementById('tabelStatistikDetail');'''

# Also fix the 1 Siswa detail mode where it might need to restore the header
fix_siswa_detail_mode = '''      if (detailRows.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada data kehadiran pada bulan ini</td></tr>`;
      } else {'''

fix_siswa_detail_mode_replacement = '''      // Restore table header for 1 siswa if it was previously in recap mode
      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Tanggal</th>
              <th>Jam</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="tabelStatistikDetail"></tbody>
        </table>
      `;
      this.dom.tabelStatistikDetail = document.getElementById('tabelStatistikDetail');

      if (detailRows.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada data kehadiran pada bulan ini</td></tr>`;
      } else {'''

js = js.replace(original_broken_code, fixed_recap_code.replace('\\`', '`'))
js = js.replace(fix_siswa_detail_mode, fix_siswa_detail_mode_replacement)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
