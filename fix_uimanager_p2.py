import codecs
import re

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Statistik - Cascading filters & "Semua Siswa" mode
statistik_logic = '''
  refreshStatFilters() {
    // Kumpulkan opsi jurusan & kelas yang ada dari daftarSiswaCache
    const setJurusan = new Set();
    const mapKelas = {}; // mapKelas[jurusan] = Set of kelas
    const mapSiswa = {}; // mapSiswa[kelas] = Array of siswa

    Object.values(this.daftarSiswaCache).forEach(d => {
      const jur = (d.jurusan || 'Lainnya').trim();
      const kel = (d.kelas || 'Lainnya').trim();
      setJurusan.add(jur);
      
      if (!mapKelas[jur]) mapKelas[jur] = new Set();
      mapKelas[jur].add(kel);

      if (!mapSiswa[kel]) mapSiswa[kel] = [];
      mapSiswa[kel].push(d);
    });

    // Populate Jurusan (hanya yang ada di data)
    // Tapi karena Jurusan sudah hardcoded di HTML, kita biarkan HTML atau kita populate dynamic. 
    // Biarkan static HTML untuk jurusan, kita tambahkan listener saja.
  }
'''

# Replace refreshStatSiswaOptions() with refreshStatFilters() entirely
refresh_stat_siswa = '''
  refreshStatSiswaOptions() {
    const currentVal = this.dom.statSiswaSelect.value;
    const entries = Object.entries(this.daftarSiswaCache);

    entries.sort((a, b) => (a[1].nama || '').localeCompare(b[1].nama || ''));

    this.dom.statSiswaSelect.innerHTML = '<option value="">-- Pilih Siswa --</option>' +
      entries.map(([uid, d]) => `<option value="${(d.nama || '').replace(/"/g, '')}">${(d.nama || '-').replace(/_/g, ' ')} (${d.kelas || '-'})</option>`).join('');

    if ([...this.dom.statSiswaSelect.options].some(o => o.value === currentVal)) {
      this.dom.statSiswaSelect.value = currentVal;
    }
  }
'''

refresh_filters = '''
  refreshStatFilters() {
    if (!this.dom.statJurusan || !this.dom.statKelas || !this.dom.statSiswaSelect) return;

    // Cache the mapping logic
    const mapKelas = {}; // mapKelas[jurusan] = Set of kelas
    const mapSiswa = {}; // mapSiswa[kelas] = Array of siswa

    Object.values(this.daftarSiswaCache).forEach(d => {
      const jur = (d.jurusan || 'Lainnya').trim();
      const kel = (d.kelas || 'Lainnya').trim();
      
      if (!mapKelas[jur]) mapKelas[jur] = new Set();
      mapKelas[jur].add(kel);

      if (!mapSiswa[kel]) mapSiswa[kel] = [];
      mapSiswa[kel].push(d);
    });

    const updateKelas = () => {
      const jur = this.dom.statJurusan.value;
      const curKelas = this.dom.statKelas.value;
      this.dom.statKelas.innerHTML = '<option value="">-- Semua Kelas --</option>';
      if (jur && mapKelas[jur]) {
        [...mapKelas[jur]].sort().forEach(k => {
          this.dom.statKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      } else if (!jur) {
        // Jika tidak ada jurusan dipilih, tampilkan semua kelas
        const allKelas = new Set();
        Object.values(mapKelas).forEach(setK => setK.forEach(k => allKelas.add(k)));
        [...allKelas].sort().forEach(k => {
          this.dom.statKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      }
      this.dom.statKelas.value = curKelas || '';
      updateSiswa();
    };

    const updateSiswa = () => {
      const kel = this.dom.statKelas.value;
      const jur = this.dom.statJurusan.value;
      const curSiswa = this.dom.statSiswaSelect.value;
      this.dom.statSiswaSelect.innerHTML = '<option value="">-- Semua Siswa (Rekap) --</option>';
      
      let siswasToShow = [];
      if (kel && mapSiswa[kel]) {
        siswasToShow = mapSiswa[kel];
      } else {
        // Gabungkan semua yang cocok dengan jurusan
        Object.values(this.daftarSiswaCache).forEach(d => {
          if (!jur || (d.jurusan || 'Lainnya') === jur) {
            siswasToShow.push(d);
          }
        });
      }

      siswasToShow.sort((a,b) => (a.nama || '').localeCompare(b.nama || ''));
      siswasToShow.forEach(d => {
        this.dom.statSiswaSelect.innerHTML += `<option value="${(d.nama || '').replace(/"/g, '')}">${(d.nama || '-').replace(/_/g, ' ')} (${d.kelas || '-'})</option>`;
      });

      if ([...this.dom.statSiswaSelect.options].some(o => o.value === curSiswa)) {
        this.dom.statSiswaSelect.value = curSiswa;
      }
    };

    // Remove old listeners to avoid duplicates if called multiple times
    const newJurusan = this.dom.statJurusan.cloneNode(true);
    this.dom.statJurusan.parentNode.replaceChild(newJurusan, this.dom.statJurusan);
    this.dom.statJurusan = newJurusan;

    const newKelas = this.dom.statKelas.cloneNode(true);
    this.dom.statKelas.parentNode.replaceChild(newKelas, this.dom.statKelas);
    this.dom.statKelas = newKelas;

    this.dom.statJurusan.addEventListener('change', updateKelas);
    this.dom.statKelas.addEventListener('change', updateSiswa);

    // Initial populate
    updateKelas();
  }
'''
js = js.replace(refresh_stat_siswa, refresh_filters)
js = js.replace("this.refreshStatSiswaOptions();", "this.refreshStatFilters();")

# Now update Laporan listeners
# Update Laporan cascading classes
laporan_cascading = '''
    // Update Laporan Filters cascading
    if (this.dom.lapJurusan && this.dom.lapKelas) {
      this.dom.lapJurusan.addEventListener('change', () => {
        const jur = this.dom.lapJurusan.value;
        const curKelas = this.dom.lapKelas.value;
        this.dom.lapKelas.innerHTML = '<option value="">Semua Kelas</option>';
        const kSet = new Set();
        Object.values(this.daftarSiswaCache).forEach(d => {
          if (!jur || (d.jurusan || 'Lainnya') === jur) {
            kSet.add(d.kelas || 'Lainnya');
          }
        });
        [...kSet].sort().forEach(k => {
          this.dom.lapKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      });
    }
'''
js = js.replace("this.dom.btnTampilkanLaporan.addEventListener('click', () => this.handleTampilkanLaporan());", laporan_cascading + "\n    this.dom.btnTampilkanLaporan.addEventListener('click', () => this.handleTampilkanLaporan());")


with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
