import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_func = '''  renderStatistikMuridDanKelas() {
    const totalMurid = this.siswaRowsCache.length;
    if (this.dom.statTotalMurid) {
      this.dom.statTotalMurid.textContent = totalMurid;
    }

    // Hitung jumlah murid per kelas
    const kelasCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const kelas = (d.kelas || 'TIDAK ADA KELAS').trim().toUpperCase();
      kelasCounts[kelas] = (kelasCounts[kelas] || 0) + 1;
    });

    // Urutkan kelas secara alfabetis
    const sortedKelas = Object.keys(kelasCounts).sort();

    // Render tabel pemetaan kelas
    if (this.dom.tabelKelasMurid) {
      if (sortedKelas.length === 0) {
        this.dom.tabelKelasMurid.innerHTML = `
          <tr>
            <td colspan="2" class="text-center py-4 text-xs text-[#64748b]">Belum ada data siswa</td>
          </tr>
        `;
      } else {
        this.dom.tabelKelasMurid.innerHTML = sortedKelas.map(kelas => `
          <tr class="hover:bg-[#f1f5f9] transition-colors">
            <td class="py-2 text-xs font-medium text-white">${kelas}</td>
            <td class="py-2 text-xs font-semibold text-right text-[#2563eb]">${kelasCounts[kelas]} Siswa</td>
          </tr>
        `).join('');
      }
    }

    // Render Chart.js diagram batang distribusi kelas
    if (this.dom.chartDistribusiMurid) {
      const counts = sortedKelas.map(kelas => kelasCounts[kelas]);
      const data = {
        labels: sortedKelas,
        datasets: [{
          label: 'Jumlah Siswa',
          data: counts,
          backgroundColor: '#2563eb',
          borderRadius: 4
        }]
      };

      if (this.chartDistribusiMurid) {
        this.chartDistribusiMurid.data = data;
        this.chartDistribusiMurid.update();
      } else {
        this.chartDistribusiMurid = new Chart(this.dom.chartDistribusiMurid, {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false }
            },
            scales: {
              y: { beginAtZero: true, ticks: { precision: 0 } }
            }
          }
        });
      }
    }
  }'''

new_func = '''  renderStatistikMuridDanKelas() {
    const totalMurid = this.siswaRowsCache.length;
    if (this.dom.statTotalMurid) {
      this.dom.statTotalMurid.textContent = totalMurid;
    }

    // Hitung jumlah murid per kelas dan jurusan unik
    const kelasCounts = {};
    const jurusanUnik = new Set();
    
    this.siswaRowsCache.forEach(({ d }) => {
      const kelas = (d.kelas || 'TIDAK ADA KELAS').trim().toUpperCase();
      const jurusan = (d.jurusan || 'Lainnya').trim().toUpperCase();
      
      kelasCounts[kelas] = (kelasCounts[kelas] || 0) + 1;
      jurusanUnik.add(jurusan);
    });

    const statTotalKelas = document.getElementById('statTotalKelas');
    const statTotalJurusan = document.getElementById('statTotalJurusan');
    
    // Urutkan kelas secara alfabetis
    const sortedKelas = Object.keys(kelasCounts).sort();
    
    if (statTotalKelas) statTotalKelas.textContent = sortedKelas.length;
    if (statTotalJurusan) statTotalJurusan.textContent = jurusanUnik.size;

    // Render tabel pemetaan kelas
    if (this.dom.tabelKelasMurid) {
      if (sortedKelas.length === 0) {
        this.dom.tabelKelasMurid.innerHTML = `
          <tr>
            <td colspan="2" class="text-center py-8 text-xs text-slate-400">Belum ada data siswa</td>
          </tr>
        `;
      } else {
        this.dom.tabelKelasMurid.innerHTML = sortedKelas.map((kelas, idx) => `
          <tr class="${idx !== sortedKelas.length - 1 ? 'border-b border-slate-100' : ''} hover:bg-slate-50 transition-colors">
            <td class="py-3 text-xs font-semibold text-slate-700">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                ${kelas}
              </div>
            </td>
            <td class="py-3 text-xs font-bold text-right text-slate-700">
              <span class="bg-blue-100 text-blue-700 py-1 px-2 rounded-md">${kelasCounts[kelas]}</span>
            </td>
          </tr>
        `).join('');
      }
    }

    // Render Chart.js diagram batang distribusi kelas
    if (this.dom.chartDistribusiMurid) {
      const counts = sortedKelas.map(kelas => kelasCounts[kelas]);
      const data = {
        labels: sortedKelas,
        datasets: [{
          label: 'Jumlah Siswa',
          data: counts,
          backgroundColor: '#3b82f6',
          hoverBackgroundColor: '#2563eb',
          borderRadius: 6,
          borderSkipped: false
        }]
      };

      if (this.chartDistribusiMurid) {
        this.chartDistribusiMurid.data = data;
        this.chartDistribusiMurid.update();
      } else {
        this.chartDistribusiMurid = new Chart(this.dom.chartDistribusiMurid, {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleFont: { size: 13 },
                bodyFont: { size: 13 },
                padding: 10,
                cornerRadius: 8,
                displayColors: false
              }
            },
            scales: {
              y: { 
                beginAtZero: true, 
                ticks: { precision: 0, color: '#64748b' },
                grid: { color: '#f1f5f9', drawBorder: false }
              },
              x: {
                ticks: { color: '#64748b', font: { size: 11 } },
                grid: { display: false, drawBorder: false }
              }
            }
          }
        });
      }
    }
  }'''

if old_func in js:
    js = js.replace(old_func, new_func)
    # cache bust
    with codecs.open('js/app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()
    with codecs.open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_js.replace('v=10', 'v=11'))
        
    with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("SUCCESS JS")
else:
    print("FAILED TO FIND OLD FUNC IN UIMANAGER")
