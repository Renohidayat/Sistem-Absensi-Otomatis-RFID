import codecs
import re

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update cacheDOM
js = js.replace("regKelas: document.getElementById('regKelas'),", "regKelas: document.getElementById('regKelas'),\n      regJurusan: document.getElementById('regJurusan'),\n      regAngkatan: document.getElementById('regAngkatan'),")
js = js.replace("editKelas: document.getElementById('editKelas'),", "editKelas: document.getElementById('editKelas'),\n      editJurusan: document.getElementById('editJurusan'),\n      editAngkatan: document.getElementById('editAngkatan'),")
js = js.replace("tglAkhir: document.getElementById('tglAkhir'),", "tglAkhir: document.getElementById('tglAkhir'),\n      lapJurusan: document.getElementById('lapJurusan'),\n      lapKelas: document.getElementById('lapKelas'),")
js = js.replace("statBulanInput: document.getElementById('statBulan'),", "statBulanInput: document.getElementById('statBulan'),\n      statJurusan: document.getElementById('statJurusan'),\n      statKelas: document.getElementById('statKelas'),")
js = js.replace("btnExportCSV: document.getElementById('btnExportCSV'),", "btnExportExcel: document.getElementById('btnExportCSV'),") # Kept btnExportCSV id on the button but variable is btnExportExcel
js = js.replace("jmTotalAngkatan: document.getElementById('jmTotalAngkatan'),", "jmTotalAngkatan: document.getElementById('jmTotalAngkatan'),\n      jmTotalJurusan: document.getElementById('jmTotalJurusan'),")

# 2. Update Registrasi & Edit Modal
js = js.replace("const kelas = this.dom.regKelas.value.trim();", "const kelas = this.dom.regKelas.value.trim();\n    const jurusan = this.dom.regJurusan.value;\n    const angkatan = this.dom.regAngkatan.value;")
js = js.replace("if (!nama || !nisn || !kelas || !uid) {", "if (!nama || !nisn || !kelas || !uid || !jurusan || !angkatan) {")
js = js.replace("await this.dbService.saveSiswa(uid, { nama, nisn, kelas, uid });", "await this.dbService.saveSiswa(uid, { nama, nisn, kelas, jurusan, angkatan, uid });")

js = js.replace("const kelas = this.dom.editKelas.value.trim();", "const kelas = this.dom.editKelas.value.trim();\n    const jurusan = this.dom.editJurusan.value;\n    const angkatan = this.dom.editAngkatan.value;")
js = js.replace("if (!nama || !nisn || !kelas) {", "if (!nama || !nisn || !kelas || !jurusan || !angkatan) {")
js = js.replace("await this.dbService.updateSiswa(uid, { nama, nisn, kelas, uid });", "await this.dbService.updateSiswa(uid, { nama, nisn, kelas, jurusan, angkatan, uid });")

js = js.replace("this.dom.editKelas.value = data.kelas || '';", "this.dom.editKelas.value = data.kelas || '';\n    this.dom.editJurusan.value = data.jurusan || '';\n    this.dom.editAngkatan.value = data.angkatan || '';")

# 3. Update Tabel Siswa
js = js.replace("<td>${d.kelas || '-'}</td>\n        <td style=\"font-family:monospace\">${uid}</td>", "<td>${d.kelas || '-'}</td>\n        <td>${d.jurusan || '-'}</td>\n        <td>${d.angkatan || '-'}</td>\n        <td style=\"font-family:monospace\">${uid}</td>")
js = js.replace("const text = `${d.nama || ''} ${d.nisn || ''} ${d.kelas || ''} ${uid}`.toLowerCase();", "const text = `${d.nama || ''} ${d.nisn || ''} ${d.kelas || ''} ${d.jurusan || ''} ${d.angkatan || ''} ${uid}`.toLowerCase();")

# 4. Laporan: Filter Jurusan & Kelas, Export Excel
laporan_logic = '''
    const filterJurusan = this.dom.lapJurusan ? this.dom.lapJurusan.value : '';
    const filterKelas = this.dom.lapKelas ? this.dom.lapKelas.value : '';

    rawRecords.forEach(record => {
      const d = record.val;
      
      // Terapkan Filter
      if (filterJurusan && (d.jurusan || '') !== filterJurusan) return;
      if (filterKelas && (d.kelas || '') !== filterKelas) return;

      const status = (d.status || '').toUpperCase();'''
js = js.replace('''    rawRecords.forEach(record => {
      const d = record.val;
      const status = (d.status || '').toUpperCase();''', laporan_logic)

js = js.replace("const jamPulang = d.jam_pulang || '-';", "")
js = js.replace("jam_pulang: jamPulang", "")
js = js.replace("<td>${d.jam_pulang}</td>", "")

# Change ExportCSV to ExportExcel
export_excel_func = '''
  handleExportExcel() {
    if (this.laporanData.length === 0) {
      alert('Tidak ada data untuk diexport. Klik "Tampilkan" dulu.');
      return;
    }
    
    // Siapkan data array-of-arrays untuk SheetJS
    const rows = [
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
    });

    if (typeof XLSX === 'undefined') {
      alert('Library SheetJS belum termuat. Silakan muat ulang halaman.');
      return;
    }

    const ws = XLSX.utils.aoa_to_sheet(rows);
    
    // Set column widths
    const wscols = [
      {wch: 12}, // Tanggal
      {wch: 25}, // Nama
      {wch: 15}, // NISN
      {wch: 10}, // Kelas
      {wch: 15}, // Status
      {wch: 12}  // Jam Masuk
    ];
    ws['!cols'] = wscols;

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Laporan Absensi");
    XLSX.writeFile(wb, `laporan_absensi_${this.dom.tglMulai.value}_sd_${this.dom.tglAkhir.value}.xlsx`);
  }
'''
js = re.sub(r'handleExportCSV\(\) \{.*?(?=  // ====== PAGE 3: STATISTIK PER SISWA ======)', export_excel_func, js, flags=re.DOTALL)
js = js.replace('this.dom.btnExportCSV.addEventListener(\'click\', () => this.handleExportCSV());', 'this.dom.btnExportExcel.addEventListener(\'click\', () => this.handleExportExcel());')

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
