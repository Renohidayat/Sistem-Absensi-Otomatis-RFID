import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. renderAbsensiTable (Hari Ini)
html = html.replace('''          const jamMasuk = d.jam_masuk || d.jam || '-';
          rows.push(`
            <tr>
              <td>${no++}</td>
              <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
              <td>${d.nisn || '-'}</td>
              <td>${d.uid || '-'}</td>
              <td>${jamMasuk}</td>
              <td><span class="status ${statusClass}">${d.status || '-'}</span></td>
            </tr>
          `);''', '''          const jamMasuk = d.jam_masuk || d.jam || '-';
          const jamPulang = d.jam_pulang || '-';
          rows.push(`
            <tr>
              <td>${no++}</td>
              <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
              <td>${d.nisn || '-'}</td>
              <td>${d.uid || '-'}</td>
              <td>${jamMasuk}</td>
              <td>${jamPulang}</td>
              <td><span class="status ${statusClass}">${d.status || '-'}</span></td>
            </tr>
          `);''')

# 2. handleTampilkanLaporan (Laporan) - parsing
html = html.replace('''      const jamMasuk = d.jam_masuk || d.jam || '-';
      
      this.laporanData.push({
        tanggal: d.tanggal || record.tanggalKey,
        nama: d.nama || '-',
        nisn: d.nisn || '-',
        kelas: d.kelas || '-',
        status: d.status || '-',
        jam_masuk: jamMasuk,''', '''      const jamMasuk = d.jam_masuk || d.jam || '-';
      const jamPulang = d.jam_pulang || '-';
      
      this.laporanData.push({
        tanggal: d.tanggal || record.tanggalKey,
        nama: d.nama || '-',
        nisn: d.nisn || '-',
        kelas: d.kelas || '-',
        status: d.status || '-',
        jam_masuk: jamMasuk,
        jam_pulang: jamPulang,''')

# 3. handleTampilkanLaporan (Laporan) - rendering
html = html.replace('''      return `
        <tr>
          <td>${d.tanggal}</td>
          <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
          <td>${d.nisn || '-'}</td>
          <td>${d.kelas || '-'}</td>
          <td><span class="status ${statusClass}">${d.status}</span></td>
          <td>${d.jam_masuk}</td>
          
        </tr>
      `;''', '''      return `
        <tr>
          <td>${d.tanggal}</td>
          <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
          <td>${d.nisn || '-'}</td>
          <td>${d.kelas || '-'}</td>
          <td><span class="status ${statusClass}">${d.status}</span></td>
          <td>${d.jam_masuk}</td>
          <td>${d.jam_pulang}</td>
        </tr>
      `;''')

# 4. handleExportExcel (Export)
html = html.replace('''    const rows = [
      ['Tanggal', 'Nama Siswa', 'NISN', 'Kelas', 'Status', 'Jam Masuk']
    ];
    
    this.laporanData.forEach(d => {
      rows.push([
        d.tanggal,
        d.nama ? d.nama.replace(/_/g, ' ') : '-',
        d.nisn || '-',
        d.kelas || '-',
        d.status,
        d.jam_masuk
      ]);
    });''', '''    const rows = [
      ['Tanggal', 'Nama Siswa', 'NISN', 'Kelas', 'Status', 'Jam Masuk', 'Jam Pulang']
    ];
    
    this.laporanData.forEach(d => {
      rows.push([
        d.tanggal,
        d.nama ? d.nama.replace(/_/g, ' ') : '-',
        d.nisn || '-',
        d.kelas || '-',
        d.status,
        d.jam_masuk,
        d.jam_pulang
      ]);
    });''')

html = html.replace('''    const wscols = [
      {wch: 12}, // Tanggal
      {wch: 25}, // Nama
      {wch: 15}, // NISN
      {wch: 10}, // Kelas
      {wch: 15}, // Status
      {wch: 12}  // Jam Masuk
    ];''', '''    const wscols = [
      {wch: 12}, // Tanggal
      {wch: 25}, // Nama
      {wch: 15}, // NISN
      {wch: 10}, // Kelas
      {wch: 15}, // Status
      {wch: 12},  // Jam Masuk
      {wch: 12}  // Jam Pulang
    ];''')

# 5. renderStatistikDetail (Statistik)
html = html.replace('''          detailRows.push({
            tanggal: tglStr,
            jam: d.jam_masuk || d.jam || '-',
            status: d.status || '-'
          });''', '''          detailRows.push({
            tanggal: tglStr,
            jam: d.jam_masuk || d.jam || '-',
            jam_pulang: d.jam_pulang || '-',
            status: d.status || '-'
          });''')

html = html.replace('''        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Tanggal</th>
              <th>Jam</th>
              <th>Status</th>
            </tr>
          </thead>''', '''        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Tanggal</th>
              <th>Jam Masuk</th>
              <th>Jam Pulang</th>
              <th>Status</th>
            </tr>
          </thead>''')

html = html.replace('''          return `
            <tr>
              <td>${i + 1}</td>
              <td>${d.tanggal}</td>
              <td>${d.jam}</td>
              <td><span class="status ${statusClass}">${d.status}</span></td>
            </tr>
          `;''', '''          return `
            <tr>
              <td>${i + 1}</td>
              <td>${d.tanggal}</td>
              <td>${d.jam}</td>
              <td>${d.jam_pulang}</td>
              <td><span class="status ${statusClass}">${d.status}</span></td>
            </tr>
          `;''')


# 6. tabel Laporan empty text and skeleton colspan
html = html.replace('''colspan="7" class="empty"''', '''colspan="9" class="empty"''')
html = html.replace('''colspan="6" class="empty"''', '''colspan="7" class="empty"''')
html = html.replace('''window.showTableSkeleton('tabelAbsensi', 6)''', '''window.showTableSkeleton('tabelAbsensi', 7)''')

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(html)
print('UIManager.js modified!')
