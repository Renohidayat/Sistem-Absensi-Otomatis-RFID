import codecs
import re

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update handleTampilkanStatistik
statistik_recap = '''
  async handleTampilkanStatistik() {
    const namaSiswa = this.dom.statSiswaSelect.value;
    const kelasSiswa = this.dom.statKelas.value;
    const jurusanSiswa = this.dom.statJurusan.value;
    const bulanVal = this.dom.statBulanInput.value; // format YYYY-MM

    if (!bulanVal) {
      alert('Pilih bulan terlebih dahulu.');
      return;
    }
    if (!namaSiswa && !kelasSiswa && !jurusanSiswa) {
      alert('Silakan pilih minimal Jurusan atau Kelas atau Siswa.');
      return;
    }

    const [yearStr, monthStr] = bulanVal.split('-');
    const year = parseInt(yearStr, 10);
    const month = parseInt(monthStr, 10);
    const jumlahHari = new Date(year, month, 0).getDate();

    this.dom.statistikKosong.textContent = 'Memuat data...';
    this.dom.statistikKosong.style.display = 'block';
    this.dom.statistikIsi.style.display = 'none';

    // Ambil data absensi sebulan (bisa berat jika 1 bulan penuh, tapi ini cara tercepat)
    const dateKeys = [];
    for (let tgl = 1; tgl <= jumlahHari; tgl++) {
      dateKeys.push(`${tgl}-${month}-${year}`);
    }
    const rawRecords = await this.dbService.getAbsensiRange(dateKeys);

    const today = new Date();
    const isBulanIni = (year === today.getFullYear()) && (month === (today.getMonth() + 1));
    const totalHariDihitung = isBulanIni ? today.getDate() : jumlahHari;

    if (namaSiswa) {
      // MODE: 1 SISWA DETAIL
      let totalHadir = 0, totalTerlambat = 0;
      const detailRows = [];
      const harianHadir = Array(jumlahHari).fill(0);
      const labelHarian = Array.from({length: jumlahHari}, (_, i) => String(i + 1));

      rawRecords.forEach(record => {
        const d = record.val;
        if ((d.nama || '') === namaSiswa) {
          const tglStr = d.tanggal || record.tanggalKey;
          const [tglPart] = tglStr.split('-');
          const hariIdx = parseInt(tglPart, 10) - 1;
          harianHadir[hariIdx] = 1;

          const status = (d.status || '').toUpperCase();
          if (status === 'HADIR') totalHadir++;
          else if (status === 'TERLAMBAT') totalTerlambat++;

          detailRows.push({
            tanggal: tglStr,
            jam: d.jam_masuk || d.jam || '-',
            status: d.status || '-'
          });
        }
      });

      const totalTercatat = totalHadir + totalTerlambat;
      const totalTidakHadir = Math.max(totalHariDihitung - totalTercatat, 0);
      const persenHadir = totalHariDihitung > 0 ? Math.round((totalTercatat / totalHariDihitung) * 100) : 0;

      this.dom.stHadir.textContent = totalHadir;
      this.dom.stTerlambat.textContent = totalTerlambat;
      this.dom.stTidakHadir.textContent = totalTidakHadir;
      this.dom.stPersenHadir.textContent = persenHadir + '%';

      if (detailRows.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada data kehadiran pada bulan ini</td></tr>`;
      } else {
        // Sort based on tanggal asc
        detailRows.sort((a,b) => parseInt(a.tanggal.split('-')[0]) - parseInt(b.tanggal.split('-')[0]));
        this.dom.tabelStatistikDetail.innerHTML = detailRows.map((d, i) => {
          const status = (d.status || '').toUpperCase();
          let statusClass = 'status-default';
          if (status === 'HADIR') statusClass = 'status-hadir';
          else if (status === 'TERLAMBAT') statusClass = 'status-terlambat';
          return `
            <tr>
              <td>${i + 1}</td>
              <td>${d.tanggal}</td>
              <td>${d.jam}</td>
              <td><span class="status ${statusClass}">${d.status}</span></td>
            </tr>
          `;
        }).join('');
      }

      this.renderChartStatistikRingkasan(totalHadir, totalTerlambat, totalTidakHadir);
      this.renderChartStatistikHarian(labelHarian.slice(0, totalHariDihitung), harianHadir.slice(0, totalHariDihitung));

    } else {
      // MODE: REKAP KELAS / JURUSAN (Semua Siswa)
      // Kumpulkan siswa yg relevan
      const siswasRelevan = [];
      Object.values(this.daftarSiswaCache).forEach(d => {
        const jur = d.jurusan || 'Lainnya';
        const kel = d.kelas || 'Lainnya';
        let match = true;
        if (jurusanSiswa && jur !== jurusanSiswa) match = false;
        if (kelasSiswa && kel !== kelasSiswa) match = false;
        if (match) siswasRelevan.push(d);
      });

      if (siswasRelevan.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada siswa terdaftar di filter ini</td></tr>`;
        this.dom.stHadir.textContent = 0;
        this.dom.stTerlambat.textContent = 0;
        this.dom.stTidakHadir.textContent = 0;
        this.dom.stPersenHadir.textContent = '0%';
        this.renderChartStatistikRingkasan(0, 0, 0);
        this.renderChartStatistikHarian([], []);
        this.dom.statistikKosong.style.display = 'none';
        this.dom.statistikIsi.style.display = 'block';
        return;
      }

      const rekap = {};
      siswasRelevan.forEach(s => {
        rekap[s.nama] = { hadir: 0, terlambat: 0, kelas: s.kelas };
      });

      let globHadir = 0, globTerlambat = 0, globTercatat = 0;
      
      rawRecords.forEach(record => {
        const d = record.val;
        const n = d.nama || '';
        if (rekap[n]) {
          const status = (d.status || '').toUpperCase();
          if (status === 'HADIR') { rekap[n].hadir++; globHadir++; globTercatat++; }
          else if (status === 'TERLAMBAT') { rekap[n].terlambat++; globTerlambat++; globTercatat++; }
        }
      });

      const totalExpected = siswasRelevan.length * totalHariDihitung;
      const globTidakHadir = Math.max(totalExpected - globTercatat, 0);
      const globPersen = totalExpected > 0 ? Math.round((globTercatat / totalExpected) * 100) : 0;

      this.dom.stHadir.textContent = globHadir;
      this.dom.stTerlambat.textContent = globTerlambat;
      this.dom.stTidakHadir.textContent = globTidakHadir;
      this.dom.stPersenHadir.textContent = globPersen + '%';

      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
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
      `;

      this.renderChartStatistikRingkasan(globHadir, globTerlambat, globTidakHadir);
      // Disable harian chart for class overview because it's too complex
      this.renderChartStatistikHarian([], []);
    }

    this.dom.statistikKosong.style.display = 'none';
    this.dom.statistikIsi.style.display = 'block';
  }
'''

# We need to replace the entire old handleTampilkanStatistik method.
js = re.sub(r'async handleTampilkanStatistik\(\) \{.*?(?=  renderChartStatistikRingkasan\()', statistik_recap, js, flags=re.DOTALL)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
