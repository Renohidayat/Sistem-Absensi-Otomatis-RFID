import codecs
import re

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Jumlah Murid mode "angkatan" to use the new field "angkatan", and add "jurusan" mode
jumlah_murid_update = '''
  renderJumlahMurid() {
    const totalMurid = this.siswaRowsCache.length;
    if (this.dom.jmTotalMurid) this.dom.jmTotalMurid.textContent = totalMurid;

    // Hitung total kelas
    const kelasCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const kelas = (d.kelas || 'TIDAK ADA KELAS').trim().toUpperCase();
      kelasCounts[kelas] = (kelasCounts[kelas] || 0) + 1;
    });
    const totalKelas = Object.keys(kelasCounts).length;
    if (this.dom.jmTotalKelas) this.dom.jmTotalKelas.textContent = totalKelas;

    // Hitung total angkatan
    const angkatanCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const angkatan = d.angkatan || 'Lainnya';
      angkatanCounts[angkatan] = (angkatanCounts[angkatan] || 0) + 1;
    });
    const totalAngkatan = Object.keys(angkatanCounts).length;
    if (this.dom.jmTotalAngkatan) this.dom.jmTotalAngkatan.textContent = totalAngkatan;

    // Hitung total jurusan
    const jurusanCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const jur = (d.jurusan || 'Lainnya').trim().toUpperCase();
      jurusanCounts[jur] = (jurusanCounts[jur] || 0) + 1;
    });
    const totalJurusan = Object.keys(jurusanCounts).length;
    if (this.dom.jmTotalJurusan) this.dom.jmTotalJurusan.textContent = totalJurusan;

    if (!this.dom.jumlahMuridContent) return;

    if (this.currentGroupMode === 'semua') {
      // Tampilkan semua murid dalam tabel
      if (totalMurid === 0) {
        this.dom.jumlahMuridContent.innerHTML = `<div class="text-center py-8 text-xs text-[#64748b]">Belum ada data siswa terdaftar.</div>`;
        return;
      }
      this.dom.jumlahMuridContent.innerHTML = `
        <div class="overflow-x-auto border border-[#e2e8f0] rounded-lg p-2 bg-[#ffffff]">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-[#e2e8f0]">
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">No</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">Nama</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">NISN</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">Kelas</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase font-mono">UID</th>
              </tr>
            </thead>
            <tbody>
              ${this.siswaRowsCache.map(({ uid, d }, i) => `
                <tr class="hover:bg-[#f1f5f9] transition-colors border-b border-[#e2e8f0] last:border-none">
                  <td class="py-3 px-2 text-xs font-semibold text-[#1e293b]">${i + 1}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${(d.nama || '-').replace(/_/g, ' ')}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${d.nisn || '-'}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${d.kelas || '-'}</td>
                  <td class="py-3 px-2 text-xs font-mono text-[#64748b]">${uid}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else if (this.currentGroupMode === 'kelas' || this.currentGroupMode === 'angkatan' || this.currentGroupMode === 'jurusan') {
      let groupingKeys = [];
      let getDataFn = null;
      let icon = '';
      let colorClass = '';

      if (this.currentGroupMode === 'kelas') {
        groupingKeys = Object.keys(kelasCounts).sort();
        getDataFn = (d) => (d.kelas || '').trim().toUpperCase();
        icon = 'meeting_room'; colorClass = 'text-[#2563eb]';
      } else if (this.currentGroupMode === 'angkatan') {
        groupingKeys = Object.keys(angkatanCounts).sort();
        getDataFn = (d) => d.angkatan || 'Lainnya';
        icon = 'calendar_today'; colorClass = 'text-orange-400';
      } else if (this.currentGroupMode === 'jurusan') {
        groupingKeys = Object.keys(jurusanCounts).sort();
        getDataFn = (d) => (d.jurusan || 'Lainnya').trim().toUpperCase();
        icon = 'category'; colorClass = 'text-purple-500';
      }

      if (groupingKeys.length === 0) {
        this.dom.jumlahMuridContent.innerHTML = `<div class="text-center py-8 text-xs text-[#64748b]">Belum ada data siswa terdaftar.</div>`;
        return;
      }

      this.dom.jumlahMuridContent.innerHTML = groupingKeys.map((groupName, index) => {
        const studentsInGroup = this.siswaRowsCache.filter(({ d }) => getDataFn(d) === groupName);
        return `
          <div class="border border-[#e2e8f0] rounded-lg mb-3 overflow-hidden bg-[#ffffff]">
            <div class="flex items-center justify-between p-3.5 hover:bg-[#f8fafc] cursor-pointer transition-colors accordion-header" data-target="group-${index}">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[20px] ${colorClass}">${icon}</span>
                <span class="text-xs font-bold text-[#1e293b] uppercase">${groupName}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-semibold text-[#64748b] bg-[#f8fafc] border border-[#e2e8f0] px-2.5 py-0.5 rounded-full">${studentsInGroup.length} Siswa</span>
                <span class="material-symbols-outlined text-[18px] text-[#64748b] transition-transform duration-300 transform" id="icon-group-${index}">expand_more</span>
              </div>
            </div>
            <div class="max-h-0 overflow-hidden transition-all duration-300 ease-in-out bg-[#ffffff]" id="content-group-${index}">
              <div class="p-3 border-t border-[#e2e8f0]">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="border-b border-[#e2e8f0]">
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">No</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">Nama</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">Kelas</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase font-mono">UID</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${studentsInGroup.map(({ uid, d }, i) => `
                      <tr class="border-b border-[#e2e8f0] last:border-none hover:bg-[#f1f5f9] transition-colors">
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${i + 1}</td>
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${(d.nama || '-').replace(/_/g, ' ')}</td>
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${d.kelas || '-'}</td>
                        <td class="py-2 px-2 text-xs font-mono text-[#64748b]">${uid}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
      }).join('');

      this.bindAccordionEvents();
    }
  }
'''

js = re.sub(r'renderJumlahMurid\(\) \{.*?(?=  // ====== PAGE 4: REGISTRASI ======)', jumlah_murid_update + '\n\n', js, flags=re.DOTALL)

# Delete getAngkatan() function
js = re.sub(r'getAngkatan\(kelasName\) \{.*?\n  \}\n', '', js, flags=re.DOTALL)


with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
